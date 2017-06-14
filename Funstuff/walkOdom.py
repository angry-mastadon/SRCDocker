import time
import rospy
import tf
import tf2_ros
import numpy
import math
from collections import OrderedDict
from math import cos, radians, sin, sqrt
import select
import sys
import termios
import tty

from geometry_msgs.msg import Quaternion, Transform, Vector3


from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, PoseWithCovariance, TwistWithCovariance, Point 
import copy
import sys
from ihmc_msgs.msg import FootstepStatusRosMessage
from ihmc_msgs.msg import FootstepDataListRosMessage
from ihmc_msgs.msg import FootstepDataRosMessage
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_matrix
import tf2_ros
from visualization_msgs.msg import Marker
import rospy
import copy
from ihmc_msgs.msg import NeckTrajectoryRosMessage
from ihmc_msgs.msg import OneDoFJointTrajectoryRosMessage
from ihmc_msgs.msg import TrajectoryPoint1DRosMessage
import time
oldAngle =0.0
#stepCounter = 0
class walk:
    ROBOT_NAME = None
    LEFT_FOOT_FRAME_NAME = None
    RIGHT_FOOT_FRAME_NAME = None
    tfBuffer = None
    tfListener = None
    footStepListPublisher =None
    neck_publisher = None
    def walkTest(self, move, direc, fir):
	global oldAngle
	self.msg = copy.deepcopy(self.msgCopy)
	LEFT = 0
	RIGHT = 1
	START =2
	TURN = 3
	SHIFTLEFT = 4
	SHIFTRIGHT = 5
	SHIFTUP = 6
	RSTART = 7
	RTURN = 8
        SHIFTR = 9
        SHIFTL = 10
        ADJUSTR = 11
        ADJUSTL = 12
        REVERSE = 13
        if move == REVERSE:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [-.1, 0 , 0], 0))
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [-.1, 0, 0], 0))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(2)
            return
        if move == ADJUSTR:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [0, 0, 0], math.pi/36))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(1)
        if move == ADJUSTL:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [0, 0, 0], -math.pi/36))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(1)
        if move == SHIFTR:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [.1, 0, 0], 0))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(1)
        if move == SHIFTL:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [.1, 0, 0], 0))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(1)
	if move == SHIFTUP:
	    self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [.1, 0, 0], 0))
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [.1, 0, 0], 0))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(2)
	    return
	if SHIFTRIGHT == move:
	    self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [0, -0.1, 0], 0))
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [0, -.1, 0], 0))
	    self.footStepListPublisher.publish(self.msg)
	    self.waitForFootsteps(2)
	    return
	if move == SHIFTLEFT:
	    self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [0, 0.1, 0], 0))
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [0, .1, 0], 0))
	    self.footStepListPublisher.publish(self.msg)
	    self.waitForFootsteps(2)
	    return
	direction = float(direc)
        if move== START:
	    self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [.05*math.sin(oldAngle), .05*math.cos(oldAngle), 0.0], 0))
	    self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [-.05*math.sin(oldAngle), -.05*math.cos(oldAngle), 0.0], 0))
	    self.footStepListPublisher.publish(self.msg)
	    self.waitForFootsteps(len(self.msg.footstep_data_list))
	    return
        if move == RSTART:
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, [-.05, 0, 0], 0))
            self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, [.05, 0, 0], 0))
            self.footStepListPublisher.publish(self.msg)
            self.waitForFootsteps(2)
            return
    #print "Hello"
        curYpos = 0
        LEFT_FOOT = [0.0, 0.00, 0.0]
        RIGHT_FOOT = [0.0, -0.00, 0.0]
        #direction = float(direc)
        curXpos = 0.0
        side = LEFT
        curDistTraveled = 0.0
	if move == TURN:
	    rospy.loginfo('Turning')
            if direction >= 0:
	        curXpos = abs(.316*(math.sin(direction) + math.sin(oldAngle)))
	        curYpos = .316*(math.cos(oldAngle)-math.cos(direction))
	    if direction< 0:
		curXpos =  abs(-.316*(math.sin(direction) + math.sin(oldAngle)))
		curYpos = .316*(-1.0*math.cos(oldAngle)+math.cos(direction))
	    #oldAngle = direction
            if direction == 0:
                curYpos = 0
            if direction >=0:
		#curYpos -= .05
    	        #retVal = self.createRotationFootStepList(direction)
		RIGHT_FOOT[0] = curXpos
		RIGHT_FOOT[1] = (curYpos) 
	        side = LEFT
                self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, LEFT_FOOT, direction/(math.pi/2.0)))
       
                self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, RIGHT_FOOT, direction/(math.pi/2.0)))
            if direction <0:
		#curYpos += .05
	        LEFT_FOOT[0] = curXpos
	        LEFT_FOOT[1] = (curYpos)
	        side = RIGHT
		retVal = self.createRotationFootStepList(direction)
	        self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, RIGHT_FOOT,direction/(math.pi/2.0)))
	        self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, LEFT_FOOT, direction/(math.pi/2.0)))
	    self.footStepListPublisher.publish(self.msg)
	    self.waitForFootsteps(len(self.msg.footstep_data_list))
	    return
	curDistTraveled = 0.0
	if move == RTURN:
	    rospy.loginfo('RTurning')
            if direction >= 0:
	        curXpos = abs(.316*(math.sin(direction) + math.sin(oldAngle)))
	        curYpos = .316*(math.cos(oldAngle)-math.cos(direction))
	    if direction< 0:
		curXpos =  abs(-.316*(math.sin(direction) + math.sin(oldAngle)))
		curYpos = .316*(-1.0*math.cos(oldAngle)+math.cos(direction))
	    #oldAngle = direction
            if direction == 0:
                curYpos = 0
            if direction <0:
		#curYpos -= .05
    	        #retVal = self.createRotationFootStepList(direction)
		LEFT_FOOT[0] = curXpos
		LEFT_FOOT[1] = (curYpos) 
	        side = LEFT
                self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, RIGHT_FOOT, direction/(math.pi/2.0)))
       
                self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, LEFT_FOOT, direction/(math.pi/2.0)))
            if direction >=0:
		#curYpos += .05
	        RIGHT_FOOT[0] = curXpos
	        RIGHT_FOOT[1] = (curYpos)
	        side = RIGHT
		retVal = self.createRotationFootStepList(direction)
	        self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, LEFT_FOOT,direction/(math.pi/2.0)))
	        self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, RIGHT_FOOT, direction/(math.pi/2.0)))
	    self.footStepListPublisher.publish(self.msg)
	    self.waitForFootsteps(len(self.msg.footstep_data_list))
	    return
   
    #generate list of steps based on magnitude and direction
    #first rotate opposite foot and then start walking
        side = int(move)
        first = int(fir)
        dist = float(direction)
        currentDist = 0
        while currentDist<dist:
            if side == LEFT:
	        if first == 1:
		    print "first left"
	            LEFT_FOOT[0] =.4
	            LEFT_FOOT[1] = 0.0
		    #print LEFT_FOOT
	            first = 0
                    currentDist += .4
                else:
	            LEFT_FOOT[0] = 0.8
	            LEFT_FOOT[1] = 0.0	    
                    currentDist += 0.8
	        self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.LEFT, LEFT_FOOT, 0.0))
            if side == RIGHT:
	        if first == 1: 
		    print "first right"
                    RIGHT_FOOT[0] = .4
                    RIGHT_FOOT[1] = 0.0
		    #print RIGHT_FOOT
                    first = 0
                    currentDist += 0.4
                else:
                    RIGHT_FOOT[0] = .8
                    RIGHT_FOOT[1] = 0.0
                    currentDist += .8

                self.msg.footstep_data_list.append(self.createFootStepOffset(FootstepDataRosMessage.RIGHT, RIGHT_FOOT, 0.0))
            side ^=1
        self.footStepListPublisher.publish(self.msg)
        rospy.loginfo('walk forward...')
        self.waitForFootsteps(len(self.msg.footstep_data_list))
        return 
    def odomCallback(self, msg):
        print "called"
        self.pose = odomCallbackdata.pose.pose.position
        self.orient = data.pose.pose.orientation
        print self.pose
        print self.orient
