from __future__ import division
from vpython import *
print("STARTED")

class Obj:
	def __init__(self, obj):
		print('x ',obj.pos.x)
		print('y ',obj.pos.y)
		self.obj = obj
		
	def rectangle_points(self, obj):
		# how the points look like
		# 1		2
		# 3		4
		# 
		x1,y1 = obj.pos.x - obj.length/2, obj.pos.y + obj.height/2
		x2,y2 = obj.pos.x + obj.length/2, obj.pos.y + obj.height/2
		x3,y3 = obj.pos.x - obj.length/2, obj.pos.y - obj.height/2
		x4,y4 = obj.pos.x + obj.length/2, obj.pos.y - obj.height/2
		print(x1, y1)
		print(x2, y2)
		print(x3, y3)
		print(x4, y4)
		
		
		

##scene = display(title= "Phase Collision Detecion", x=0, y=0, width = 800, height = 600, background= color.white)
R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.yellow)
R2 = box(pos=vector(5,0,0), size=vector(2,5,0), axis=vector(1,0,0), color=color.yellow)

T = triangle(
          v0=vertex( pos=vec(0,0,0) ),
          v1=vertex( pos=vec(1,0,0) ),
          v2=vertex( pos=vec(1,1,0) ) )

drag_pos = None # No object has been picked yet
my_object = box(pos=vector(-10,0,0), size=vector(5,2,0),color = color.cyan)

#
o = Obj(R1)
o.rectangle_points(R1)
#

selected = False

def grab(evt):
    global drag_pos
    print('evt ', evt.event)
    print('scene mouse pick ', scene.mouse.pick)
    print('scene mouse pos ', scene.mouse.pos)
    if scene.mouse.pick == R1: # if mouseclick on R1, object = R1
        drag_pos = evt.pos
        print("SELECTED HERE")
        selected = True
        scene.bind('mousemove', moveR1)
        scene.bind('mouseup', drop)
    if scene.mouse.pick == R2: # if mouseclick on R2, object =R2
        drag_pos = evt.pos
        scene.bind('mousemove', moveR2)
        scene.bind('mouseup', drop)

        
def moveR1(evt):
    global drag_pos
    #print('obj ', obj)
    # project onto xy plane, even if scene rotated:
    new_pos = evt.pos		# vector added
    if new_pos != drag_pos: # checks if mouse has moved
        # offset for where the rectangle was touched:
        #print('moving')
        displace = new_pos - drag_pos
        R1.pos += displace
        drag_pos = new_pos # updates drag position
        
def moveR2(evt):
    global drag_pos
    #print('obj ', obj)
    # project onto xy plane, even if scene rotated:
    new_pos = evt.pos		# vector added
    if new_pos != drag_pos: # checks if mouse has moved
        # offset for where the rectangle was touched:
        displace = new_pos - drag_pos
        R2.pos += displace
        drag_pos = new_pos # updates drag position

def drop(evt):
    scene.unbind('mousemove', moveR1)
    scene.unbind('mousemove', moveR2)
    scene.unbind('mouseup', drop)

print('start')

scene.bind('mousedown', grab)
