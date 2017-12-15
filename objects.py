from vpython import box
from vpython import vector
from vpython import color
class Obj:
	def __init__(self, obj):
		print('hello')
		
		
R1 = box(pos=vector(-5,0,0), size=vector(5,2,0),axis=vector(1,0,0), color=color.yellow)
o = Obj(R1)