import pygame
import random
import gym
from gym import spaces
import stable_baselines3
from Cell import Cell, Eat


pygame.init()

WIDTH = 1000
HEIGTH = 600
pixel_dimension = 10
cols = WIDTH // pixel_dimension
rows = HEIGTH // pixel_dimension


COLOR_CELL = (0, 0, 0)       
COLOR_FOOD = (0, 255, 0)     
COLOR_EMPTY = (255, 255, 255)  
COLOR_GRID = (200, 200, 200)  


p_cell = 0.02   
p_food = 0.002 




def generate_initial():
    r = random.random()
    if r < p_cell:
        return Cell()
    elif r < p_cell + p_food:
        return Eat()
    else:
        return None

def initialize_matrix():
    return [[generate_initial() for _ in range(cols)] for _ in range(rows)]

screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Simulación")

def draw_grid(matrix):
   
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * pixel_dimension, y * pixel_dimension, pixel_dimension, pixel_dimension)
            if isinstance(matrix[y][x], Cell):
                pygame.draw.rect(screen, COLOR_CELL, rect)
            elif isinstance(matrix[y][x], Eat):
                pygame.draw.rect(screen, COLOR_FOOD, rect)
            else:
                pygame.draw.rect(screen, COLOR_EMPTY, rect)
    for x in range(0, WIDTH, pixel_dimension):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, HEIGTH))
    for y in range(0, HEIGTH, pixel_dimension):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (WIDTH, y))

class Environment(gym.Env):
    def __init__(self, width, height, pixel_dimension):
        super(Environment, self).__init__()
        self.width = width
        self.height = height
        self.pixel_dimension = pixel_dimension
        self.cols = width // pixel_dimension
        self.rows = height // pixel_dimension
        self.matrix = initialize_matrix()
        self.iteration = 0
        self.action_space = spaces.Discrete(4)  

    def step(self):

        positions = []
        for y in range(self.rows):
            for x in range(self.cols):
                if isinstance(self.matrix[y][x], Cell):
                    positions.append((x, y))
        random.shuffle(positions)
        for x, y in positions:
    
            if not isinstance(self.matrix[y][x], Cell):
                continue

            cell = self.matrix[y][x]
            cell.perceive_environment(self, x, y)
            direction = random.randint(0, 3) 
            new_x, new_y = x, y
            
            
            if direction == 0:
                new_y = y - 1
            elif direction == 1:
                new_y = y + 1
            elif direction == 2:
                new_x = x - 1
            elif direction == 3:
                new_x = x + 1
            if new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows:
                continue
            
        


            if not isinstance(self.matrix[new_y][new_x], Cell):
                self.matrix[new_y][new_x] = self.matrix[y][x]
                self.matrix[y][x] = None
     
        self.iteration += 1
        if self.iteration % 20 == 0:
            self.regenerate_food()
        return self.matrix

    def regenerate_food(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.matrix[y][x] is None and random.random() < p_food:
                    self.matrix[y][x] = Eat()

    def render(self, mode='human'):
        screen.fill(COLOR_EMPTY)
        draw_grid(self.matrix)
        pygame.display.flip()

env = Environment(WIDTH, HEIGTH, pixel_dimension)

running = True
clock = pygame.time.Clock()

while running:
    env.step()
    env.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(5)  

pygame.quit()
