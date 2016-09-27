import pygame,sys
from pygame.locals import *
import random
import time
pygame.init()
DISPLAY=pygame.display.set_mode((1240,720))
pygame.display.set_caption('Maze runner')
BLACK = ( 0,0,0)
WHITE = (255, 255, 255)
RED= (255,0,0)
GREEN = ( 0, 255,0)
BLUE = ( 0,0, 255)
AQUA=( 0, 255, 255)
FUCKSIA=(255,0, 255)
GRAY=(128, 128, 128)
OLIVE=(128, 128,0)
PURPLE=(128,0, 128)
YELLOW=(255, 255,0)
TEAL=( 0, 128, 128)
BACKGROUND=BLACK
WALL=TEAL
FOOD_INIT=YELLOW
FOOD_MID=RED
FOOD_FINAL=GREEN
DISPLAY.fill(BACKGROUND)
row=17
col=30
WIDTH=40
INITIAL_X=36
INITIAL_Y=50
OFFSET_X=INITIAL_X-WIDTH/2
OFFSET_Y=INITIAL_Y-WIDTH/2
def find_neighbours():
    current=stack[top]
    direction=[]
    direction.append(0)
    if(current.row!=0 and cell_list[current.row-1][current.col].visited==0):
        direction.append(1)
    else:
        direction.append(0)
    if(current.col!=col-1 and cell_list[current.row][current.col+1].visited==0):
        direction.append(1)
    else:
        direction.append(0)
    if(current.row!=row-1 and cell_list[current.row+1][current.col].visited==0):
        direction.append(1)
    else:
        direction.append(0)
    if(current.col!=0 and cell_list[current.row][current.col-1].visited==0):
        direction.append(1)
    else:
        direction.append(0)
    return direction
        
# north wall number is 1,east wall number is 2,south wall number is 3 and west wall number is 4 taken in clockwise number
# cell class will contain the properties of the cells. the cell has four walls north,south,west and east. the class contains functions to build all the walls and then to remove the individual walls
class cell:
    def __init__(self,x,y,i,j):
        self.x=x
        self.y=y
        self.row=i
        self.col=j
    def build_walls(self):
        pygame.draw.line(DISPLAY,WALL,(self.x-WIDTH/2,self.y-WIDTH/2),(self.x+WIDTH/2,self.y-WIDTH/2),1)
        pygame.draw.line(DISPLAY,WALL,(self.x+WIDTH/2,self.y-WIDTH/2),(self.x+WIDTH/2,self.y+WIDTH/2),1)
        pygame.draw.line(DISPLAY,WALL,(self.x+WIDTH/2,self.y+WIDTH/2),(self.x-WIDTH/2,self.y+WIDTH/2),1)
        pygame.draw.line(DISPLAY,WALL,(self.x-WIDTH/2,self.y+WIDTH/2),(self.x-WIDTH/2,self.y-WIDTH/2),1)
    def remove_wall(self,wall_no):
        pixObj=pygame.PixelArray(DISPLAY)
        if wall_no==1:
            if self.row!=0:
                pygame.draw.line(DISPLAY,BACKGROUND,(self.x-WIDTH/2,self.y-WIDTH/2),(self.x+WIDTH/2,self.y-WIDTH/2),1)
                pixObj[self.x-WIDTH/2][self.y-WIDTH/2]=WALL
                pixObj[self.x+WIDTH/2][self.y-WIDTH/2]=WALL
                self.n=0
                cell_list[self.row-1][self.col].s=0
        elif wall_no==2:
            if self.col!=col-1:
                pygame.draw.line(DISPLAY,BACKGROUND,(self.x+WIDTH/2,self.y-WIDTH/2),(self.x+WIDTH/2,self.y+WIDTH/2),1)
                pixObj[self.x+WIDTH/2][self.y-WIDTH/2]=WALL
                pixObj[self.x+WIDTH/2][self.y+WIDTH/2]=WALL
                self.e=0
                cell_list[self.row][self.col+1].w=0
        elif wall_no==3:
            if self.row!=row-1:
                pygame.draw.line(DISPLAY,BACKGROUND,(self.x+WIDTH/2,self.y+WIDTH/2),(self.x-WIDTH/2,self.y+WIDTH/2),1)
                pixObj[self.x+WIDTH/2][self.y+WIDTH/2]=WALL
                pixObj[self.x-WIDTH/2][self.y+WIDTH/2]=WALL
                self.s=0
                cell_list[self.row+1][self.col].n=0
        elif wall_no==4:
            if self.col!=0:
                pygame.draw.line(DISPLAY,BACKGROUND,(self.x-WIDTH/2,self.y+WIDTH/2),(self.x-WIDTH/2,self.y-WIDTH/2),1)
                pixObj[self.x-WIDTH/2][self.y+WIDTH/2]=WALL
                pixObj[self.x-WIDTH/2][self.y-WIDTH/2]=WALL
                self.w=0
                cell_list[self.row][self.col-1].e=0
        del pixObj 
    n=1
    s=1
    w=1
    e=1
    visited=0

