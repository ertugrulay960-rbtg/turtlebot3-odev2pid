#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# PID sabitleri
Kp = 0.8
Ki = 0.0
Kd = 0.4

# Hedef mesafe (metre)
hedef_mesafe = 0.5
tolerans     = 0.02  # +- 2 cm deadband

# PID degiskenleri
onceki_hata  = 0.0
toplam_hata  = 0.0
kilitli      = False

pub = None

def tarama_callback(msg):
    global onceki_hata, toplam_hata, kilitli

    if kilitli:
        return

    # Robotun tam onundaki mesafe
    on_mesafe = msg.ranges[0]

    if on_mesafe == float('inf') or on_mesafe != on_mesafe:
        return

    hata = on_mesafe - hedef_mesafe

    # Tolerans araligi - kilitle
    if abs(hata) <= tolerans:
        hiz = Twist()
        hiz.linear.x = 0.0
        pub.publish(hiz)
        kilitli = True
        rospy.loginfo(f"HEDEFE ULASILDI! Mesafe: {on_mesafe:.3f}m")
        return

    # PID hesapla
    dt = 0.1

    P = Kp * hata
    toplam_hata += hata * dt
    I = Ki * toplam_hata
    D = Kd * (hata - onceki_hata) / dt
    onceki_hata = hata

    cikis_hiz = P + I + D

    # Hiz sinirlamasi
    cikis_hiz = max(-0.3, min(0.3, cikis_hiz))

    hiz = Twist()
    hiz.linear.x = cikis_hiz
    pub.publish(hiz)

    rospy.loginfo(f"Mesafe: {on_mesafe:.3f}m | Hata: {hata:.3f} | Hiz: {cikis_hiz:.3f}")

def pid_kontrol():
    global pub

    rospy.init_node('pid_kontrol', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/scan', LaserScan, tarama_callback)

    rospy.loginfo("PID kontrol baslatildi! Hedef mesafe: 0.5m")
    rospy.spin()

if __name__ == '__main__':
    try:
        pid_kontrol()
    except rospy.ROSInterruptException:
        pass
