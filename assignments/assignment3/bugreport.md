# Design and Professional Skills Assignment 3: Debugging the Frogger Game

*Charlie Barber*



## Bug 1

### Report

**Moving the frog onto a turtle causes death**

When the player (frog) moves onto one of the turtles on the river crossing, they die.

They should not die and instead be able to use the turtles as a method of crossing to get home.

To recreate this bug, you have to move the frog on to a turtle.

### Cause

After following the logic of the code in the `check_frog_crossing_river()` function, I spotted a spelling mistake in line 371 which checked whether the frog is on a *log*. Note that the program considers a turtle as a *log* in the context of crossing the river. This is shown with a comment below

```python
    def check_frog_crossing_river(self):
        # frog is crossing the river
        on_log = self.frog.on_log()
        if (not (on_log is None)) and (not on_log.contains(self.frog)):
            # frog was on a log, but has now left that log
            on_log = None
        if on_log is None:
            # it's no longer on the previous log
            # check if it's now on any other log
            for log in self.logs:
                if log.contains(self.frog):
                    # Here is the spelling mistake:
                    on_long = log
                    break
```

### Fix

To fix this, I had to change

```python
on_long = log
```

to

```python
on_log = log
```



## Bug 2

### Report

**Moving up or down out of the playing screen does not lead to death but moving out of the left or right bounds does**

The frog is able to go beyond the limits of the vertical canvas without dying where as if they go beyond the horizontal limits they die.

I believe the limits should be consistent. Therefore, the frog should die if they go beyond the vertical limits.

To recreate the bug, you have to move all the way down from the spawn point.

### Cause

I searched in the file for any functions which call the the `died()` function of the Frog class. I found in the `check_frog()` function that there is an if statement checking if the frog is past the canvas width.

```python
		(x, y) = self.frog.get_position()
        if x < 0 or x > CANVAS_WIDTH:
            print("canvas width")
            self.died()
            return
```

I tested that this was indeed the correct part of code which led to death by printing to the console and going out of the bounds while playing. This confirmed that this is the function.

This code is lacking anything which checks for the y position and canvas_height.

### Fix

Therefore, I need to implement an if statement that checks for the y position in a similar vein to the above code snippet for the x position.

All I had to do was duplicate the function with the correct variable names.

```python
 if y < 0 or y > CANVAS_HEIGHT:
            self.died()
            return
```



## Bug 3

### Report

**When the frog dies, they continue to lose lives until the game is over**

The previous bug exposed another bug where once the frog dies, they keep on dying and losing lives until the have none left and the game is over.

Instead, after dying the frog should respawn and have another life, until they run out of lives.

To recreate the bug, you have to die by being hit by a car or falling in the river.

### Cause

I suspect that the cause of this bug is related to a variable dictating if the frog has died never getting changed back to False or alive.

I used a print function to check if the `new_life()` function is getting called, which confirmed that it is.

This made me realise that it cannot be to do with any variables not being set to a new life or alive. Alternatively, I noticed that the frog never respawns in the start position so the game is never properly reset upon a new life. I tried including the `self.reset_level()` function in the `new_life()` function to respawn the frog. However this had the side effect of meaning the frog gained all their lives back. This meant I would have to use some of the code from the `self.reset_level()` function without including any part that resets lives.

### Fix

Upon looking through the mentioned reset level function, I noticed a line of code calling:

```python 
        self.frog.reset_position()
```

This described exactly what I needed to do. I then added this to the `new_life()` function and it successfully respawned the frog without resetting the lives:

```python
  def new_life(self):
        print("new life called")
        self.controller.update_lives(self.lives)
        self.frog.reset_position()
```



## Bug 4

### Report

**The time bar does not start moving until about a minute after the game starts**

The time bar at the bottom of the screen does not represent any progress until after around a minute of play time.

I think the time bar should start moving immediately. 

To recreate the bug, start the game.

### Cause

My first idea for the cause was that the time bar is not scaled correctly and part of it is running down outside of the canvas - invisible to the player.

The value for time is declared at the top as 120 seconds or 2 minutes.

```python
LEVEL_TIME = 120
```

The class which creates the time bar on the canvas is located in the *fr_view.py* file rather than the model file used previously.

