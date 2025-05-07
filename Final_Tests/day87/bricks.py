from turtle import Turtle

class Brick(Turtle):
    COLOR_STAGES = {
        "red":    ["#ff0000", "#cc0000", "#990000", "#660000"],  # 4 stages = 4 hits
        "orange": ["#ffa500", "#cc8400", "#996300"],             # 3 stages = 3 hits
        "yellow": ["#ffff00", "#cccc00"],                        # 2 stages/hits
        "green":  ["#00ff00"]                                    # 1 hit
    } #color feedback to hits

    def __init__(self, x, y, color):
        super().__init__()
        self.color_sequence = Brick.COLOR_STAGES[color]
        self.hits_remaining = len(self.color_sequence)
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=3) #scale to retangle
        self.goto(x, y) #self atributted pos
        self.update_color()

    def hit(self):
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            self.destroy()
            return True
        else:
            self.update_color()
            return False

    def update_color(self):
        stage_index = len(self.color_sequence) - self.hits_remaining
        self.color(self.color_sequence[stage_index])

    def destroy(self):
        self.hideturtle()
        self.goto(1000, 1000)