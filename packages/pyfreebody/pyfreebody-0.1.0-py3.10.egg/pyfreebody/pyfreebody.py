from random import randint
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime
import enum


class Body:
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
        self.forces = []
class Force:
    def __init__(self, name, magnitude, theta):
        self.name = name
        self.magnitude = magnitude
        self.theta = theta

class Direction(enum.Enum):
    up = math.pi /2
    down = (3 * math.pi) / 2
    left = math.pi
    right = 0


class Freebody:


    def __init__ (self,name="empty", mass=24):
        body = Body(name, mass)
        self.body = body

    def addForce(self, name, magnitude, theta):
        self.body.forces.append(Force(name, magnitude, theta.value))


    def diagram(self):

        img  = Image.new( mode = "RGB", size = (size, size), color = (225,225,225))
        canvas = ImageDraw.Draw(img)

        mean = 0
        for force in self.body.forces:
            mean+=force.magnitude

        mean /= len(self.body.forces)
        print(mean)
        i=0
        print(self.body.forces)
        for force in self.body.forces:
            color = randomColor()
            force.prop =  force.magnitude / mean
            CreatArrow(canvas, force, color)
            ForceLegend(canvas, force, i, color)

            i+=1

        #TODO optional shapes
        canvas.rectangle(((center*0.8, center*0.8), (center*1.2, center*1.2)), outline = black, fill = black)

        masstxt  = str(self.body.mass) + "kg"
        mtsw, mtsh = canvas.textsize(masstxt, font = font)
        canvas.text((center-(mtsw/2), center), masstxt, font = font)

        canvas.text((10,size-30), str(self.body.name), fill = black, font = font)

        now = datetime.now()
        dtstr = now.strftime("%d-%m-%Y %H:%M:%S")
        path = "pyfreebody-"+self.body.name+".png"
        img.save(path)
        return path
    #    img.show()

size = 600
arrowHeadSize = 15
cw = 400 * 0.1
center = size / 2;
rectW = size * 0.4

black = (0,0,0)

font = ImageFont.truetype("/usr/share/fonts/noto/NotoSans-Regular.ttf", 20)

def randomColor():
    return (randint(0, 180),
          randint(0, 180),
          randint(0, 180))

def ArrowCordinates(force):
    theta = force.theta
    print(force.prop)
    m = force.prop * 100
    m+=rectW/2
    yc = m * math.sin(theta)
    xc = m * math.cos(theta)
    return ((center, center), (center+ xc, center - yc))


# faulty
def ArrowHeadCordinates(arrowCords):
    x, y = arrowCords[1][0], arrowCords[1][1]
    dx = arrowHeadSize * math.cos(math.pi/4)
    dy = (2 * arrowHeadSize * math.sin(math.pi/4))/2
    print(dx, dy)
    print(x, y)
    return (
        (x-dx, y + dy),
        (x+dx, y - dy),
        (x-arrowHeadSize, y + arrowHeadSize)
    )
def ForceLegend(canvas, force, i, color):
    text = force.name + " Force = " + str(force.magnitude) + "N"
    canvas.text((5,5+i*20), text, fill = color, font = font)

def CreatArrow(canvas, force, color):
    arrowBase = ArrowCordinates(force)
    canvas.line(arrowBase, width=10, fill = color)
    #canvas.polygon(ArrowHeadCordinates(arrowBase), fill = color)
