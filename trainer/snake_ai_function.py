
import pygame
import random
from enum import Enum, IntEnum
from collections import namedtuple
import csv
from tensorflow import keras
import pandas as pd
import numpy as np
from multiprocessing import Process

class Direction(IntEnum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class UserAction(IntEnum):
    RIGHT = 1
    LEFT = 2
    STRAIGHT = 3

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
SPEED = 135


Point = namedtuple('Point', 'x, y')


class SnakeGame:
    
    def __init__(self, model_path, w=1000, h=480):
        self.x_border_offset = 0
        self.font = pygame.font.Font('arial.ttf', 25)
        self.model = keras.models.load_model(model_path)
        
        self.up_collision = 0
        self.down_collision = 0
        self.left_collision = 0
        self.right_collision = 0

        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint((self.x_border_offset + 100)//BLOCK_SIZE, (((self.w)+self.x_border_offset)//BLOCK_SIZE ) )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
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
        current_event = UserAction.STRAIGHT
        
        
        # record what happened
        # get food difference on X axis
        food_diff_x = (self.food.x - self.head.x)/20
        # get food difference on Y axis
        food_diff_y = (self.food.y - self.head.y)/20

        # make action
        # kera_input = keras.Input()
        snake_list = [food_diff_x, food_diff_y, self.up_collision, self.down_collision, self.left_collision, self.right_collision, int(self.direction)]

        ai_action_array = self.model.predict( pd.DataFrame([snake_list]) )
        ai_action = ai_action_array.argmax() + 1
        # if ai_action == 1:
        #     self.direction = right_dir[self.direction]
        # elif ai_action == 2:
        #     self.direction = left_dir[self.direction]

        if ai_action == 1:
            if self.direction == Direction.LEFT:
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.RIGHT
        elif ai_action == 2:
            if self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN
        
            else:
                self.direction = Direction.LEFT
        elif ai_action == 3 :
            if self.direction == Direction.DOWN:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.UP
        elif ai_action == 4:
            if self.direction == Direction.UP:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.DOWN

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
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
        
        text = self.font.render("Score: " + str(self.score), True, WHITE)
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

class SnakeAI:
    def __init__(self, model_path):
        self.model_path = model_path

    def play_game(self,game:SnakeGame, i:int) -> int:
        # print("Path: " ,self.model_path + "_" + str(i) + ".h5")
        # game = SnakeGame(self.model_path + "_" + str(i) + ".h5")
    
        # game loop
        while True:
            game_over, score = game.play_step()
            
            if game_over == True:
                break
        # record the score
        self.score_arr[i] = score
        return score

    def ai_play(self, game_count:int=5):
        game_count = int(game_count)    
        process_arr = []
        self.score_arr = [0] * game_count

        for i in range(game_count):
            # create array to store process
            pygame.init()
            game = SnakeGame(self.model_path)
            self.score_arr[i] = self.play_game(game, i)
            pygame.quit()

        # for process in process_arr:
        #     process.join()
    def get_average(self):
        return sum(self.score_arr) / len(self.score_arr)
    
    def end():
        pygame.quit()



if __name__ == '__main__':
    AI = SnakeAI(model_path='first_model.h5')
    AI.ai_play(game_count=2)
    print(AI.get_average())