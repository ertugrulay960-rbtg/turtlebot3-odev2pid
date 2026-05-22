# TurtleBot3 Engel Kacma ve PID Kontrol

Bu repo, ROS 1 Noetic ortaminda TurtleBot3 icin gelistirilmis otonom robot gorevlerini icermektedir.

## Kurulum

```bash
cd ~/catkin_ws/src
git clone https://github.com/ertugrulay960-rbtg/turtlebot3-odev2pid.git my_pkg
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

## Ortam Gereksinimleri

- Ubuntu 20.04
- ROS 1 Noetic
- Python 3.x
- TurtleBot3 simulasyon paketleri

## Simulasyonu Baslat

```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_stage_2.launch
```

---

## Gorev 1: Engel Kacma (Move-Stop-Rotate)

Dosya: `src/engel_kacma.py`

Robot, LaserScan verileriyle onune cikan engellerden kacinar. Hicbir hedefe gitmez, sadece carpismadan kacma mantigiyla calisir.

- **Move**: Onunde engel yoksa duz ilerler
- **Stop**: Engel algilaninca durur
- **Rotate**: Yol acilana kadar doner, sonra tekrar ilerler

```bash
rosrun my_pkg engel_kacma.py
```

---

## Gorev 2: PID Mesafe Kontrolu

Dosya: `src/pid_kontrol.py`

Robot, onundeki engele tam 0.5 metre mesafede durmak icin PID kontrolcu kullanir. Hedefe yaklastikca hizi oransal olarak duser.

- Yumusak durus: PID ile hedefe yaklastikca yavaslama
- Tolerans: +-2 cm deadband ile titresim onlenir
- Hedef araliga girilince sistem kilitlenir

```bash
rosrun my_pkg pid_kontrol.py
```

---

## Gorev 3: Engel Kacma + PID Hiz Kontrolu (Birlesik)

Dosya: `src/engel_pid.py`

Engel kacma ve PID kontrolunun birlesimi. Robot sonsuz dongu halinde calisir.

- **ILERI**: PID ile engele olan mesafeye gore hizi ayarlar, engele yaklastikca yavaslara
- **DUR**: Engel 0.5m'den yakin gelince aninda durur
- **DON**: Yol acilana kadar kendi ekseni etrafinda doner
- Yol acilinca tekrar ILERI moduna gecer ve PID ile hizlanir

```bash
rosrun my_pkg engel_pid.py
```
