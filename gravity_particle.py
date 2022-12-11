import random
import pygame
import math


pygame.init()
screen = pygame.display.set_mode((1300, 700))

pygame.display.set_caption("Gravity")
clock = pygame.time.Clock()
FPS = 60

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROZA = (200, 0, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)
colors = [GREEN, RED, BLUE, ROZA, BLACK, WHITE, GREY, YELLOW]


ball_size = 30
ball_mass = 100
ball_color = WHITE    # If Random_color is False
ball_speed_x = [-5, 6]    # Interval
ball_speed_y = [-5, 6]    # Interval
decrease_rate = 0.1   # If Decrease is True

Physics = True    # Gravity
Collision = False
Random_color = True
Loss_of_speed = True
Decrease = False


class Ball:
    def __init__(self, surface, mass, color, size, speed_x, speed_y):
        self.surface = surface
        self.mass = mass
        self.color = color
        self.size = size
        self.vx = speed_x
        self.vy = speed_y
        self.balls = []    # [loc, velocity, timer, acceleration]
        
    def create_balls(self, x, y):
        self.balls.append([[x, y], [random.randint(self.vx[0], self.vx[1]), random.randint(self.vy[0], self.vy[1])], self.size, [0, 0]])

    def draw_balls(self):
        if len(self.balls) != 0:
            screen.fill(BLACK)
            for ball in self.balls:
                pygame.draw.circle(self.surface, self.color, [int(ball[0][0]), int(ball[0][1])], ball[2])
            pygame.display.update()
            clock.tick(FPS)

    def move(self):
        if len(self.balls) != 0:
            for ball in self.balls:

                # Velocity + acceleration
                ball[1][0] += ball[3][0]
                ball[1][1] += ball[3][1]

                if Decrease:
                    ball[2] -= decrease_rate
                    if ball[2] <= 0:
                        self.balls.remove(ball)

                ball[0][0] += ball[1][0]
                ball[0][1] += ball[1][1]

                if Loss_of_speed:
                    # decrease speed
                    if ball[1][0] > 0:
                        ball[1][0] -= 0.05
                    if ball[1][1] > 0:
                        ball[1][1] -= 0.05
                    if ball[1][0] < 0:
                        ball[1][0] += 0.05
                    if ball[1][1] < 0:
                        ball[1][1] += 0.05

                    # decrease acceleration
                    if ball[3][0] > 0:
                        ball[3][0] -= 0.1
                    if ball[3][1] > 0:
                        ball[3][1] -= 0.1
                    if ball[3][0] < 0:
                        ball[3][0] += 0.1
                    if ball[3][1] < 0:
                        ball[3][1] += 0.1

    def acceleration(self):
        for particle in self.balls:
            for part in self.balls:
                # Euclidean distance
                distance = math.sqrt((particle[0][0] - part[0][0]) ** 2 + (particle[0][1] - part[0][1]) ** 2)
                if distance == 0:
                    continue
                # calculate acceleration for 1st ball
                particle[3][0] = self.mass * (part[0][0] - particle[0][0]) / distance ** 2
                particle[3][1] = self.mass * (part[0][1] - particle[0][1]) / distance ** 2

                # calculate acceleration for 2nd ball
                part[3][0] = self.mass * (particle[0][0] - part[0][0]) / distance ** 2
                part[3][1] = self.mass * (particle[0][1] - part[0][1]) / distance ** 2

    def check_walls(self):
        size = self.surface.get_size()
        for ball in self.balls:
            if ball[0][0] - self.size <= 0:
                ball[1][0] *= -1
                ball[0][0] += 5

            if ball[0][0] + self.size >= size[0]:
                ball[1][0] *= -1
                ball[0][0] -= 5

            if ball[0][1] - self.size <= 0:
                ball[1][1] *= -1
                ball[0][1] += 5

            if ball[0][1] + self.size >= size[1]:
                ball[1][1] *= -1
                ball[0][1] -= 5

    def check_collision(self):
        for ball in self.balls:
            for part in self.balls:
                if ball[0][0] == part[0][0]:
                    continue
                # Check if balls collide
                if pygame.rect.Rect(ball[0][0], ball[0][1], self.size * 2, self.size * 2).colliderect(pygame.rect.Rect(part[0][0], part[0][1], self.size * 2, self.size * 2)):
                    ball[1][0] *= -1
                    ball[1][1] *= -1


def stop_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()


ball = Ball(surface=screen, mass=ball_mass, color=random.choice(colors) if Random_color else ball_color, size=ball_size, speed_x=ball_speed_x, speed_y=ball_speed_y)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_loop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coords = pygame.mouse.get_pos()
                    ball.create_balls(coords[0], coords[1])

        ball.draw_balls()
        ball.check_walls()
        ball.move()
        if Collision:
            ball.check_collision()
        if Physics:
            ball.acceleration()


if __name__ == "__main__":
    main()
