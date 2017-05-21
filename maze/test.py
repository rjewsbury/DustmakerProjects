#that's a lot of things named maze
from maze.Maze import Maze
from dustmaker import MapWriter, Var, VarType
from dustmaker.Entity import Entity, FogTrigger, Apple, EnemyGargoyleSmall, AIController
import random

wall_r = int(random.uniform(0x80, 0xFF))
wall_g = int(random.uniform(0x80, 0xFF))
wall_b = int(random.uniform(0x80, 0xFF))
wall_primary = 0xFF000000 + 0x10000*wall_r + 0x100*wall_g + 0x1* wall_b
wall_secondary = 0xFF000000 + 0x10000*(wall_r//2) + 0x100*(wall_g//2) + 0x1* (wall_b//2)
wall_back = 0xFF000000 + 0x10000*(wall_r//4) + 0x100*(wall_g//4) + 0x1* (wall_b//4)
#print('%02x %02x %02x' % (wall_r, wall_g, wall_b))
#print('%02x %02x %02x' % (wall_r//2, wall_g//2, wall_b//2))
#print('%02x %02x %02x' % (wall_r//4, wall_g//4, wall_b//4))

player_base = wall_primary
back_center = wall_secondary
back_edge = wall_back

# player_r = int(random.uniform(0x80, 0xFF))
# player_g = int(random.uniform(0x80, 0xFF))
# player_b = int(random.uniform(0x80, 0xFF))
# player_base = 0xFF000000 + 0x10000*player_r + 0x100*player_g + 0x1* player_b
# back_center = 0xFF000000 + 0x10000*(player_r//2) + 0x100*(player_g//2) + 0x1* (player_b//2)
# back_edge = 0xFF000000 + 0x10000*(player_r//4) + 0x100*(player_g//4) + 0x1* (player_b//4)

fog_vars = {'fog_colour': Var(VarType.ARRAY,
                              (VarType.UINT,
                               [Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, 0xFF000000),
                                Var(VarType.UINT, wall_back),
                                Var(VarType.UINT, player_base),
                                Var(VarType.UINT, wall_primary),
                                Var(VarType.UINT, wall_secondary)])),
            'fog_per': Var(VarType.ARRAY,
                           (VarType.FLOAT,
                            [Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 0.0),
                             Var(VarType.FLOAT, 1.0),
                             Var(VarType.FLOAT, 1.0),
                             Var(VarType.FLOAT, 1.0),
                             Var(VarType.FLOAT, 1.0)])),
            'fog_per_test': Var(VarType.ARRAY,
                                (VarType.FLOAT, [])),
            'fog_speed': Var(VarType.FLOAT, 0.0),   #not sure what fog speed to use, or if it matters
            'gradient': Var(VarType.ARRAY,
                            (VarType.UINT,
                             [Var(VarType.UINT, back_edge),
                              Var(VarType.UINT, back_center),
                              Var(VarType.UINT, back_edge)])),
            'gradient_middle': Var(VarType.FLOAT, 0.5),
            'has_sub_layers': Var(VarType.BOOL, False),
            'sound_ambience_names': Var(VarType.ARRAY,(VarType.STRING, [])),
            'sound_ambience_vol': Var(VarType.ARRAY, (VarType.FLOAT, [])),
            'sound_music_names': Var(VarType.ARRAY, (VarType.STRING, [])),
            'sound_music_vol': Var(VarType.ARRAY, (VarType.FLOAT, [])),
            'star_bottom': Var(VarType.FLOAT, 0.0),
            'star_middle': Var(VarType.FLOAT, 0.0),
            'star_top': Var(VarType.FLOAT, 0.0),
            'width': Var(VarType.INT, 500)}

music_vars = {'music_speed': Var (VarType.FLOAT, 5.0),
              'sound_music_names': Var (VarType.ARRAY,
                                        (VarType.STRING,
                                         [Var (VarType.STRING, '9-bit Expedition')])),
              'sound_music_vol': Var (VarType.ARRAY,
                                      (VarType.FLOAT,
                                       [Var (VarType.FLOAT, 1.0)])),
              'width': Var (VarType.INT, 500)}

f1 = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/temp_maze"

maze = Maze(10,10)
maze.cell_size = 4
maze.wall_size = 2

maze.add_cell_entity((maze.width//2,maze.height//2),Apple())
maze.add_cell_entity(maze.start_cell(), FogTrigger(fog_vars, 0, 22))

music = Entity(music_vars, 0, 22)
music.type = 'music_trigger'
maze.add_cell_entity(maze.start_cell(), music)

for x in range(0,10):
    for y in range(1-x%2, 10, 2):
        maze.add_cell_entity((x, y), EnemyGargoyleSmall())

maze.build_maze()

#make a shallow copy to avoid 'changed size during iteration'
entities = maze.entities.copy()
for key in entities:
    if isinstance(maze.get_entity(key), EnemyGargoyleSmall):
        x = maze.get_entity_xposition(key)
        y = maze.get_entity_yposition(key)
        ai_vars = {'nodes': Var(VarType.ARRAY,
                                (VarType.VEC2,
                                 [Var(VarType.VEC2, (x*48, y*48))])),
                   'nodes_wait_time': Var(VarType.ARRAY,
                                          (VarType.INT,
                                           [Var(VarType.INT, 0)])),
                   'puppet_id': Var(VarType.UINT, key)}
        ai = AIController(ai_vars, 0, 18, 1, 1, 1)
        maze.add_entity(x, y, ai)

with open(f1, "wb") as f:
    f.write(MapWriter.write_map(maze))