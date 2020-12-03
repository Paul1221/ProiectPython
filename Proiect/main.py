import random
import pygame


class SnakePart:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.changes = []


class Fruit:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0)

    def draw_fruit(self, dis):
        pygame.draw.rect(dis, self.color, [self.x, self.y, 10, 10])
        pygame.display.update()


class Snake:
    def __init__(self):
        super().__init__()
        self.nrOfParts = 5
        self.parts = [SnakePart(10, 10), SnakePart(10, 20), SnakePart(10, 30), SnakePart(10, 40), SnakePart(10, 50)]
        self.direction = 'down'
        self.color = (0, 255, 0)

    def init_snake(self, dis):
        for part in self.parts:
            pygame.draw.rect(dis, self.color, [part.x, part.y, 10, 10])
        pygame.display.update()

    def draw_snake(self, dis):
        pygame.draw.rect(dis, (0, 0, 0), [self.parts[0].x, self.parts[0].y, 10, 10])
        pygame.draw.rect(dis, self.color, [self.parts[-1].x, self.parts[-1].y, 10, 10])
        pygame.display.update()
        self.parts.pop(0)

    def move_snake(self, dis):
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
        self.direction = direction


class Game:
    def __init__(self):
        super().__init__()
        self.player = Snake()
        self.gameOver = False
        self.gameRunning = True
        self.dis = None
        self.score = 0
        self.highScore = 0
        self.fruit = Fruit(int(random.randrange(10, 390, 10)), int(random.randrange(10, 390, 10)))

        self.start_game()

    def start_game(self):
        pygame.init()
        self.dis = pygame.display.set_mode((400, 400))
        pygame.display.update()
        pygame.display.set_caption('Snake')
        self.player.init_snake(self.dis)
        self.fruit.draw_fruit(self.dis)
        pygame.display.update()
        while not self.gameOver:
            if self.gameRunning:
                self.run_game()
            else:
                self.end_screen()
                print(self.score)
                if self.score > self.highScore:
                    self.highScore = self.score
                self.reset()
        print(self.highScore)
        pygame.quit()
        quit()

    def run_game(self):
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
        if not (0 <= self.player.parts[-1].x <= 390 and 0 <= self.player.parts[-1].y <= 390):
            self.gameRunning = False
            return
        for part in self.player.parts:
            if part.x == self.player.parts[-1].x and part.y == self.player.parts[-1].y:
                if part != self.player.parts[-1]:
                    self.gameRunning = True
                    break

    def eat(self):
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
            self.fruit.x = int(random.randrange(10, 390, 10))
            self.fruit.y = int(random.randrange(10, 390, 10))
            self.fruit.draw_fruit(self.dis)
            self.score += 1

    def reset(self):
        self.player = Snake()
        self.gameRunning = True
        self.score = 0
        self.dis = pygame.display.set_mode((400, 400))
        pygame.display.update()
        self.player.init_snake(self.dis)
        self.fruit.draw_fruit(self.dis)
        pygame.display.update()

    def end_screen(self):
        choosedOption = False
        self.dis = pygame.display.set_mode((400, 400))
        myfont = pygame.font.SysFont("monospace", 15)
        label1 = myfont.render(f"You ate {self.score} fruits.", 1, (255, 255, 0))
        label2 = myfont.render("Press Y to continue or N to exit.", 1, (255, 255, 0))
        self.dis.blit(label1, (125, 100))
        self.dis.blit(label2, (75, 200))
        pygame.display.update()
        while not choosedOption:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        choosedOption = True
                    elif event.key == pygame.K_n:
                        self.dis = pygame.display.set_mode((400, 400))
                        myfont = pygame.font.SysFont("monospace", 15)
                        label1 = myfont.render(f"Your highscore is {self.highScore}.", 1, (255, 255, 0))
                        self.dis.blit(label1, (125, 100))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        self.gameOver = True
                        choosedOption = True

start = Game()
