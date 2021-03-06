# phase_collision_detection
## Team members: Alexander Szendy, Juraj Maslej

## Topic of our project
### V-Clip: narrow phase collision detection
#### Scene: Two 2D convex poly-line objects

### Branch active: vpython file mng

Implement object definition, 
either read line segment positions from text file
or implement user interface to create poly-line by clicking on canvas <br>
<p>
Implement simplified 2D V-Clip algorithm  <br>
Implement method ClipVertex() for VV and VE case  <br>
Implement method ClipEdge() for VE and EE case  <br>
Implement user interaction with object 
</p>

User can move object (rotation is optional) <br>
Show closest points (features) on both geometries <br>

## State exams topic
### https://drive.google.com/file/d/1VnM3IE4yIKGkk51aGQKZoY5UnIW1hVJV/view?usp=sharing

## Our progress so far
### https://www.youtube.com/watch?v=lmj4MT5yGOU

### Multi-line object added
### https://youtu.be/_x1wac8dQdQ

### Code in progress on master
### convex objects implemented
### command line args for creating circle from polygons
### VV, VE, EE collisions detected
### Linear time complexity
Implemented scene with 2 objects.  <br>
Scene is scalable, user can rotate screen
### Objects
User can move objects <br>
Closest vertices are marked

### Code-base
#### Class Obj <br>
Wrapper class for vpython objects <br>
Object has vertices and vpython instance of object it represents <br>
There are two sub-classes, Vertex and Line <br>
#### Vertex <br>
 - position on x-axis <br>
 - position on y-axis <br>
 - list of neighbouring vertices <br>
 
 #### Objects displayed
 <p>
 Rectangles
 - built in object 'box' object imported from vpython library </p>
 N-line object
 - created using 'rectangle' object from vpython lib.
 <br>
 Both are wrapped by Obj class
 
### Technology
We used vpython library, it allows us to run GUI on browser <br>
We plan to use numpy for further math applications 

### V-clip algorithm

We studied clipping algorithm and Voronoi regions. <br>
We tried to implement checking nearest vertices only by looking on 
neighbouring vertices. However we still have issues with updating vertex positions. <br>
Sources: https://pdfs.semanticscholar.org/8bc2/9a05f06e557fb711df7769e2d1e6535a1516.pdf <br>
https://dai.fmph.uniba.sk/upload/2/2b/Ca15_lesson07.pdf
