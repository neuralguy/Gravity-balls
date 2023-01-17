"""
SPACE - pause
Q - clear
W - increase FPS
LEFT MOUSE - create attracting particles
RIGHT MOUSE - create repulsive particles
MIDDLE MOUSE - create particles one or more
"""

import random
import pygame


pygame.init()
WIDTH = 1300
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

ball_size = 7
ball_mass = 100
# If Random_color is False
ball_color1 = RED
ball_color2 = BLUE
ball_speed_x = [-5, 6]    # Interval
ball_speed_y = [-5, 6]
decrease_rate = 0.01   # If Decrease is True

Physics = True    # Gravity
Collision = True
Random_color = True
Loss_of_speed = False
Decrease = False
Walls = False


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Ball:
    def __init__(self, surface, mass, color1, color2, size, speed_x, speed_y):
        self.surface = surface
        self.mass = mass
        self.color1 = color1
        self.color2 = color2
        self.size = size
        self.vx = speed_x
        self.vy = speed_y
        self.balls = []    # [[loc], [velocity], timer, [acceleration], group]
        self.distance = 0
        self.G = 6.6743 * 10 ** -11
        
    def create_balls1(self, x, y, group):
        self.balls.append([[x, y], [random.randint(self.vx[0], self.vx[1]), random.randint(self.vy[0], self.vy[1])], self.size, [0, 0], group])

    def draw_balls(self):
        screen.fill(BLACK)
        count = font.render(str(len(self.balls)), False, WHITE)
        screen.blit(count, (0, 0))
        if len(self.balls) != 0:
            for ball in self.balls:
                if ball[4]:
                    pygame.draw.circle(self.surface, self.color1, [int(ball[0][0]), int(ball[0][1])], ball[2])
                else:
                    pygame.draw.circle(self.surface, self.color2, [int(ball[0][0]), int(ball[0][1])], ball[2])
        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.update()
        clock.tick(FPS)

    def move(self):
        if len(self.balls) != 0:
            for ball in self.balls:
                # Velocity + acceleration
                if self.distance <= ball_size + 10 and self.distance != 0:
                    ball[1][0] -= ball[3][0] / 3
                    ball[1][1] -= ball[3][1] / 3

                else:
                    if ball[4]:
                        ball[1][0] += ball[3][0]
                        ball[1][1] += ball[3][1]
                    else:
                        ball[1][0] -= ball[3][0]
                        ball[1][1] -= ball[3][1]

                if Decrease:
                    ball[2] -= decrease_rate
                    if ball[2] <= 1:
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

    def acceleration(self):
        for particle in self.balls:
            for part in self.balls:
                # Euclidean distance
                distance = (particle[0][0] - part[0][0]) ** 2 + (particle[0][1] - part[0][1]) ** 2
                if distance == 0:
                    continue
                else:
                    self.distance = distance
                # calculate acceleration for 1st ball
                ax = self.mass * (part[0][0] - particle[0][0]) / self.distance
                ay = self.mass * (part[0][1] - particle[0][1]) / self.distance
                particle[3][0] = ax
                particle[3][1] = ay

                # calculate acceleration for 2nd ball
                part[3][0] = -ax
                part[3][1] = -ay

    def check_walls(self):
        for ball in self.balls:
            if ball[0][0] - self.size <= 0:
                if Walls:
                    ball[1][0] *= -1
                    ball[0][0] += 5
                else:
                    ball[0][0] = WIDTH - self.size - 1

            if ball[0][0] + self.size >= WIDTH:
                if Walls:
                    ball[1][0] *= -1
                    ball[0][0] -= 5
                else:
                    ball[0][0] = 0 + self.size + 1

            if ball[0][1] - self.size <= 0:
                if Walls:
                    ball[1][1] *= -1
                    ball[0][1] += 5
                else:
                    ball[0][1] = HEIGHT - self.size - 1

            if ball[0][1] + self.size >= HEIGHT:
                if Walls:
                    ball[1][1] *= -1
                    ball[0][1] -= 5
                else:
                    ball[0][1] = 0 + self.size + 1

    def check_collision(self):
        for ball in self.balls:
            for part in self.balls:
                if ball[0][0] == part[0][0]:
                    continue
                # Check if balls1 collide
                if pygame.rect.Rect(ball[0][0], ball[0][1], self.size * 2, self.size * 2).colliderect(pygame.rect.Rect(part[0][0], part[0][1], self.size * 2, self.size * 2)):
                    ball[1][0] *= -1
                    ball[1][1] *= -1


ball = Ball(surface=screen, mass=ball_mass, color1=random_color() if Random_color else ball_color1, color2=random_color() if Random_color else ball_color2, size=ball_size, speed_x=ball_speed_x, speed_y=ball_speed_y)
font = pygame.font.Font("freesansbold.ttf", 32)


def main():
    pause = False
    spawn = False
    left = False
    right = False
    global FPS
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coords = pygame.mouse.get_pos()
                ball.create_balls1(coords[0], coords[1], 1)
                left = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                left = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                spawn = not spawn
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                coords = pygame.mouse.get_pos()
                ball.create_balls1(coords[0], coords[1], 0)
                right = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                right = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                ball.balls.clear()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if FPS >= 100:
                    FPS = 10
                else:
                    FPS += 10

        ball.draw_balls()
        if not pause:
            ball.check_walls()
            ball.move()
            if Collision:
                ball.check_collision()
            if Physics:
                ball.acceleration()
        if spawn:
            coords = pygame.mouse.get_pos()
            if left:
                ball.create_balls1(coords[0], coords[1], 1)
            if right:
                ball.create_balls1(coords[0], coords[1], 0)


if __name__ == "__main__":
    main()
