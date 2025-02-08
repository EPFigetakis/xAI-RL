from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN
from stable_baselines3 import A2C
from sb3_contrib import ARS
from sb3_contrib import MaskablePPO
from sb3_contrib import RecurrentPPO
from sb3_contrib import QRDQN
from sb3_contrib import TRPO
from stable_baselines3 import PPO
import os
import time
import tkinter as tk 

        
def A2C_Settings1(window,env):
        global p_item,LR,Steps,Gamma,Iters
        sub_frame1 = tk.Frame(window,bg="black")
        sub_frame1.grid(row=1,column=3,padx=10,pady=10,sticky="nw")
        
        p_item = tk.StringVar()
        options = ["MlpPolicy", "CnnPolicy", "MultiInputPolicy"]
        dropdown_menu1 = tk.OptionMenu(sub_frame1, p_item, *options)
        dropdown_menu1.config(bg="gray",fg="white",font=("Times New Roman",12), highlightthickness=0)
        dropdown_menu1.grid(row=2,column=1,padx=10,pady=10,sticky="w")
    
        SLabel1 = tk.Label(sub_frame1, text="Policy", bg = "gray", fg="white", font=("Times New Roman",12))
        SLabel1.grid(row=2,column=0,padx=10,pady=5,sticky="w")
    
    
        LR = tk.Entry(sub_frame1,bg="white", font=("Times New Roman",12), justify="center")
        LR.grid(row=3,column=1,padx=5,pady=5,sticky="w")
        SLabel2 = tk.Label(sub_frame1, text="Learning Rate(Float)", bg = "gray", fg="white", font=("Times New Roman",12))
        SLabel2.grid(row=3,column=0,padx=10,pady=5,sticky="w")
    
        Steps = tk.Entry(sub_frame1,bg="white", font=("Times New Roman",12), justify="center")
        Steps.grid(row=4,column=1,padx=5,pady=5,sticky="w")
        
        SLabel3 = tk.Label(sub_frame1, text="Steps(Int)", bg = "gray", fg="white", font=("Times New Roman",12))
        SLabel3.grid(row=4,column=0,padx=10,pady=5,sticky="w")
    
        Gamma = tk.Entry(sub_frame1,bg="white", font=("Times New Roman",12), justify="center")
        Gamma.grid(row=5,column=1,padx=5,pady=5,sticky="w")
        
        SLabel4 = tk.Label(sub_frame1, text="Gamma(Float)", bg = "gray", fg="white", font=("Times New Roman",12))
        SLabel4.grid(row=5,column=0,padx=10,pady=5,sticky="w")
        
        SLabel5 = tk.Label(sub_frame1, text="Iterations", bg = "gray", fg="white", font=("Times New Roman",12))
        SLabel5.grid(row=6,column=0,padx=10,pady=5,sticky="w")
        
        Iters = tk.Entry(sub_frame1,bg="white", font=("Times New Roman",12), justify="center")
        Iters.grid(row=6,column=1,padx=5,pady=5,sticky="w")
        
        button = tk.Button(sub_frame1, text="Simulate" , bg="gray", fg="white", command=lambda : button_send_settings("A2C",env))
        button.grid(row=7,column=1,padx=5,pady=5,sticky='w')
        
def button_send_settings(X,env):
    
    if X == "A2C":
        print(p_item.get(),LR.get(),Steps.get(),Gamma.get())
        _ = A2C_settings_create(p_item.get(),float(LR.get()),int(Steps.get()),float(Gamma.get()),env)
        TS = 30
        iters = int(Iters.get())
        print("\n ====STARTING A2C TRAINING==== \n")
        while iters > 0: 
            _.learn(total_timesteps=TS, log_interval=100,reset_num_timesteps=True,tb_log_name=f"A2C")
            _.save(f"{models_dir_A2C}/{TS*iters}")
            iters = iters - 1
        
    
    
    
    
def A2C_settings_create(P,LR,S,G,env):
    global models_dir_A2C, log_dir_A2C
    try:
        check_env(env)
        print("Env Check Passed")
    except Exception as error:
        print("Enviornment Error", error)
    models_dir_A2C = f"models/A2C/{int(time.time())}/"
    log_dir_A2C = f"logs/A2C/{int(time.time())}/"
    if not os.path.exists(models_dir_A2C):
        os.makedirs(models_dir_A2C)
        print("Model Dir Created")
    else:
        print("Model Dir Found")
    if not os.path.exists(log_dir_A2C):
        os.makedirs(log_dir_A2C)
        print("Log Dir Created")
    else:
        print("Model Dir Found")
        
    MODEL_A2C = A2C(str(P), env, learning_rate=LR, n_steps=S, gamma=G, verbose=0, tensorboard_log=log_dir_A2C)
    return MODEL_A2C
