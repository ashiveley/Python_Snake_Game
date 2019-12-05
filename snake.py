__authors__ = "Alexander Shiveley, Sujay Dammoju, Adra Smith"  # Your name
__emails__ = "shivelat@mail.uc.edu, dammojsy@mail.uc.edu, smit4ar@mail.uc.edu"  # Your email address

import pygame, sys, time, random

width = 720
height = 480
snake_size = 10

pygame.init()
pygame.display.set_caption('Snake Game')
window = pygame.display.set_mode((width, height))

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)

fps_controller = pygame.time.Clock()

class Snake:  
    def __init__(self, x, y, direction):
        self.pos = [x,y]
        self.body = [[x, y], [x-snake_size, y], [x-(2*snake_size), y]]    
        self.direction = direction

    def change_dir(self, keyPressed):
        if keyPressed == pygame.K_UP:
            new_dir = 'UP'
        elif keyPressed == pygame.K_DOWN:
            new_dir = 'DOWN'
        elif keyPressed == pygame.K_LEFT:
            new_dir = 'LEFT'
        elif keyPressed == pygame.K_RIGHT:
            new_dir = 'RIGHT'

        if new_dir == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if new_dir == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if new_dir == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if new_dir == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self, game):
        if self.direction == 'UP':
            self.pos[1] -= 1
        if self.direction == 'DOWN':
            self.pos[1] += 1
        if self.direction == 'LEFT':
            self.pos[0] -= 1
        if self.direction == 'RIGHT':
            self.pos[0] += 1

        self.body.insert(0, list(self.pos))      
        apple_eaten = self.try_eat_apple(game.apple)  
        if apple_eaten:
            game.score += 1 
        else:           
            self.body.pop()


    def try_eat_apple(self, apple):
        if self.pos[0] == apple.pos[0] and self.pos[1] == apple.pos[1]:
            apple.spawn = False
            return True
        else:
            return False
    
    
class Apple:
  def __init__(self):
    self.pos = [random.randrange(1, width//snake_size), random.randrange(1, height//snake_size)]
    self.spawn = True

  def respawn(self, snake):
    if not self.spawn:
        collision = True
        while collision:
            self.pos = [random.randrange(1, width//snake_size), random.randrange(1, height//snake_size)]
            collision = False
            for body in snake.body:
                if self.pos[0] == body[0] and self.pos[1] == body[1]:
                    collision = True
        self.spawn = True

    
class Game: 
  def __init__(self):
    self.score = 0
    self.snake = Snake(6,9, 'RIGHT')
    self.apple = Apple()    
    self.is_game_over = False    
  
  def show_score(self, color, font_name, size):
    font = pygame.font.SysFont(font_name, size)
    surface = font.render('Score : ' + str(self.score), True, color)
    rect = surface.get_rect()
    rect.midtop = (width/10, 15)
    window.blit(surface, rect)
    
  def game_over(self):
    if self.snake.pos[0] < 0 or self.snake.pos[0] > width // snake_size - 1:
            self.is_game_over = True
    if self.snake.pos[1] < 0 or self.snake.pos[1] > height // snake_size - 1:
        self.is_game_over = True
    for block in self.snake.body[1:]:
        if self.snake.pos[0] == block[0] and self.snake.pos[1] == block[1]:
            self.is_game_over = True

  def draw(self):
    window.fill(black)
    for pos in self.snake.body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0]*snake_size, pos[1]*snake_size, snake_size, snake_size))

    pygame.draw.rect(window, red, pygame.Rect(self.apple.pos[0]*snake_size, self.apple.pos[1]*snake_size, snake_size, snake_size))

    if self.is_game_over:
        font = pygame.font.SysFont('comicsansms', 90)
        surface = font.render('GAME OVER', True, red)
        rect = surface.get_rect()
        rect.midtop = (width/2, height/6)
        window.fill(black)
        window.blit(surface, rect)
        pygame.display.flip()           
                
    fps_controller.tick(10+self.score)
    self.show_score(green, 'comicsansms', 20)

    pygame.display.update()
  
  def main(self):
    while True:
      for event in pygame.event.get():        
          if event.type == pygame.QUIT:
              self.quit_game()
          elif event.type == pygame.KEYDOWN:
              self.snake.change_dir(event.key)
      if not self.is_game_over:
        self.snake.move(self)

        self.apple.respawn(self.snake)        

        self.game_over()       
                
        self.draw()

  def quit_game(self):
      pygame.quit()
      sys.exit()

game = Game()
game.main()