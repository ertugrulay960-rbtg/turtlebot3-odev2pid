#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# PID sabitleri
Kp = 1.0
Ki = 0.0
Kd = 0.3

# Mesafe parametreleri
hedef_hiz      = 0.2   # hedef ileri hiz (m/s)
engel_mesafesi = 0.5   # bu mesafeden yakin engel varsa dur-don

# PID degiskenleri
onceki_hata = 0.0
toplam_hata = 0.0

# Durumlar
ILERI = 0
DUR   = 1
DON   = 2

durum = ILERI
pub   = None

def tarama_callback(msg):
    global onceki_hata, toplam_hata, durum

    on_sol   = list(msg.ranges[0:15])
    on_sag   = list(msg.ranges[345:360])
    on       = on_sol + on_sag
    on_temiz = [r for r in on if r != float('inf') and r == r and r > 0.01]

    if len(on_temiz) == 0:
        return

    min_mesafe = min(on_temiz)
    hiz        = Twist()

    if durum == ILERI:
        if min_mesafe <= engel_mesafesi:
            # Engel algilandi - dur
            hiz.linear.x  = 0.0
            hiz.angular.z = 0.0
            pub.publish(hiz)
            durum = DUR
            toplam_hata = 0.0
            onceki_hata = 0.0
            rospy.loginfo(f"ENGEL! Mesafe: {min_mesafe:.3f}m - DURUYOR")
            return

        # PID ile hiz kontrol et
        hata = hedef_hiz - 0.0  # sabit hedef hiza dogru ivmelen
        dt   = 0.1

        # Mesafeye gore hizi ayarla - engele yaklastikca yavasla
        hiz_orani = (min_mesafe - engel_mesafesi) / engel_mesafesi
        hiz_orani = max(0.0, min(1.0, hiz_orani))

        P = Kp * (min_mesafe - engel_mesafesi)
        toplam_hata += (min_mesafe - engel_mesafesi) * dt
        I = Ki * toplam_hata
        D = Kd * ((min_mesafe - engel_mesafesi) - onceki_hata) / dt
        onceki_hata = min_mesafe - engel_mesafesi

        cikis_hiz = P + I + D
        cikis_hiz = max(0.05, min(0.25, cikis_hiz))

        hiz.linear.x  = cikis_hiz
        hiz.angular.z = 0.0
        pub.publish(hiz)
        rospy.loginfo(f"ILERI | Mesafe: {min_mesafe:.3f}m | Hiz: {cikis_hiz:.3f}")

    elif durum == DUR:
        hiz.linear.x  = 0.0
        hiz.angular.z = 0.0
        pub.publish(hiz)
        durum = DON
        rospy.loginfo("DONUYOR...")

    elif durum == DON:
        if min_mesafe > engel_mesafesi:
            durum = ILERI
            toplam_hata = 0.0
            onceki_hata = 0.0
            rospy.loginfo("YOL ACIK - TEKRAR ILERLIYOR")
            return

        hiz.linear.x  = 0.0
        hiz.angular.z = 0.5
        pub.publish(hiz)

def main():
    global pub
    rospy.init_node('engel_pid', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/scan', LaserScan, tarama_callback)
    rospy.loginfo("Baslatildi! Engel gelince dur-don, yol acilinca PID ile hizlan.")
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
