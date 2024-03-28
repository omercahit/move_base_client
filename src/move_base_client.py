#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
import json
import time

def movebase_client(id):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    target_list = hamal["Targets"]

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = float(target_list[id]["Position"]["x"])
    goal.target_pose.pose.position.y = float(target_list[id]["Position"]["y"])
    goal.target_pose.pose.position.z = float(target_list[id]["Position"]["z"])
    goal.target_pose.pose.orientation.x = float(target_list[id]["Orientation"]["x"])
    goal.target_pose.pose.orientation.y = float(target_list[id]["Orientation"]["y"])
    goal.target_pose.pose.orientation.z = float(target_list[id]["Orientation"]["z"])
    goal.target_pose.pose.orientation.w = float(target_list[id]["Orientation"]["w"])

    print(goal)

    client.send_goal(goal)
    wait = client.wait_for_result()
        
    target_list[id]["targetExecuted"] = True
    collection.update_one({"robotName":"robot2"}, { "$set": {"Targets": target_list}})
        
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == '__main__':
       
    client=MongoClient()
    client = MongoClient("mongodb://172.16.66.130:27017/")
    db = client.altinay_amr_fleet
    collection = db.robots
    
    rospy.init_node('move_base_client')
    
    while True:
        hamal = collection.find_one({"robotName" : "robot2"})
        target_count = len(hamal["Targets"])
        for i in range (0,target_count):
            if hamal["Targets"][i]["targetExecuted"] == False:
                result = movebase_client(i)
                if result:
                    rospy.loginfo("Goal execution done!")
                    collection.update_one({"robotName":"robot2"}, { "$set":{"Task.taskPercentage": 100.0, "Task.pathPoints": []}})
            else:
                print("No new target!")
            rate = rospy.Rate(10)
            if not rospy.is_shutdown():
                rate.sleep()
    

    #rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
