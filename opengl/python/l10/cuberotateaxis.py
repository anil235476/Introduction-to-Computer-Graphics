from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

MS_PER_FRAME = 10
millis = 0

width, height = 600, 600
mouse = [0,0]

viewYR = 0

axis_of_rotation = p,q = ((1,0,0),(1,1,1))

def draw_axis():
	glBegin(GL_LINES)
	for v in [(1,0,0),(0,1,0),(0,0,1)]:
		glColor3fv(v)
		glVertex3f(0,0,0)
		glVertex3fv(v)
	glEnd()

def draw_cube():
	glPushMatrix()
	glColor3f(1,1,1)
	glutWireCube(1)
	glPopMatrix()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(0,1,2,0,0,0,0,1,0)	
	glRotatef(viewYR,0,1,0)

	draw_axis()

	# draw_axis_of_rotation
	glColor3f(1,1,0)
	glBegin(GL_LINES)
	glVertex3fv(p)
	glVertex3fv(q)
	glEnd()

	# draw cube rotated around the axis
	glTranslatef(p[0],p[1],p[2])
	glRotatef(360.*mouse[0]/width,q[0]-p[0],q[1]-p[1],q[2]-p[2])
	glTranslatef(-p[0],-p[1],-p[2])
	draw_cube()

	glFlush()

def init():
	glClearColor(0,0,0,0)
	glEnable(GL_DEPTH_TEST)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60,1,0.1,10)
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
	global viewYR
	if key==GLUT_KEY_LEFT:
		viewYR += 10
	elif key==GLUT_KEY_RIGHT:
		viewYR -= 10
	glutPostRedisplay()

if __name__=="__main__":
	glutInit()
	glutInitWindowSize(width,height)
	glutInitDisplayMode(GLUT_DEPTH)
	glutCreateWindow("cube")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(resize)
	glutPassiveMotionFunc(motion)
	glutKeyboardFunc(key)
	glutSpecialFunc(keysp)
	glutTimerFunc(MS_PER_FRAME,timer,0)
	glutMainLoop()

