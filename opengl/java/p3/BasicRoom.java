/*
 * BasicRoom.java
 *
 * Simple jogl demo:
 * Displays a simple room as viewed by a single perspective camera 
 * that is oriented by moving the mouse.
 *
 * The "virtual camera" in this demo is very basic. 
 * It maps mouseX and mouseY directly to an absolute yaw and pitch.
 *
 * Ben Porter, August 2010
 */

import javax.media.opengl.*;
import javax.media.opengl.glu.*;
import javax.media.opengl.awt.*;
import com.jogamp.opengl.util.*;
import com.jogamp.opengl.util.gl2.GLUT;

import java.awt.*;
import java.awt.event.*;

public class BasicRoom extends Frame implements GLEventListener, MouseMotionListener, WindowListener
{
	static GLU glu;
	static GLUT glut;
	static GLCanvas canvas;

	static int width = 800, height = 800;
	static int[] INSETS = new int[2]; // need this so we can get proper mouse coordinates
	
	int mouseX, mouseY;

	Room room;

	public static void main(String[] args)
	{
		BasicRoom frame = new BasicRoom();
		frame.setTitle("A basic room rendered with OpenGL");
		frame.setSize(width,height);
		frame.setVisible(true);

		INSETS[0] = frame.getInsets().left;
		INSETS[1] = frame.getInsets().top;
	}	

	public BasicRoom()
	{
		/* create default capabilities object. Init options can be set here */
		GLCapabilities capabilities = new GLCapabilities(GLProfile.get(GLProfile.GL2));
		
	
		/* create canvas with specified capabilities */
		canvas = new GLCanvas(capabilities);
		canvas.addGLEventListener(this);
		canvas.addMouseMotionListener(this);
		addWindowListener(this);
		add(canvas,BorderLayout.CENTER);
	
		glu = new GLU();		// for gluPerspective
		glut = new GLUT();	// for glutCube

		mouseX = width/2;
		mouseY = height/2;
		room = new Room();
	}


	public void init(GLAutoDrawable drawable)
	{
		GL2 gl = drawable.getGL().getGL2();
		gl.glClearColor(1.0f,1.0f,1.0f,1.0f);	// set bg to white
		gl.glEnable(GL2.GL_DEPTH_TEST);			// enable depth buffering
		gl.glEnable(GL2.GL_LIGHTING);			// enable lighting
		gl.glEnable(GL2.GL_LIGHT0);				// use default light
		gl.glEnable(GL2.GL_COLOR_MATERIAL); // use glColor to specify material colour 
		gl.glColorMaterial(GL2.GL_FRONT_AND_BACK, GL2.GL_DIFFUSE);

	}

	public void reshape(GLAutoDrawable drawable, int x, int y, int w, int h)
	{
		GL2 gl = drawable.getGL().getGL2();
		
		width = w;
		height = h;

		/* CAMERA: Set up projection matrix */
		// set correct aspect ratio for perspective projection
		gl.glMatrixMode(GL2.GL_PROJECTION);
		gl.glLoadIdentity();
		glu.gluPerspective(60,1.0*width/height,1,100);
	
		// Change mode back to modelview
		gl.glMatrixMode(GL2.GL_MODELVIEW);
		gl.glLoadIdentity();
	}

	public void display(GLAutoDrawable drawable)
	{
		GL2 gl = drawable.getGL().getGL2();
		
		// display callback
		gl.glClear(GL2.GL_COLOR_BUFFER_BIT | GL2.GL_DEPTH_BUFFER_BIT);
		gl.glLoadIdentity();

		/* CAMERA: The viewing transformation. */
		glu.gluLookAt(
				0,
				Room.dy/2,
				0,
				0,Room.dy/2,10,
				0,1,0);
		gl.glTranslatef(0,Room.dy/2,0);
		gl.glRotatef(-90.f+180.f*mouseY/height,1,0,0);
		gl.glRotatef(-180.f+360.f*mouseX/width,0,1,0);
		gl.glTranslatef(0,-Room.dy/2,0);

		/* Place the light in absolute world coordinates. */		
		float lightPosition[] = {0,Room.dy/2,0,1};
		gl.glLightfv(GL2.GL_LIGHT0,GL2.GL_POSITION,lightPosition,0);

		/* Draw the room */

		room.draw(drawable);	

		gl.glFlush();
	}

	public void dispose(GLAutoDrawable d){}

	public void displayChanged(GLAutoDrawable drawable, boolean modeChanged, boolean deviceChanged)
	{}

	public void mouseMoved(MouseEvent e)
	{
		int x = e.getX();
		int y = e.getY();
		mouseX = x - INSETS[0];
		mouseY = height - y - INSETS[1]; // vertical screencoords flipped
		canvas.repaint();
	}

	public void mouseDragged(MouseEvent e)
	{}
	
	public void windowClosing(WindowEvent e)
	{
		setVisible(false);
		System.exit(0);
	} 
	
	public void windowActivated(WindowEvent e){}
	public void windowClosed(WindowEvent e){}
	public void windowDeactivated(WindowEvent e){}
	public void windowDeiconified(WindowEvent e){}
	public void windowIconified(WindowEvent e){}
	public void windowOpened(WindowEvent e){}
}
