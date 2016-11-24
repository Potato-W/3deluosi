import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random  import randint
from math import sqrt,cos,sin,acos,pi,floor

    
def main():
    
    TX,TY,TZ=8,16,8
    #定义初始矩阵值为1，游戏空间
    Reblock=[[[-1]*TZ for i in range(TY)]for j in range(TX)]
    #print("Reblock: ",Reblock)
    #空间坐标，顶点的坐标给定，序号定义面和线
    verticies = (
        (-.5, -.5, -.5),
        (.5, -.5, -.5),
        (.5, .5, -.5),
        (-.5, .5, -.5),
        (-.5, -.5, .5),
        (.5, -.5, .5),
        (.5, .5, .5),
        (-.5, .5, .5)
        )

    edges = (
        (0,1),
        (0,3),
        (0,4),
        (1,2),
        (1,5),
        (2,3),
        (2,6),
        (3,7),
        (4,5),
        (4,7),
        (5,6),
        (6,7)
            )

    surcubess = [ 
                (0,1,2,3), 
                (4,5,6,7),  
                (0,4,7,3), 
                (1,5,6,2),  
                (0,1,5,4), 
                (3,2,6,7) ] 
        
    colors = (
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (1,1,0),
        (0,1,1),
        (1,1,1),
        (1,0,1))
    
    PRECISION=10
    #绘制一个砖块
    def cubes():
        glColor(1,1,1)
        glBegin(GL_QUADS)
        for surcubes in surcubess:
            for vertex in surcubes:
                glVertex(verticies[vertex])
        glEnd()

    #点的旋转
    def point_rotation(u,v,rotation):
        if u==v==0:return 0,0
        d=sqrt(u**2+v**2)
        if v!=abs(v):d*=-1
        angle=acos(u/d)
        return cos(angle+rotation)*d,sin(angle+rotation)*d
    
    #砖块类
    class Brick:
        #砖块类型
        forms=[(4,((0,0,0),(1,0,0),(2,0,0),(3,0,0))),
                  (2,((0,0,0),(0,1,0),(1,0,0),(1,1,0))),
                  (3,((0,0,0),(1,0,0),(1,1,0),(2,0,0))),
                  (3,((0,0,0),(1,0,0),(2,0,0),(2,1,0))),
                  (3,((0,0,0),(1,0,0),(1,1,0),(2,1,0))),
                  (2,((0,0,0),(1,0,0),(1,1,0),(1,0,1))),
                  (2,((0,0,0),(1,0,0),(1,1,0),(0,0,1)))]
                  
        #初始化，生成位置，砖块形式，所需空间
        def __init__(self):
            self.Brick= randint(0,6)
            #定义砖块旋转所需空间
            self.level=Brick.forms[self.Brick][0]
            print("level: ",self.level)
            self.forme=[[[0]*self.level for i in range(self.level)]for j in range(self.level)]
            #print("forme: ",self.forme)
      
            #定义砖块在空间中的样子
            for x,y,z in Brick.forms[self.Brick][1]:
                #print("x,y,z: ",x,y,z)
                #print("b.forme: ",self.forme)
                self.forme[x][y][z]=1
                #print("b.forme: ",self.forme)
            #定义生成位置
            self.x=randint(0,TX-self.level)
            self.y=1
            self.z=randint(0,TZ-self.level)
            self.new=True

            if not self.update():
                print("game over")
                self.new=False
        
        #旋转操作，每次旋转90
        def rotation(self,btn,angle=pi/2):
            tmp=self.forme
            self.forme=[[[0]*self.level for i in range(self.level)]for j in range(self.level)] 
            for x,Lx in enumerate(tmp):
                for y,Ly in enumerate(Lx):
                    for z,pix in enumerate(Ly):
                        #print("z,pix ",z,pix)
                        if pix:
                            nx,ny,nz=x,y,z
                            if btn==0:nx,ny=point_rotation(nx,ny,angle)
                            elif btn==1:nz,ny=point_rotation(nz,ny,angle)
                            else: nx,nz=point_rotation(nx,nz,angle)
                            #print(nx,ny,nz)                       
                            self.forme[round(nx)][round(ny)][round(nz)]=1
        
        #处理冲突    
        def update(self):
            for x,xL in enumerate(self.forme):
                for y,yL in enumerate(xL):
                    for z,pix in enumerate(yL):
                        if pix:
                            if not (0<=x+self.x <TX and 0<=y+self.y <TY and 0<=z+self.z <TZ):
                                #print(" xyz ",x,y,z)
                                #print(self.x,self.y,self.z)
                                return False
                            if  Reblock[x+self.x][y+self.y][z+self.z]!=-1:
                                #print(self.Brick)
                                return False
            return True
           
        #显示砖块           
        def view(self):
            for x,xL in enumerate(self.forme):
                    for y,yL in enumerate(xL):
                        for z,el in enumerate(yL):
                            if el:
                                Cube((x+self.x-TX/2,y-TY/2+self.y,z-TZ/2+self.z),self.Brick)

    #显示文字  
    def drawText(position, text):                                                                                                      
        font = pygame.font.Font(None, 64)                                          
        textSurcubes = font.render(text, True, (255,255,255,255),                   
                                  (0,0,0,0))                                     
        textData = pygame.image.tostring(textSurcubes, "RGBA", True)                
        glRasterPos3d(*position)                                                
        glDrawPixels(textSurcubes.get_width(), textSurcubes.get_height(),         
                        GL_RGBA, GL_UNSIGNED_BYTE, textData)
        
    def add(arg,mul):
        res=list(arg[:3])
        for i in range(3):
            res[i]+=arg[3+i]
            res[i]*=mul
        #print("res ",res)
        return res
    #绘制
    def Cube(pos,couleur):
        glBegin(GL_QUADS)
        glColor(colors[couleur])
        for surcubes in surcubess:
            for vertex in surcubes:
                #print(add(verticies[vertex]+pos,1))
                glVertex(add(verticies[vertex]+pos,1))
        glEnd()

        glColor(1,1,1)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex(add(verticies[vertex]+pos,1))
        glEnd()
     
    #游戏     
    pygame.init()
    #检查手柄
    if not pygame.joystick.get_count():
        print('No joystick')
        return
    stick=pygame.joystick.Joystick(0)
    print(stick.get_name)
    stick.init()
    
    display = (640,480)
   
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.mouse.set_visible(False)

    gluPerspective(70, (display[0]/display[1]), 0.5, 1000)#设置景深
    glShadeModel(GL_SMOOTH)
    #glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)#光线反射
    glEnable(GL_DEPTH_TEST)#隐藏显示被遮住的
    glTranslatef(0.0,0,-max(TX,TY)*3/2)
    glRotatef(180,1,0,0)#旋转，

    view_line=True
    Y_rotation=0
    X_rotation=0
    acceleration=False
    score=0
    notevent=False
    text_position=(-20,-10,0)

    a=Brick()


    while True:  
        for i in range(10):
            #print("i: ",i)
            for event in pygame.event.get():
               # print("event: ",event.dict)
                #print("event type: ",event.type)
                #获得正确响应
                if event.type == JOYBUTTONDOWN and event.button < 0:
                    notevent=1-notevent
                    continue
                #游戏退出
                if event.type == pygame.QUIT:
                     pygame.quit()
                     return
                #正确响应，继续
                if event.type == JOYBUTTONDOWN :
                    #print("button: ",event.button)
                    if event.button==3:
                        view_line=1-view_line
                    elif event.button==5:#加速
                        acceleration=1-acceleration
                    
                    elif event.button==1 or event.button==2 or event.button==0:
                        #print("!")
                        a.rotation(event.button)#旋转后或得你的坐标
                        if not a.update():
                            cubes()
                            a.rotation(event.button,-pi/2)
                                    
            Text_X,Text_Y,Text_Z=text_position
            
            #摇杆控制视角旋转
            x,y=stick.get_axis(1),stick.get_axis(0)
            if abs(x)<.5:x=0
            if abs(y)<.5:y=0
            Y_rotation+=y*PRECISION
            glRotatef(y*PRECISION,0,1, 0)
            Text_X,Text_Z=point_rotation(Text_X,Text_Z,y*PRECISION*pi/180)
            X_rotation+=x*PRECISION  
            if X_rotation<-90:
                X_rotation=-90
                x=0
            if X_rotation>90:
                X_rotation=90
                x=0
            
            #分数跟随转动            
            glRotatef(x*PRECISION, cos(Y_rotation*pi/180), 0,sin(Y_rotation*pi/180))
            Text_Y,Text_Z=point_rotation(Text_Y,Text_Z,-x*PRECISION*cos(Y_rotation*pi/180)*pi/180)
            Text_X,Text_Y=point_rotation(Text_X,Text_Y,-x*PRECISION*sin(Y_rotation*pi/180)*pi/180)
            text_position=(Text_X,Text_Y,Text_Z)
            drawText(text_position, "score : {}".format(score) )
            
            #绘制空间
            glColor(1,1,1)
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex(verticies[vertex][0]*TX,
                            verticies[vertex][1]*TY,verticies[vertex][2]*TZ)
                            
            glEnd()
          
            #绘制当前界面         
            for x,xL in enumerate(Reblock):
                #print("x,xL ",x,xL)
                for y,yL in enumerate(xL):
                    #print("y,yL ",y,yL)
                    for z,pix in enumerate(yL):
                        #print("z,pix ",z,pix)
                        if pix!=-1:
                           Cube((x-TX/2,y-TY/2,z-TZ/2),pix)
            #print(" ",Reblock)
            x,z=point_rotation(stick.get_axis(2),-stick.get_axis(3),Y_rotation/180*pi)

            if i:
                #摇杆位置，左右移动
                if x<-.5: x=-1
                elif x>.5: x= 1
                else:x=0
                
                if z<-.5:z=-1
                elif z>.5: z= 1
                else:z=0

                a.x+=x
                if not a.update():
                    cubes()
                    a.x-=x
                
                a.z+=z
                if not a.update():
                    cubes()
                    a.z-=z
                    
            #a.view()
            pygame.display.flip()
            pygame.time.wait(50)#下降速度
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            a.view()
            
            if notevent or not(i==4 or acceleration ) :continue
            
            #下移
            a.y+=1
            if not a.update():
                acceleration=False
                for x,xL in enumerate(a.forme):
                    for y,yL in enumerate(xL):
                        for z,pix in enumerate(yL):
                            if pix:
                                Reblock[x+a.x][y+a.y-1][z+a.z]=a.Brick

                a.__init__()
                if not a.new:
                    a.view()
                    pygame.display.flip()
                    pygame.quit()
                    return
                
                #这一层，xz都不是-1，那么记录，准备消除
                destruction=[]
                for y in range(TY):
                    for x in range(TX):
                        for z in range(TZ):
                            if Reblock[x][y][z]==-1:
                                break
                        else:
                            destruction+=[(x,y,z) for z in range(TZ)]

                    for z in range(TZ):
                        for x in range(TX):
                            if Reblock[x][y][z]==-1:
                                break
                        else:
                            destruction+=[(x,y,z) for x in range(TX)]
                
                #print(" ",destruction) 
                #显示分数，消除                
                if len(destruction):
                    score+=len(destruction)**2*100
                    print(score)
                    avant=(-1,-1,-1)
                    for x,y,z in destruction:
                        if (x,y,z)==avant:continue
                        avant=(x,y,z)
                        for y in range(y,0,-1):
                            Reblock[x][y][z]=Reblock[x][y-1][z]
                        Reblock[x][0][z]=-1
main()
