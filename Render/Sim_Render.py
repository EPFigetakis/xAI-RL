import pygame
import os 
import time 

def Global_Vars():
    pygame.font.init()
    global RED, GREEN, BLUE, BLACK, WHITE, TIME_DELAY, FONT, WIDTH, HEIGHT
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    TIME_DELAY = .5
    WIDTH, HEIGHT = 500, 500
    FONT = pygame.font.SysFont('Arial' , 16)
    pygame.font.init()
    print("Ran")
    
    
def init_background():
    global WIN,FPS
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Stochastic Game Env")
    WIN.fill((255,255,255))
    
    FPS = 60
    pygame.display.update()
    
    
def init_image_vars():
    global AgentIC,NodeIC,AgentICGREEN,AgentICRED,NodeICGREEN,NodeICRED
    AgentIC = pygame.image.load(os.path.join("Icons", "Agent1.png"))
    AgentIC = pygame.transform.scale(AgentIC, (50,50))
    NodeIC = pygame.image.load(os.path.join("Icons", "Node.png"))
    NodeIC = pygame.transform.scale(NodeIC, (50,50))
    AgentICGREEN = AgentIC.copy()
    AgentICRED = AgentIC.copy()
    AgentICGREEN.fill(GREEN, special_flags = pygame.BLEND_ADD)
    AgentICRED.fill(RED,special_flags = pygame.BLEND_ADD)
    NodeICGREEN = NodeIC.copy()
    NodeICGREEN.fill(GREEN, special_flags = pygame.BLEND_ADD)
    NodeICRED = NodeIC.copy()
    NodeICRED.fill(RED, special_flags = pygame.BLEND_ADD)
    
def add_element(AG,NN):
    AG_HOLDER = []
    NN_HOLDER = []
    for x in range(1,AG+1):
        AG_HOLDER.append(pygame.Rect((x*(WIDTH/AG)) - 100, 50,50,50))
    for x in range(1,NN+1):
        if (x % 2) == 0:
            c = 100
        else:
            c = 0
        NN_HOLDER.append(pygame.Rect((x*(50)), (150+c) ,50,50))
    return AG_HOLDER, NN_HOLDER
    
def init_window(A,N):
    for z in A:
        WIN.blit(AgentIC, (z.x,z.y))
    for c in N:
        WIN.blit(NodeIC,  (c.x,c.y))
    pygame.display.update()
    
def init_borders(A,Num):
    pygame.draw.rect(WIN,BLUE,(A.x,A.y,50*Num,150))
    pygame.draw.rect(WIN,WHITE,(A.x +10,A.y+10,(50*Num)-20,130))
    pygame.display.update()

def drawboard(A,N,Num):
    init_background()
    init_borders(N[0],Num)
    init_window(A,N)
    
def create_link(A,N):
    pygame.draw.line(WIN,RED, A.center, N.center)
    pygame.display.update()


Global_Vars()
init_image_vars()