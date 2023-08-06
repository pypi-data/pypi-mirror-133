"""
This file contains code for the game "Box Keep Ups".
Author: NativeApkDev

The game "Box Keep Ups" is inspired by the "Pong Game" in the Kivy tutorial in
https://kivy.org/doc/stable/tutorials/pong.html and the Kivy code example in
https://github.com/attreyabhatt/Kivy-Pong-Game.
"""


# Game version: 1


# Importing necessary libraries


import random
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Box(Widget):
    """
    This class contains attributes of the box the player can control in this game.
    """

    score: NumericProperty = NumericProperty(0)

    def bounce_ball(self, ball):
        # type: (Ball) -> bool
        # If the box collides with the ball
        if self.collide_widget(ball):
            # Make the ball move faster and increase the score by 1
            if random.random() < 0.5:
                ball.velocity_x *= -1.05
            else:
                ball.velocity_x *= 1.05

            ball.velocity_y *= -1.05
            self.score += 1
            return True
        return False


class Ball(Widget):
    """
    This class contains attributes of the ball in this game.
    """

    # Velocity of the ball
    velocity_x: NumericProperty = NumericProperty(0)
    velocity_y: NumericProperty = NumericProperty(0)
    velocity: ReferenceListProperty = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        # type: () -> None
        # This function updates the position of the ball.
        # Latest Position = Current Position + Current Velocity
        self.pos = Vector(*self.velocity) + self.pos


class BoxKeepUpsGame(Widget):
    """
    This class contains attributes of the representation of "Box Keep Ups" game.
    """

    ball: ObjectProperty = ObjectProperty(Ball())
    player: ObjectProperty = ObjectProperty(Box())

    # Creating a method to move the ball
    def move_ball(self):
        # type: () -> None
        rotation_angle: int = random.randint(15, 45)
        self.ball.velocity = Vector(0, -10).rotate(rotation_angle)

    # Creating a method to update the representation of the game every time interval
    def update(self, dt):
        # type: (float) -> None
        self.ball.move()

        try:
            with open("scores.txt") as f:
                pass
        except FileNotFoundError:
            new_file = open("scores.txt", "w")
            new_file.write("High score: 0")

            # bounce off left and right
        if self.ball.x < 0 or self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1

        # bounce off bottom, update the player's high score if possible, and then reset score to 0
        if self.ball.y < 0:
            lines: str = ""  # initial value
            with open("scores.txt") as f:
                lines += str(f.readline())
                f.close()

            line_words: list = lines.split(" ")
            curr_high_score: int = int(line_words[len(line_words) - 1])
            if self.player.score > curr_high_score:
                file = open("scores.txt", "w")
                file.write("High score: " + str(self.player.score))
                file.close()

            self.player.score = 0

            # Reset the position of the ball
            self.ball.center = self.parent.center

        # bounce off top
        if self.ball.y > self.height - 50:
            self.ball.velocity_y *= -1

        # Trying to bounce the ball of the box
        self.player.bounce_ball(self.ball)

    # Moving the box when the player touches the screen
    def on_touch_move(self, touch):
        self.player.x = touch.x


class BoxKeepUpsApp(App):
    """
    This class contains attributes of the application "Box Keep Ups".
    """

    def build(self):
        # type: () -> BoxKeepUpsGame
        # Building the game
        game: BoxKeepUpsGame = BoxKeepUpsGame()

        # Moving the ball in the game
        game.move_ball()

        # Initialising the clock in the game with 'BoxKeepUpsGame.update' function as the callback function
        # and the time interval as the parameter
        Clock.schedule_interval(game.update, 1.0 / 60.0)

        # Returning the initialised game
        return game


if __name__ == '__main__':
    BoxKeepUpsApp().run()
