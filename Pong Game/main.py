import turtle
import time

# ==================== CONSTANTS ====================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH_STRETCH = 5
PADDLE_LENGTH_STRETCH = 1
PADDLE_MOVE_DISTANCE = 20
RIGHT_PADDLE_X = 350
LEFT_PADDLE_X = -350
PADDLE_Y_LIMIT = 250
BALL_SPEED_START = 0.07  # Slightly faster start for more engagement
PADDLE_COLLISION_X = 320
WALL_Y_LIMIT = 280
SCORE_LIMIT = 10

# ==================== Paddle Class ====================
class Paddle(turtle.Turtle):
    """Represents the player's paddle with bounded movement."""

    def __init__(self, x_cord, y_cord):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=PADDLE_WIDTH_STRETCH, stretch_len=PADDLE_LENGTH_STRETCH)
        self.color("white")
        self.goto(x_cord, y_cord)

    def move_up(self):
        """Moves the paddle up but stops it at the screen edge."""
        if self.ycor() < PADDLE_Y_LIMIT:
            new_y = self.ycor() + PADDLE_MOVE_DISTANCE
            self.goto(self.xcor(), new_y)

    def move_down(self):
        """Moves the paddle down but stops it at the screen edge."""
        if self.ycor() > -PADDLE_Y_LIMIT:
            new_y = self.ycor() - PADDLE_MOVE_DISTANCE
            self.goto(self.xcor(), new_y)

# ==================== Ball Class ====================
class Ball(turtle.Turtle):
    """Represents the game ball."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("white")
        self.x_move = 10
        self.y_move = 10
        self.pace = BALL_SPEED_START

    def move(self):
        """Moves the ball according to its current trajectory."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Reverses the ball's vertical direction."""
        self.y_move *= -1

    def bounce_x(self):
        """Reverses the ball's horizontal direction and increases its speed."""
        self.x_move *= -1
        self.pace *= 0.9  # Increase speed by 10%

    def reset_pos(self):
        """Resets the ball to the center and resets its speed."""
        self.goto(0, 0)
        self.pace = BALL_SPEED_START
        self.bounce_x()  # Reverse direction for the other player

# ==================== Scoreboard Class ====================
class Scoreboard(turtle.Turtle):
    """Manages the game's score display."""

    def __init__(self):
        super().__init__()
        self.l_score = 0
        self.r_score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears and redraws the score on the screen."""
        self.clear()
        self.goto(-100, 190)
        self.write(self.l_score, align="center", font=("Verdana", 80, "bold"))
        self.goto(100, 190)
        self.write(self.r_score, align="center", font=("Verdana", 80, "bold"))

    def l_point(self):
        """Increments the left player's score."""
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        """Increments the right player's score."""
        self.r_score += 1
        self.update_scoreboard()

    def game_over(self):
        """Displays the winner at the end of the game."""
        self.goto(0, 0)
        winner_message = ""
        if self.l_score >= SCORE_LIMIT:
            winner_message = "Left Player Wins!"
        elif self.r_score >= SCORE_LIMIT:
            winner_message = "Right Player Wins!"
        self.write(winner_message, align="center", font=("Verdana", 30, "bold"))

# ==================== Main Game Setup & Logic ====================

# --- Screen Setup ---
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Pong")
screen.tracer(0)  # Turns off screen animations

# --- Draw Center Divider ---
divider = turtle.Turtle()
divider.color("white")
divider.hideturtle()
divider.penup()
divider.goto(0, SCREEN_HEIGHT / 2)
divider.setheading(270)  # Point downwards
for _ in range(int(SCREEN_HEIGHT / 40)):
    divider.pendown()
    divider.forward(20)
    divider.penup()
    divider.forward(20)

# --- Game Object Initialization ---
r_paddle = Paddle(RIGHT_PADDLE_X, 0)
l_paddle = Paddle(LEFT_PADDLE_X, 0)
ball = Ball()
scoreboard = Scoreboard()

# --- Pause State & Function ---
game_paused = False

def toggle_pause():
    """Toggles the game's paused state."""
    global game_paused
    game_paused = not game_paused

# --- Keyboard Bindings ---
screen.listen()
screen.onkey(r_paddle.move_up, "Up")
screen.onkey(r_paddle.move_down, "Down")
screen.onkey(l_paddle.move_up, "w")
screen.onkey(l_paddle.move_down, "s")
screen.onkey(toggle_pause, "space")

# --- Main Game Loop ---
game_is_on = True
while game_is_on:
    if not game_paused:
        time.sleep(ball.pace)
        screen.update()
        ball.move()

        # Detect collision with top and bottom walls
        if ball.ycor() > WALL_Y_LIMIT or ball.ycor() < -WALL_Y_LIMIT:
            ball.bounce_y()

        # Detect collision with right paddle (with glitch fix)
        if ball.distance(r_paddle) < 50 and ball.xcor() > PADDLE_COLLISION_X:
            ball.bounce_x()
            ball.setx(PADDLE_COLLISION_X) # Move ball out to prevent sticking

        # Detect collision with left paddle (with glitch fix)
        if ball.distance(l_paddle) < 50 and ball.xcor() < -PADDLE_COLLISION_X:
            ball.bounce_x()
            ball.setx(-PADDLE_COLLISION_X) # Move ball out to prevent sticking

        # Detect when right paddle misses
        if ball.xcor() > SCREEN_WIDTH / 2:
            ball.reset_pos()
            scoreboard.l_point()

        # Detect when left paddle misses
        if ball.xcor() < -SCREEN_WIDTH / 2:
            ball.reset_pos()
            scoreboard.r_point()

        # Check for a winner
        if scoreboard.l_score >= SCORE_LIMIT or scoreboard.r_score >= SCORE_LIMIT:
            game_is_on = False
            scoreboard.game_over()
    else:
        # Keep the screen responsive even when paused
        screen.update()

screen.exitonclick()