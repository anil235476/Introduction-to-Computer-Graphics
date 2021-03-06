#
# FIT3088: Assignment 2
# An example of hard-coding the building complex
# and then generating the geometry to use in 
# rendering.
#
# Ben Porter, August 2010
#

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

from complex import Complex

MS_PER_FRAME = 10
millis = 0

width, height = 600, 600
mouse = [0,0]

complex = None

def setup_scene():
	global complex
	complex = Complex()

def draw_axis():
	glBegin(GL_LINES)
	for v in [(1,0,0),(0,1,0),(0,0,1)]:
		glColor3fv(v)
		glVertex3f(0,0,0)
		glVertex3fv(v)
	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	sp = list(complex.starting_position)
	eye = sp[0]-complex.width/4,sp[1]+complex.height*4,sp[2]
	lookat = sp[0],0,sp[2]+(80.*(height-mouse[1])/height)

	gluLookAt(eye[0],eye[1],eye[2],lookat[0],lookat[1],lookat[2],0,1,0)	
	glTranslatef(eye[0],eye[1],eye[2])
	glRotatef(360.*mouse[0]/width,0,1,0)
	glTranslatef(-eye[0],-eye[1],-eye[2])

	# make the light move around
	light_pos = [complex.width/2,complex.height,complex.length/2,1]
	cycle = math.sin(0.001*millis*math.pi), math.cos(0.001*millis*math.pi)
	light_pos[0] += cycle[0]*complex.width/2
	light_pos[1] += cycle[1]*complex.height/2
	light_pos[2] += (cycle[0]*cycle[1])*complex.length/2
	glLightfv(GL_LIGHT0,GL_POSITION,light_pos)

	# draw a cube to represent the light
	glDisable(GL_LIGHTING)
	glColor3f(1,1,1)
	glPushMatrix()
	glTranslatef(light_pos[0],light_pos[1],light_pos[2])
	glutSolidCube(1)
	glPopMatrix()
	glEnable(GL_LIGHTING)
	
	# draw the complex
	complex.draw()

	glFlush()

def init():
	glClearColor(0,0,0,0)
	glEnable(GL_DEPTH_TEST)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)	
	glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER,1)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60,1,.5,200)
	glMatrixMode(GL_MODELVIEW)

def resize(w,h):
	global width, height
	width, height = w,h
	glViewport(0,0,w,h)
	glutPostRedisplay()

def motion(x,y):
	global mouse
	mouse = x, y
	glutPostRedisplay()

def timer(i):
	global millis
	millis += MS_PER_FRAME
	glutPostRedisplay()
	glutTimerFunc(MS_PER_FRAME,timer,0)

def key(key,x,y):
	glutPostRedisplay()

def keysp(key,x,y):
	glutPostRedisplay()

if __name__=="__main__":
	glutInit()
	glutInitWindowSize(width,height)
	glutInitDisplayMode(GLUT_DEPTH)
	glutCreateWindow("A simple lit building complex.")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(resize)
	glutPassiveMotionFunc(motion)
	glutKeyboardFunc(key)
	glutSpecialFunc(keysp)
	glutTimerFunc(MS_PER_FRAME,timer,0)
	setup_scene()
	glutMainLoop()

