import turtle
import time
import random
import math

# Set up the screen
screen = turtle.Screen()
screen.title("Turtle Movement Game")
screen.bgcolor("lightblue")
screen.setup(width=600, height=600)

# Global variables
player_health = 3
boss_health = 5
score = 0
game_over = False

# Create a menu screen
def show_menu():
    screen.clear()
    screen.bgcolor("lightblue")

    title_turtle = turtle.Turtle()
    title_turtle.color("black")
    title_turtle.penup()
    title_turtle.hideturtle()
    title_turtle.goto(0, 100)
    title_turtle.write("Turtle Movement Game", align="center", font=("Arial", 24, "normal"))

    play_button = turtle.Turtle()
    play_button.shape("square")
    play_button.color("green")
    play_button.penup()
    play_button.shapesize(stretch_wid=2, stretch_len=6)
    play_button.goto(0, 0)
    play_button.write("PLAY", align="center", font=("Arial", 16, "bold"))

    quit_button = turtle.Turtle()
    quit_button.shape("square")
    quit_button.color("red")
    quit_button.penup()
    quit_button.shapesize(stretch_wid=2, stretch_len=6)
    quit_button.goto(0, -100)
    quit_button.write("QUIT", align="center", font=("Arial", 16, "bold"))

    # Define play and quit functions
    def play_game(x, y):
        play_button.hideturtle()
        quit_button.hideturtle()
        start_game()

    def quit_game(x, y):
        turtle.bye()

    # Bind buttons to functions
    play_button.onclick(play_game)
    quit_button.onclick(quit_game)

