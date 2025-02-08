import gymnasium as gym
from gymnasium import Env
from gymnasium import spaces
import numpy as np
import os 
import time 
import random
import pandas as pd
import pygame

def define_global_vars():
    global HRB
    HRB = []
    print('Hidden Replay Buffer Intialized', HRB)
    return None

    
def load_replay_buffer():
    #print(HRB.shape)
    return HRB



def save_hidden_replay_buffer():
    temp1 = load_replay_buffer()
    print(len(temp1))
    p1 = f"HiddenReplay/"
    if not os.path.exists(p1):
        os.makedirs(p1)
    file_name = f"HRB-{int(time.time())}"
    fullpath = os.path.join(p1, file_name)
    #print(fullpath)
    np.save(fullpath, temp1)

def hidden_replay_buffer(x):
    #global HRB
    HRB.append(x)

def load_HRB_from_file(filename):
    global HRB
    loaded_data = np.load(filename)
    HRB = np.array(loaded_data)
    print(len(HRB))


def get_global_vars():
    states1,actions1,Network_Influence1,Agent_Links1,Agent_Resources1,NetworkElements1 = states,actions,Network_Influence,Agent_Links,Agent_Resources,NetworkElements
    return states1,actions1,Network_Influence1,Agent_Links1,Agent_Resources1,NetworkElements1


def I_finder(NetI,AgentL,AgentR):
    temp = []
    count = -1
    for x in AgentL:
        count = count+1
        for z in range(0,x):
            temp.append(AgentR[count])
    fnetI = np.multiply(NetI,temp)
    
    return fnetI




def control_gen(Size,Sum):
    array = [1] * Size 
    current_sum = sum(array)
    while current_sum != Sum:
        x = random.randint(0,2)
        array[x] = array[x] + 1
        current_sum = sum(array)
    return array


def save_params(Agents,NetworkElements,N,AL,AR):
    paramfolder = f"Sim-Params/"
    if not os.path.exists(paramfolder):
        os.makedirs(paramfolder)
    file_name = f"Sim{int(Agents)}{int(NetworkElements)}-{int(time.time())}.npz"
    fullpath = os.path.join(paramfolder, file_name)
    print(fullpath)
    np.savez(fullpath, array1=Agents,array2=NetworkElements,array3=N,array4=AL,array5=AR)
    print("====Configuration Saved====")
    
    
    
def load_params_from_file(filename):
    global states,actions,Network_Influence,Agent_Links,Agent_Resources,NetworkElements
    
    loaded_data = np.load(filename)
    Agents = loaded_data['array1']
    NetworkElements = loaded_data['array2']
    
    states = spaces.Discrete(int(Agents))
    actions = spaces.Discrete(int(Agents))
    
    Network_Influence = loaded_data['array3']
    Agent_Links = loaded_data['array4']
    Agent_Resources = loaded_data['array5']
    print("====Configuration Loaded====")
    print("====Env Params Created====","\nstates ", states, "\nActions",actions,"\nNet-Elements-Inf",Network_Influence,"\nAgents-Net-Elements",Agent_Links,"\nAgent-Starting-Resource-Pool",Agent_Resources, "\nNetworkElements", NetworkElements)
    return states,actions,Network_Influence,Agent_Links,Agent_Resources,NetworkElements


def create_env_params(A,N):
    global states,actions,Network_Influence,Agent_Links,Agent_Resources,NetworkElements
    print("Agents:",A)
    print("Network Elements:",N)
    ####Generate the simulation space#### (Action and States)
    states = spaces.Discrete(A) ####Determine number of states
    actions = spaces.Discrete(A) ####Determine number of elems
    ###Generate the Network Elements Influence Factors### 
    elements = [round(random.uniform(0,1),2) for _ in range(N)]
    total = sum(elements)
    Network_Influence = [round(value/total,2) for value in elements]
    ###Generate the Agents Control Over Network Elements###
    Agent_Links = control_gen(A,N)
    ###Generate Pool of Resources (We set this at a total of 10), we can use the same function as above just with different params
    Agent_Resources = control_gen(A,10)
    ###Status Message
    print("====Env Params Created====\nAgents ", A, "\nNetwork Elements",N,"\nNet-Elements-Inf",Network_Influence,"\nAgents-Net-Elements",Agent_Links,"\nAgent-Starting-Resource-Pool",Agent_Resources)
    ###Create A save for the arrays so the simulation can be recreated 
    save_params(A,N,Network_Influence,Agent_Links,Agent_Resources)
    NetworkElements = N
    return states,actions,Network_Influence,Agent_Links,Agent_Resources,NetworkElements