def rebuild_cell(i,j):
    if cell_list[i][j].n==1:
        pygame.draw.line(DISPLAY,WALL,(cell_list[i][j].x-WIDTH/2,cell_list[i][j].y-WIDTH/2),(cell_list[i][j].x+WIDTH/2,cell_list[i][j].y-WIDTH/2),1)
    if cell_list[i][j].e==1:
        pygame.draw.line(DISPLAY,WALL,(cell_list[i][j].x+WIDTH/2,cell_list[i][j].y-WIDTH/2),(cell_list[i][j].x+WIDTH/2,cell_list[i][j].y+WIDTH/2),1)
    if cell_list[i][j].s==1:
        pygame.draw.line(DISPLAY,WALL,(cell_list[i][j].x+WIDTH/2,cell_list[i][j].y+WIDTH/2),(cell_list[i][j].x-WIDTH/2,cell_list[i][j].y+WIDTH/2),1)
    if cell_list[i][j].w==1:
        pygame.draw.line(DISPLAY,WALL,(cell_list[i][j].x-WIDTH/2,cell_list[i][j].y+WIDTH/2),(cell_list[i][j].x-WIDTH/2,cell_list[i][j].y-WIDTH/2),1)
            
cell_list=[]
for i in range(row):
    temp_list=[]
    for j in range(col):
        temp_list.append(cell(INITIAL_X+j*WIDTH,INITIAL_Y+i*WIDTH,i,j))
        temp_list[j].build_walls()
    cell_list.append(temp_list)
stack=[]
top=0
initial_x=random.randrange(0,16)
initial_y=random.randrange(0,29)
stack.append(cell_list[initial_x][initial_y])
pygame.draw.circle(DISPLAY,FOOD_INIT,(stack[top].x,stack[top].y),8)
pygame.display.update()
time.sleep(2)
FPS=70
fpsClock=pygame.time.Clock()
while len(stack)>0:
    paths=find_neighbours()
    if 1 not in paths:
        stack[top].visited=1
        pygame.draw.circle(DISPLAY,FOOD_MID,(stack[top].x,stack[top].y),2)
        stack.pop()
        top-=1
    else:
        rand=random.randrange(1,5)
        while paths[rand]!=1:
            rand=random.randrange(1,5)
        if rand==1:
            stack.append(cell_list[stack[top].row-1][stack[top].col])
            stack[top].remove_wall(1)
        elif rand==2:
            stack.append(cell_list[stack[top].row][stack[top].col+1])
            stack[top].remove_wall(2)
        elif rand==3:
            stack.append(cell_list[stack[top].row+1][stack[top].col])
            stack[top].remove_wall(3)
        elif rand==4:
            stack.append(cell_list[stack[top].row][stack[top].col-1])
            stack[top].remove_wall(4)
        pygame.draw.circle(DISPLAY,FOOD_INIT,(stack[top].x,stack[top].y),2)
        stack[top].visited=1
        top+=1
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
pygame.draw.circle(DISPLAY,BACKGROUND,(cell_list[initial_x][initial_y].x,cell_list[initial_x][initial_y].y),10)
pygame.display.update()
time.sleep(1)
pygame.draw.circle(DISPLAY,FOOD_FINAL,(cell_list[initial_x][initial_y].x,cell_list[initial_x][initial_y].y),2)
pygame.display.update()
food_check=[[0]*col for i in range(row)]
for i in range(0,17):
    for j in range(0,30):
        rand=random.randrange(0,5)
        if rand!=0:
            food_check[i][j]=0
            pygame.draw.circle(DISPLAY,BACKGROUND,(cell_list[i][j].x,cell_list[i][j].y),2)
        else:
            pygame.draw.circle(DISPLAY,GREEN,(cell_list[i][j].x,cell_list[i][j].y),2)
            food_check[i][j]=1
        pygame.display.update()
        fpsClock.tick(FPS)

