from __future__ import division
from vpython import *
import math
from object_class import Obj
from loader import Loader
import object_class
import incident_features
import paintjob
import sys
print("STARTED")

print ('Argument List:', str(sys.argv))


text_file_obj3 = 'Objects/object1.txt'
text_file_obj2 = 'Objects/object2.txt'
text_file_obj_circle = 'Objects/circle.txt'

def load_circle(size = 4, points = 24):
	circle_load = Loader()
	circle_load.create_circle_file(int(size), int(points))
	vertices_circle = Loader.load_object_vertices(text_file_obj_circle)
	circle = Loader.create_obj_from_vertices(vertices_circle)
	circle.color = color.blue
	
	circle = Obj(circle, vertices_circle)
	return circle

def load_Rx(text_file_objx, color = None):
	vertices_multilinex = Loader.load_object_vertices(text_file_objx)
	Rx = Loader.create_obj_from_vertices(vertices_multilinex)
	if color is not None:
		Rx.color = color
	Rx = Obj(Rx,vertices_multilinex)
	return Rx

args = sys.argv
if len(args) > 1:
	if str(args[1]) == '-circle':
		if len(args) == 4:
			R2 = load_circle(args[2], args[3])
		R2 = load_circle()
	else:
		R2 = load_Rx(text_file_obj2)
else:
	R2 = load_Rx(text_file_obj2)
	
R3 = load_Rx(text_file_obj3, color.yellow)

objects = []    # store objects
painted_vertices = [] # store painted points(verteces)
painted_edge = None # only one edge at time can be in collision
painted_edge2 = None # with exception of 2 colliding edges

# for nearest vertices computing with neighbours
# GLOBALS
v1_index = 1000		#assume we would not have so many vertices
v2_index = 1000		#assume we would not have so many vertices
already_counted = False
closest_dst = 10000000

# count iterations
iterations = 0

#T2 = box(pos=vector(2,0,0), length=4, height=1, width=0.1) 
#L2 = label(text='Rotate white object',
#     pos = T2.pos, color=color.green)

def closest_vertices_crossroad(obj1, obj2):
	#print('v1 ', v1_index)
	#print('v2 ', v2_index)
	if already_counted is False:
		return closest_vertices(obj1, obj2)
	else:
		return closest_vertices_neigh(obj1,obj2)

def closest_vertices(obj1, obj2):
        '''
        at first compare all the vertices
        possibly slow for multi-vertice objects
        '''
        global v1_index
        global v2_index
        global already_counted
        global iterations
        already_counted = True
        closest_dst = 10000000
        iterations = 0
        for v1 in obj1.obj_vertices:
                for v2 in obj2.obj_vertices:
                        v_dst = object_class.vertex_dst(v1, v2)		#new method from object_class file, outside main class
                        iterations += 1
                        if v_dst <= closest_dst:
                                closest_dst = v_dst
                                closest_pair = (v1,v2)
                                v1_index = obj1.obj_vertices.index(v1)
                                v2_index = obj2.obj_vertices.index(v2)
        return (closest_pair, closest_dst)

def closest_vertices_neigh(obj1,obj2):
	global v1_index
	global v2_index
	global closest_dst
	global iterations
	iterations = 0
	closest_dst = 10000000
	list1 = [v1_index - 1, v1_index, (v1_index + 1) % len(obj1.obj_vertices)]
	list2 = [v2_index - 1, v2_index, (v2_index + 1) % len(obj2.obj_vertices)]
	for v1 in list1:
		for v2 in list2:
			vertex1 = obj1.obj_vertices[v1]
			vertex2 = obj2.obj_vertices[v2]
			v_dst = object_class.vertex_dst(vertex1, vertex2)
			#print ('v dst ', v_dst, ' v1:', v1, ' v2:', v2) 
			iterations += 1
			if v_dst < closest_dst:
				closest_dst = v_dst
				closest_pair = (vertex1,vertex2)
				v1_index = obj1.obj_vertices.index(vertex1)
				v2_index = obj2.obj_vertices.index(vertex2)
	if closest_dst < 0.1:
		print('Vertices collision detected', closest_dst)
		print ('iterations need for vertices collision ', iterations)
	return (closest_pair, closest_dst)

