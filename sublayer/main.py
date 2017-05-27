from dustmaker import *
from dustmaker.Entity import FogTrigger
from sublayer.Circle import Circle

f0 = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/rainbow"
with open(f0, "rb") as f:
    map = read_map(f.read())

colors = [Var(VarType.UINT, 0xFF000000) for i in range(567)]
intensity = [Var(VarType.FLOAT, 1.0) for i in range(567)]

def hue_to_rgb(h) -> (int):
    h = h % 360
    x = (1 - abs((h / 60) % 2 - 1))
    r,g,b = 0,0,0
    if 0 <= h < 60:
        r, g, b = 1, x, 0
    elif 60 <= h < 120:
        r, g, b = x, 1, 0
    elif 120 <= h < 180:
        r, g, b = 0, 1, x
    elif 180 <= h < 240:
        r, g, b = 0, x, 1
    elif 240 <= h < 300:
        r, g, b = x, 0, 1
    elif 300 <= h < 360:
        r, g, b = 1, 0, x
    r, g, b = int(r * 0xFF), int(g * 0xFF), int(b * 0xFF)
    return 0xFF000000 + 0x10000 * r + 0x100 * g + 0x1 * b

for i in range(0,300,3):
    layer = (i//3)//25 + 12
    sub = (i//3)%25
    colors[layer + 21*sub + 21].value = hue_to_rgb(i)
    #print(layer, sub, "%02x"%hue_to_rgb(i,1,1))

for i in range(95):
    layer = i//25+12
    sub = i%25
    prop = Prop(sub, 0x330, True, True, 1, 4, 28, 6, 0)
    circ = Circle(prop, 60-0.05*i, 3.2)
    circ.build_circle(map, layer, 0, -10)

sub_fog_vars = {'fog_colour': Var(VarType.ARRAY,
                                  (VarType.UINT,
                                   colors)),
                'fog_per': Var(VarType.ARRAY,
                               (VarType.FLOAT,
                                intensity)),
                'fog_per_test': Var(VarType.ARRAY, (VarType.FLOAT, [])),
                'fog_speed': Var(VarType.FLOAT, 1.0),
                'gradient': Var(VarType.ARRAY,
                                (VarType.UINT,
                                 [Var(VarType.UINT, 4279933878),
                                  Var(VarType.UINT, 4283749873),
                                  Var(VarType.UINT, 4287627243)])),
                'gradient_middle': Var(VarType.FLOAT, 0.5),
                'has_sub_layers': Var(VarType.BOOL, True),
                'sound_ambience_names': Var(VarType.ARRAY,
                                            (VarType.STRING, [])),
                'sound_ambience_vol': Var(VarType.ARRAY, (VarType.FLOAT, [])),
                'sound_music_names': Var(VarType.ARRAY, (VarType.STRING, [])),
                'sound_music_vol': Var(VarType.ARRAY, (VarType.FLOAT, [])),
                'star_bottom': Var(VarType.FLOAT, 0.5),
                'star_middle': Var(VarType.FLOAT, 0.5),
                'star_top': Var(VarType.FLOAT, 0.5),
                'width': Var(VarType.INT, 500)}

map.add_entity(0, 0, FogTrigger(sub_fog_vars, 0, 22))

with open(f0+"_generated", "wb") as f:
    f.write(write_map(map))
