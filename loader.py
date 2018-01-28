from vpython import *
import math
class Loader:
	
	def __init__(self):
		pass
	
	def load_object_vertices(file_name): 
			file = open(file_name, 'r')
			obj_vertices = []
			for line in file:
					line = line.strip().split(' ')
					if len(line)>1:
							obj_vertices.append(vertex(pos = vec(float(line[0]), float(line[1]),0)))
			file.close()
			return obj_vertices
		
	def create_obj_from_vertices(obj_vertices):
			b_idx = 0
			e_idx = len(obj_vertices) - 1
			tris = []
			for i in range(0,e_idx):
					if b_idx+1==e_idx:
							break
					if i%2 == 0:
							tris.append( triangle(vs = [obj_vertices[b_idx],obj_vertices[b_idx+1],obj_vertices[e_idx]]))
							b_idx+=1
					else:
							tris.append( triangle(vs = [obj_vertices[e_idx],obj_vertices[e_idx-1],obj_vertices[b_idx]]))
							e_idx-=1
			new_obj = compound(tris)
			return new_obj
		
	def points_in_circle(self, r, n = 100):
		return [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in range(0,n+1)]
	
	def create_circle_file(self, size, number_of_points = 100):
		points = self.points_in_circle(size, number_of_points)
		f = open('Objects/circle.txt','w')
		for point in points:
			f.write(str(point[0]) + ' ' + str(point[1]) + '\n')
		f.close()
