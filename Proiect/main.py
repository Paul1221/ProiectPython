import random
import pygame
import sys
import json
from win32api import GetSystemMetrics


class SnakePart:
    def __init__(self, x, y):
        """
        :param x: the x coordinate of the part
        :param y: the y coordinate of the part
        """
        super().__init__()
        self.x = x
        self.y = y
        self.changes = []


class Fruit:
    def __init__(self, x, y):
        """
        :param x: the x coordinate of the part
        :param y: the y coordinate of the part
        """
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0)

    def draw_fruit(self, dis):
        """
        Used for drawing the points the player collects
        :param dis: the display on witch it is drown
        :return: none
        """
        pygame.draw.rect(dis, self.color, [self.x, self.y, 10, 10])
        pygame.display.update()


class Snake:
    def __init__(self):
        super().__init__()
        '''
        The snake always starts with the length of 5 and heading downwards 
        '''
        self.nrOfParts = 5
        self.parts = [SnakePart(10, 10), SnakePart(10, 20), SnakePart(10, 30), SnakePart(10, 40), SnakePart(10, 50)]
        self.direction = 'down'
        self.color = (0, 255, 0)

    def init_snake(self, dis):
        """
        For drawing the initial snake
        :param dis: the display on witch it is drown
        :return: none
        """
        for part in self.parts:
            pygame.draw.rect(dis, self.color, [part.x, part.y, 10, 10])
        pygame.display.update()

    def draw_snake(self, dis):
        """
        Used to draw the snake. The last part of the snake is colored as the background
        and we only draw the head(for better performance).
        :param dis: the display on witch it is drown
        :return: none
        """
        pygame.draw.rect(dis, (0, 0, 0), [self.parts[0].x, self.parts[0].y, 10, 10])
        pygame.draw.rect(dis, self.color, [self.parts[-1].x, self.parts[-1].y, 10, 10])
        pygame.display.update()
        self.parts.pop(0)

    def move_snake(self, dis):
        """
        Used to move the snake. It gets the coordinates of the head and changes direction based on the
        direction attribute. A new head is created and the last part is removed when using the draw_snake method.
        :param dis: the display on witch it is drown
        :return: none
        """
        x = self.parts[-1].x
        y = self.parts[-1].y
        if self.direction == 'down':
            y += 10
        elif self.direction == 'up':
            y -= 10
        elif self.direction == 'left':
            x -= 10
        elif self.direction == 'right':
            x += 10
        self.draw_snake(dis)
        self.parts.append(SnakePart(x, y))

    def change_direction(self, direction):
        """
        Changes the direction attribute.
        :param direction: The new direction
        :return: none
        """
        self.direction = direction


class Obstacle:
    def __init__(self, x, y):
        """
        :param x: the x coordinate of the part
        :param y: the y coordinate of the part
        """
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self, dis):
        """
        Used to draw the obstacle.
        :param dis: the display on witch it is drown
        :return: none
        """
        pygame.draw.rect(dis, self.color, [self.x, self.y, 10, 10])
        pygame.display.update()


