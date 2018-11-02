"""
Dobble SVG generator.
By Thibault Nocchi.
https://github.com/Tiwenty

Run this script from a folder where it has a child folder named "img" with PNG symbols named as 1.png, 2.png, etc.
It'll create a "svg" folder with all generated cards as SVG.

The script will notify you when it has finished, although it is the only alert it'll give you. If you want to watch what it is doing, go into the "svg" folder and watch what is generated.
"""
import svgwrite
import struct
import imghdr
from math import pi, sqrt
from random import randint

def generateCards(numberOfSymb):
	"""
	Generates a list of cards which are themselves a list of symbols needed on each card to respect the rules of Dobble.
	This algorithm was taken from the french Wikipedia page of "Dobble".
	https://fr.wikipedia.org/wiki/Dobble
	:param numberOfSymb: Number of symbols needed on each card.
	:type numberOfSymb: int
	:returns: List of cards which are list of symbols on it.
	:rtype: List[List[int]]
	"""
	nbSymByCard = numberOfSymb
	nbCards = (nbSymByCard**2) - nbSymByCard + 1
	cards = []
	n = nbSymByCard - 1
	t = []
	t.append([[(i+1)+(j*n) for i in range(n)] for j in range(n)])
	for ti in range(n-1):
	  t.append([[t[0][((ti+1)*i) % n][(j+i) % n] for i in range(n)] for j in range(n)])
	t.append([[t[0][i][j] for i in range(n)] for j in range(n)])
	for i in range(n):
	  t[0][i].append(nbCards - n)
	  t[n][i].append(nbCards - n + 1)
	  for ti in range(n-1):
	    t[ti+1][i].append(nbCards - n + 1 + ti + 1)
	t.append([[(i+(nbCards-n)) for i in range(nbSymByCard)]])
	for ti in t:
	  cards = cards + ti
	return cards

def get_image_size(fname):
    """
	Determine the image type of fhandle and return its size. From draco
	Code copied from https://stackoverflow.com/a/20380514 and made by https://stackoverflow.com/users/2372270/fred-the-fantastic
	:param fname: Name of the file to open with the path.
	:type fname: string
	:returns: Width and height of the image.
	:rtype: int, int.
	"""
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def distanceBetweenTwoPoints(a, b):
	"""
	Gives the distance between two points on a 2D grid.
	:param a: Tuple of the first point with a X and Y coordinate.
	:type a: List
	:param b: Same as a.
	:type b: List
	:returns: Distance between those points.
	:rtype: Float or int depending of the type of the coordinates.
	"""
	return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

def collisionBetweenTwoSurfaces(r1_ul, r1_lr, r2_ul, r2_lr):
	"""
	Check wheter two rectangles are colliding.
	:param r1_ul: Point of the upper left corner of the first rectangle.
	:param r1_lr: Point of the lower right corner of the first rectangle.
	:param r2_ul: Point of the upper left corner of the second rectangle.
	:param r2_lr: Point of the lower right corner of the second rectangle.
	:returns: Boolean telling if the rectangles are colliding.
	:rtype: Boolean
	"""
	return not (r2_ul[0] > r1_lr[0] or r2_lr[0] < r1_ul[0] or r2_ul[1] > r1_lr[1] or r2_lr[1] < r1_ul[1])
	
""" Number of symbols on each card. """
numberOfSymb = 5

""" Size of a Dobble card in mm. """
docX = 100
docY = docX

""" Ratio to reduce symbols size. """
surfaceReduction = 4

circleRadius = round(docX / 2) - 1
circleArea = round(pi * circleRadius * circleRadius)
circleCenter = (docX/2, docY/2)

""" Area allocated to a symbol. """
imgArea = round(circleArea / (numberOfSymb*surfaceReduction))

""" Retrieves symbols needed on each card. """
cardsList = generateCards(numberOfSymb)

cardNbr = 0

