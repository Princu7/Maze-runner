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
FOOD_MID=BLACK
FOOD_FINAL=GREEN
DISPLAY.fill(BACKGROUND)
row=17
col=30
WIDTH=40
INITIAL_X=40
INITIAL_Y=40
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
initial_x=random.randrange(0,row-1)
initial_y=random.randrange(0,col-1)
stack.append(cell_list[initial_x][initial_y])
pygame.draw.circle(DISPLAY,FOOD_INIT,(stack[top].x,stack[top].y),8)
pygame.display.update()
time.sleep(2)
FPS=60
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
for i in range(0,row):
    for j in range(0,col):
        rand=random.randrange(0,4)
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
initial_cell=0
final_cell=row*col-1
queue=[]
predecessor=[0]*(row*col)
queue.append(initial_cell)
visited_cell=[0]*(row*col)
visited_cell[initial_cell]=1
while True:
    a=queue[0]
    del(queue[0])
    row=int(a/30)
    col=a%30
    if row!=0 and cell_list[row][col].n==0:
        if visited_cell[a-30]==0:
            queue.append(a-30)
            predecessor[a-30]=a
            visited_cell[a-30]=1
        if (a-30)==final_cell:
            break
    if row!=16 and cell_list[row][col].s==0:
        if visited_cell[a+30]==0:
            queue.append(a+30)
            predecessor[a+30]=a
            visited_cell[a+30]=1
        if (a+30)==final_cell:
            break
    if col!=0 and cell_list[row][col].w==0:
        if visited_cell[a-1]==0:
            queue.append(a-1)
            predecessor[a-1]=a
            visited_cell[a-1]=1
        if (a-1)==final_cell:
            break
    if col!=29 and cell_list[row][col].e==0:
        if visited_cell[a+1]==0:
            queue.append(a+1)
            predecessor[a+1]=a
            visited_cell[a+1]=1 
        if (a+1)==final_cell:
            break
    #print queue
start=initial_cell
initial_cell=final_cell
path=[]
while initial_cell!=start:
    path.append(initial_cell)
    initial_cell=predecessor[initial_cell]
path.append(0)
path=path[::-1]

def find_dir(initial):
    if path[initial+1]-path[initial]==-30:
        return 1
    elif path[initial+1]-path[initial]==1:
        return 2
    elif path[initial+1]-path[initial]==30:
        return 3
    elif path[initial+1]-path[initial]==-1:
        return 4

def move_hero():
    newpacx=INITIAL_X
    newpacy=INITIAL_Y
    oldpacx=0
    oldpacy=0
    counter=0
    FPS=30
    cur_row=0
    cur_col=0
    FPS=80
    rand=0
    while counter!=len(path)-1:
        cur_dir=find_dir(counter)
        cur_cell=path[counter]
        if cur_dir==1:
            dest=newpacy-40
            while newpacy!=dest:
                if rand>16:
                    rand=0
                if rand==16:
                    food_check[cur_row][cur_col]=0
                rand+=1
                oldpacy=newpacy
                oldpacx=newpacx
                newpacy-=2
                pygame.draw.rect(DISPLAY,BACKGROUND,(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),0)
                rebuild_cell(cur_row,cur_col)
                if food_check[cur_row][cur_col]:
                    DISPLAY.blit(pacUpClosed,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                else:
                    DISPLAY.blit(pacUp,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                pygame.display.update([(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col-1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col+1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row-1)*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row+1)*WIDTH,WIDTH,WIDTH)])
                fpsClock.tick(FPS)
            cur_row-=1
             
        elif cur_dir==2:
             dest=newpacx+40
             while newpacx!=dest:
                if rand>16:
                    rand=0
                if rand==16:
                    food_check[cur_row][cur_col]=0
                rand+=1
                oldpacy=newpacy
                oldpacx=newpacx
                newpacx+=2
                pygame.draw.rect(DISPLAY,BACKGROUND,(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),0)
                rebuild_cell(cur_row,cur_col)
                if food_check[cur_row][cur_col]:
                    DISPLAY.blit(pacRightClosed,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                else:
                    DISPLAY.blit(pacRight,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                pygame.display.update([(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col-1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col+1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row-1)*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row+1)*WIDTH,WIDTH,WIDTH)])
                fpsClock.tick(FPS)
             cur_col+=1

        elif cur_dir==3:
            dest=newpacy+40
            while newpacy!=dest:
                if rand>16:
                    rand=0
                if rand==16:
                    food_check[cur_row][cur_col]=0
                rand+=1
                oldpacy=newpacy
                oldpacx=newpacx
                newpacy+=2
                pygame.draw.rect(DISPLAY,BACKGROUND,(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),0)
                rebuild_cell(cur_row,cur_col)
                if food_check[cur_row][cur_col]:
                    DISPLAY.blit(pacDownClosed,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                else:
                    DISPLAY.blit(pacDown,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                pygame.display.update([(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col-1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col+1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row-1)*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row+1)*WIDTH,WIDTH,WIDTH)])
                fpsClock.tick(FPS)
            cur_row+=1

        elif cur_dir==4:
            dest=newpacx-40
            while newpacx!=dest:
                if rand>16:
                    rand=0
                if rand==16:
                    food_check[cur_row][cur_col]=0
                rand+=1
                oldpacy=newpacy
                oldpacx=newpacx
                newpacx-=2
                pygame.draw.rect(DISPLAY,BACKGROUND,(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),0)
                rebuild_cell(cur_row,cur_col)
                if food_check[cur_row][cur_col]:
                    DISPLAY.blit(pacLeftClosed,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                else:
                    DISPLAY.blit(pacLeft,(newpacx-CENT_SHIFT,newpacy-CENT_SHIFT))
                pygame.display.update([(OFFSET_X+cur_col*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col-1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+(cur_col+1)*WIDTH,OFFSET_Y+cur_row*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row-1)*WIDTH,WIDTH,WIDTH),(OFFSET_X+cur_col*WIDTH,OFFSET_Y+(cur_row+1)*WIDTH,WIDTH,WIDTH)])
                fpsClock.tick(FPS)
            cur_col-=1
        counter+=1

move_hero()         
