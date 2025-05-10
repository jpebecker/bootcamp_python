import turtle

def create_screen():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Space Invaders Copy")
    screen.setup(width=600, height=600)
    screen.tracer(0)
    return screen

def create_scoreboard():
    score_display = turtle.Turtle()
    score_display.speed(0)
    score_display.color("white")
    score_display.penup()
    score_display.hideturtle()
    score_display.goto(-270, 260)
    score_display.write("Pontos: 0", font=("Arial", 16, "bold"))
    return score_display

def update_score(score_display, score):
    score_display.clear()
    score_display.write(f"Pontos: {score}", font=("Arial", 16, "bold"))
