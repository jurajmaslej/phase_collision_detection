from __future__ import division
from vpython import *
import math
print("STARTED")
obj1_id = 'obj1'
obj2_id = 'obj2'


class Obj:
        
        # todo class Line
        class Line:
                def __init__(self, start, end):
                        self.start = start # Vertex
                        self.end = end
                        p = vector((start.x+end.x)/2,(start.y+end.y)/2,0) # p = center of line
                        s = vector(abs(start.x-end.x) if abs(start.x-end.x)!=0 else 0.1,abs(start.y-end.y) if abs(start.y-end.y)!= 0 else 0.1,0) # s = line length
                        self.visual = box(pos= p, size = s, axis=vector(1,0,0), color = color.red)

                def set_visible(self, b):
                        self.visual.visible = b

                def update(self, start, end):
                        self.start = start
                        self.end = end
                        p = vector((start.x+end.x)/2,(start.y+end.y)/2,0) # p = center of line
                        self.visual.pos = p
                
        class Vertex:
                def __init__(self, x, y):
                        self.x = x
                        self.y = y
                        self.neighbours = []
                        
                def __str__(self):
                        return 'x: ' + str(self.x) + ' y: ' + str(self.y)
                
                def __repr__(self):
                        return 'x: ' + str(self.x) + ' y: ' + str(self.y)
                        
                def add_neighbourg(self, neighbour):
                        if type(neighbour) == list:
                                for vertex in neighbour:
                                        self.neighbours.append(vertex)
                        else:
                                self.neighbours.append(neighour)
                                
                def vertex_dst(self, v2):
                        x = abs(self.x - v2.x)
                        y = abs(self.y - v2.y)
                        return math.sqrt(x**2 + y**2)
                        # find distance between this vertex and v2
                        
        def __init__(self, obj, obj_vertices):
                #print('x ',obj.pos.x)
                #print('y ',obj.pos.y)
                self.obj = obj
                self.obj_vertices = obj_vertices
                self.vertices = []
                self.lines = []
                
        def __str__(self):
                return 'wrapper class for vpython object ' + str(self.obj)

        def add_obj(self, obj):
                self.obj.append(obj)

        def add_vertex(self, x, y):
                self.vertices.append(self.Vertex(x,y))
                
        def rectangle_points(self, obj):
                # how the points look like
                # 1             2
                # 3             4
                # 
                v1 = self.Vertex(obj.pos.x - obj.length/2, obj.pos.y + obj.height/2)
                v2 = self.Vertex(obj.pos.x + obj.length/2, obj.pos.y + obj.height/2)
                v3 = self.Vertex(obj.pos.x - obj.length/2, obj.pos.y - obj.height/2)
                v4 = self.Vertex(obj.pos.x + obj.length/2, obj.pos.y - obj.height/2)
                #self.vertices.extend((v1, v2, v3, v4))
                self.vertices = [v1,v2,v3,v4]
                
                v1.add_neighbourg([v2, v3])
                v2.add_neighbourg([v1, v4])
                v3.add_neighbourg([v1, v4])
                v4.add_neighbourg([v2, v3])
                
                #print(v1)
                #print(v2)
                #print(v3)
                #print(v4)
                

        def rectangle_lines(self): ## requires to have vertices counted
                # lines :
                # v1 - v2
                # v2 - v4
                # v4 - v3
                # v3 - v1
                if not self.lines:                                
                        line1 = self.Line(self.vertices[0],self.vertices[1])
                        line2 = self.Line(self.vertices[1],self.vertices[3])
                        line3 = self.Line(self.vertices[3],self.vertices[2])
                        line4 = self.Line(self.vertices[2],self.vertices[0])
                        self.lines = [line1,line2,line3,line4]
                else:
                        self.lines[0].update(self.vertices[0],self.vertices[1])
                        self.lines[1].update(self.vertices[1],self.vertices[3])
                        self.lines[2].update(self.vertices[3],self.vertices[2])
                        self.lines[3].update(self.vertices[2],self.vertices[0])
                                
                
        def nearest_vertices(self, obj2):
                # find couple of nearest vertexes between this obj and obj2
                # will run in 'move' function
                # at the beginning check all vertices
                # during movement check only neighbours of nearest vertices
                # still need to implement signed distance for checking distance line-vertex
                closest = []
                closest_dst = 1000000000
                for i in self.vertices:
                        for j in obj2.vertices:
                                dst = i.vertex_dst(j)
                                if closest_dst > dst:
                                        closest_dst = dst
                                        closest = [i,j]
                                elif closest_dst == dst:
                                        if i not in closest:
                                                closest.append(i)
                                        if j not in closest:
                                                closest.append(j)
                return closest

