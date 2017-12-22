from __future__ import division
from vpython import *
import math
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
                def __init__(self, x, y, name=None):
                        self.x = x
                        self.y = y
                        self.name = name
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
                self.obj_vertices = obj_vertices		# for n-lines objects
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
                
        def nline_points(self):
            '''
            create list of Vertices for nline object (from triangles)
            every vertex is in self.vertices only once - even if stated multiple times in input file
            needed for moving object
            '''
            names = set()
            for v in self.obj_vertices:
                name = (v.pos.x, v.pos.y)
                if name not in names:
                    self.vertices.append(self.Vertex(v.pos.x, v.pos.y, name))
                names.add((v.pos.x, v.pos.y))
            #print('names ', names)
                

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
                                
                
##                if not self.lines:
##                        for i in range(0,self.vertices):
##                                if i<len(self.vertices-1):
##                                        line = self.Line(self.vertices[i].pos,self.vertices[i+1].pos)
##                                else:
##                                        line = self.Line(self.vertices[i].pos,self.vertices[0].pos)
##                                self.lines.append(line)
##                else:
##                        for i in range(0, self.vertices):
##                                if i<len(self.vertices):
##                                        self.lines[i].update(self.vertices[i].pos,self.vertices[i+1].pos)
##                                else
##                                        self.lines[i].update(self.vertices[i].pos,self.vertices[0].pos)

                
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
