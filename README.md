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
- 🏠 Çok odalı ev senaryosu desteği
- 🧠 **YAML tabanlı görev yapılandırması**

---

## 🗂️ Proje Klasör Yapısı

```text
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
│   ├── rviz.jpeg
│   ├── rapor.jpeg
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


👩‍💻 Geliştirici
Sude
📍 Konya Teknik Üniversitesi
📘 Robotik & Yapay Zeka
📌 ROS • Python • OpenCV • Gazebo
