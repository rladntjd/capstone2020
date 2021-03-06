#!/usr/bin/env python

import rospy
from math import pi
from capstone2020.msg import GpsData
from capstone2020.srv import SetArea

class safeArea:
    def __init__(self):
        self.recieve = False
        self.gps_data = GpsData()

        self.width = 0
        self.height = 0
        self.radius = 0

        rospy.Subscriber("/gps_data", GpsData, self.gpsCb)

        self.set_area_client = rospy.ServiceProxy("/set_area", SetArea)

    def send_srv(self, shape, latitude, longitude, width, height, radius):
        rospy.wait_for_service('/set_area')

        resp = self.set_area_client(shape, latitude, longitude, width, height, radius)

        if resp.result == True:
            rospy.loginfo("OK")
            return True

        else:
            rospy.loginfo("Fail")
            return False

    def gpsCb(self, msg):
        self.recieve = True
        self.gps_data = msg

    def input_area(self):
        rospy.loginfo("shape of safe area[rec, cir]: ")
        shape = {"rec": 1, "cir": 2}.get(input(), 3)

        try:
            if shape == 1:
                rospy.loginfo("Width[m]: ")
                self.width = float(input())
                rospy.loginfo("Height[m]: ")
                self.height = float(input())

            elif shape == 2:
                rospy.loginfo("Radius[m]: ")
                self.radius = float(input())

            else:
                rospy.logerr("Should be \"rec\" or \"cir\"")
                return False

        except:
            rospy.logerr("Input only number")
            return False

        return self.send_srv(shape, self.gps_data.latitude, self.gps_data.longitude, self.width, self.height, self.radius)

if __name__ == "__main__":
    rospy.init_node("set_area_node")

    safe_area = safeArea()

    result = False

    try:
        while not rospy.is_shutdown() and safe_area.recieve is False:
            rospy.logwarn("Waiting until GPS data recieve")
            rospy.sleep(1)
        
        while not rospy.is_shutdown() and result is False:
            result = safe_area.input_area()

    except:
        pass