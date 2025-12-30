# 🤖 KTUN Robotics – QR Tabanlı Otonom Temizlik Robotu 🧹

Bu proje, **ROS Noetic** ortamında çalışan,  
**QR kod ile oda doğrulaması**, **otonom navigasyon** ve  
**oda bazlı temizlik** gerçekleştiren akıllı bir mobil robot sistemidir.

Robot, ev ortamında odalara girerken QR kodları okuyarak hangi odaya girdiğini doğrular,  
her oda için belirlenen temizlik görevlerini yerine getirir ve  
tüm görevler tamamlandığında **detaylı bir temizlik raporu** oluşturur.

---

## 📌 Proje Özellikleri

- 📷 **QR Kod ile Oda Tanıma**
- 🔁 QR okuma için **2 deneme hakkı**
- 🔄 QR bulunamazsa **açı taraması (scan behavior)**
- ⏱️ Her oda için **timeout süresi**
- 🧭 `move_base` ile **otonom navigasyon**
- 🧹 **Oda bazlı temizlik görevleri**
- 📊 Görev sonunda **temizlik raporu**
- 🏠 Çok odalı ev senaryosu
- 🧠 **YAML tabanlı görev yapılandırması**

---

## 🖼️ Sistemden Görseller

### 🏠 Gazebo Ev Ortamı
![Gazebo](images/gazebo.jpeg)

### 🧭 RViz Navigasyon
![RViz](images/rviz.jpeg)

### 📊 Temizlik Raporu
![Rapor](images/rapor.jpeg)

### 💻 Terminal Çıktıları
![Terminal](images/terminal.png)

---


⚙️ Gereksinimler
Ubuntu 20.04

ROS Noetic

Gazebo

RViz

OpenCV

pyzbar

move_base

🚀 Kurulum
Catkin workspace içine paketi ekledikten sonra:

cd ~/catkin_ws

catkin_make

source ~/catkin_ws/devel/setup.bash

▶️ Çalıştırma Komutları

1️⃣ Gazebo Ortamını Başlatma

roslaunch ktun_robotics start_my_project.launch

2️⃣ Navigasyon Çalıştırma

roslaunch turtlebot3_navigation turtlebot3_navigation.launch \map_file:=$HOME/catkin_ws/src/ktun_robotics/maps/my_map.yaml

3️⃣ Görev Yöneticisini Başlatma

rosrun ktun_robotics qr+task.py

🧠 Görev Akışı

Robot ev ortamında başlar

Oda giriş noktasına gider

QR kodu okumaya çalışır (maksimum 2 deneme)

QR okunamazsa:

Robot bulunduğu yerde açı taraması yapar

Hâlâ okunamazsa oda atlanır

QR doğruysa:

Odaya ait temizlik noktalarına sırayla gider

Oda için belirlenen timeout süresi aşılırsa:

Oda başarısız sayılır

Tüm odalar tamamlanınca:

Temizlik raporu oluşturulur

🏷️ QR Kod Kuralları
QR içerikleri şu formatta olmalıdır:
ROOM=LIVINGROOM
ROOM=BATHROOM
ROOM=KITCHEN
ROOM=BEDROOM
ROOM=CORRIDOR
❌ Yanlış QR → görev iptal edilir

⏳ 2 denemede okunamazsa → oda atlanır

⏱️ Timeout Mekanizması
Her oda için ayrı timeout süresi vardır

Süre aşılırsa:

O oda TAMAMLANAMADI (timeout) olarak işaretlenir

Robot bir sonraki odaya geçer

📄 mission.yaml Örneği
rooms:
  - name: "LIVINGROOM"
    qr_expected: "ROOM=LIVINGROOM"
    entry_goal: {x: 1.5, y: -0.5, yaw: 0.0}
    cleaning_goals:
      - {x: 1.8, y: -1.0, yaw: 1.57}
      - {x: 2.2, y: -0.5, yaw: 0.0}


📊 Temizlik Raporu
Örnek çıktı:
=== TEMİZLİK RAPORU ===
LIVINGROOM : TEMİZLENDİ
BATHROOM   : TEMİZLENDİ
KITCHEN    : TAMAMLANAMADI (timeout)
BEDROOM    : KISMEN (1/3)
CORRIDOR   : TEMİZLENDİ
======================
👩‍💻 Geliştirici
Sude

📍 Konya Teknik Üniversitesi
📘 Robotik & Yapay Zeka
📌 ROS • Python • OpenCV • Gazebo
