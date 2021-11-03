#---------------------------------------------LIBRARIES----------------------------------------------------------------
from __future__ import print_function

import time

#---------------------------------------IMPORTING CLASS ROBOT----------------------------------------------------------
from sr.robot import *

#----------------------------------------IMPORTANT VARIABLES-----------------------------------------------------------
a_th = 2.0
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

R = Robot()
""" instance of the class Robot """

g_th = 1.0
""" float: Threshold for the control of robot distance from the closest golden token """

#-----------------------------------------DEFINING FUNCTIONS-----------------------------------------------------------
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
#######################################################################################################################

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
#######################################################################################################################

def find_silver_token():
    """
    Function to find the closest silver token in front of the robot

    Returns:
	dist (float): distance of the closest silver token in front of the robot (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token in front of the robot (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -60<token.rot_y<60:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
#######################################################################################################################

def find_golden_token():
    """
    Function to find the closest golden token in front of the robot.

    Returns:
	dist (float): distance of the closest golden token in front of the robot (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token in front of the robot (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -35<token.rot_y<35:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
#######################################################################################################################
  	
def find_golden_token_right():
    """
    Function to find the closest golden token on the right of the robot

    Returns:
	dist (float): distance of the closest golden token on the right of the robot (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -70<token.rot_y<-110:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1
    else:
   	return dist
#######################################################################################################################

def find_golden_token_left():
    """
    Function to find the closest golden token on the left of the robot

    Returns:
	dist (float): distance of the closest golden token on the left of the robot (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 70<token.rot_y<110:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1
    else:
   	return dist
#######################################################################################################################

def grab():
	"""
	Function to define the routine grab made by the robot
	"""
	if R.grab():
		print("Gotcha!")
		turn(30,2)
		drive(20,2)
		R.release()
		drive(-20,2)
		turn(-30,2)








