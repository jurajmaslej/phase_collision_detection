from vpython import *
R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.green)
R2 = box(pos=vector(5,0,0), size=vector(2,3,0), axis=vector(1,0,0), color=color.green)

drag_pos = None # No object has been picked yet

def grab(evt):
    global drag_pos
    print('evt ', evt.event)
    print('scene mouse pick ', scene.mouse.pick)
    print('scene mouse pos ', scene.mouse.pos)
    if scene.mouse.pick == R1: # if mouseclick on R1, object = R1
        #print('evt ppick R1')
        R2 = box(pos=vector(5,0,0), size=vector(2,3,0), axis=vector(1,0,0), color=color.blue)
        drag_pos = scene.mouse.pos
        scene.bind('mousemove', moveR1())
        scene.bind('mouseup', drop)
    if scene.mouse.pick == R2: # if mouseclick on R2, object =R2
        drag_pos = scene.mouse.pos
        scene.bind('mousemove', move(evt, R2))
        scene.bind('mouseup', drop)

def move(evt, obj):
    global drag_pos
    print('obj ', obj)
    # project onto xy plane, even if scene rotated:
    new_pos = scene.mouse.project(normal=vector(0,0,1))		# vector added
    if new_pos != drag_pos: # checks if mouse has moved
        # offset for where the rectangle was touched:
        obj.pos += new_pos - drag_pos
        drag_pos = new_pos # updates drag position
        
def moveR1():
    global drag_pos
    print('drag_pos ', drag_pos)
    # project onto xy plane, even if scene rotated:
    new_pos = scene.mouse.project(normal=vector(0,0,1))		# vector added
    if new_pos != drag_pos: # checks if mouse has moved
        # offset for where the rectangle was touched:
        R1.pos += new_pos - drag_pos
        drag_pos = new_pos # updates drag position

def drop(evt):
    scene.unbind('mousemove', move)
    scene.unbind('mouseup', drop)

print('start')
scene.bind('mousedown', grab)