```python
class TimeView():
    def __init__(self, canvas):
        self.canvas = canvas
        self.end_time = time.time()
        self.bar = self.canvas.create_rectangle(0,0,0,0) #placeholder
```

This initiation of the object does not create the bar but rather a placeholder. Instead, it is created in the `update()` function:

```python
    def update(self, time_now):
        remaining = self.end_time - time_now
        if remaining > 0:
            self.canvas.delete(self.bar)
            self.bar = self.canvas.create_rectangle(CANVAS_WIDTH - 20*remaining - 100, GRID_SIZE*16.25, CANVAS_WIDTH - 100, GRID_SIZE*16.75, fill="green")
```

 This creates a new rectangle every second that goes by and deletes the old one. I checked that the remaining time is actually being calculated correctly by printing it out every time `update()` gets called. By printing this, I could see that it is at the 45 second mark that the bar starts moving. 

On top of this, I realised that running out of time does not lead to game over, which I will fix in the next bug report. 

The `create_rectangle` function accepts 4 parameters, (x1, y1, x2, y2, option). This means that the issues stems from the first parameter as this is the left hand horizontal edge of the rectangle. Canvas width is set at 1000, so at the start if time remaining is 120, `CANVAS_WIDTH - 20*remaining - 100` will evaluate to `1000 - 20*120 - 100` = `1000 - 2400 - 100` = `z-1500` which is way off the screen. I checked this was the case with a print statement which confirms that it counts down from -1500.

### Fix

After realising this I used trial and error with a calculator changing the multiplier of 20 until I found a result that was within the bounds. 7 turned out to be this magic number which had a starting x value of 60 and a final x value of 900 - both within the bounds.

```python
self.bar = self.canvas.create_rectangle(CANVAS_WIDTH - 7*remaining - 100, GRID_SIZE*16.25,CANVAS_WIDTH - 100, GRID_SIZE*16.75, fill="green")
```



### Bug 5

### Report

**Time running out does not lead to game over** 

As previously mentioned, when the game runs out of time it does not lead to game over. 

Instead, the game should finish when it runs out of time. 

To recreate the bug, you must let the time run out. This can be done more easily by changing the time to a 10 seconds.

### Cause

While fixing the last bug and printing out the time left every time `update()` is called, I could see that after 0 seconds the time goes into negative numbers.

### Fix

To fix this, I needed to add a condition which checks if time remaining is less than 0 and to call game over.

I would need to include this in a function which is constantly checked, which `check_frog()` seemed suitable for. I calculated the remaining time by copying another local variable declaration to calculate the remaining time later in the code.

```python
        remaining_time = int(self.end_time - time.time())
        if remaining_time < 0:
            self.game_over()
```



## Bug 6

### Report

**It is impossible to enter the first home**

The frog is unable to go into the first home from the left.

They should be able to go into this in order to finish the level by entering all 5 homes.

To recreate the bug, the frog must try and enter the first home from the left.

### Cause

I suspect that the problem is in the `create_homes()` function as this is the one that creates the homes. The graphical aspect of the homes is created separately but the code defining where they are is in this function. 

```python
        x = (spacing + GRID_SIZE)//2
        for i in range(0,6):
            x = x + GRID_SIZE + spacing
            self.homes_x.append(x)
            self.homes_occupied.append(False)
```

The for loop creates the position of each home and then appends it to an array containing its x value. To find the cause I tried to print the x value that gets created by the for loop. Upon printing the X values, I noticed that the first homes value is 300 and the final one is 1100, which is out of the bounds.

### Fix

To fix this, I had to offset the initial x value by 200. 

```python
        x = (spacing + GRID_SIZE)//2 - 200
```



## Bug 7

### Report

**When frog dies and tries to restart, the x game is frozen**

When the frog dies and the player presses r to restart, the game freezes.

Instead the player should press r and the game restarts as normal.

To recreate the bug, the player must restart the game by pressing the R key.

### Cause

The cause should be in the `restart()` function. I noticed that in the `move_frog()` function, moving the frog relies on a variable called `game_running`. I guessed that this would need to be changed when the 

### Fix

To fix this, I would have to add a line in `restart()` which sets `game_running` to True upon being called.

```python
    def restart(self):
       self.game_running = True
```

