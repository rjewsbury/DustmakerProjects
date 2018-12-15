from PIL import Image
from collections import Counter
from dustmaker import Prop
import imageMaker.PropConstants as Group
import copy
import PropUtils

LOWEST_LAYER = 12
LOWEST_SUBLAYER = 0
SUBLAYERS = 25
# The numbers of sublayers available from 12-0 to 17-24
MAX_COLORS = 150
# SCALED PROPS ARE HORRIBLE TO WORK WITH SO THE SCALE IS FIXED FOR NOW
SCALE = 0.06
SPACING = 4 / 48
MAX_SIZE = 128
# Quick attempt to make the following array more readable
ARGS = (0, 0, True, True)
# An array of arrays of (dx,dy,prop) tuples to build squares of different sizes
PROPS = [None for i in range(129)]
PROPS[1] = [(0, 0, Prop(*ARGS, SCALE, *Group.STORAGE, 4, 0))]
PROPS[2] = [(-2 / 48, -3 / 48, Prop(*ARGS, 0.13, *Group.STORAGE, 4, 0))] # 0.141
PROPS[4] = [(-6 / 48, -9 / 48, Prop(*ARGS, 0.271, *Group.STORAGE, 4, 0))]
PROPS[8] = [(-14 / 48, -22 / 48, Prop(*ARGS, 0.521, *Group.STORAGE, 4, 0))]
PROPS[16] = [(-30 / 48, -46 / 48, Prop(*ARGS, 1.000, *Group.STORAGE, 4, 0))]

PROPS[32] = [(-55 / 48, 11 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0)),
             (-55 / 48, -29 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0)),
             (-55 / 48, -57 / 48, Prop(*ARGS, 0.442, *Group.BACKDROP, 6, 0))]

PROPS[64] = [(-168 / 48, -159 / 48, Prop(*ARGS, 0.721, *Group.BACKDROP2, 7, 0)),
             (-168 / 48, -35 / 48, Prop(*ARGS, 0.721, *Group.BACKDROP2, 7, 0))]

PROPS[128] = [(-823 / 48, -558 / 48, Prop(*ARGS, 1.919, *Group.MACHINERY, 14, 0)),
              (-275 / 48, -58 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0)),
              (-275 / 48, -269 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0)),
              (-275 / 48, -358 / 48, Prop(*ARGS, 1.177, *Group.BACKDROP2, 7, 0))]


def _compress(image_size, data, size=1):
    """A bad compression algorithm.
    groups tiles into squares of the same color,
    and recursively doubles the size of the square
    """
    width, height = image_size
    repeat = False
    for y in range(size * 2 - 1, height, size * 2):
        for x in range(size * 2 - 1, width, size * 2):
            SE = data[y * width + x]
            SW = data[y * width + (x - size)]
            NE = data[(y - size) * width + x]
            NW = data[(y - size) * width + (x - size)]

            # none of the colors are below the current color, and all cells are the same size
            # if the cells are not the same size, one of them failed the previous iteration
            if min([SE[0], SW[0], NE[0], NW[0]]) is not 0 and SW[1] == SE[1] == NW[1] == NE[1]:
                SE[0] = min([SE[0], SW[0], NE[0], NW[0]])
                SE[1] = SE[1] * 2
                SW[1] = 0
                NE[1] = 0
                NW[1] = 0
                repeat = True

    # The larger the props, the fuzzier the edges. prevents over-fuzzing
    if repeat and size * 2 < MAX_SIZE:
        _compress(image_size, data, size * 2)


def _outline(image_size, data, size=1):
    width, height = image_size
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            Pixel = data[y*width + x]
            N = data[(y - 1) * width + x]
            E = data[y * width + x + 1]
            S = data[(y + 1) * width + x]
            W = data[y * width + x - 1]
            NE = data[(y - 1) * width + x + 1]
            NW = data[(y - 1) * width + x - 1]
            SE = data[(y + 1) * width + x + 1]
            SW = data[(y + 1) * width + x - 1]

            if Pixel[0] == 1 and N[0] and E[0] and S[0] and W[0] and NE[0] and NW[0] and\
                            SE[0] and SW[0] :
                data[y * width + x][1] = 0

