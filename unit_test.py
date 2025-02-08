import pygame
import os
import time 
import random
from Render import render_board
import gymnasium as gym
from gymnasium import Env
from gymnasium import spaces
from collections import deque 
import tensorflow as tf 
from tensorflow import keras
from stable_baselines3 import PPO
import numpy as np
pygame.font.init()


render_board.Global_Vars()
render_board.init_image_vars()



def calc_scores(z1,z2,NumsA,NumsL,NumsM):
    z1 = []
    temp1 = NumsA[0]/NumsL[0]
    temp2 = NumsA[1]/NumsL[1]
    temp3 = NumsA[2]/NumsL[2]
    for x in range(0,NumsL[0]):
        z1.append(temp1)
        
    for x in range(NumsL[0],NumsL[0]+NumsL[1]):
        z1.append(temp2)
        
    for x in range(NumsL[1]+NumsL[0],NumsL[2]+NumsL[1]+NumsL[0]):
        z1.append(temp3)
    
    z2 = []
    for x in range(0,len(NumsM)):
        z2.append(NumsM[x] * z1[x])
    return z1,z2

def step_forward(z1,z2,NumsA,NumsL,NumsM):
###rand action
    StepVar = random.randint(0,2)
    if StepVar == 0:
        HSV = random.randint(1,2)
        if HSV == 1:
            if NumsA[0] != 0:
                NumsA[0] = NumsA[0] - 1
                NumsA[2] = NumsA[2] + 1
        if HSV == 2:
            if NumsA[2] != 0:
                NumsA[0] = NumsA[0] + 1
                NumsA[2] = NumsA[2] - 1
            
    if StepVar == 1:
        HSV = random.randint(1,2)
        if HSV == 1:
            if NumsA[1] != 0:
                NumsA[1] = NumsA[1] - 1
                NumsA[0] = NumsA[0] + 1
        if HSV == 2:
            if NumsA[0] != 0:
                NumsA[1] = NumsA[1] + 1
                NumsA[0] = NumsA[0] - 1

    if StepVar == 2:
        HSV = random.randint(1,2)
        if HSV == 1:
            if NumsA[2] != 0:
                NumsA[2] = NumsA[2] - 1
                NumsA[1] = NumsA[1] + 1
        if HSV == 2:
            if NumsA[1] != 0:
                NumsA[2] = NumsA[2] + 1
                NumsA[1] = NumsA[1] - 1
    z1, z2 = calc_scores(z1,z2,NumsA,NumsL,NumsM)
    return z1,z2,StepVar

class ABN_Game(Env):
    def __init__(self):
        self.NumsI = []
        self.NumsU = []
        self.NumsL = [2,4,2]
        self.NumsA = [6,3,1]
        self.NumsM = [2,1,2,2,1,1,2,2]
        self.reward = 0
        self.action_space = spaces.Discrete(3) # 3 actions
        self.state_space = spaces.Discrete(3) # States
        self.observation_space = spaces.Box(low=0, high=3.5, shape=(8,), dtype=np.float64) #space
        self.NumsI, self.NumsU = calc_scores(self.NumsI,self.NumsU,self.NumsA,self.NumsL,self.NumsM)
        self.NumsI, self.NumsU, self.state_space = step_forward(self.NumsI,self.NumsU,self.NumsA,self.NumsL,self.NumsM)
        self.count = 0
        self.Agent, self.Node = render_board.create_player_node(3,8)
        
    def step(self,action):
        
        #drawboard(self.Agent,self.Node,self.NumsL,self.NumsI,self.NumsA)
        
        
        if action == self.state_space :
            #render_board.green_shake_Agent(self.Agent[action])
            self.done = True
            self.trunc = True
            self.reward = self.reward + 1
            pygame.quit()
            #print('Passed', 'Action:', action , 'State:', self.state_space)
        else:
            #render_board.red_shake_Agent(self.Agent[action])
            self.done = False
            self.trunc = False
            self.reward = self.reward + -1
            self.count = self.count + 1
            #print('Failed', 'Action:', action , 'State:', self.state_space)
        
        self.observation = list(self.NumsI)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
            
        if self.count >= 10:
            self.done = True
            pygame.quit()
            
        
        self.info = {}
        return self.observation, self.reward, self.done, self.trunc, self.info
        
    def render(self):
        pass
    
    def reset(self, seed=None):
        self.NumsI = []
        self.NumsU = []
        self.NumsL = [2,4,2]
        self.NumsA = [6,3,1]
        self.NumsM = [2,1,2,2,1,1,2,2]
        self.NumsI, self.NumsU = calc_scores(self.NumsI,self.NumsU,self.NumsA,self.NumsL,self.NumsM)
        self.NumsI, self.NumsU, self.state_space = step_forward(self.NumsI,self.NumsU,self.NumsA,self.NumsL,self.NumsM)
        self.reward = 0
        self.count = 0
        self.prev_action = []
        self.observation = list(self.NumsI)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
        self.Agent, self.Node = render_board.create_player_node(3,8)
        info = {}
        return self.observation, info

env = ABN_Game()

env.reset()
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN
from stable_baselines3 import A2C
from sb3_contrib import ARS
from sb3_contrib import MaskablePPO
from sb3_contrib import RecurrentPPO
from sb3_contrib import QRDQN
from sb3_contrib import TRPO
from stable_baselines3 import PPO
check_env(env)


print('GYM Env SB3 Passed Check')