while cardNbr < len(cardsList):

	""" Retrieves list of symbols to put on current image. """
	imagesToAdd = cardsList[cardNbr]

	""" Prepares the SVG file. """
	cardSVG = svgwrite.drawing.Drawing("svg/{}.svg".format(cardNbr), size=("{}mm".format(docX), "{}mm".format(docY)), viewBox="0 0 {} {}".format(docX, docY))

	""" Draws a circle on the SVG. """
	circleBorder = svgwrite.shapes.Circle(center = (circleCenter[0], circleCenter[1]), r = circleRadius, fill = "white", stroke = "black", stroke_width = 1)
	cardSVG.add(circleBorder)

	""" List which will store tuples of each symbol upper left and lower right corner. Each of these corners are also tuples with X and Y coordinates. """
	imgList = []

	for i in imagesToAdd:
		""" For each symbol on the current card. """

		""" Number of tries for placing the current symbol. """
		triesNumber = 0

		imgPath = "img/{}.png".format(i)
		imgSize = get_image_size(imgPath)

		aspectRatio = imgSize[0] / imgSize[1]
		y = sqrt(imgArea/aspectRatio)
		x = aspectRatio * y

		""" Getting a random upscaling (or downscaling) ratio to be applied to the current symbol, from 80% to 120%. """
		upscale = randint(80, 120) / 100

		""" Sizes of the symbol on the SVG. """
		x = round(x*upscale)
		y = round(y*upscale)

		""" Defining default corners and a collision boolean to True to enter the checking loop once. """
		corner_ul = (-1,-1)
		corner_ur = corner_ul
		corner_ll = corner_ul
		corner_lr = corner_ul

		collision = True

		while distanceBetweenTwoPoints(corner_ul, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_ur, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_ll, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_lr, circleCenter) >= circleRadius or collision == True:
			"""
			This loop tries to put the current symbol on the card, and checks for whether there is a collision with a symbol already in place or if the symbol is out of bounds.
			If the symbol isn't well placed, it loops again.
			distanceBetweenTwoPoints(corner_ul, circleCenter) >= circleRadius: if the symbol is in the lower right part of the SVG and outside the circle.
			distanceBetweenTwoPoints(corner_ur, circleCenter) >= circleRadius: if the symbol is in the lower left part of the SVG and outside the circle.
			distanceBetweenTwoPoints(corner_ll, circleCenter) >= circleRadius: if the symbol is in the upper right part of the SVG and outside the circle.
			distanceBetweenTwoPoints(corner_lr, circleCenter) >= circleRadius: if the symbol is in the upper left part of the SVG and outside the circle.
			collision == True: if the symbol collides with another one.
			"""
			
			""" Thoses are the maximum coordinates for the upper left corner (with SVG Y = 0 is at the top) of the symbol based on its size.
			It assures the symbol will be entirely in the SVG. """
			maxX = docX - x
			maxY = docY - y
			
			""" We find a random position on the SVG for upper left corner of the symbol, and extrapolates the other 3 coordinates from it. """
			corner_ul = (randint(0, maxX), randint(0, maxY))
			corner_ur = (corner_ul[0]+x, corner_ul[1])
			corner_ll = (corner_ul[0], corner_ul[1]+y)
			corner_lr = (corner_ul[0]+x, corner_ul[1]+y)

			""" We reset the collision boolean. """
			collision = False


			for val in imgList:
				""" Checking each already placed symbol. """
				if collisionBetweenTwoSurfaces(corner_ul, corner_lr, val[0], val[1]):
					""" If there is a collision, we break the current for, sets the collision flag to True so it'll retry for the current symbol. """
					collision = True
					break
			
			""" We increase the tries counter and if it exceeds a certain constant we stop trying to put the symbol. """
			triesNumber += 1
			if triesNumber > numberOfSymb**2:
				break

		""" If we stopped trying the current symbol, we just stop trying other symbols, and decrease the card counter so we will retry it next round. """
		if triesNumber > numberOfSymb**2:
			cardNbr -= 1
			break

		""" Whether the symbol was successfully put or not, we find its center coordinate and rotate it randomly. Collsion may occur now but it'll be subtle. """
		imgCenter = (corner_ul[0] + x/2, corner_ul[1] + y/2)
		imgRotation = randint(0, 359)

		""" We add the new symbol to the list of approved symbols. """
		imgList.append((corner_ul, corner_lr))

		""" We add the symbol to the SVG. """
		image = svgwrite.image.Image("../{}".format(imgPath), insert = (corner_ul[0], corner_ul[1]), size = (x, y))
		image.rotate(imgRotation, imgCenter)
		cardSVG.add(image)

	""" We save the SVG even if it was a failure.
		Also, the card counter is always increased as if the card was a success, we will try the next card, and if it was a failure we will retry the same card because we previously decreased it. """
	cardSVG.save()
	cardNbr += 1

print("Success!")
