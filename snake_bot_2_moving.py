import pygame
import random
from enum import Enum, IntEnum
from collections import namedtuple
import csv
import uuid

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(IntEnum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class UserAction(IntEnum):
    RIGHT = 1
    LEFT = 2
    STRAIGHT = 3
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREY = (54,57,63)

VISION_GREY = (142,146,151)
VISION_GREEN = (154, 162, 90)

BLOCK_SIZE = 20
SPEED =50
SNAKE_LENGTH = 6

class SnakeGame:
    
    def __init__(self, w=1000, h=480):
        self.x_border_offset = 0
        # self.csv_file = open(f'bot-data-2/{str(uuid.uuid4())}.csv', 'a', newline='')
        self.csv_file = open(f'bot-2-moving.csv', 'w', newline='')

        self.csv_file_writer = csv.writer(self.csv_file, delimiter=',')
        # self.csv_file_writer.writerow(['foodDiffX','foodDiffY','up_collision','down_collision','left_collision', 'right_collision','direction','action'])
        self.up_collision = 0
        self.down_collision = 0
        self.left_collision = 0
        self.right_collision = 0
        self.step_count=0


        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        # self.snake = [self.head, 
        #               Point(self.head.x-BLOCK_SIZE, self.head.y),
        #               Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.snake = [self.head]
        for i in range(1,SNAKE_LENGTH +1):
            self.snake.append(Point(self.head.x, self.head.y + (i*BLOCK_SIZE)))
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint((self.x_border_offset + 100)//BLOCK_SIZE, (((self.w)+self.x_border_offset)//BLOCK_SIZE ) )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        print("Food: ", self.food.x, ", ", self.food.y)
        if self.food in self.snake or self.food.x <= self.x_border_offset:
            self._place_food()
        
    def play_step(self):
        # direction dictionary
        left_dir = {Direction.UP: Direction.LEFT,
                    Direction.DOWN: Direction.RIGHT,
                    Direction.LEFT: Direction.DOWN,
                    Direction.RIGHT: Direction.UP}
        right_dir = {Direction.UP: Direction.RIGHT,
                    Direction.DOWN: Direction.LEFT,
                    Direction.LEFT: Direction.UP,
                    Direction.RIGHT: Direction.DOWN}
        # current_event = UserAction.STRAIGHT

        

        previous_direction = self.direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # automate controller
        
        # record what happened
        # get food difference on X axis
        food_diff_x = (self.food.x - self.head.x)/20
        # get food difference on Y axis
        food_diff_y = (self.food.y - self.head.y)/20


        # automate playing
        if food_diff_x < 0 and self.left_collision > 0:
            if self.direction == Direction.RIGHT:
                if food_diff_y < 0:
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.DOWN
            else:
                self.direction = Direction.LEFT
        elif food_diff_x > 0 and self.right_collision >0:
            if (self.direction == Direction.LEFT):
                if food_diff_y < 0:
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.DOWN
            else:
                self.direction = Direction.RIGHT
        elif food_diff_y < 0 and self.up_collision > 0:
            if (self.direction == Direction.DOWN):
                if (food_diff_x < 0):
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.RIGHT
            else:
                self.direction = Direction.UP
        elif food_diff_y > 0  and self.down_collision > 0:
            if (self.direction == Direction.UP):
                if (food_diff_x < 0):
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.RIGHT
            else:
                self.direction = Direction.DOWN
                
        def checkValid():
            if self.up_collision == 0 and self.down_collision == 0 and self.right_collision == 0 and self.left_collision == 0:
                return True
            if self.direction == Direction.LEFT and self.left_collision <= 1:
                return False
            elif self.direction == Direction.RIGHT and self.right_collision <= 1:
                return False
            elif self.direction == Direction.UP and self.up_collision <= 1:
                return False
            elif self.direction == Direction.DOWN and self.down_collision <= 1:
                return False
            return True

        while(not checkValid()):
            self.step_count+=1
            config = [self.up_collision,self.down_collision,self.left_collision,self.right_collision]
            if config.count(1) > 2:
                index = config.index(max(config))
                # print("Step counter:",self.step_count, config, max(config), config.index(max(config)), "Score:", self.score)
                if config == [1,1,1,1]:
                    self.csv_file_writer.writerow([food_diff_x, food_diff_y, self.up_collision, self.down_collision, self.left_collision, self.right_collision, int(previous_direction) , int(self.direction)])
                    exit()
                if index == 0:
                    self.direction = Direction.UP
                elif index == 1:
                    self.direction = Direction.DOWN
                elif index == 2:
                    self.direction = Direction.LEFT
                elif index == 3:
                    self.direction = Direction.RIGHT
            # auto avoid collision
            if self.direction == Direction.LEFT and self.left_collision <= 1:
                if self.up_collision <=1:
                    self.direction = Direction.DOWN
                else: 
                    self.direction = Direction.UP
            elif self.direction == Direction.RIGHT and self.right_collision <= 1:
                if self.down_collision <=1:
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.DOWN
            elif self.direction == Direction.UP and self.up_collision <= 1:
                if self.right_collision <=1 :
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.RIGHT
            elif self.direction == Direction.DOWN and self.down_collision <= 1:
                if self.left_collision <= 1:
                    self.direction = Direction.RIGHT
                else:
                    self.direction = Direction.LEFT


        # record data
        # if (current_event != None):
        #     self.csv_file_writer.writerow([food_diff_x, food_diff_y, self.left_collision, self.front_collision, self.right_collision, int(previous_direction) , int(current_event)])
        
        self.csv_file_writer.writerow([food_diff_x, food_diff_y, self.up_collision, self.down_collision, self.left_collision, self.right_collision, int(previous_direction) , int(self.direction)])
        self.csv_file.flush()

        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()

       


        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w + self.x_border_offset - BLOCK_SIZE or self.head.x < self.x_border_offset or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _custom_collision_check(self, x, y):
        if x > self.w + self.x_border_offset - BLOCK_SIZE or x < self.x_border_offset or y > self.h - BLOCK_SIZE or y < 0:
            return True
        if Point(x,y) in self.snake[1:]:
            return True
        return False
    
    def _custom_food_check(self, x, y):
        if x == self.food.x and y == self.food.y:
            return True
        if x > self.w - BLOCK_SIZE or x < 0 or y > self.h - BLOCK_SIZE or y < 0:
            return True
        return False

    def _update_ui(self):
        self.x_border_offset += 5
        self.display.fill(GREY)
        self._check_food_valid()
        self._draw_collision_vision()
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x - self.x_border_offset, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4 - self.x_border_offset, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x - self.x_border_offset, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _check_food_valid(self):
        if self.food.x <= self.x_border_offset + 30:
            self._place_food()
    
    def _draw_food_vision_front(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            # x += BLOCK_SIZE
            while not self._custom_food_check(x, y):
                x += BLOCK_SIZE
                pygame.draw.rect(self.display, VISION_GREEN, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

        elif self.direction == Direction.LEFT:
            # x -= BLOCK_SIZE
            while not self._custom_food_check(x, y):
                x -= BLOCK_SIZE
                pygame.draw.rect(self.display, VISION_GREEN, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))
        elif self.direction == Direction.DOWN:
            # y += BLOCK_SIZE
            while not self._custom_food_check(x, y):
                y += BLOCK_SIZE
                pygame.draw.rect(self.display, VISION_GREEN, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))
        elif self.direction == Direction.UP:
            # y -= BLOCK_SIZE
            while not self._custom_food_check(x, y):
                y -= BLOCK_SIZE
                pygame.draw.rect(self.display, VISION_GREEN, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

    # draw collision vision
    def _draw_collision_vision(self):
        self._draw_collision_vision_up()
        self._draw_collision_vision_down()
        self._draw_collision_vision_left()
        self._draw_collision_vision_right()

    def _draw_collision_vision_up(self):
        x = self.head.x
        y = self.head.y
        self.up_collision = 0
        while not self._custom_collision_check(x, y):
            y -= BLOCK_SIZE
            self.up_collision += 1
            pygame.draw.rect(self.display, VISION_GREY, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

    def _draw_collision_vision_down(self):
        x = self.head.x
        y = self.head.y
        self.down_collision = 0
        while not self._custom_collision_check(x, y):
            y += BLOCK_SIZE
            self.down_collision += 1
            pygame.draw.rect(self.display, VISION_GREY, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

    def _draw_collision_vision_left(self):
        x = self.head.x
        y = self.head.y
        self.left_collision = 0
        while not self._custom_collision_check(x, y):
            x -= BLOCK_SIZE
            self.left_collision += 1
            pygame.draw.rect(self.display, VISION_GREY, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

    def _draw_collision_vision_right(self):
        x = self.head.x
        y = self.head.y
        self.right_collision = 0
        while not self._custom_collision_check(x, y):
            x += BLOCK_SIZE
            self.right_collision += 1
            pygame.draw.rect(self.display, VISION_GREY, pygame.Rect(x + 4 - self.x_border_offset, y + 4, 12, 12))

     
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()