# Start the game
def start_game():
    screen.clear()
    screen.bgcolor("lightblue")
    
    global player_turtle, bullet, score_turtle, health_turtle, boss_health_turtle, player_health, boss_health, score, soldier_turtles, boss_turtle, game_over

    player_health = 3
    boss_health = 5
    score = 0
    game_over = False

    # Create the player turtle
    player_turtle = turtle.Turtle()
    player_turtle.shape("turtle")
    player_turtle.color("green")
    player_turtle.speed(0)
    player_turtle.penup()
    player_turtle.goto(0, -250)

    # Create a bullet turtle
    bullet = turtle.Turtle()
    bullet.shape("triangle")
    bullet.color("black")
    bullet.speed(0)
    bullet.penup()
    bullet.goto(0, -1000)  # Initial position off the screen
    bullet.hideturtle()

    # Create the scoreboard turtle
    score_turtle = turtle.Turtle()
    score_turtle.color("black")
    score_turtle.penup()
    score_turtle.hideturtle()
    score_turtle.goto(250, 250)
    score_turtle.write("Score: {}".format(score), align="right", font=("Arial", 16, "normal"))

    # Create the health turtle
    health_turtle = turtle.Turtle()
    health_turtle.color("black")
    health_turtle.penup()
    health_turtle.hideturtle()
    health_turtle.goto(-250, 250)
    health_turtle.write("Health: {}".format(player_health), align="left", font=("Arial", 16, "normal"))

    # Create the boss health turtle
    boss_health_turtle = turtle.Turtle()
    boss_health_turtle.color("black")
    boss_health_turtle.penup()
    boss_health_turtle.hideturtle()
    boss_health_turtle.goto(-250, 220)

    # Define movement functions for the player turtle
    def move_forward():
        player_turtle.setheading(90)
        player_turtle.forward(20)

    def turn_left():
        player_turtle.setheading(180)
        player_turtle.forward(20)

    def turn_right():
        player_turtle.setheading(0)
        player_turtle.forward(20)

    def move_backward():
        player_turtle.setheading(270)
        player_turtle.forward(20)

    def move_up_left():
        player_turtle.setheading(135)
        player_turtle.forward(20)

    def move_up_right():
        player_turtle.setheading(45)
        player_turtle.forward(20)

    def move_down_left():
        player_turtle.setheading(225)
        player_turtle.forward(20)

    def move_down_right():
        player_turtle.setheading(315)
        player_turtle.forward(20)

    # Function to shoot
    def shoot():
        if not bullet.isvisible():
            bullet.showturtle()
            bullet.setposition(player_turtle.xcor(), player_turtle.ycor())
            bullet.setheading(player_turtle.heading())
            bullet.forward(50)  # Move the bullet forward initially
            screen.ontimer(move_bullet, 100)  # Move the bullet every 0.1 second

    # Function to move the bullet
    def move_bullet():
        if bullet.isvisible():
            bullet.forward(10)
            check_bullet_collision()
            if bullet.distance(player_turtle) > 300:  # Distance limit for bullet travel
                bullet.hideturtle()  # Hide the bullet if it travels too far
            screen.ontimer(move_bullet, 100)  # Move the bullet every 0.1 second

    # Function to check bullet collision with soldier turtles or boss
    def check_bullet_collision():
        global score, boss_health, game_over
        for soldier_turtle in soldier_turtles:
            if bullet.distance(soldier_turtle) < 20:
                soldier_turtle.hideturtle()  # Hide the soldier turtle
                soldier_turtles.remove(soldier_turtle)  # Remove the soldier turtle from the list
                bullet.hideturtle()  # Hide the bullet
                score += 1  # Increase score by 1
                update_score()  # Update the score display
                break
        if boss_turtle.isvisible() and bullet.distance(boss_turtle) < 20:
            boss_health -= 1
            bullet.hideturtle()  # Hide the bullet
            update_boss_health()
            if boss_health <= 0:
                boss_turtle.hideturtle()
                game_over = True
                game_over_screen("Player Wins!")

    # Function to update the score display
    def update_score():
        score_turtle.clear()
        score_turtle.write("Score: {}".format(score), align="right", font=("Arial", 16, "normal"))
        if score >= 15 and not boss_turtle.isvisible():
            show_boss_message()  # Show boss after scoring 15 points

    # Function to update the boss health display
    def update_boss_health():
        boss_health_turtle.clear()
        boss_health_turtle.write("Boss Health: {}".format(boss_health), align="left", font=("Arial", 16, "normal"))

    # Create soldier turtles
    soldier_turtles = []

    # Function to create soldier turtles
    def create_soldier():
        for _ in range(5):
            soldier_turtle = turtle.Turtle()
            soldier_turtle.shape("turtle")
            soldier_turtle.color("red")
            soldier_turtle.speed(0)
            soldier_turtle.penup()
            x = random.randint(-290, 290)  # Random x coordinate
            y = random.randint(-290, 290)  # Random y coordinate
            soldier_turtle.goto(x, y)
            soldier_turtles.append(soldier_turtle)

    # Create boss turtle
    boss_turtle = turtle.Turtle()
    boss_turtle.shape("turtle")
    boss_turtle.color("blue")
    boss_turtle.speed(0)
    boss_turtle.penup()
    boss_turtle.goto(0, 0)
    boss_turtle.hideturtle()

    # Function to show "BOSSSS!" message
    def show_boss_message():
        boss_message = turtle.Turtle()
        boss_message.color("red")
        boss_message.penup()
        boss_message.hideturtle()
        boss_message.goto(0, 0)
        boss_message.write("BOSSSS!", align="center", font=("Arial", 24, "normal"))
        screen.update()
        screen.ontimer(spawn_boss, 1000)  # Spawn boss after 1 second

    # Function to spawn boss
    def spawn_boss():
        boss_turtle.showturtle()
        boss_turtle.setposition(0, 0)
        update_boss_health()
        boss_shoot()  # Start shooting

    # Function to calculate angle between two points
    def calculate_angle(x1, y1, x2, y2):
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return angle

    # Function to throw arrows in a circular manner
    def boss_shoot():
        global player_health, game_over
        if boss_turtle.isvisible() and not game_over:
            # Calculate angle to the player
            angle = boss_turtle.towards(player_turtle)
            
            # Create an arrow
            arrow = turtle.Turtle()
            arrow.shape("arrow")
            arrow.color("orange")
            arrow.speed(0)
            arrow.penup()
            arrow.setposition(boss_turtle.xcor(), boss_turtle.ycor())
            arrow.setheading(angle)

            def move_arrow():
                if arrow.isvisible():
                    arrow.forward(10)
                    if bullet.distance(arrow) < 20:
                        bullet.hideturtle()
                        arrow.hideturtle()
                    if arrow.distance(player_turtle) < 20:
                        player_health -= 1
                        health_turtle.clear()
                        health_turtle.write("Health: {}".format(player_health), align="left", font=("Arial", 16, "normal"))
                        arrow.hideturtle()
                        if player_health <= 0:
                            game_over = True
                            game_over_screen("Boss Wins!")
                    else:
                        screen.ontimer(move_arrow, 100)
            move_arrow()
            
            # Schedule next shot
            if not game_over:
                screen.ontimer(boss_shoot, 1000)  # Boss shoots every second

    # Function to display the game over screen
    def game_over_screen(message):
        screen.clear()
        game_over_message = turtle.Turtle()
        game_over_message.color("black")
        game_over_message.penup()
        game_over_message.hideturtle()
        game_over_message.goto(0, 0)
        game_over_message.write(message, align="center", font=("Arial", 24, "normal"))
        screen.update()
        time.sleep(3)
        show_menu()

    # Main event loop
    screen.listen()
    screen.onkey(move_forward, "Up")
    screen.onkey(turn_left, "Left")
    screen.onkey(turn_right, "Right")
    screen.onkey(move_backward, "Down")
    screen.onkey(move_up_left, "u")  # Up + Left
    screen.onkey(move_up_right, "i")  # Up + Right
    screen.onkey(move_down_left, "j")  # Down + Left
    screen.onkey(move_down_right, "k")  # Down + Right
    screen.onkey(shoot, "space")  # Shoot when Space key is pressed

    # Game loop
    while player_health > 0 and not game_over:
        if len(soldier_turtles) < 5 and not boss_turtle.isvisible():
            create_soldier()
        for soldier_turtle in soldier_turtles:
            soldier_turtle.setheading(soldier_turtle.towards(player_turtle))
            soldier_turtle.forward(2)  # Adjust the movement speed of the soldiers
            if player_turtle.distance(soldier_turtle) < 20:
                player_health -= 1
                health_turtle.clear()
                health_turtle.write("Health: {}".format(player_health), align="left", font=("Arial", 16, "normal"))
                soldier_turtle.hideturtle()
                soldier_turtles.remove(soldier_turtle)
        screen.update()
        time.sleep(0.01)

    if player_health <= 0:
        game_over_screen("Boss Wins!")

# Show the menu
show_menu()
screen.mainloop()
