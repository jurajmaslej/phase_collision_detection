## todo : Delete this
def create_obj_from_vertices2(obj_vertices):
	if len(obj_vertices) % 3 != 0:
		raise RuntimeError('Wrong number of vertices in input file')
	tris = []
	for i in range (2, len(obj_vertices) + 2, 3):
		tris.append(triangle(vs = [obj_vertices[i-2],obj_vertices[i-1],obj_vertices[i]], my_id = 'obj1'))
	new_obj = compound(tris)
	return new_obj
###

##vertices_multiline = load_object_vertices('object1.txt')
##R3 = create_obj_from_vertices2(vertices_multiline)



'''        
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
'''


'''
if scene.mouse.pick == R1.obj: # if mouseclick on R1, object = R1
                for i in painted_vertices:
                        i.color = color.black
                drag_pos = evt.pos
                scene.bind('mousemove', moveR1)
                scene.bind('mouseup', drop)
'''

#R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.yellow)

#R1 = Obj(R1,[])
#R1.rectangle_points(R1.obj)

#objects.append(R1)

#R2 = box(pos=vector(5,0,0), size=vector(2,5,0), axis=vector(1,0,0), color=color.yellow)

#R2.rectangle_points(R2.obj)
#R1.rectangle_lines()
#R3.rectangle_points(R3.obj)

'''
print(R3.obj_vertices[0].pos.x)
print(R3.obj_vertices[0].pos.y)
print(R3.obj_vertices[1].pos.x)
print(R3.obj_vertices[1].pos.y)
print(R3.obj_vertices[-1].pos.x)
print(R3.obj_vertices[-1].pos.y)
'''

'''
def paint_vertex_pair(closest_pts, dst):
	for i in range (0,len(closest_pts)):
		if len(painted_vertices) <= i:
			if dst <= 0.15:
				painted_vertices.append(sphere(pos = vector(closest_pts[i].pos.x,closest_pts[i].pos.y,0),radius = 0.1, color = color.cyan))
				return
			painted_vertices.append(sphere(pos = vector(closest_pts[i].pos.x,closest_pts[i].pos.y,0),radius = 0.1, color = color.red))
		else:
			if dst <= 0.15:
				painted_vertices[i].pos = vector(closest_pts[i].pos.x,closest_pts[i].pos.y,0)
				painted_vertices[0].color = color.cyan
				painted_vertices[1].color = color.cyan
				return
			#print(painted_vertices[i].pos)
			painted_vertices[i].pos = vector(closest_pts[i].pos.x,closest_pts[i].pos.y,0)
			painted_vertices[i].color = color.red
			
def paint_edge(v):		# v is instance of Line class
	global painted_edge
	if painted_edge is None:
		painted_edge = curve(vector(v.v1.pos.x,v.v1.pos.y,0), vector(v.v2.pos.x,v.v2.pos.y,0), radius = 0.05)
		painted_edge.color = color.red
'''