class Game:
    def __init__(self, width, height, obstacles):
        """
        Initializes the game.
        Checks if the obstacles parsed from the config file are valid.
        :param width: width of the board
        :param height: height of the board
        :param obstacles: obstacle list
        """
        super().__init__()
        self.player = Snake()
        self.gameOver = False
        self.gameRunning = True
        self.dis = None
        self.score = 0
        self.highScore = 0
        self.width = width
        self.height = height
        self.obstacles = []
        for ob in obstacles:
            if 10 < ob['x'] < self.width - 10 and 10 < ob['y'] < self.height - 10:
                self.obstacles.append(Obstacle(ob['x'], ob['y']))
        self.fruit = Fruit(int(random.randrange(10, self.width-10, 10)), int(random.randrange(10, self.height-10, 10)))
        self.start_game()

    def start_game(self):
        """
        Keeps the game running and initializes the board.
        :return: none
        """
        pygame.init()
        self.dis = pygame.display.set_mode((self.width, self.height))
        pygame.display.update()
        pygame.display.set_caption('Snake')
        self.draw_obstacles()
        self.player.init_snake(self.dis)
        self.fruit.draw_fruit(self.dis)
        pygame.display.update()
        while not self.gameOver:
            if self.gameRunning:
                self.run_game()
            else:
                if self.score > self.highScore:
                    self.highScore = self.score
                self.end_screen()
                self.reset()
        pygame.quit()
        quit()

    def run_game(self):
        """
        Used to draw the snake continuously, check for points, end of the game etc.
        It checks for player keyboard input(the arrow keys) for changing the direction.
        :return: none
        """
        self.player.move_snake(self.dis)
        self.fruit.draw_fruit(self.dis)
        self.eat()
        self.check_end()
        i = 0
        move_flag = False
        while i < 15000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOver = True
                if event.type == pygame.KEYDOWN:
                    if move_flag is False:
                        if event.key == pygame.K_LEFT:
                            if self.player.direction != 'right':
                                self.player.change_direction('left')
                                move_flag = True

                        elif event.key == pygame.K_RIGHT:
                            if self.player.direction != 'left':
                                self.player.change_direction('right')
                                move_flag = True

                        elif event.key == pygame.K_UP:
                            if self.player.direction != 'down':
                                self.player.change_direction('up')
                                move_flag = True

                        elif event.key == pygame.K_DOWN:
                            if self.player.direction != 'up':
                                self.player.change_direction('down')
                                move_flag = True
            i += 1

    def check_end(self):
        """
        Checks if the player got in contact with the border or with an obstacle.
        :return: none
        """
        if not (0 <= self.player.parts[-1].x <= self.width-10 and 0 <= self.player.parts[-1].y <= self.height-10):
            self.gameRunning = False
            return
        for part in self.player.parts:
            if part.x == self.player.parts[-1].x and part.y == self.player.parts[-1].y:
                if part != self.player.parts[-1]:
                    self.gameRunning = False
                    break
        for ob in self.obstacles:
            if ob.x == self.player.parts[-1].x and ob.y == self.player.parts[-1].y:
                self.gameRunning = False
                break

    def eat(self):
        """
        Used when the player gets in contact with a point.
        When the snake gets a point it grows in size.
        :return: none
        """
        if self.player.parts[-1].x == self.fruit.x and self.player.parts[-1].y == self.fruit.y:
            if self.player.direction == 'down':
                self.player.parts.append(SnakePart(self.fruit.x, self.fruit.y+10))
            elif self.player.direction == 'up':
                self.player.parts.append(SnakePart(self.fruit.x, self.fruit.y-10))
            elif self.player.direction == 'left':
                self.player.parts.append(SnakePart(self.fruit.x-10, self.fruit.y))
            elif self.player.direction == 'right':
                self.player.parts.append(SnakePart(self.fruit.x+10, self.fruit.y))
            pygame.draw.rect(self.dis, (0, 255, 0), [self.fruit.x, self.fruit.y, 10, 10])
            self.choose_fruit_xy()
            self.fruit.draw_fruit(self.dis)
            self.score += 1

    def reset(self):
        """
        Starts the game over.
        :return: none
        """
        self.player = Snake()
        self.gameRunning = True
        self.score = 0
        self.dis = pygame.display.set_mode((self.width, self.height))
        pygame.display.update()
        self.draw_obstacles()
        self.player.init_snake(self.dis)
        self.fruit.draw_fruit(self.dis)
        pygame.display.update()

    def end_screen(self):
        """
        Used to draw the high score screen.
        It takes keyboard input from the player to either start a new game or exit the game.
        :return: none
        """
        choosedoption = False
        self.dis = pygame.display.set_mode((400, 400))
        myfont = pygame.font.SysFont("monospace", 15)
        label1 = myfont.render(f"You ate {self.score} fruits.", True, (255, 255, 0))
        label2 = myfont.render("Press Y to continue or N to exit.", True, (255, 255, 0))
        self.dis.blit(label1, (125, 100))
        self.dis.blit(label2, (75, 200))
        pygame.display.update()
        while not choosedoption:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        choosedoption = True
                    elif event.key == pygame.K_n:
                        self.dis = pygame.display.set_mode((400, 400))
                        myfont = pygame.font.SysFont("monospace", 15)
                        label1 = myfont.render(f"Your highscore is {self.highScore}.", True, (255, 255, 0))
                        self.dis.blit(label1, (125, 100))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        self.gameOver = True
                        choosedoption = True

    def choose_fruit_xy(self):
        """
        Used to choose where the next point will be created.
        It makes sure its not where there are obstacles or snake parts.
        :return: none
        """
        ok1 = False
        ok2 = False
        while not (ok1 and ok2):
            self.fruit.x = int(random.randrange(10, self.width-10, 10))
            self.fruit.y = int(random.randrange(10, self.height-10, 10))
            for part in self.player.parts:
                if self.fruit.x != part.x or self.fruit.y != part.y:
                    ok1 = True
                    break
            for ob in self.obstacles:
                if ob.x != self.fruit.x or ob.y != self.fruit.y:
                    ok2 = True
                    break

    def draw_obstacles(self):
        """
        Used to draw all the obstacles.
        :return: none
        """
        for ob in self.obstacles:
            ob.draw(self.dis)


with open(sys.argv[1]) as f:
    data = json.load(f)

w = data['width']
h = data['height']

if w <= 300:
    w = 300
if h <= 300:
    h = 300
if w > GetSystemMetrics(0):
    w = GetSystemMetrics(0)
if h > GetSystemMetrics(1):
    h = GetSystemMetrics(1)

print(w, h)
start = Game(w, h, data['obstacles'])
