import gym
from gym import spaces
import numpy as np
import pygame
from pygame import event
import random
import math

#TODO: optimize ball physics
#TODO: fix paddle vibrations
#TODO: set up score system




class PongEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(PongEnv, self).__init__()

        self.WIDTH = 900
        self.HEIGHT = 600
        self.PADDLE_HEIGHT = 100

        #ACTION SPACE || for single agent training
        self.action_space = spaces.Tuple(
            (
                spaces.Discrete(3),
                spaces.Discrete(3),

            )
        ) #here

        #OBSERVATION SPACE || 
        low = np.array([0, 0 ,-10,-10,0])
        high = np.array([self.WIDTH, self.HEIGHT, 10,10,self.HEIGHT], dtype=np.float32)
        self.observation_space = spaces.Box(low,high,dtype=np.float32)

        
        #init
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.reset()

    def _get_obs(self):
        return np.array([
            self.ball_x, self.ball_y,
            self.ball_vx, self.ball_vy,
            self.paddle_1y, self.paddle_2y
        ], dtype=np.float32)


    def step(self,action):

        a1,a2 = action 

        if a1 == 1: 
            self.paddle_1y -= 10


        if a1 == 2: 
            self.paddle_1y += 10
        
        if a2 == 1: 
            self.paddle_2y -= 10


        if a2 == 2: 
            self.paddle_2y += 10


        self.paddle_1y = np.clip(self.paddle_1y,0,self.HEIGHT - 100)
        self.paddle_2y = np.clip(self.paddle_2y,0,self.HEIGHT - 100)
            
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        reward = [0,0] 
        done = False

        angle1 = random.uniform(0, 2 * math.pi)
        angle2= random.uniform(0, -2*math.pi)

        #bounde from top/bottom
        if self.ball_y <= 0 or self.ball_y >= self.HEIGHT:
            self.ball_vy *= -1
            if self.ball_x > self.WIDTH // 2:
                self.ball_vx = math.cos(angle1) * 5
                self.ball_vy = math.sin(angle2) * 5
            else:
                 self.ball_vx = math.cos(angle1) * 5
                 self.ball_vy = math.sin(angle1) * 5

        #bounce from paddle
        if self.ball_x <= 30 and self.paddle_1y < self.ball_y < self.paddle_1y + self.PADDLE_HEIGHT:
            self.ball_vx *= -1

            reward = [1,-1]

        elif self.ball_x <= 0:
            reward = [-1,1]
            self.reset()
        
        if self.ball_x >= self.WIDTH-30 and self.paddle_2y < self.ball_y < self.paddle_2y + self.PADDLE_HEIGHT:
            self.ball_vx *= -1

            reward = [-1,1]


        if self.ball_x >= self.WIDTH:
            reward = [1,-1]
            self.reset()

        return self._get_obs(), reward,done,{}
    

    def reset(self):
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        self.ball_vx = math.cos(angle) * 5
        self.ball_vy = math.sin(angle) * 5
        self.paddle_2y = self.HEIGHT // 2 - 50
        self.paddle_1y = self.HEIGHT // 2 - 50
        return self._get_obs()



    def render(self, mode='human'):
        
        self.screen.fill((0,0,0))
        
        pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(self.WIDTH-20, self.paddle_2y, 10, 100))
        pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(20, self.paddle_1y, 10, 100))

        pygame.draw.circle(self.screen, (255,255,255), (int(self.ball_x), int(self.ball_y)), 7)
        pygame.display.flip()
        self.clock.tick(30)

    

    def close(self):
        pygame.quit()
        
    
# def main():

#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_DOWN:
#             pygame.quit()
            


