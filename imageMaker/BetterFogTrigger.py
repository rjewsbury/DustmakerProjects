from dustmaker import *
from dustmaker.Entity import FogTrigger
import copy


def rgb_to_hex(red, green, blue):
    # converts an r, g, b triplet to an ARGB hex code
    return 0xFF000000 + 0x10000 * red + 0x100 * green + 0x1 * blue


def hsv_to_rgb(hue, sat, val):
    # Voodoo magic to convert HSV values to RGB values
    # saturation and value must be percentages from 0.0 to 1.0
    hue %= 360
    # main value
    max = sat * val
    # remaining value
    rem = (1 - abs((hue / 60) % 2 - 1))

    r, g, b = 0, 0, 0
    if 0 <= hue < 60:
        r, g, b = max, rem, 0
    elif 60 <= hue < 120:
        r, g, b = rem, max, 0
    elif 120 <= hue < 180:
        r, g, b = 0, max, rem
    elif 180 <= hue < 240:
        r, g, b = 0, rem, max
    elif 240 <= hue < 300:
        r, g, b = rem, 0, max
    elif 300 <= hue < 360:
        r, g, b = max, 0, rem

    return (int(r * 0xFF), int(g * 0xFF), int(b * 0xFF))


class BetterFogTrigger(FogTrigger):
    def __init__(self, fog_trigger=None):
        """Creates a new blank sublayer fog trigger.
        Default Color values are all black
        Default Intensity values are all 0.0
        Default Sky Color is all black
        Default Fog Speed is 1.0 (whatever that means)
        Default Star Opacity is 0.5
        """
        if fog_trigger is not None:
            assert isinstance(fog_trigger, FogTrigger)
            super().__init__(None, fog_trigger.rotation, fog_trigger.layer,
                           fog_trigger.unk2, fog_trigger.unk3, fog_trigger.unk4)
            self.vars = copy.deepcopy(fog_trigger.vars)
            self._colors = self.vars.get('fog_colour').value[1]
            self._intensity = self.vars.get('fog_per').value[1]
            self._gradient = self.vars.get('gradient').value[1]
        else:
            super().__init__(None, 0, 22)
            self._colors = [Var(VarType.UINT, 0xFF000000) for i in range(567)]
            self._intensity = [Var(VarType.FLOAT, 0.0) for i in range(567)]
            self._gradient = [Var(VarType.UINT, 0xFF000000) for i in range(3)]

            fog_vars = {'fog_colour': Var(VarType.ARRAY,
                                          (VarType.UINT,
                                           self._colors)),
                        'fog_per': Var(VarType.ARRAY,
                                       (VarType.FLOAT,
                                        self._intensity)),
                        'fog_per_test': Var(VarType.ARRAY, (VarType.FLOAT, [])),
                        'fog_speed': Var(VarType.FLOAT, 1.0),
                        'gradient': Var(VarType.ARRAY,
                                        (VarType.UINT,
                                         self._gradient)),
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

            # setting the vars outside of the super constructor avoids the deep copy, so I can change things
            self.vars = fog_vars

    def set_color(self, color=None, intensity=None, layer=1, sub=-1):
        """ Sets the color and intensity of a sublayer
        
        :param layer: the layer for the new color. in range 1 to 20
        :param sub: the sublayer for the new color. -1 is the base sublayer. from -1 to 25
        :param color: an RGB triplet (R,G,B). if None, the existing color is kept
        :param intensity: a percentage intensity from 0.0 to 1.0. if None, the existing intensity is kept
        """
        if color is not None:
            # unpacks the color tuple to generate a hex, then stores it at the correct sublayer
            self._colors[layer + 21 * sub + 21].value = rgb_to_hex(*color)
        if intensity is not None:
            self._intensity[layer + 21 * sub + 21].value = intensity

    def set_gradient(self, upper=None, middle=None, lower=None):
        """Sets the color of the sky.
        Each section is given as an RGB triple.
        If a section is None, the existing color is used
        """
        if upper is not None:
            self._gradient[0].value = rgb_to_hex(*upper)
        if middle is not None:
            self._gradient[1].value = rgb_to_hex(*middle)
        if lower is not None:
            self._gradient[2].value = rgb_to_hex(*lower)
