KTUN Robotics – QR Tabanlı Otonom Temizlik Robotu 🤖🧹

Bu proje, ROS (Robot Operating System) kullanılarak geliştirilmiş,
QR kod ile oda tanıma, otonom navigasyon ve oda bazlı temizlik gerçekleştiren
akıllı bir mobil robot sistemidir.

Robot, ev ortamında odalara girerken QR kodları okuyarak hangi odaya girdiğini doğrular,
her oda için belirlenen temizlik görevlerini yerine getirir ve tüm görevler tamamlandığında
detaylı bir temizlik raporu oluşturur.

📌 Proje Özellikleri

📷 QR Kod ile Oda Tanıma

🔁 QR okuma için 2 deneme hakkı

🔄 QR bulunamazsa açı taraması (scan behavior)

⏱️ Her oda için timeout süresi

🧭 move_base ile otonom navigasyon

🧹 Oda bazlı temizlik görevleri

📊 Görev sonunda temizlik raporu

🏠 Çok odalı ev senaryosu desteği

🧠 YAML tabanlı görev yapılandırması

🗂️ Proje Klasör Yapısı
ktun_robotics/
├── launch/
│   └── start_my_project.launch
│
├── config/
│   └── mission.yaml
│
├── scripts/
│   └── qr_task.py
│
├── worlds/
│   └── my_house.world
│
├── maps/
│   ├── my_map.pgm
│   └── my_map.yaml
│
├── report/
│   └── temizlik_raporu.txt
│
├── images/
│   ├── gazebo.jpeg
│   ├── rapor.jpeg
│   ├── rviz.jpeg
│   └── terminal.png
│
├── README.md
├── package.xml
└── CMakeLists.txt

⚙️ Gereksinimler

Ubuntu 20.04

ROS Noetic

Gazebo

RViz

OpenCV

pyzbar

move_base

🚀 Kurulum
source ~/catkin_ws/devel/setup.bash

▶️ Gazebo Ortamını Çalıştırma
roslaunch ktun_robotics start_my_project.launch

▶️ Navigasyon Stack
roslaunch turtlebot3_navigation turtlebot3_navigation.launch \
map_file:=$HOME/catkin_ws/src/ktun_robotics/maps/my_map.yaml

▶️ Görev Yöneticisini Çalıştırma
rosrun ktun_robotics qr_task.py


⚠️ qr+task.py yerine qr_task.py kullanılması gereklidir.

🧠 Görev Akışı

Robot ev ortamında başlar

Oda giriş noktasına gider

QR kodu okumaya çalışır

Maksimum 2 deneme

QR bulunamazsa:

Robot bulunduğu yerde açı taraması yapar

Yine bulunamazsa oda atlanır

QR doğruysa:

Temizlik noktalarına sırayla gider

Oda için belirlenen timeout süresi aşılırsa:

Oda başarısız sayılır

Tüm odalar tamamlanınca:

Temizlik raporu oluşturulur

🏷️ QR Kod Kuralları

QR içeriği aşağıdaki formatta olmalıdır:

ROOM=LIVINGROOM
ROOM=BATHROOM
ROOM=KITCHEN
ROOM=BEDROOM
ROOM=CORRIDOR


❌ Yanlış QR → görev iptal edilir

⏳ QR 2 denemede okunamazsa → oda atlanır

⏱️ Timeout Mekanizması

Her oda için ayrı bir timeout süresi vardır

Süre aşılırsa:

O oda TAMAMLANAMADI (timeout) olarak işaretlenir

Robot bir sonraki odaya geçer

📄 mission.yaml Yapısı
rooms:
  - name: "LIVINGROOM"
    qr_expected: "ROOM=LIVINGROOM"
    entry_goal: {x: 1.5, y: -0.5, yaw: 0.0}
    cleaning_goals:
      - {x: 1.8, y: -1.0, yaw: 1.57}
      - {x: 2.2, y: -0.5, yaw: 0.0}

📊 Temizlik Raporu

Görev sonunda hem terminalde hem de report/temizlik_raporu.txt dosyasında rapor oluşturulur.

Örnek Çıktı
=== TEMİZLİK RAPORU ===
LIVINGROOM : TEMİZLENDİ
BATHROOM   : TEMİZLENDİ
KITCHEN    : TAMAMLANAMADI (timeout)
BEDROOM    : KISMEN (1/3)
CORRIDOR   : TEMİZLENDİ
=======================

🖼️ Görseller
🏠 Gazebo Ev Ortamı

🧭 RViz Navigasyon

📊 Temizlik Raporu

💻 Terminal Çıktıları

👩‍💻 Geliştirici

Sude
📍 Konya Teknik Üniversitesi
📘 Robotik & Yapay Zeka
📌 ROS • Python • OpenCV • Gazebo
