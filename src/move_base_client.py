#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
import json
import time

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()


    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = hamal["position"]["x"]
    goal.target_pose.pose.position.y = hamal["position"]["y"]
    goal.target_pose.pose.position.z = hamal["position"]["z"]
    goal.target_pose.pose.orientation.x = hamal["orientation"]["x"]
    goal.target_pose.pose.orientation.y = hamal["orientation"]["y"]
    goal.target_pose.pose.orientation.z = hamal["orientation"]["z"]
    goal.target_pose.pose.orientation.w = hamal["orientation"]["w"]

    client.send_goal(goal)
    wait = client.wait_for_result()
        
    collection.update_one({"data":"robot3"}, { "$set": {"target_executed":1}})
        
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == '__main__':
       
    client=MongoClient()
    client = MongoClient("mongodb://localhost:27017/")
    db = client.ros_db
    collection = db.ros_db_col
    
    rospy.init_node('move_base_client')
    
    while True:
        hamal = collection.find_one({"data" : "robot3"})
        if hamal["target_executed"] == 0:
            result = movebase_client()
            if result:
                rospy.loginfo("Goal execution done!")
        else:
            print("No new target!")
        time.sleep(1)
    

    #rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
