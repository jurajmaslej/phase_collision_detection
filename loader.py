from vpython import *
class Loader:
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