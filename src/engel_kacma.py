#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# Durum sabitleri
ILERI = 0
DUR   = 1
DON   = 2

durum = ILERI
engel_mesafesi = 0.5  # metre

def tarama_callback(msg):
    global durum

    # Onun ortasindaki 30 derecelik alan (-15 ile +15 arasi)
    on_soldaki  = msg.ranges[0:15]
    on_sagdaki  = msg.ranges[345:360]
    on = list(on_soldaki) + list(on_sagdaki)

    # Sonsuz ve NaN degerleri filtrele
    on_temiz = [r for r in on if not (r == float('inf') or r != r)]

    if len(on_temiz) == 0:
        min_mesafe = float('inf')
    else:
        min_mesafe = min(on_temiz)

    if durum == ILERI:
        if min_mesafe < engel_mesafesi:
            durum = DUR
            rospy.loginfo("ENGEL ALGILANDI - DURUYOR")

    elif durum == DUR:
        durum = DON
        rospy.loginfo("DONUYOR")

    elif durum == DON:
        if min_mesafe >= engel_mesafesi:
            durum = ILERI
            rospy.loginfo("YOL ACIK - ILERLIYOR")

def engel_kacma():
    global durum

    rospy.init_node('engel_kacma', anonymous=True)

    rospy.Subscriber('/scan', LaserScan, tarama_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)
    hiz = Twist()

    rospy.loginfo("Engel kacma baslatildi!")

    while not rospy.is_shutdown():
        if durum == ILERI:
            hiz.linear.x  = 0.2
            hiz.angular.z = 0.0

        elif durum == DUR:
            hiz.linear.x  = 0.0
            hiz.angular.z = 0.0

        elif durum == DON:
            hiz.linear.x  = 0.0
            hiz.angular.z = 0.5

        pub.publish(hiz)
        rate.sleep()

if __name__ == '__main__':
    try:
        engel_kacma()
    except rospy.ROSInterruptException:
        pass
