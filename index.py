import sys
import time
import turtle
import os
import math
import easygui
import tkinter as tk

# set up screen
mainScreen = turtle.Screen()
mainScreen.bgcolor("black")
mainScreen.title("Space Invdaders")
mainScreen.bgpic("ezgif-com-f278563c07.gif")
mainScreen.tracer(0)

# the shapes
turtle.register_shape("spaceship.gif")
turtle.register_shape("invaders.gif")

# the border
borderPen = turtle.Turtle()
borderPen.speed(0)
borderPen.color("white")
borderPen.penup()
borderPen.setposition(-300, -300)
borderPen.pendown()
borderPen.pensize(3)
for side in range(4):  # draw square
    borderPen.fd(600)  # go forward
    borderPen.lt(90)  # go left
borderPen.hideturtle()

# score
score = 0
scorePen = turtle.Turtle()
scorePen.speed(0)
scorePen.color("white")
scorePen.penup()
scorePen.setposition(-290, 280)
scoreString = "Score: {}".format(score)
scorePen.write(scoreString, False, align="left", font=("Arial", 14, "normal"))
scorePen.hideturtle()

# create player
player = turtle.Turtle()
player.color("blue")
player.shape("spaceship.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# create bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()  # so it doesnt draw a line
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bulletSpeed = 17


# def press():
#     print("hello")
#
# # pause button
# canvas = mainScreen.getcanvas()
# button = tk.Button(canvas.master, text="Press me", command=press)
# canvas.create_window(0, 300, window=button)

msg = "Please enter your name and age to play"
title = "Welcome to Space Invaders!"
fieldNames = ["Name", "Age"]
fieldValues = []
fieldValues = easygui.multenterbox(msg, title, fieldNames)
if fieldValues is None:
    exit()

# make sure that none of the fields were left blank
while 1:
    if fieldValues is None:
        break
    errmsg = ""
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            print(fieldValues[i])
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
    if errmsg == "": break  # no problems found
    fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)

# create enemy
numberOfEnemies = 30
enemies = []

for i in range(numberOfEnemies):
    enemies.append(turtle.Turtle())
enemyStartX = -225
enemyStartY = 250
enemyNumber = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invaders.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemyStartX + (50 * enemyNumber)
    y = enemyStartY
    enemy.setposition(x, y)

    # fix enemy number
    enemyNumber += 1
    if enemyNumber == 10:
        enemyStartY -= 50
        enemyNumber = 0
enemySpeed = 1

# define bullet states: ready and dire
bulletState = "ready"


def IsCollision(turtle1, turtle2):
    # calculate the collision based on the distance
    # math.pow in dutch terms is "tot de macht". Dus 2^2
    distance = math.sqrt(math.pow(turtle1.xcor() - turtle2.xcor(), 2) + math.pow(turtle1.ycor() - turtle2.ycor(), 2))

    # the higher the number, the closer the distance and greater the collision
    # if the number was 5 or 10, it's going to be hard to hit a target,
    # the bullet will pass thru the target or the target will pass thru the player
    if distance < 30:
        return True
    else:
        return False


def FireBullet():
    global bulletState
    if bulletState == "ready":
        bulletState = "fire"
        # set bullet position
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


# move the player
def MoveLeft():
    player.speed = -2


def MoveRight():
    player.speed = 2


def MovePlayer():
    x = player.xcor()  # at the start of the game x is 0
    x += player.speed  # subtracts speed every time key is pressed (make the ship move left to right on key press)

    if x < -280:  # set the boundaries
        x = -280

    if x > 280:
        x = 280
    player.setx(x)


# keyboard bindings
mainScreen.listen()
mainScreen.onkeypress(MoveLeft, "Left")
mainScreen.onkeypress(MoveRight, "Right")
mainScreen.onkeypress(FireBullet, "space")

# Using for loop
for u in range(len(fieldNames)):
    if fieldNames[u] == "Age":
        age = int(fieldValues[u])
        isinstance(age, int)

IsGameRunning = True


def main(score=score, enemySpeed=enemySpeed):
    while True:
        global bulletState, IsGameRunning
        while True:
            # IsGameRunning = True
            # update the screen, if this is turned off, nothing will show on the screen
            mainScreen.update()
            MovePlayer()
            msg = "Please enter your name and age to play"
            title = "Welcome to Space Invaders!"

            # move the bullet
            if bulletState == "fire":
                y = bullet.ycor()
                y += bulletSpeed
                bullet.sety(y)

            # if bullet is outside border
            if bullet.ycor() > 275:
                bullet.hideturtle()
                bulletState = "ready"

            for enemy in enemies:
                # move the enemy
                x = enemy.xcor()
                x += enemySpeed
                enemy.setx(x)

                # move enemies down
                if enemy.xcor() > 280:
                    for e in enemies:
                        y = e.ycor()
                        y -= 40
                        e.sety(y)
                    enemySpeed *= -1

                if enemy.xcor() < -280:
                    for e in enemies:
                        y = e.ycor()
                        y -= 40
                        e.sety(y)
                    enemySpeed *= -1

                # collision between bullet and enemy
                if IsCollision(bullet, enemy):
                    # reset bullet
                    bullet.hideturtle()
                    bulletState = "ready"
                    bullet.setposition(0, -400)
                    # remove enemy
                    enemies.remove(enemy)
                    enemy.hideturtle()
                    score += 10
                    scoreString = "Score: {}".format(score)
                    scorePen.clear()
                    scorePen.write(scoreString, False, align="left", font=("Arial", 14, "normal"))
                    if not enemies:
                        easygui.msgbox("You win", "Congratulation!")
                        # break

                if IsCollision(player, enemy):
                    time.sleep(1)
                    IsGameRunning = False
                    easygui.msgbox('You lost. Please try again', 'Game over!')
                    player.hideturtle()
                    break
            break

        if IsGameRunning is False:
            time.sleep(1)
            if easygui.ccbox(msg, title):  # show a Continue/Cancel dialog
                # user chose Continue
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:  # user chose Cancel
                exit()


if __name__ == "__main__":
    main()
    mainScreen.exitonclick()
