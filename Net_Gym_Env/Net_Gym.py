import gymnasium as gym
from gymnasium import Env
from gymnasium import spaces
import numpy as np
import os 
import time 
import random
import pandas as pd 

def define_global_vars():
    global HRB
    HRB = []
    print ('Hidden Replay Buffer Init',HRB)
    return True

def load_replay_buffer():
    return HRB

def save_hidden_replay_buffer():
    p1 = f"HiddenReplay/"
    if not os.path.exists(p1):
        os.makedirs(p1)

    file_name = f"HRB-{int(time.time())}.npz"
    fullpath = os.path.join(p1, file_name)
    #print(fullpath)
    np.savez(fullpath, array1=HRB)
    print("====Configuration Saved====")

def hidden_replay_buffer(x):
    #global HRB
    HRB.append(x)

def load_HRB_from_file(filename):
    global HRB
    loaded_data = np.load(filename)
    HRB = np.array(loaded_data['array1'])

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

def stepforward(AR):
    Stepvar = random.randint(0,len(AR)-1) #increase this agent is making the action
    Stepvar1 = random.randint(0,len(AR)-1) #decrease
    
    if ((AR[Stepvar1] - 1) > 0):
        AR[Stepvar1] = AR[Stepvar1] - 1
        AR[Stepvar] = AR[Stepvar] + 1
        
    return AR,Stepvar


class ABN_Game(Env):
    def __init__self(self):
        states1,actions1,Network_Influence1,Agent_Links1,Agent_Resources1,NetworkElements1 = get_global_vars()
        print("\n",states1,actions1,Network_Influence1,Agent_Links1,Agent_Resources1,NetworkElements1)
        self.state_space = states1
        self.action_space = actions1
        self.agent_resources = Agent_Resources1
        self.agent_links = Agent_Links1
        self.network_influence = Network_Influence1
        self.observation_space = spaces.Box(low=0, high=100, shape=(int(NetworkElements1+1),),dtype=np.float64)
        temp = I_finder(self.network_influence,self.agent_links,self.agent_resources)
        temp2 = sum(temp)
        total_temp = temp
        total_temp = np.append(total_temp,temp2)
        self.observation = list(total_temp)
        self.reward = 0
        self.count = 0
        self.agent_resources,self.state_space = stepforward(self.agent_resources)
    
    def step(self,action):
        
        self.agent_resources,self.state_space = stepforward(self.agent_resources)
        
        
        if action == self.state_space:
            self.done = True
            self.trunc = True
            self.reward = self.reward + 1
            
        else:
            self.done = False
            self.trunc = False
            self.reward = self.reward + -1
            self.count = self.count + 1
        
        
        temp = I_finder(self.network_influence,self.agent_links,self.agent_resources)
        temp2 = sum(temp)
        total_temp = temp
        total_temp = np.append(total_temp,temp2)
        self.observation = list(total_temp)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
        hidden_replay_buffer(self.observation)
        
        
        if self.count >= 30:
            self.done = True
        
        self.info = {}
        
        return self.observation, self.reward, self.done, self.trunc, self.info
    def render(self):
        pass
    
    def reset(self,seed=None):
        states1,actions1,Network_Influence1,Agent_Links1,Agent_Resources1,NetworkElements1 = get_global_vars()
        self.state_space = states1
        self.action_space = actions1
        self.agent_resources = Agent_Resources1
        self.agent_links = Agent_Links1
        self.network_influence = Network_Influence1
        self.observation_space = spaces.Box(low=0, high=100, shape=(int(NetworkElements1+1),),dtype=np.float64)
        self.reward = 0
        self.count = 0
        self.prev_action = []
        
        temp = I_finder(self.network_influence,self.agent_links,self.agent_resources)
        temp2 = sum(temp)
        total_temp = temp
        total_temp = np.append(total_temp,temp2)
        self.observation = list(total_temp)
        self.observation = np.array(self.observation)
        self.observation = self.observation.astype(np.float32)
        info = {}
        return self.observation, info
    


define_global_vars()
