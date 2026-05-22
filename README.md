# TurtleBot3 Otonom Navigasyon Gorevleri

ROS 1 Noetic ve TurtleBot3 Waffle kullanilarak gelistirilmis uc farkli otonom robot davranisi.

## Gereksinimler

Ubuntu 20.04 ve ROS Noetic kurulu olmasi gerekiyor. Asagidaki paketler de yuklu olmali:

```bash
sudo apt install ros-noetic-turtlebot3 ros-noetic-turtlebot3-simulations -y
```

## Kurulum

```bash
cd ~/catkin_ws/src
git clone https://github.com/ertugrulay960-rbtg/turtlebot3-odev2pid.git my_pkg
cd ~/catkin_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle
```

Bu son iki satiri kalici yapmak icin:

```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc
```

## Simulasyonu Baslat

Her gorev icin once Gazebo'yu ac:

```bash
roslaunch turtlebot3_gazebo turtlebot3_stage_2.launch
```

---

## Gorev 1: Move-Stop-Rotate (Engelden Kacma)

Robot hicbir hedefe gitmeksizin ilerler. Onune engel cikinca durur, engel gorunumden cikana kadar doner ve tekrar ilerler. Tamamen reaktif bir davranis sergilar.

```bash
rosrun my_pkg engel_kacma.py
```

---

## Gorev 2: PID ile Mesafe Kontrolu

Robot, onundeki engele veya duvara tam olarak 0.5 metre mesafede durmak uzere PID kontrolcu kullanir. Hedefe yaklastikca hizi oransal olarak duser, hedef araligina girince kilitlenir ve titresimi onler.

```bash
rosrun my_pkg pid_kontrol.py
```

---

## Gorev 3: PID Hiz Kontrollu Engel Kacma

Gorev 1 ve Gorev 2'nin birlesimidir. Robot surekli ilerler, engele yaklastikca PID ile yavaslama, durma ve donme davranisini gosterir. Yol acilinca tekrar PID ile hizlanir. Sonsuz dongude calisir.

```bash
rosrun my_pkg engel_pid.py
```