objects = []    # store objects
painted_vertices = [] # store painted points(verteces)
R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.yellow)
R2 = box(pos=vector(5,0,0), size=vector(2,5,0), axis=vector(1,0,0), color=color.yellow)

R1 = Obj(R1,[])
R2 = Obj(R2,[])

R1.rectangle_points(R1.obj)
R2.rectangle_points(R2.obj)

objects.append(R1)
objects.append(R2)

##a = vertex( pos=vec(0,0,0) )
##b = vertex( pos=vec(1,0,0) )
##c = vertex( pos=vec(1,1,0) )
##T = triangle( v0=a, v1=b, v2=c )

# objects.append(T) we assunme only two objects

def closest_vertices():
        '''
        at first compare all the vertices
        possibly slow for multi-vertice objects
        '''
        closest_dst = 10000000
        for v1 in objects[0].vertices:
                for v2 in objects[1].vertices:
                        v_dst = v1.vertex_dst(v2)
                        if v_dst <= closest_dst:
                                #print('closest_dst ', closest_dst)
                                closest_dst = v_dst
                                closest_pair = (v1,v2)
        #print('closest_dst ', closest_dst)
        #print('closest_pair ', closest_pair[0], closest_pair[1])
        return closest_pair

def new_pair():
        global vertex_pair
        '''
        should run in move()
        calculates new closest vertices from neighbours
        of now closest vertices (ones in old_pair)
        '''

        
        old_pair = vertex_pair
        closest_pair = old_pair
        v1 = old_pair[0]
        v2 = old_pair[1]
        #print ('vertices')
        #print (v1)
        #print (v2)
        #print('###')
        closest = v1.vertex_dst(v2)             #closest dst so far
        for neigh1 in v1.neighbours:
                for neigh2 in v2.neighbours:
                        dst = neigh1.vertex_dst(neigh2)
                        #print (' closest in new_pair ', dst)
                        if dst < closest:
                                print ('## change1 ##')
                                closest = dst
                                closest_pair = (neigh1,neigh2)
        for neigh1 in v1.neighbours:
                dst = neigh1.vertex_dst(v2)
                #print (' closest in new_pair ', dst)
                if dst < closest:
                        print ('## change2 ##')
                        closest = dst
                        closest_pair = (neigh1,v2)
        for neigh2 in v2.neighbours:
                dst = neigh2.vertex_dst(v1)
                #print (' closest in new_pair ', dst)
                if dst < closest:
                        print ('## change3 ##')
                        closest = dst
                        closest_pair = (v1,neigh2)
        return closest_pair

def paint_vertex_pair(closest_pts):
        for i in range (0,len(closest_pts)):
                if len(painted_vertices) <= i:
                        painted_vertices.append(sphere(pos = vector(closest_pts[i].x,closest_pts[i].y,0),radius = 0.1, color = color.red))
                else:
                        #print(painted_vertices[i].pos)
                        painted_vertices[i].pos = vector(closest_pts[i].x,closest_pts[i].y,0)
                        painted_vertices[i].color = color.red

vertex_pair = closest_vertices()
print ('vertex pair at start ', vertex_pair)
drag_pos = None # No object has been picked yet

def grab(evt):
        global drag_pos
        print('evt ', evt.event)
        print('scene mouse pick ', scene.mouse.pick)
        print('scene mouse pos ', scene.mouse.pos)

