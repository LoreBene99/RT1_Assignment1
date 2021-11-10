First Assignment of Research Track 1 <img src="https://media.giphy.com/media/3o7bu9HvCRRp7MjpT2/giphy.gif/giphy.gif" height=60>
================================
## Professor : Carmine Recchiuto, University of Genoa
This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course.
The main task of this assignment, given by the Professor Recchiuto, is to make the HOLONOMIC robot moves counterclockwisely in the virtual environment that he has presented. In this environment there are golden and silver tokens; the robot MUST avoid the golden tokens, that are regarded as WALLS, whereas it has to grab and release (thanks to specific
commands) the silver ones, letting them behind itself.
### Holonomic robot
<img height="35" width = "35" src="https://github.com/LoreBene99/RT_Assignment1/blob/main/sr/robot.png">

### The golden token regarded as WALLS that the robot must avoid
![alt text](https://github.com/LoreBene99/RT_Assignment1/blob/main/sr/token.png)

### The silver token with which it interacts
![alt text](https://github.com/LoreBene99/RT_Assignment1/blob/main/sr/token_silver.png)

### Environment (Maze)
<img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/map.png" > 
 
In this maze the robot starts its ride on the top left corner and, like i said before, has to:
* Moves counterclockwisely
* Avoids golden tokens 
* Grabs and releases behind it the silver tokens

All this is made by several lines of codes thanks to which the robot completes the proposed tasks. This assignment was not so easy, since i had to cope with
several problems that i will discuss. 



Installing and running 
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).
You could have some problems installing pygame in virtual enivronments since [not impossible](http://askubuntu.com/q/312767)). If you are using `pip`:
* you might try `pip install hg+https://bitbucket.org/pygame/pygame`
* you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). 
PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

Troubleshooting
---------------
When running `python run.py <file>`, there might be an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.
On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Running the programm
--------------------
In order to run the scripts in the simulator and make the game starts you have to insert this command on the shell,
after entering in the directory

```bash

$ python run.py assignment.py

```
Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

Project
-------
The robot interacts with the environment thanks to a series of properties extracted by the Robot class given by the Professor. 
Here are presented:

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision 

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

Methods
-------
We can achieve the aim of the project by using some functions that i have made so that the robot interacts,
in the correct way, with the environment, trying to get over the problems i have faced, like, for example, make the robot change direction properly 
in the turning points of the maze. Here there are:

### drive():
First of all the `drive()` function is used to make the robot moves in the maze. The speed of the motors are equals in order to make the robot goes straight.
The robot "drives" in the environment with a certain speed and for a certain interval of time. 
- Arguments 
  - `speed`: the linear velocity with which the robot moves.
  - `seconds`: the interval of time in which the robot moves.
- Returns
  - None.
- Code
```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
### turn():
Thanks to the function `turn()` the robot turns exactly in the spot in which it is, without having a linear velocity. It rotates on itself.
- Arguments 
  - `speed`: the angular velocity with which the robot rotates on itself.
  - `seconds`: the interval of time in which the robot turns, rotating on itself.
- Returns
  - None.
- Code
```python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
### find_silver_token():
The robot can see all the the tokens around it in the map, in a field of view of 360 degrees and within a particular distance. This function checks all the tokens that the robot see thanks to the R.see() method and returns the distance and the angle between the robot and the closest silver token. This might create some problems since the silver token, after grabbing it and releasing it behind itself, will remain the closest silver token, so the robot will turn and grab it again. To avoid this problem, in order to make the robot goes directly to the next token, we can limit its field of view in a maximum range of 3 and inside a particular angle `φ`, which is -65°<`φ`<65°; then the robot will see the silver tokens only in front of it and will no longer grab the token behind it. 
- Arguments 
  - None.
- Returns
  - Returns distance of the closest silver token and the angle between the robot and the closest silver token [`dist`(-1 if no silver token is detected), `rot_y`(-1 if no silver token is detected)].
- Code
```python
def find_silver_token():
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -65<token.rot_y<65:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y
```
<p align="center">
<img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/fov.png" width="300" height="300"> 
</p>

### find_golden_token():
The `find_golden_token()` function has the same structure of the previous one (find_silver_token()). This function is very important since it is used to not let the robot crush against the golden tokens (walls) in front of it, so the robot can move properly in the maze. This time the we have an higher distance (100) in order to check where is the closest golden token and a restricted view inside a particular angle `φ`, which is -35°<`φ`<35° in order to have the robot checking the golden tokens in front it.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token and angle between the robot and the closest golden token [`dist`(-1 if no golden token is detected), `rot_y`(-1 if no golen token is detected)]..
- Code
```python
def find_golden_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -35<token.rot_y<35:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
```
<p align="center">
<img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/fov1.png" width="300" height="300"> 
</p>

### find_golden_token_left(): 
The `find_golden_token_left()` function is used to check the distance of the golden tokens on the left and we can use it with the function `find_golden_token_right()` in order to make the robot changes direction properly in the maze, turning itself in the critical turning points of the maze. We can check the golden boxes on the left by restricting the field of view within a particular angle, which now is `-110°<φ<-70°` (the angle is negative on the left).
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token on the left [`dist`(-1 if no silver token is detected)].
- Code
```python
def find_golden_token_left():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -110<token.rot_y<-70:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
```
### find_golden_token_right(): 
The `find_golden_token_right()` function is the same of the previous one. Thanks to this function the robot detects the distance of the golden token on the right. It only changes the angle which is `70°<φ<110°`(the angle is positive on the right).
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token on the right (`dist`).
- Code
```python
def find_golden_token_right():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
            dist=token.dist
    if dist==100:

```
<p align="center">
<img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/rl.png" width="300" height="300"> 
</p>

### grab():
The function `grab()` was made to "clean" the main and insert the grab routine, made by the robot, inside a function. When the robot is close to a silver token, it will grab it and then release it always in the same way.
- Arguments 
  - None.
- Returns
  - None.
- Code
```python
def grab():
	if R.grab():
		print("Gotcha!")
		turn(30,2)
		drive(20,2)
		R.release()
		drive(-20,2)
		turn(-30,2)
```
<p align="center">
 <img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/grab.gif" width="250" height="200">
</p>

### adjust_grab(dist_silver,rot_y_silver):
This function is very important since the robot has to allign in the right way before getting closer to the silver token and then starting the grab routine. 
- Arguments 
  - rot_silver (float): angle between the robot and the closest silver token;
  - dist_silver (float): distance from the closest silver token.
- Returns
  - None.
- Code
```python
def adjust_grab(dist_silver, rot_y_silver):
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
```
### detect_walls(dist_left_golden, dist_right_golden):
This is one of the main function in the entire code. This function is very important since it makes the robot turns and change direction in the map. The return values of find_golden_token_left and find_golden_token_right are the arguments of this function thanks to which the robot turns properly: when the robot is close to a wall it will computes the distance of the golden tokens on the left and the one of the golden tokens on the right. If the distance of the golden token on the left is higher than the distance of the golden tokens on the right the robot will turn on the left, otherwise it will turn on the right, until no golden tokens are detected in a threshold area g_th. Thus this function helps the robot changing its direction inside the environment correctly.
- Arguments
  - dist_left_golden (float): distance of the closest gloden token on the left of the robot;
  - dist_right_golden (float): distance of the closest gloden token on the right of the robot; 
- Returns
  - None.
- Code
```python
def detect_walls():
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
```
<p align="center">
 <img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/wall.gif" width="250" height="200">
</p>

## MAIN()
The main function is the core of the project. In the main function there are all the functions that a previously described and developed and are all logically connected in order to make the robot moves around the environment, fulfilling all the requirements proposed by our Professor. Since we want the robot moves in loop endlessy inside the map, we have to put the instructions inside a while loop which loops endlessy, always updating the informations.
This is the main code, in which all the commands i've done are explained:
```python
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
```
#### NB: I've personally put the parameters in the functions, since i tested how they worked during several proofs testing the code
#### IMPORTANT!: The images don't have the proper scale, of course d=3 e d=100 have a huge difference, but you can not notice it very well

Conclusions
-----------
This project was very helpful since i practiced a lot with python coding. Furthermore i learned a lot about github, a platform that was an unknown to me since i've started this course, and how important it can be. I'm very satisfied about the time i spent on this project because, even if the overall result can be much better, i've put together different acquaintances, be they IT, logical or geometric (even simple things) in order to make the robot move in the right way in the environment. 
This is a speeded up video that i recorded from my screen just to show how the robot moves:

https://user-images.githubusercontent.com/91314586/140918228-6ee706e0-ecd4-4978-b335-035736894618.mp4

Flowchart
---------
This is a flowchart that perfectly described how the robot behaves inside the environment. We can examine in details all the possible routes that the robot can take in various circumstances; It is very useful since we can have a better look on how the robot "thinks" during the loops and in which state it enter depending on the situation.
<p align="center">
<img src="https://github.com/LoreBene99/RT_Assignment1/blob/main/images/flowchart.jpeg" width="1200" height="800"> 
</p>

### WARNING!: There is an END because the robot stop its moving when the left and the right distance from the wall is similar (this is a particular case). Checking the loops i noticed that this problem happens very rarely, but i wanted to specify it anyway. Of course this problem can be avoided and indeed is one of the main points on the possible improvements to do.

Possible Improvements
---------------------



   
