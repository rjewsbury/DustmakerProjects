import numpy
from dustmaker import Map, Prop

class Circle(object):
    def __init__(self, base_prop, radius=10, prop_spacing=1):
        """A representation of a ring of props
        
        base_prop keeps track of the:
            layer_sub, flip_x, flip_y, scale,
            prop_set, prop_group, prop_index, palette
        for all of the props
        
        prop positions is an array of (dx,dy,rotation) tuples
        """
        self._prop = base_prop
        self._prop_positions = self._generate_positions(radius, prop_spacing)

    def _generate_positions(self, radius, prop_spacing):
        positions = []
        angle = 2 * numpy.arctan2(prop_spacing, 2 * radius)
        total_angle = 0
        # done in two steps to keep things symmetrical about the top-center ray
        while total_angle < numpy.pi:
            dy = float(-numpy.cos(total_angle) * radius)
            dx = float(numpy.sin(total_angle) * radius)
            rotation = int(total_angle * 0x10000 / 2 / numpy.pi)
            positions.append((dx,dy,rotation))
            total_angle += angle
            print(dx, dy, rotation)

        total_angle = 2*numpy.pi - angle
        while total_angle > numpy.pi:
            dy = float(-numpy.cos(total_angle) * radius)
            dx = float(numpy.sin(total_angle) * radius)
            rotation = int(total_angle * 0x10000 / 2 / numpy.pi)
            positions.append((dx, dy, rotation))
            total_angle -= angle
            print(dx, dy, rotation, "bing")
        return positions

    def build_circle(self, map, layer, center_x = 0, center_y = 0):
        for dx, dy, rotation in self._prop_positions:
            #make a copy of the base prop
            prop = Prop(
                self._prop.layer_sub,
                self._prop.rotation + rotation,
                self._prop.flip_x,
                self._prop.flip_y,
                self._prop.scale,
                self._prop.prop_set,
                self._prop.prop_group,
                self._prop.prop_index,
                self._prop.palette)
            #print(center_x+dx, center_y+dy,prop)
            map.add_prop(layer,center_x+dx, center_y+dy,prop)
