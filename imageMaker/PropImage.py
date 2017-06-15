from PIL import Image
from collections import Counter
from dustmaker import Prop
import imageMaker.PropConstants as Group
import copy

MAX_PROP_SIZE = 5
LOWEST_LAYER = 12
LOWEST_SUBLAYER = 0
SUBLAYERS = 25
#The numbers of sublayers available from 12-0 to 17-24
MAX_COLORS = 150
#A default box prop
PROP = Prop(0, 0, True, True, 1, *Group.STORAGE, 4, 0)
#Temporary position constants until I start using PropUtils
SPACE_FACTOR = 1.2
X_OFFSET_FACTOR = 0.6
Y_OFFSET_FACTOR = 0.9

class PropImage(object):
    def __init__(self, file_name):
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

        # make sure there arent too many colors
        assert len(self.colors) <= MAX_COLORS

        # pixel data
        self.size = img.size
        width, height = img.size

        self._pixel_data = [(i%width, i//width, self.colors.index(color), 1) for i, color in enumerate(data)]

        # map data
        self.x = 0
        self.y = 0

        #With the current constant-based implementation, the prop type must be fixed
        #PropUtils could fix this?
        self._prop = copy.deepcopy(PROP)

    @property
    def prop_size(self):
        return self._prop.scale

    @prop_size.setter
    def prop_size(self, size):
        self._prop.scale = size

    def compress(self):
        """builds larger colored regions that can be covered with a single prop
        
        takes advantage of the fact that the colors are ordered by frequency to place the most common
        colors on bottom layers.
        
        temp data is a list of (color_index, size) tuples
        stores compressed (x, y, color_index, size) tuples
        """
        width, height = self.size
        self._pixel_data = []

        for index, color in enumerate(self.colors):
            temp_data = []
            for pixel in self._image.getdata():
                i = self.colors.index(pixel)
                if i < index:
                    i = 0 # This pixel is below the current layer and must not be covered
                elif i == index:
                    i = 1 # This pixel is on the current layer and must be covered
                else:
                    i = 2 # This pixel is on a higher layer, and it doesnt matter
                temp_data.append([i, 1]) # assigns each pixel an initial group size of 1

            #compresses the current color
            self._compress(temp_data)

            #separates the data by row, and draws it
            for row in (temp_data[start:(start+width)] for start in range(0,width*height,width)):
                for type, size in (row[i] for i in range(len(row))):
                    #ternary operators!
                    print('_ ' if size == 0 or type != 1 else '%02d'%size,end="")
                print()
            print()

            for pos, (i, size) in enumerate(temp_data):
                if i == 1 and size > 0:
                    self._pixel_data.append((pos%width, pos//width, index, size))

    def _compress(self, data, size=1):
        """A bad compression algorithm.
        groups tiles into squares of the same color,
        and recursively doubles the size of the square
        """
        width, height = self.size
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

        #The larger the props, the fuzzier the edges. prevents over-fuzzing
        if repeat and size*4*self.prop_size < MAX_PROP_SIZE:
            self._compress(data, size * 2)

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
        spacing = self._prop.scale * SPACE_FACTOR

        for pixel_x, pixel_y, color_index, size in self._pixel_data:
            layer = (base + color_index) // SUBLAYERS
            sub = (base + color_index) % SUBLAYERS

            x = self.x + (pixel_x)*spacing
            y = self.y + (pixel_y)*spacing
            prop = copy.deepcopy(self._prop)
            prop.layer_sub = sub
            prop.scale *= size

            x_offset = prop.scale*X_OFFSET_FACTOR
            y_offset = prop.scale*Y_OFFSET_FACTOR
            x -= x_offset
            y -= y_offset

            map.add_prop(layer, x, y, prop)