pacUp=pygame.image.load('1.png').convert()
pacRight=pygame.image.load('2.png').convert()
pacDown=pygame.image.load('3.png').convert()
pacLeft=pygame.image.load('4.png').convert()
pacUpClosed=pygame.image.load('closed1.png').convert()
pacRightClosed=pygame.image.load('closed2.png').convert()
pacDownClosed=pygame.image.load('closed3.png').convert()
pacLeftClosed=pygame.image.load('closed4.png').convert()

pacx=INITIAL_X
pacy=INITIAL_Y
FPS=70
CENT_SHIFT=WIDTH/2-1
DISPLAY.blit(pacRight,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
pygame.display.update()
time.sleep(0.5)
fpsClock.tick(10)
cur_row=0
cur_col=0
down=0
up=0
right=0
left=0
cur_dir=0
rand=0
while True:
    pygame.draw.rect(DISPLAY,BLACK,(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),0)
    if cur_dir==0:
        DISPLAY.blit(pacRight,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
    rebuild_cell(cur_row,cur_col)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
             if event.key==K_RIGHT:
                cur_dir=2
             elif event.key==K_LEFT:
                cur_dir=4
             elif event.key==K_UP:
                cur_dir=1
             elif event.key==K_DOWN:
                cur_dir=3
    if (pacx-INITIAL_X)%WIDTH==0 and (pacy-INITIAL_Y)%WIDTH==0:
        up=0
        down=0
        left=0
        right=0
        if cur_dir==1:
            up=1
        elif cur_dir==2:
            right=1
        elif cur_dir==3:
            down=1
        elif cur_dir==4:
            left=1
    if right==1:
        if cell_list[cur_row][cur_col].e==0:
            pacx+=2
            if (pacx-INITIAL_X)%WIDTH==0:
                cur_col+=1
        if food_check[cur_row][cur_col]:
            DISPLAY.blit(pacRightClosed,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
        else:
            DISPLAY.blit(pacRight,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
    elif left==1:
        if cell_list[cur_row][cur_col].w==0:
            pacx-=2
            if (pacx-INITIAL_X)%WIDTH==0:
                cur_col-=1
        if food_check[cur_row][cur_col]:
            DISPLAY.blit(pacLeftClosed,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
        else:
            DISPLAY.blit(pacLeft,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
    elif up==1:
        if cell_list[cur_row][cur_col].n==0:
            pacy-=2
            if (pacy-INITIAL_Y)%WIDTH==0:
                cur_row-=1
        if food_check[cur_row][cur_col]:
            DISPLAY.blit(pacUpClosed,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
        else:
            DISPLAY.blit(pacUp,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
    elif down==1:
        if cell_list[cur_row][cur_col].s==0:
            pacy+=2
            if (pacy-INITIAL_Y)%WIDTH==0:
                cur_row+=1
        if food_check[cur_row][cur_col]:
            DISPLAY.blit(pacDownClosed,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
        else:
            DISPLAY.blit(pacDown,(pacx-CENT_SHIFT,pacy-CENT_SHIFT))
    if rand>15:
        rand=0
    if rand==15:
        food_check[cur_row][cur_col]=0
    rand+=1
    #pygame.display.update()
    pygame.display.update([(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col-1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col+1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row-1)*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row+1)*WIDTH,WIDTH,WIDTH)])
    fpsClock.tick(FPS)
