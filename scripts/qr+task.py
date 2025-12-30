#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
import yaml
import time
import os
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from pyzbar import pyzbar
import tf


class AkilliKtunRobotu:
    def __init__(self):
        rospy.init_node("akilli_gorev_yoneticisi")
        rospy.loginfo("Task Manager started (FINAL MODE)")

        # ---------------- MOVE BASE ----------------
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.client.wait_for_server()
        rospy.loginfo("move_base connected")

        # ---------------- KAMERA / QR ----------------
        self.bridge = CvBridge()
        self.current_qr_data = None
        self.beklenen_qr = None
        self.qr_log_basildi = False
        rospy.Subscriber("/camera/rgb/image_raw", Image, self.camera_callback)

        # ---------------- ODA BİLGİLERİ ----------------
        mission_file = rospy.get_param(
            "~mission_file",
            "/home/sude/catkin_ws/src/ktun_robotics/config/mission.yaml"
        )
        with open(mission_file, "r") as f:
            mission_data = yaml.safe_load(f)

        self.odalar = mission_data["rooms"]

        # ---------------- TIMEOUT & RAPOR ----------------
        self.ROOM_TIMEOUT = 150  # saniye
        self.temizlik_raporu = []

    # ---------------- CAMERA CALLBACK ----------------
    def camera_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            barcodes = pyzbar.decode(cv_image)

            for barcode in barcodes:
                okunan_qr = barcode.data.decode("utf-8")
                if okunan_qr == self.beklenen_qr:
                    self.current_qr_data = okunan_qr

                    if not self.qr_log_basildi:
                        rospy.loginfo("✔ QR algılandı")
                        self.qr_log_basildi = True
                    return
        except Exception as e:
            rospy.logwarn(f"Kamera hatası: {e}")

    # ---------------- MOVE BASE ----------------
    def hedefe_git(self, x, y, yaw):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

        q = tf.transformations.quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        self.client.send_goal(goal)
        finished = self.client.wait_for_result(rospy.Duration(90))

        if not finished:
            self.client.cancel_goal()
            rospy.logwarn("Hedefe gidilemedi (timeout)")
            return False

        return self.client.get_state() == 3  # SUCCEEDED

    # ---------------- TEMİZLİK ----------------
    def temizlik_turu(self):
        rospy.loginfo("→ Temizlik yapılıyor...")
        rospy.sleep(3)

    # ---------------- GÖREV DÖNGÜSÜ ----------------
    def gorev_dongusu(self):
        for oda in self.odalar:
            oda_baslangic = time.time()

            self.beklenen_qr = oda["qr_expected"]
            self.current_qr_data = None
            self.qr_log_basildi = False

            rospy.loginfo(f"=== {oda['name']} GİRİŞİNE GİDİLİYOR ===")

            x = oda["entry_goal"]["x"]
            y = oda["entry_goal"]["y"]
            yaw = oda["entry_goal"]["yaw"]

            if not self.hedefe_git(x, y, yaw):
                rospy.logwarn(f"!!!{oda['name']} GİRİŞİNE ULAŞILAMADI")
                self.temizlik_raporu.append(f"{oda['name']}: GİRİŞE ULAŞILAMADI")
                continue

            rospy.sleep(2)

            basarili_qr = False

            # -------- QR DOĞRULAMA --------
            if self.current_qr_data == self.beklenen_qr:
                rospy.loginfo("✔ QR okuma başarılı")
                basarili_qr = True
            else:
                rospy.loginfo("QR bulunamadı, açı taraması başlıyor...")
                for aci in [0.0, 0.5, -0.5]:
                    self.hedefe_git(x, y, yaw + aci)
                    rospy.sleep(2)
                    if self.current_qr_data == self.beklenen_qr:
                        rospy.loginfo("✔ QR okuma başarılı (açı taraması)")
                        basarili_qr = True
                        break

            if not basarili_qr:
                rospy.logerr(f"{oda['name']} QR doğrulanamadı")
                self.temizlik_raporu.append(f"{oda['name']}: QR OKUNAMADI")
                continue

            rospy.loginfo(f"{oda['name']} temizliğine başlanıyor")

            basarili_hedef = 0
            toplam_hedef = len(oda["cleaning_goals"])

            for cg in oda["cleaning_goals"]:
                if time.time() - oda_baslangic > self.ROOM_TIMEOUT:
                    rospy.logwarn(f"{oda['name']} TIMEOUT!")
                    self.temizlik_raporu.append(
                        f"{oda['name']}: TAMAMLANAMADI (timeout) {basarili_hedef}/{toplam_hedef}"
                    )
                    break

                if self.hedefe_git(cg["x"], cg["y"], cg["yaw"]):
                    self.temizlik_turu()
                    basarili_hedef += 1
                else:
                    rospy.logwarn("Temizlik hedefine ulaşılamadı")

            if basarili_hedef == toplam_hedef:
                rospy.loginfo(f"✔ {oda['name']} ODA TEMİZLİĞİ TAMAMLANDI")
                self.temizlik_raporu.append(f"{oda['name']}: TEMİZLENDİ")
            else:
                rospy.logwarn(f"{oda['name']} KISMEN TEMİZLENDİ")
                self.temizlik_raporu.append(
                    f"{oda['name']}: KISMEN ({basarili_hedef}/{toplam_hedef})"
                )

            rospy.loginfo("--------------------------------")

        self.rapor_yaz()
        rospy.loginfo("🏁 GÖREV TAMAMLANDI")

    # ---------------- RAPOR ----------------
    def rapor_yaz(self):
        klasor = "/home/sude/catkin_ws/src/ktun_robotics/report"
        os.makedirs(klasor, exist_ok=True)

        dosya = os.path.join(klasor, "temizlik_raporu.txt")

        with open(dosya, "w") as f:
            f.write("TEMİZLİK RAPORU\n")
            f.write("====================\n")
            for satir in self.temizlik_raporu:
                f.write(satir + "\n")

        rospy.loginfo("📄 Temizlik raporu kaydedildi")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        robot = AkilliKtunRobotu()
        robot.gorev_dongusu()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

