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
    WIDTH, HEIGHT = 800, 600
    FONT = pygame.font.SysFont('Arial' , 16)
    pygame.font.init()


def init_background():
    Global_Vars()
    global WIN,FPS
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Stochastic Game Env")
    FPS = 60
    #print("Begin Render")

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
    
    print("Render Images")






def create_player_node(AN,NN):
    AN_HOLDER = []
    NN_HOLDER = []
    for x in range(1,AN+1):
        AN_HOLDER.append(pygame.Rect((x*(WIDTH/AN)) - 100, 50,50,50))
    for x in range(1,NN+1):
        NN_HOLDER.append(pygame.Rect((x*(WIDTH/NN)) - 100, 250,50,50))
    return AN_HOLDER, NN_HOLDER


def init_window(A,N):
    WIN.fill((255,255,255))
    for z in A:
        WIN.blit(AgentIC, (z.x,z.y))
    for c in N:
        WIN.blit(NodeIC,  (c.x,c.y))
    pygame.display.update()
    
    
def green_shake_Agent(N):
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    
def red_shake_Agent(N):
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(AgentICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    
    WIN.blit(AgentIC,(N.x,N.y))
    pygame.display.update()

    
def green_shake_Node(N):
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICGREEN, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    
def red_shake_Node(N):
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeICRED, (N.x,N.y))
    pygame.display.update()
    time.sleep(TIME_DELAY)
    WIN.blit(NodeIC,(N.x,N.y))
    pygame.display.update() 

    
def create_text_label(N,T):
    text = FONT.render(T, False, BLACK)
    WIN.blit(text,N.midbottom)
    pygame.display.update()
    
def create_link(A,N):
    pygame.draw.lines(WIN,RED, A.center, N.center)
    pygame.display.update()

        
'''        
Agent,Node = create_player_node(3,8)
clock = pygame.time.Clock()
init_window(Agent,Node)
create_text_label(Agent[2],'5')
green_shake_Agent(Agent[0])
red_shake_Agent(Agent[1])
create_link(Agent[0],Node[2])
green_shake_Node(Node[3])
red_shake_Node(Node[4])
run = True
while run:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
pygame.quit()
'''
    