def calc_scores(z1, z2, NumsA, NumsL, NumsM):
    z1 = []
    temp1 = NumsA[0] / NumsL[0]
    temp2 = NumsA[1] / NumsL[1]
    temp3 = NumsA[2] / NumsL[2]

    for x in range(0, NumsL[0]):
        z1.append(temp1)

    for x in range(NumsL[0], NumsL[0] + NumsL[1]):
        z1.append(temp2)

    for x in range(NumsL[1] + NumsL[0], NumsL[2] + NumsL[1] + NumsL[0]):
        z1.append(temp3)

    z2 = []
    for x in range(0, len(NumsM)):
        z2.append(NumsM[x] * z1[x])
    return z1, z2


def step_forward(z1, z2, NumsA, NumsL, NumsM):
    ###rand action
    StepVar = random.randint(0, 2)
    if StepVar == 0:
        HSV = random.randint(1, 2)
        if HSV == 1:
            if NumsA[0] != 0:
                NumsA[0] = NumsA[0] - 1
                NumsA[2] = NumsA[2] + 1
        if HSV == 2:
            if NumsA[2] != 0:
                NumsA[0] = NumsA[0] + 1
                NumsA[2] = NumsA[2] - 1

    if StepVar == 1:
        HSV = random.randint(1, 2)
        if HSV == 1:
            if NumsA[1] != 0:
                NumsA[1] = NumsA[1] - 1
                NumsA[0] = NumsA[0] + 1
        if HSV == 2:
            if NumsA[0] != 0:
                NumsA[1] = NumsA[1] + 1
                NumsA[0] = NumsA[0] - 1

    if StepVar == 2:
        HSV = random.randint(1, 2)
        if HSV == 1:
            if NumsA[2] != 0:
                NumsA[2] = NumsA[2] - 1
                NumsA[1] = NumsA[1] + 1
        if HSV == 2:
            if NumsA[1] != 0:
                NumsA[2] = NumsA[2] + 1
                NumsA[1] = NumsA[1] - 1
    z1, z2 = calc_scores(z1, z2, NumsA, NumsL, NumsM)
    return z1, z2, StepVar


class ABN_Game(Env):
    def __init__(self):
        self.NumsI = []
        self.NumsU = []
        self.NumsL = [2, 4, 2]
        self.NumsA = [6, 3, 1]
        self.NumsM = [2, 1, 2, 2, 1, 1, 2, 2]
        self.reward = 0
        self.action_space = spaces.Discrete(3)  # 3 actions
        self.state_space = spaces.Discrete(3)  # States
        self.observation_space = spaces.Box(low=0, high=3.5, shape=(8,), dtype=np.float64)  # space
        self.NumsI, self.NumsU = calc_scores(self.NumsI, self.NumsU, self.NumsA, self.NumsL, self.NumsM)
        self.NumsI, self.NumsU, self.state_space = step_forward(self.NumsI, self.NumsU, self.NumsA, self.NumsL,
                                                                self.NumsM)
        self.count = 0
        #self.Agent, self.Node = render_board.create_player_node(3, 8)

    def step(self, action):

        # drawboard(self.Agent,self.Node,self.NumsL,self.NumsI,self.NumsA)

        if action == self.state_space:
            # render_board.green_shake_Agent(self.Agent[action])
            self.done = True
            self.trunc = True
            self.reward = self.reward + 1
            pygame.quit()
            # print('Passed', 'Action:', action , 'State:', self.state_space)
        else:
            # render_board.red_shake_Agent(self.Agent[action])
            self.done = False
            self.trunc = False
            self.reward = self.reward + -1
            self.count = self.count + 1
            # print('Failed', 'Action:', action , 'State:', self.state_space)

        self.observation = list(self.NumsI)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
        hidden_replay_buffer(self.observation)
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
        self.NumsL = [2, 4, 2]
        self.NumsA = [6, 3, 1]
        self.NumsM = [2, 1, 2, 2, 1, 1, 2, 2]
        self.NumsI, self.NumsU = calc_scores(self.NumsI, self.NumsU, self.NumsA, self.NumsL, self.NumsM)
        self.NumsI, self.NumsU, self.state_space = step_forward(self.NumsI, self.NumsU, self.NumsA, self.NumsL,
                                                                self.NumsM)
        self.reward = 0
        self.count = 0
        self.prev_action = []
        self.observation = list(self.NumsI)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
       #self.Agent, self.Node = render_board.create_player_node(3, 8)
        info = {}
        return self.observation, info

    
    
define_global_vars()