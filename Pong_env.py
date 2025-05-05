import gym
from gym import spaces
import numpy as np
import pygame
import random
import math

#TODO: optimize ball physics - DONE
#TODO: fix paddle vibrations - couldnt do it lol
#TODO: set up score system - DONE




class PongEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(PongEnv, self).__init__()



        self.WIDTH = 900
        self.HEIGHT = 600
        self.PADDLE_HEIGHT = 100
        
        self.score_1 = 0 
        self.score_2 = 0 


        #ACTION SPACE || for single agent training
        self.action_space = spaces.Discrete(3) 

        #OBSERVATION SPACE || 
        low = np.array([0, 0 ,-10,-10,0,0])
        high = np.array([self.WIDTH, self.HEIGHT, 10,10,self.HEIGHT,self.HEIGHT], dtype=np.float32)
        self.observation_space = spaces.Box(low,high,dtype=np.float32)

        
        #init
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.reset()

    def _get_obs(self):

        # return a NORMALIZED array
        return np.array([
            self.ball_x / self.WIDTH,
            self.ball_y / self.HEIGHT,
            self.ball_vx / 10.0, 
            self.ball_vy / 10.0,
            self.paddle_1y / self.HEIGHT, 
            self.paddle_2y / self.HEIGHT
        ], dtype=np.float32)


    def reflect_ball(self,surface : str):
        #ball is 2D vector Vx and Vy - speed is sqrt, angle is arcrtan
        angle = math.atan2(self.ball_vy,self.ball_vx)

        if surface == "horizontal":
            # top or bottom
            angle = -angle
        elif surface == "vertical":
            # paddle
            angle = math.pi - angle 

        speed = math.sqrt(self.ball_vy**2 + self.ball_vx**2)
        self.ball_vx = math.cos(angle) * speed
        self.ball_vy = math.sin(angle) * speed




    def step(self,action):

        a1 = action 

        if a1 == 1: 
            self.paddle_1y -= 10


        if a1 == 2: 
            self.paddle_1y += 10
        
        # if a2 == 1: 
        #     self.paddle_2y -= 10


        # if a2 == 2: 
        #     self.paddle_2y += 10


        self.paddle_1y = np.clip(self.paddle_1y,0,self.HEIGHT - 100)
        self.paddle_2y = np.clip(self.paddle_2y,0,self.HEIGHT - 100)
        



        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        reward = [0]
        done = False



        #hardcoded a rule based opponent ( paddle 2 )
        if self.ball_y<self.paddle_2y + self.PADDLE_HEIGHT // 2:
            self.paddle_2y -= 5
            self.reflect_ball("horizontal")
        elif self.ball_y > self.paddle_2y + self.PADDLE_HEIGHT // 2:
            self.paddle_2y += 5
            self.reflect_ball("horizontal")

        #bounde from top/bottom
        if self.ball_y <= 0 or self.ball_y >= self.HEIGHT:
            self.reflect_ball("horizontal")
                

        #bounce from paddle - 1
        if self.ball_x <= 30 and self.paddle_1y < self.ball_y < self.paddle_1y + self.PADDLE_HEIGHT:
            self.reflect_ball("vertical")

            reward = [1]
       
        #bounce from paddle - 2
        if self.ball_x >= self.WIDTH-30 and self.paddle_2y < self.ball_y < self.paddle_2y + self.PADDLE_HEIGHT:
            self.ball_vx *= -1
            
            reward = [-1]

        #+1 point for left paddle
        elif self.ball_x <= 0:
            reward = [-1]
            self.score_2 += 1
            done = True
     

        #+1 point for right paddle
        if self.ball_x >= self.WIDTH:
            reward = [1]
            self.score_1 += 1
            done = True

        # return dictionary for logging
        return self._get_obs(), reward[0],done, {"score_1": self.score_1, "score_2": self.score_2}

    

    def reset(self):
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        self.ball_vx = math.cos(angle) * 5
        self.ball_vy = math.sin(angle) * 5
        self.paddle_2y = self.HEIGHT // 2 - 50
        self.paddle_1y = self.HEIGHT // 2 - 50



        return self._get_obs()

    def display_score(self,text,score,color,pos):
        font20 = pygame.font.Font('freesansbold.ttf', 20)
        text = font20.render(text + str(score),True,color)
        return text, pos





    def render(self, mode='human'):
        
        self.screen.fill((0,0,0))
        
        pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(self.WIDTH-20, self.paddle_2y, 10, 100))
        pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(20, self.paddle_1y, 10, 100))

        pygame.draw.circle(self.screen, (255,255,255), (int(self.ball_x), int(self.ball_y)), 7)

        
        score1 , score1_pos = self.display_score("AGENT 1 : ", self.score_1, (0,0,255),(30,10))
        score2 , score2_pos = self.display_score("AGENT 2 : ", self.score_2, (0,255,0),(self.WIDTH - 180,10))

        self.screen.blit(score1,score1_pos)
        self.screen.blit(score2,score2_pos)
        pygame.display.flip()


        
        self.clock.tick(30)

    

    def close(self):
        pygame.quit()
