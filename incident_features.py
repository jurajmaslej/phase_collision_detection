from __future__ import division
from vpython import *
import math
import object_class

print('detect_incident')
#possibly createclass for this
class Collision_detect():
	def __init__(self, objects, dst, R2, R3):
		self.obj1, self.obj2 = objects
		self.R2 = R2
		self.R3 = R3
		self.iterations = 0
		
	def collision_possible(self):
		r2_neigh= self.R2.get_neighbours(self.obj1)
		r3_neigh= self.R3.get_neighbours(self.obj2)
		
		# vectors for edges in r2
		vectors_r2 = (object_class.Obj.Line(r2_neigh[0], r2_neigh[1]), object_class.Obj.Line(r2_neigh[1], r2_neigh[2]))
		
		# vectors for edges in r3
		vectors_r3 = (object_class.Obj.Line(r3_neigh[0], r3_neigh[1]), object_class.Obj.Line(r3_neigh[1], r3_neigh[2]))
		
		# vectors perpendicular to edges in r2
		perpen_vectors_R2 = self.create_perpen_vectors(self.obj1, self.R2, r2_neigh)
		
		# vectors perpendicular to edges in r3
		perpen_vectors_R3 = self.create_perpen_vectors(self.obj2, self.R3, r3_neigh)
		
		# for vector in R2,R3
		# 	for point in oppposite R
		# 		get_dst_point to line
		# 		if dst small enough
		# 			check if point displays in line boundaries
		# 				if yes : Collision_detected
		# counted 12 checks
		
		# line to line
		line_collision = self.line_to_line_collision(vectors_r2, vectors_r3)
		if line_collision[0] is not None:
			return line_collision
		# end line to line
		
		# v1 and v2 are vectors
		v1, dst1 = self.all_vectors_all_points(vectors_r2, r3_neigh)
		v2, dst2 = self.all_vectors_all_points(vectors_r3, r2_neigh)
		if v1 is not None and v2 is not None:
			if dst1 < dst2:
				return v1
			else:
				return v2
		if v1 is None and v2 is not None:
			return v2
		if v1 is not None and v2 is None:
			return v1
		
		
	def all_vectors_all_points(self, vectors_rx, rx_neigh):
		for v in vectors_rx:
			#print ('vect ', vect.vect.x)
			c = self.parametric(v.v1, v.vect)
			#print ('check param')
			#print ('v.v1 ', v.v1.pos.x, v.v1.pos.y)
			#print ('v.v2 ', v.v2.pos.x, v.v2.pos.y)
			#print ('vect ', v.vect)
			#print ('c ', c)
			for point in rx_neigh:
				self.iterations += 1
				#print ('point in r2 neigh ', point.pos.x, point.pos.y)
				dst = self.dst_point_vect(point, v, c)
				
				if v.vect.x == 0:
					#print('been there X')
					dst = v.v1.pos.x - point.pos.x
					
				if v.vect.y == 0:
					#print('been there Y')
					dst = v.v1.pos.y - point.pos.y
				
				#print ('dst ', dst)
				#print ('with point ', point.pos.x, point.pos.y)
				if abs(dst) <= 0.10:
					on_line = self.check_point_on_line(point, v)
					if on_line:
						print(' EDGE COLLISION DETECTED ', dst)
						return (v, dst)
		return (None, None)
		
		
	def create_perpen_vectors(self, objx, Rx, rx_neigh):
		# create vectors perpendicular to vectors of edges of Rx
		# Rx -> once R2, second time R3
		
		#try to create Line:
		#print('r2 ', r2_neigh[1].pos.x, r2_neigh[1].pos.y)
		#print('r1 ', r3_neigh[1].pos.x, r3_neigh[1].pos.y)
		line1 = Rx.Line(objx, rx_neigh[0])
		line2 = Rx.Line(objx, rx_neigh[1])
		#print ('line1 ', line1.vect)
		perp1 = line1.perpendicular(line1.vect)
		perp2 = line1.perpendicular(line2.vect)
		#print ('perpens')
		#print ('orig ', line1.vect)
		#print ('perpd ', perp1)
		#move_point_along_pepren_vector(obj1)
		return [perp1, perp2]
	
	def condition_for_linetoline(self, vect1, vect2):
		slope1x = vect1.v2.pos.x - vect1.v1.pos.x
		slope2x = vect2.v2.pos.x - vect2.v1.pos.x
		if slope1x == 0 and slope2x == 0:
			return True
		elif (slope1x == 0 and slope2x != 0) or (slope1x != 0 and slope2x == 0):
			return False
		slope1 = (vect1.v2.pos.y - vect1.v1.pos.y)/(slope1x)
		slope2 = (vect2.v2.pos.y - vect2.v1.pos.y)/(slope2x)
		return slope1 == slope2
	
	def line_to_line_dst(self, vect1, vect2):
		# use dst of pointA1 to line by pointB1, pointB2
		dst = self.dst_point_vect(vect1.v1, vect2, 0)
		return dst
	
	def line_to_line_collision(self, vects1, vects2):
		#dst = abs(c2 - c1) / math.sqrt(vect1.vect.x**2 + vect1.vect.y**2)
		closest_dst = 100000
		for vect1 in vects1:
			for vect2 in vects2:
				paralel = self.condition_for_linetoline(vect1, vect2)
				#print(paralel)
				if paralel:
					dst = self.line_to_line_dst(vect1, vect2)
					on_line1 = self.check_point_on_line(vect1.v1, vect2)
					on_line2 = self.check_point_on_line(vect1.v2, vect2)
					on_line3 = self.check_point_on_line(vect2.v1, vect1)
					on_line4 = self.check_point_on_line(vect2.v2, vect1)
					if dst <= 0.12 and any([on_line1, on_line2, on_line3, on_line4]):
						return (vect1, vect2)
		return (None, None)
	
	def check_point_on_line(self, point, vect):
		#print('vect x ', vect.v1.pos.x, vect.v2.pos.x)
		#print( 'point x ', point.pos.x)
		#print('vect y ', vect.v1.pos.y, vect.v2.pos.y)
		#print( 'point y ', point.pos.y)
		sorted_x = sorted([vect.v1.pos.x, vect.v2.pos.x])
		sorted_y = sorted([vect.v1.pos.y, vect.v2.pos.y])
		eps = 0.05
		if (sorted_x[0] - eps <= point.pos.x <= sorted_x[1] + eps) and (sorted_y[0] -eps <= point.pos.y <= sorted_y[1] + eps):
			return True
		return False
		
	def parametric(self, point, vect):
		# checked, working fine, return 'c' in ax + by + c = 0
		c = vect.x * point.pos.x + vect.y * point.pos.y
		return -1 * c	# ax+by+c = 0 ,thats why *-1
	
	def dst_point_vect(self, point, v, c):	#c is from ax + by + c = 0
		#distance point to line
		up = abs(v.vect.x * point.pos.x + v.vect.y * point.pos.y + c)
		#print('up ', up)
		down = math.sqrt(v.vect.x**2 + v.vect.y**2)
		#print('down ', down)
		result = up/down
		# alternative
		up2 = abs(point.pos.x*(v.v2.pos.y - v.v1.pos.y) - point.pos.y*(v.v2.pos.x - v.v1.pos.x) + v.v2.pos.x*v.v1.pos.y - v.v2.pos.y*v.v1.pos.x)
		down2 = math.sqrt((v.v2.pos.y - v.v1.pos.y)**2 + (v.v2.pos.x - v.v1.pos.x)**2)
		result2 = up2/down2
		return result2
	
	def light_line(self, painted_edge, v):
		x = abs(v.v1.pos.x - v.v2.pos.x)
		y = abs(v.v1.pos.y - v.v2.pos.y)
		if painted_edge is False:
			curve(vector(v.v1.pos.x,v.v1.pos.y,0), vector(v.v2.pos.x,v.v2.pos.y,0))
			return True
		#cyl = cylinder(pos=vector(v.vect.x, v.vect.y, 0), axis=vector(x,y,0), radius=0.05)
	
	def move_point_along_pepren_vector(self, point, vect):
		#print('origin point', point.pos.x, point.pos.y)
		#print('vect ', vect)
		x = point.pos.x + vect.x
		y = point.pos.y + vect.y
		return [x,y]
		
	def detect_incident(self, vertex, edge):
		pass
		
	def point_to_point(self, obj1, obj2):
		pass
	
	