##        obj = scene.mouse.pick
##        if (obj and
##            obj.my_id != undefined and
##            obj.my_id == obj1_id):
##                pass # object created from triangles was chosen

        
        if scene.mouse.pick == R1.obj: # if mouseclick on R1, object = R1
                for i in painted_vertices:
                        i.color = color.black
                drag_pos = evt.pos
                scene.bind('mousemove', moveR1)
                scene.bind('mouseup', drop)
        if scene.mouse.pick == R2.obj: # if mouseclick on R2, object =R2
                for i in painted_vertices:
                        i.color = color.black
                drag_pos = evt.pos
                scene.bind('mousemove', moveR2)
                scene.bind('mouseup', drop)

        
def moveR1(evt):
        global drag_pos
        #print('obj ', obj)
        # project onto xy plane, even if scene rotated:
        new_pos = evt.pos               # vector added
        if new_pos != drag_pos: # checks if mouse has moved
                # offset for where the rectangle was touched:
                #print('moving')
                displace = new_pos - drag_pos
                R1.obj.pos += displace
                drag_pos = new_pos # updates drag position
                
                update_closest_pts()

def update_closest_pts():
        R1.rectangle_points(R1.obj)
        R1.rectangle_lines()
        R2.rectangle_points(R2.obj)
        closest_pts = closest_vertices()
        #closest_pts2 = new_pair()
        paint_vertex_pair(closest_pts)

        
def moveR2(evt):
        global drag_pos
        # print('obj ', obj)
        # project onto xy plane, even if scene rotated:
        new_pos = evt.pos               # vector added
        
        if new_pos != drag_pos: # checks if mouse has moved
                # offset for where the rectangle was touched:
                displace = new_pos - drag_pos
                R2.obj.pos += displace
                drag_pos = new_pos # updates drag
                
                update_closest_pts()
        # paint_vertex_pair()
                
def drop(evt):
        scene.unbind('mousemove', moveR1)
        scene.unbind('mousemove', moveR2)
        scene.unbind('mouseup', drop)
        # do something - label/light closest vertices somehow
        
        # vertex_pair = close   # error "variable referenced before assingment"

def setup_scene():
        scene.title = 'Phase Collision Detection'
        scene.bind('mousedown', grab)

def load_object_vertices(file_name): 
        file = open(file_name, 'r')
        obj_vertices = []
        for line in file:
                line = line.strip().split(' ')
                if len(line)>1:
                        obj_vertices.append(vertex(pos = vec(float(line[0]), float(line[1]),0)))
        file.close()
        return obj_vertices

def create_obj_from_vertices(obj_vertices): # TODO
        '''
        goal is to create object from triangles connecting 1stVertex-2ndVertex-LastVertex
        e.g. lets create 5 vertices obj. we connect:
        we do 2vertices from one side connected to one from the other side
        then we switch from the other side - two from end and one vertex from 
        1st-2nd-5th, 5th-4th-2nd, 2nd-3rd-4th
        for 5 vertices it works, need to make some more conditions for different numbers
        '''
        b_idx = 0
        e_idx = len(obj_vertices) - 1
        print('e_idx ', e_idx)
        tris = []
        for i in range(0,e_idx):
                if b_idx+1==e_idx:
                        break
                if i%2 == 0:
                        print('b_idx ', b_idx, ' obj vertices ', obj_vertices[b_idx],obj_vertices[b_idx+1],obj_vertices[e_idx])
                        tris.append( triangle(vs = [obj_vertices[b_idx],obj_vertices[b_idx+1],obj_vertices[e_idx]], my_id = 'obj1'))
                        b_idx+=1
                else:
                        tris.append( triangle(vs = [obj_vertices[e_idx],obj_vertices[e_idx-1],obj_vertices[e_idx]], my_id = 'obj1'))
                        print ('lowering e_idx ', e_idx)
                        e_idx-=1
        new_obj = compound(tris)
        return new_obj
        
        
print('start')

os.listdir()

setup_scene()
vertices = load_object_vertices('object1.txt')
R = create_obj_from_vertices(vertices)