class PropImage(object):
    def __init__(self, file_name, *_, transparency = None):
        """loads image data from the given file

        Public Attributes:
        colors = a list of RGB tuples sorted by descending frequency in the image
        size = a (width, height) tuple
        x, y = the coordinates of the upper left corner
        """

        # load image as a pixel list
        img = Image.open(file_name)
        img = img.convert("RGB")
        self._image = img
        data = list(img.getdata())

        # get a list of unique colors sorted by frequency.
        color_count = Counter(data)
        self.colors = sorted(list(color_count), key=color_count.get, reverse=True)
        if transparency is not None:
            try:
                self.colors.remove(transparency)
            except ValueError:
                print('transparent color',transparency,'not found in',file_name)
        self.transparency = transparency

        # make sure there arent too many colors
        assert len(self.colors) <= MAX_COLORS

        # pixel data
        self.size = img.size

        #the image should originally be uncompressed
        self.uncompress()

        # map data
        self.x = 0
        self.y = 0

        # With the current constant-based implementation, the prop type must be fixed
        # PropUtils could fix this?
        # Update: PropUtils is great, but not precise enough for this.

    def uncompress(self):
        self._pixel_data = []
        width, _ = self.size
        for i, color in enumerate(list(self._image.getdata())):
            if color != self.transparency:
                self._pixel_data.append((i%width, i//width, self.colors.index(color),1))

    def compress(self, algorithm=_compress):
        """builds larger colored regions that can be covered with a single prop

        takes advantage of the fact that the colors are ordered by frequency to place the most common
        colors on bottom layers.

        temp data is a list of (color_index, size) tuples
        stores compressed (x, y, color_index, size) tuples
        """
        width, height = self.size
        self._pixel_data = []

        for index, color in enumerate(self.colors):
            #print(index, color)
            temp_data = []
            for pixel in self._image.getdata():
                if pixel == self.transparency:
                    i = 0
                else:
                    i = self.colors.index(pixel)
                    if i < index:
                        i = 0  # This pixel is below the current layer and must not be covered
                    elif i == index:
                        i = 1  # This pixel is on the current layer and must be covered
                    else:
                        i = 2  # This pixel is on a higher layer, and it doesnt matter
                temp_data.append([i, 1])  # assigns each pixel an initial group size of 1

            # compresses the current color
            algorithm(self.size, temp_data)

            # separates the data by row, and draws it
            '''
            for row in (temp_data[start:(start + width)] for start in range(0, width * height, width)):
                for type, size in (row[i] for i in range(len(row))):
                    # ternary operators!
                    print('_ ' if size == 0 or type != 1 else '%02d' % size, end="")
                print()
            print()
            '''

            for pos, (i, size) in enumerate(temp_data):
                if i == 1 and size > 0:
                    self._pixel_data.append((pos % width, pos // width, index, size))

    def build_image(self, map, fog, layer=LOWEST_LAYER, sublayer=LOWEST_SUBLAYER):
        # map = a Dustmaker Map
        # fog = a BetterFogTrigger

        self._adjust_fog(fog, layer, sublayer)
        self._place_props(map, layer, sublayer)

    def _adjust_fog(self, fog, base_layer=LOWEST_LAYER, sublayer=LOWEST_SUBLAYER):
        # fog = a BetterFogTrigger
        base = SUBLAYERS * base_layer + sublayer
        # sets the colors
        for i, color in enumerate(self.colors):
            layer = (base + i) // SUBLAYERS
            sub = (base + i) % SUBLAYERS
            fog.set_color(color, 1.0, layer, sub)

    def _place_props(self, map, base_layer=LOWEST_LAYER, sublayer=LOWEST_SUBLAYER):
        """places sscaled props according to the pixel data
        DOES NOT WORK PERFECTLY ON COMPRESSED DATA
        currently being worked on
        """
        base = SUBLAYERS * base_layer + sublayer
        spacing = SPACING

        for pixel_x, pixel_y, color_index, size in self._pixel_data:
            layer = (base + color_index) // SUBLAYERS
            sub = (base + color_index) % SUBLAYERS

            #add an offset to avoid rounding problems
            #THERES A BUG WHERE IMAGES THAT CROSS THE 0 AXIS CHANGE HOW THEY ROUND
            x = self.x + (pixel_x) * spacing + 0.1/48
            y = self.y + (pixel_y) * spacing + 0.1/48

            for dx, dy, base_prop in PROPS[size]:
                prop = copy.deepcopy(base_prop)
                prop.layer_sub = sub
                map.add_prop(layer, x+dx, y+dy, prop)