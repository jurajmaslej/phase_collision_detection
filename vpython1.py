from vpython import *
print("STARTED")
##scene = display(title= "Phase Collision Detecion", x=0, y=0, width = 800, height = 600, background= color.white)
R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.green)
R2 = box(pos=vector(5,0,0), size=vector(2,3,0), axis=vector(1,0,0), color=color.green)
arrow(pos = R1.pos,axis = R2.pos-R1.pos, color = color.white)
drag_pos = None # No object has been picked yet
my_object = box(pos=vector(-10,0,0), size=vector(5,2,0),color = color.cyan)

selected = False

def grab(evt):
    global drag_pos
    print('evt ', evt.event)
    print('scene mouse pick ', scene.mouse.pick)
    print('scene mouse pos ', scene.mouse.pos)
    if scene.mouse.pick == my_object: # if mouseclick on R1, object = R1
        #print('evt ppick R1')
        R2 = box(pos=vector(5,0,0), size=vector(2,3,0), axis=vector(1,0,0), color=color.blue)
        drag_pos = evt.pos
        print("SELECTED HERE")
        selected = True
        scene.bind('mousemove', move)
        scene.bind('mouseup', drop)
##    if scene.mouse.pick == R2: # if mouseclick on R2, object =R2
##        drag_pos = scene.mouse.pos
##        scene.bind('mousemove', move(evt, R2))
##        scene.bind('mouseup', drop)

        
def move(evt):
    global drag_pos
    #print('obj ', obj)
    # project onto xy plane, even if scene rotated:
    new_pos = evt.pos		# vector added
    if new_pos != drag_pos: # checks if mouse has moved
        # offset for where the rectangle was touched:
        displace = new_pos - drag_pos
        my_object.pos += displace
        drag_pos = new_pos # updates drag position

def drop(evt):
    scene.unbind('mousemove', move)
    scene.unbind('mouseup', drop)

print('start')
scene.bind('mousedown', grab)
