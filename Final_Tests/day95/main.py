from interface import create_screen, create_scoreboard, update_score
from player import create_player, move_left, move_right
from ships import Enemy
from bullet import create_bullet, fire_bullet
import turtle, time

#global variable
label = None
button = None
text = None
last_shot_time = 0
reload_times = []

def is_collision(projectile, enemy_body):
    return projectile.distance(enemy_body) < 20

def fire():
    global bullet_state, last_shot_time, bullets_fired, reload_times, gameover #load the globals

    if gameover: #it dont fire if its paused at game over screen
        return

    now = time.time() #gets now time

    #half sec delay between shots
    if now - last_shot_time < 0.5:
        return

    #reloading shooted bullets
    reload_times = [t for t in reload_times if now - t < 3]
    bullets_fired = len(reload_times)

    if bullets_fired < 3:
        bullet_state = fire_bullet(bullet, player, bullet_state)
        if bullet_state == "fire":
            last_shot_time = now
            reload_times.append(now)
    else:
        pass  #no bullets

def game_over():
    global gameover, label, button, text
    gameover = True

    #game over label
    label = turtle.Turtle()
    label.hideturtle()
    label.color("red")
    label.penup()
    label.goto(0, 50)
    label.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

    #white btn to restart
    button = turtle.Turtle()
    button.hideturtle()
    button.penup()
    button.color("white")
    button.goto(-60, -65)
    button.begin_fill()
    for _ in range(2):
        button.forward(120)
        button.left(90)
        button.forward(30)
        button.left(90)
    button.end_fill()

    #white btn text
    text = turtle.Turtle()
    text.hideturtle()
    text.color("black")
    text.penup()
    text.goto(0, -58)
    text.write("REINICIAR", align="center", font=("Arial", 14, "bold"))

    #calling to check the click
    screen.onclick(check_click)

def check_click(x, y):
    #checking the click area
    if -60 <= x <= 60 and -65 <= y <= -35:
        restart_game()

def restart_game(x=None, y=None):
    global gameover, bullet_state, bullets_fired, reload_times, score
    global label, button, text

    #cleaning the screen
    if label:
        label.clear()
        label.hideturtle()
    if button:
        button.clear()
        button.hideturtle()
    if text:
        text.clear()
        text.hideturtle()

    #reseting objects and variables
    player.goto(0, -250)
    bullet.hideturtle()
    bullet.goto(0, -400)
    bullet_state = "ready"
    bullets_fired = 0
    reload_times = []
    score = 0
    update_score(score_display, score)

    #reseting enemies pos
    for enemy in enemies:
        enemy.reset_position()

    #game on again
    gameover = False

####################################SCREEN INIT
screen = create_screen()
score_display = create_scoreboard()

#player init
player = create_player()
player_speed = 20

bullet = create_bullet()
bullet_speed = 20
bullet_state = "ready"

enemies = [Enemy() for _ in range(10)]
enemy_speed = 2

score = 0
gameover = False
bullets_fired = 0

#control listeners
screen.listen()
screen.onkeypress(lambda: move_left(player, player_speed) if not gameover else None, "Left")
screen.onkeypress(lambda: move_right(player, player_speed) if not gameover else None, "Right")
screen.onkeypress(fire, "space")

##############################main loop
while True:
    screen.update()

    #recharging time
    now = time.time()
    reload_times = [t for t in reload_times if now - t < 3]
    bullets_fired = len(reload_times)

    if not gameover: #enemie movement if not paused at game over screen
        for enemy in enemies:
            enemy.move()

            if enemy.is_off_screen():
                enemy.reset_position()

            if enemy.body.distance(player) < 30: #contact with player
                game_over()
                break

            if bullet_state == "fire" and is_collision(bullet, enemy.body):
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.goto(0, -400)
                enemy.reset_position()
                score += 10
                update_score(score_display, score) #update score if enemy hit by bullet

        if bullet_state == "fire":
            y = bullet.ycor()
            y += bullet_speed
            bullet.sety(y)

            if bullet.ycor() > 275:
                bullet.hideturtle()
                bullet_state = "ready"