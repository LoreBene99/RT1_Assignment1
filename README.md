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

### Troubleshooting
When running `python run.py <file>`, there might be an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.
On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

### Running the programm
In order to run the scripts in the simulator and make the game starts you have to insert this command on the shell,
after entering in the directory

```bash

$ python run.py assignment(name_file).py

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
The robot can see all the the tokens around it in the map, in a field of view of 360 degrees and within a particular distance. This function checks all the tokens that the robot see thanks to the R.see() method and return the distance and the angle between the robot and the token.  

The `find_silver_token()` function is used to study all the silver tokens that are around the robot. The function checks all the tokens that the robot, we can say, sees thanks to `R.see()` method. The function only takes the tokens that are closer than 3 (which is pretty close inside the enviroment) and inside the angle `φ`, which is `-70°<φ<70°`. Obviously, as long as we want only silver tokens, we want to have as `marker_type` `MARKER_TOKEN_SILVER`, because it's what it differentiates it from the golden ones.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest silver token and angle between the robot and the closest silver token (`dist`, `rot_y`).
- Code
```python
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

