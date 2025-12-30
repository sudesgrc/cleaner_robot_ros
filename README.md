
# 🤖 KTUN Robotics: QR Tabanlı Otonom Temizlik Robotu 🧹

![ROS Noetic](https://img.shields.io/badge/ROS-Noetic-blue?logo=ros) ![Ubuntu 20.04](https://img.shields.io/badge/OS-Ubuntu%2020.04-orange?logo=ubuntu) ![Python](https://img.shields.io/badge/Language-Python-yellow?logo=python)

Bu proje, **ROS Noetic** ortamında çalışan; **QR kod ile oda doğrulaması**, **otonom navigasyon** ve **akıllı temizlik görev yönetimi** gerçekleştiren bir mobil robot sistemidir. Robot, ev ortamında odaları tanır, doğrular ve her oda için özelleştirilmiş temizlik rotalarını takip ederek görev sonunda detaylı bir rapor sunar.

---

## 📌 Proje Özellikleri

* 📷 **QR Kod ile Oda Tanıma:** `OpenCV` ve `pyzbar` entegrasyonu ile kimlik doğrulama.
* 🔄 **Hata Toleransı:** QR okuma için 2 deneme hakkı ve başarısızlık durumunda **açı taraması (scan behavior)**.
* ⏱️ **Zaman Yönetimi:** Her oda için bağımsız **timeout (zaman aşımı)** süresi.
* 🧭 **Otonom Navigasyon:** `move_base` kullanarak dinamik rota planlama.
* 🧠 **YAML Yapılandırması:** Görevlerin ve koordinatların kolayca düzenlenebildiği esnek yapı.
* 📊 **Raporlama:** Görev bitiminde başarı/başarısızlık durumlarını içeren temizlik raporu.

---

## 🖼️ Sistemden Görseller

### 🏠 Simülasyon ve Navigasyon
| Gazebo Ev Ortamı | RViz Navigasyon Görüntüsü |
| :---: | :---: |
| ![Gazebo](images/gazebo.jpeg) | ![RViz](images/rviz.jpeg) |

### 📊 Çıktılar
| Temizlik Raporu | Terminal Logları |
| :---: | :---: |
| ![Rapor](images/rapor.jpeg) | ![Terminal](images/terminal.png) |

---

## 🛠️ Kurulum ve Gereksinimler

### Ön Koşullar
* Ubuntu 20.04 & ROS Noetic
* Gazebo & RViz
* Python Kütüphaneleri: `opencv-python`, `pyzbar`, `pyyaml`

### Kurulum Adımları
```bash
# Workspace içine paketi dahil edin
cd ~/catkin_ws/src
# (Proje dosyalarını buraya kopyalayın)

# Derleme işlemi
cd ~/catkin_ws
catkin_make
source ~/catkin_ws/devel/setup.bash

```

---

## 🚀 Çalıştırma Talimatları

1️⃣ **Gazebo Dünyasını Başlatma**

```bash
roslaunch ktun_robotics start_my_project.launch

```

2️⃣ **Navigasyon Paketini Çalıştırma**

```bash
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/catkin_ws/src/ktun_robotics/maps/my_map.yaml

```

3️⃣ **Görev Yöneticisini Başlatma**

```bash
rosrun ktun_robotics qr+task.py

```

---

## 🧠 Görev Akış Şeması

1. **Hedefe Git:** Robot oda girişine (`entry_goal`) ulaşır.
2. **QR Doğrula:** QR kodu okumaya çalışır. Okunamazsa robot yerinde dönerek tarama yapar.
3. **Temizlik:** QR içeriği `mission.yaml` ile eşleşirse temizlik noktalarına (`cleaning_goals`) sırayla gider.
4. **Zaman Kontrolü:** Oda için ayrılan süre aşılırsa görev iptal edilir ve bir sonraki odaya geçilir.
5. **Rapor:** Tüm odalar bittiğinde başarı analizi ekrana basılır.

---

## 📄 Yapılandırma Örneği (mission.yaml)

```yaml
rooms:
  - name: "LIVINGROOM"
    qr_expected: "ROOM=LIVINGROOM"
    entry_goal: {x: 1.5, y: -0.5, yaw: 0.0}
    cleaning_goals:
      - {x: 1.8, y: -1.0, yaw: 1.57}
      - {x: 2.2, y: -0.5, yaw: 0.0}

```

---

## 🏷️ QR Kod Formatı

Robotun tanıması için QR içerikleri şu yapıda olmalıdır:

* `ROOM=LIVINGROOM`, `ROOM=KITCHEN`, `ROOM=BATHROOM` vb.
* ❌ Yanlış veya geçersiz formatlı QR kodlar görevi iptal ettirir.

---

## 👩‍💻 Geliştirici

**Sude**
📍 **Konya Teknik Üniversitesi**
📘 Robotik & Yapay Zeka
📌 ROS • Python • OpenCV • Gazebo

---
