from __future__ import division
from vpython import *

def paint_vertex_pair(painted_vertices, closest_pts, dst):
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
			
def paint_edge(painted_edge, v):		# v is instance of Line class
	#global painted_edge
	if painted_edge is None:
		painted_edge = curve(vector(v.v1.pos.x,v.v1.pos.y,0), vector(v.v2.pos.x,v.v2.pos.y,0), radius = 0.05)
		painted_edge.color = color.red
	return painted_edge