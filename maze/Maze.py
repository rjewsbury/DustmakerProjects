from dustmaker import Map, Tile, TileSide
from dustmaker.Entity import EnemyHeavyPrism, LevelEnd
from dustmaker.Var import Var, VarType
from random import choice


class Maze(Map):
    """ Represents a Dustforce maze map
        
        cell numbers are zero-indexed and measured from the top left-corner
        
        maze.width  - the number of maze cells wide the maze will be
        maze.height - the number of maze cells tall the maze will be
        maze.start_cell - the cell the player spawns in
        maze.end_cell   - the cell the end trigger spawns in
    """

    def __init__(self, width=20, height=10):
        super().__init__()
        self.width = width
        self.height = height
        self.cell_size = 3
        self.wall_size = 1
        self.base_x = 0
        self.base_y = 0
        self._start_cell = [(0, 0)] * 4
        self._end_cell = (width - 1, height - 1)
        self._cell_entities = []

    def _generate_walls_kruskal(self):
        """ Generates the set of walls to be placed in the interior of the maze randomly
            uses a randomized Kruskal's algorithm
        """
        # each cell has its own group initially
        # yes, I did just make a matrix of sets of tuples
        groups = [[{(x, y)} for x in range(self.width)] for y in range(self.height)]
        # walls are placed half way between cells
        unchecked = [(x, y + .5) for x in range(self.width) for y in range(self.height - 1)]
        unchecked += [(x + .5, y) for x in range(self.width - 1) for y in range(self.height)]
        # make a shallow copy so that we can track which walls to keep
        walls = unchecked[:]

        # check every wall
        while len(unchecked) > 0:
            # choose a random unchecked wall
            wall = choice(unchecked)
            # mark the wall as checked
            unchecked.remove(wall)
            # get the coordinates of the wall
            x1 = x2 = wall[0]
            y1 = y2 = wall[1]
            # get the coordinates of the cells on either side of the wall
            if wall[0] % 1 == 0:
                y1 = int(y1 - 0.5)
                y2 = int(y2 + 0.5)
            else:
                x1 = int(x1 - 0.5)
                x2 = int(x2 + 0.5)

            # if the walls are in different groups...
            if not (x2, y2) in groups[y1][x1]:
                # merge groups
                groups[y1][x1].update(groups[y2][x2])
                # unfortunately this is the only way I can come up with to get every
                # cell to reference the same set. seems really inefficient
                for x, y in groups[y2][x2]:
                    groups[y][x] = groups[y1][x1]
                # remove the wall
                walls.remove(wall)

        return walls

    def _place_intersections(self, tile_function):
        for cell_x in range(1, self.width):
            for cell_y in range(1, self.height):
                for dx in range(self.wall_size):
                    for dy in range(self.wall_size):
                        x = self.base_x + cell_x * (self.cell_size + self.wall_size) + dx
                        y = self.base_y + cell_y * (self.cell_size + self.wall_size) + dy
                        tile_function(x, y)

    def _place_border(self, tile_function):
        for dx in range(self.width * (self.cell_size + self.wall_size) + self.wall_size):
            for dy in range(self.wall_size):
                x = self.base_x + dx
                y = self.base_y + dy
                tile_function(x, y)

                y += self.height * (self.cell_size + self.wall_size)
                tile_function(x, y)

        for dy in range(self.wall_size, self.height * (self.cell_size + self.wall_size)):
            for dx in range(self.wall_size):
                x = self.base_x + dx
                y = self.base_y + dy
                tile_function(x, y)

                x += self.width * (self.cell_size + self.wall_size)
                tile_function(x, y)

    def _place_walls(self, tile_function):
        for cell_x, cell_y in self._generate_walls_kruskal():
            if cell_x % 1 == 0:
                width, height = self.cell_size, self.wall_size
                cell_x = self.base_x + self.wall_size + cell_x * (self.cell_size + self.wall_size)
                cell_y = int(cell_y + 0.5)
                cell_y = self.base_y + cell_y * (self.cell_size + self.wall_size)
            else:
                width, height = self.wall_size, self.cell_size
                cell_x = int(cell_x + 0.5)
                cell_x = self.base_x + cell_x * (self.cell_size + self.wall_size)
                cell_y = self.base_x + self.wall_size + cell_y * (self.cell_size + self.wall_size)
            for dx in range(width):
                for dy in range(height):
                    x = cell_x + dx
                    y = cell_y + dy
                    tile_function(x, y)

    def _place_background(self):
        x_range = range(self.width * (self.cell_size+self.wall_size) + self.wall_size)
        y_range = range(self.height * (self.cell_size+self.wall_size) + self.wall_size)
        for dx in x_range:
            for dy in y_range:
                tile = Tile(0)
                if not dx == 0:
                    tile.edge_bits(TileSide.LEFT, 0x0)
                if not dy == 0:
                    tile.edge_bits(TileSide.TOP, 0x0)
                if not dx == len(x_range)-1:
                    tile.edge_bits(TileSide.RIGHT, 0x0)
                if not dy == len(y_range)-1:
                    tile.edge_bits(TileSide.BOTTOM, 0x0)
                self.add_tile(17, self.base_x + dx, self.base_y + dy, tile)

    def start_cell(self, x = None, y = None, player=1):
        """Returns the starting cell of the player as an (x,y) tuple
            
            cell    - if not None, sets the starting cell
            player  - the player ID to get the cell of
        """
        current = self._start_cell[player]
        if x != None and y != None:
            self._start_cell[player] = (x, y)
        return current

    def end_cell(self, x = None, y = None):
        current = self._end_cell
        if x != None and y != None:
            self._end_cell = (x, y)
        return current

    def add_cell_entity(self, cell, entity):
        """ Stores an entity to be added to a cell 
  
            cell    - the (x,y) tuple describing the cell
            entity - The Entity object to add to the map.
        """
        x, y = cell
        self._cell_entities.append((x, y, entity))

    def build_maze(self):
        # place tiles
        def tile_function(x_pos, y_pos):
            tile = Tile(0)
            if(x_pos+y_pos) % 2 == 0:
                tile.sprite_palette(1)
                self.add_tile(20, x_pos, y_pos, tile)
            self.add_tile(19, x_pos, y_pos, tile)

        self._place_intersections(tile_function)
        self._place_border(tile_function)
        self._place_walls(tile_function)
        self._place_background()

        # place start and end
        for i,cell in enumerate(self._start_cell):
            x = self.base_x + (cell[0]+1) * (self.cell_size + self.wall_size) - self.cell_size/2
            y = self.base_y + (cell[1]+1) * (self.cell_size + self.wall_size)
            self.start_position((x,y),i)

        x = self.base_x + (self._end_cell[0]+1) * (self.cell_size + self.wall_size) - self.cell_size / 2
        y = self.base_y + (self._end_cell[1]+1) * (self.cell_size + self.wall_size) - self.cell_size / 2
        entity = EnemyHeavyPrism()

        id = self.add_entity(x, y, entity)
        ent_list = {'ent_list':Var(VarType.ARRAY, (VarType.UINT, [Var (VarType.UINT, id)]))}

        self.add_entity(x, y, LevelEnd(ent_list))

        for cell_x, cell_y, entity in self._cell_entities:
            x = self.base_x + (cell_x + 1) * (self.cell_size + self.wall_size) - self.cell_size / 2
            y = self.base_y + (cell_y + 1) * (self.cell_size + self.wall_size) - self.cell_size / 2
            self.add_entity(x, y, entity)