# Creates footstep with the current position and orientation of the foot.
    def createFootStepInPlace(self, stepSide):
        footstep = FootstepDataRosMessage()
        footstep.robot_side = stepSide

        if stepSide == FootstepDataRosMessage.LEFT:
            foot_frame = self.LEFT_FOOT_FRAME_NAME
        else:
            foot_frame = self.RIGHT_FOOT_FRAME_NAME
        rospy.Subscriber('/ihmc_ros/localization/pelvis_odom/pelvis_odom_pose_correction', Odometry, self.odomCallback)
        print "here"
        footstep.orientation = self.orient
        footstep.location = self.pose
        return footstep

# Creates footstep offset from the current foot position. The offset is in foot frame.
    
    def createFootStepOffset(self, stepSide, offset, zrot):
        footstep = self.createFootStepInPlace(stepSide)
        
    # transform the offset to world frame
        quat = footstep.orientation
        rot = quat
        print rot
        print offset
        transformedOffset = numpy.dot(rot, offset)
	self.addMarker(zrot)
        footstep.location.x += transformedOffset[0]
        footstep.location.y += transformedOffset[1]
        footstep.location.z += transformedOffset[2]

        footstep.orientation.z += zrot

        return footstep
    def waitForFootsteps(self, numberOfSteps):
        global stepCounter
        stepCounter = 0
        while stepCounter < numberOfSteps:
            time.sleep(1)
        rospy.loginfo('finished set of steps')

    def recievedFootStepStatus(self, msg):
        global stepCounter
        if msg.status == 1:
            stepCounter += 1
    def appendTrajectoryPoint(self, neck_trajectory, time, positions):
        if not neck_trajectory.joint_trajectory_messages:
            neck_trajectory.joint_trajectory_messages = [copy.deepcopy(OneDoFJointTrajectoryRosMessage()) for i in range(len(positions))]
        for i, pos in enumerate(positions):
            point = TrajectoryPoint1DRosMessage()
            point.time = time
            point.position = pos
            point.velocity = 0
            neck_trajectory.joint_trajectory_messages[i].trajectory_points.append(point)
        return neck_trajectory

    def adjustNeck(self, position, time):
	testmsg = NeckTrajectoryRosMessage()
	testmsg.unique_id = -1
	testmsg = self.appendTrajectoryPoint(testmsg, time, position)
        self.neck_publisher.publish(testmsg)
    def __init__(self):
        self.orient = None
        self.pose = None
        try:
            rospy.init_node('ihmc_walk_test')

            if not rospy.has_param('/ihmc_ros/robot_name'):
                rospy.logerr("Cannot run walk_test.py, missing parameters!")
                rospy.logerr("Missing parameter '/ihmc_ros/robot_name'")

            else:
                self.ROBOT_NAME = rospy.get_param('/ihmc_ros/robot_name')

                right_foot_frame_parameter_name = "/ihmc_ros/{0}/right_foot_frame_name".format(self.ROBOT_NAME)
                left_foot_frame_parameter_name = "/ihmc_ros/{0}/left_foot_frame_name".format(self.ROBOT_NAME)

                if rospy.has_param(right_foot_frame_parameter_name) and rospy.has_param(left_foot_frame_parameter_name):
                    self.RIGHT_FOOT_FRAME_NAME = rospy.get_param(right_foot_frame_parameter_name)
                    self.LEFT_FOOT_FRAME_NAME = rospy.get_param(left_foot_frame_parameter_name)
		     
                    self.footStepStatusSubscriber = rospy.Subscriber("/ihmc_ros/{0}/output/footstep_status".format(self.ROBOT_NAME), FootstepStatusRosMessage, self.recievedFootStepStatus)
                    self.footStepListPublisher = rospy.Publisher("/ihmc_ros/{0}/control/footstep_list".format(self.ROBOT_NAME), FootstepDataListRosMessage, queue_size=1)
                    #self.tfBuffer = tf2_ros.Buffer()
                    #self.tfListener = tf2_ros.TransformListener(self.tfBuffer)
		    self.neck_publisher = rospy.Publisher("/ihmc_ros/{0}/control/neck_trajectory".format(self.ROBOT_NAME), NeckTrajectoryRosMessage, queue_size=1)
                    rate = rospy.Rate(10) # 10hz
                    time.sleep(1)

                # make sure the simulation is running otherwise wait
                    if self.footStepListPublisher.get_num_connections() == 0:
                        rospy.loginfo('waiting for subsciber...')
                        while self.footStepListPublisher.get_num_connections() == 0:
                                
			    rate.sleep()
			
		    if not rospy.is_shutdown():
			self.msg = FootstepDataListRosMessage()
        		self.msg.default_transfer_time = 0.8
       			self.msg.default_swing_time = 0.8
        		self.msg.execution_mode = 0
        		self.msg.unique_id = -1
			self.msgCopy = copy.deepcopy(self.msg)
			self.pub = rospy.Publisher('/torso', Marker, queue_size = 1)
			return
                    else:
                        if not rospy.has_param(left_foot_frame_parameter_name):
                            rospy.logerr("Missing parameter {0}".format(left_foot_frame_parameter_name))
                        if not rospy.has_param(right_foot_frame_parameter_name):
                            rospy.logerr("Missing parameter {0}".format(right_foot_frame_parameter_name))

        except rospy.ROSInterruptException:
            pass