vertex_pair = closest_vertices_crossroad(R2, R3)
print ('vertex pair at start ', vertex_pair)
drag_pos = None # No object has been picked yet

def grab(evt):
        global drag_pos
        print('evt ', evt.event)
        print('scene mouse pick ', scene.mouse.pick)
        print('scene mouse pos ', scene.mouse.pos)
      
        if scene.mouse.pick == R2.obj: # if mouseclick on R2, object =R2
                for i in painted_vertices:
                        i.color = color.black
                drag_pos = evt.pos
                scene.bind('mousemove', moveR2)
                scene.bind('mouseup', drop)
       
        if scene.mouse.pick == R3.obj: # if mouseclick on R3, object =R3
                for i in painted_vertices:
                        i.color = color.black
                drag_pos = evt.pos
                scene.bind('mousemove', moveR3)
                scene.bind('mouseup', drop)
        '''
        if scene.mouse.pick == T2:
                drag_pos = evt.pos
                R2.obj.rotate(angle=1, axis=vector(0,0,1))
                
                scene.bind('mousemove', rotateR2)
                scene.bind('mouseup', drop)
        '''

def update_closest_pts():
	global closest_dst
	global painted_edge
	global painted_edge2
	closest_pts, dst = closest_vertices_crossroad(R2, R3)
	paintjob.paint_vertex_pair(painted_vertices, closest_pts, dst)
	if dst <= 0.12:
		#print('iterations to found vertex collision ', iterations)
		return		# show collision only on vertices or edges, not both at time
	collision = incident_features.Collision_detect(closest_pts, closest_dst, R2, R3)
	vect = collision.collision_possible()
	if vect is not None:
		if type(vect) is tuple:
			print('edge to edge collision ')
			painted_edge = paintjob.paint_edge(painted_edge, vect[0])
			painted_edge2 = paintjob.paint_edge(painted_edge2, vect[1])
			if painted_edge2 is not None:
				painted_edge2.visible = False
				del painted_edge2
				painted_edge2 = None
			return
		painted_edge = paintjob.paint_edge(painted_edge, vect)
		print('iterations to find edge collision ', collision.iterations)
		collision.iterations = 0
	elif painted_edge is not None:
		painted_edge.visible = False
		del painted_edge
		painted_edge = None

        
def moveR2(evt):
        global drag_pos
        # print('obj ', obj)
        # project onto xy plane, even if scene rotated:
        new_pos = evt.pos               # vector added
        
        if new_pos != drag_pos: # checks if mouse has moved
                # offset for where the rectangle was touched:
                displace = new_pos - drag_pos
                R2.obj.pos += displace 
                for i in R2.obj_vertices:
                        i.pos += displace
                drag_pos = new_pos # updates drag
                update_closest_pts()
        
def moveR3(evt):
        global drag_pos
        # project onto xy plane, even if scene rotated:
        new_pos = evt.pos               # vector added
        
        if new_pos != drag_pos: # checks if mouse has moved
                # offset for where the rectangle was touched:
                displace = new_pos - drag_pos
                R3.obj.pos += displace 
                for i in R3.obj_vertices:
                        i.pos += displace
                drag_pos = new_pos # updates drag
                update_closest_pts()
'''                
def rotateR2(evt):
	global drag_pos
	#print('R2 rotating')
	new_pos = evt.pos              # vector added
        
	if new_pos != drag_pos: # checks if mouse has moved
		# offset for where the rectangle was touched:
		displace = new_pos - drag_pos
		R2.obj.pos += displace 
		for i in R2.obj_vertices:
			i.pos += displace
		drag_pos = new_pos # updates drag
		update_closest_pts()
'''
                
def drop(evt):
        scene.unbind('mousemove', moveR2)
        scene.unbind('mousemove', moveR3)
        #scene.unbind('mousemove', rotateR2)
        scene.unbind('mouseup', drop)

def setup_scene():
        scene.title = 'Phase Collision Detection'
        scene.bind('mousedown', grab)        
        
print('start')

setup_scene()



