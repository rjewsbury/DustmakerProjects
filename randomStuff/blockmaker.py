from dustmaker import *
from imageMaker.BetterFogTrigger import BetterFogTrigger
from PIL import Image
from collections import Counter

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

class BlockImage(object):
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

    def build_image(self, map, fog, layer=LOWEST_LAYER):
        # map = a Dustmaker Map
        # fog = a BetterFogTrigger

        self._adjust_fog(fog, layer)
        self._place(map, layer)

    def _adjust_fog(self, fog, base_layer=LOWEST_LAYER):
        # sets the colors
        for i, color in enumerate(self.colors):
            fog.set_color(color, 1.0, base_layer+i)

    def _place(self, map, base_layer=LOWEST_LAYER):
        """places sscaled props according to the pixel data
        DOES NOT WORK PERFECTLY ON COMPRESSED DATA
        currently being worked on
        """

        for pixel_x, pixel_y, color_index, size in self._pixel_data:
            layer = base_layer+color_index
            map.add_tile(layer,pixel_x,pixel_y,Tile(0))

map_file = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/greed'

with open(map_file, "rb") as f:
    map = read_map(f.read())
map.level_type(LevelType.DUSTMOD)

fog = BetterFogTrigger()

map.add_entity(0,0,fog)

FOLDER = 'C:/Users/Ryley/Documents/Ryleys Documents/Games/Dustforce/Mapmaking/Images/'
img = BlockImage(FOLDER+'greed.png',transparency=(0,0,0))

img.build_image(map,fog,11)

# save map
map.name(map.name() + '_modified')
with open(map_file + "_modified", "wb") as f:
    f.write(write_map(map))