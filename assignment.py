#---------------------------------------------LIBRARIES----------------------------------------------------------------
from __future__ import print_function

import time

#---------------------------------------IMPORTING CLASS ROBOT----------------------------------------------------------
from sr.robot import *

#----------------------------------------IMPORTANT VARIABLES-----------------------------------------------------------
a_th = 2.2
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

R = Robot()
""" instance of the class Robot """

g_th = 1.0
""" float: Threshold for the control of robot distance from the closest golden token """

s_th = 1.5
""" float: Threshold for the control of the robot near to a silver token in order to start the grab routine """


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
    Function to find the closest silver token in front of the robot.

    Returns:
	dist (float): distance of the closest silver token in front of the robot (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token in front of the robot (-1 if no silver token is detected)
    """
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -65<token.rot_y<65:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
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
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 70<token.rot_y<110:
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
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -110<token.rot_y<-70:
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
#######################################################################################################################

def detect_walls(dist_left_golden, dist_right_golden):
	"""
	Function to detect the walls near the robot that avoid them
	"""
	print("There is a wall near me!!")

	if (dist_left_golden > dist_right_golden):
		print("Turn left a bit because the wall is on the right at this precise distance:" + str(dist_right_golden))
		turn(-20, 0.2)
			
	elif (dist_left_golden < dist_right_golden):
		print("Turn right a bit because the wall is on the left at this precise distance:" + str(dist_left_golden))
		turn(20,0.2)
			
	else:
		print("Similar distance from left and right golden token")
		print("Distance of the wall on the left:" + str(dist_left_golden))
		print("Distance of the wall on the right:" + str(dist_right_golden))
#######################################################################################################################

def adjust_grab(dist_silver,rot_y_silver):
	"""
	Function that makes the robot adjust his orientation toward the token
	"""

	print("I'm near to a silver token!")
			
	if (dist_silver < d_th):
		print("Found it!!")
		grab()
		
	elif -a_th <= rot_y_silver <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, that'll do.")
		drive(35, 0.2)
		
	elif rot_y_silver < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-8, 0.2)
		
	elif rot_y_silver > a_th:
		print("Right a bit...")
		turn(+8, 0.2)
#######################################################################################################################

def main():
	while 1:
		
		# In order to make the robot moves in an infinite cycle we use a while loop. Thanks to this while
		# we also update every single time the information about the silver and golden tokens. 
		
		dist_silver, rot_y_silver = find_silver_token()
		dist_golden, rot_y_golden = find_golden_token()
		dist_right_golden = find_golden_token_right()
		dist_left_golden = find_golden_token_left()
	    
		# The robot should avoid golden tokens and grab the silver ones, so if the robot is far from golden tokens 
		# and it's not close enough to the silver ones, it goes straight, thanks to the defined function drive().
		# The parameters are set in order to make the robot move fast.
		# We also introduce a threshold "s_th" in order to make the robot adjust properly his orientation toward the silver tokens
		# before getting close to them and then grabbing them. Moreover (thanks to s_th) the robot doesn't push the silver token without grabbing them
	    
		if (dist_silver > s_th and dist_golden > g_th) or (dist_silver == -1 and dist_golden > g_th):
			print("Go!!")
			drive(100,0.05)
		
		# The robot detect a silver token and get closer to it, changing its velocity and 
		# always adjusting its orientation thanks to the elif commands put in the adjust_grab() function
		
		if (dist_silver < s_th) and (dist_silver != -1):
		
		# When the robot is near to a silver token, perfectly allineated, it will grab the silver one.
		
			adjust_grab(dist_silver, rot_y_silver)
		
		# Of course we have to check the distance of the robot from the golden tokens, since they represents the "walls" and 
		# the robot must avoid them. The robot should also check the distance from the right golden token and from the left golden 
		# so we can make it easily turns direction, in order to complete counterclockwisely the path in the environment
		
		if (dist_golden < g_th) and (dist_golden != -1):
			detect_walls(dist_left_golden, dist_right_golden)
#---------------------------------------------MAIN CALL-----------------------------------------------------------------------

main()
