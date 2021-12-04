import random
import math

def distanceFromCentre(x,y):
    # Calculate distance from centre
    distx = (0.5 - x)**2
    disty = (0.5 - y)**2
    distance = math.sqrt(distx + disty)
    return distance

# Determine if point falls within circle
def inCircle(x,y):
    if distanceFromCentre(x,y) <= 0.5:
        return True
    else:
        return False

def countDecimals(num):
    if num > 0:
        splitNum = str(num).split('.')
        decimals = len(splitNum[1])
        return int(decimals)
    else:
        return 0

def estimate_pi(precision):
    totalPoints = 0
    circlePoints = 0
    estimate = 0
    for i in range(0,1000000):
        randomX = random.random()
        randomY = random.random()
        if inCircle(randomX, randomY) == True:
            circlePoints += 1
            totalPoints += 1
        else:
            totalPoints += 1
        estimate = 4 * (circlePoints / totalPoints)
    print(totalPoints)
    print(estimate)
    return round(estimate, precision)


print(estimate_pi(3))
