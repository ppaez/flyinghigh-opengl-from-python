from __future__ import division

from itertools import chain
from random import randint

from ..geometry.geometry import Cube
from ..geometry.matrix import Matrix
from ..geometry.orientation import Orientation
from ..geometry.vec3 import Origin, Vec3, XAxis, YAxis, ZAxis


white=(255, 255, 255, 255)


class Shape(object):

    def __init__(self, geometry, color=white, position=None, orientation=None):
        self.geometry = geometry
        self.color = color
        if type(position) is tuple:
            position = Vec3(*position)
        self.position = position
        if type(orientation) is tuple:
            orientation = Orientation(orientation)
        self.orientation = orientation

        self._vertices = None

    @property
    def vertices(self):
        if self._vertices is None:
            matrix = Matrix(self.position, self.orientation)
            self._vertices = [
                matrix.transform(vert)
                for vert in self.geometry.vertices]
        return self._vertices

    @property
    def faces(self):
        return self.geometry.faces

    @property
    def colors(self):
        return [self.color for _ in xrange(len(self.vertices))]


class MultiShape(object):

    def __init__(self, *args, **kwargs):
        self.children = list(args)
        self.position = kwargs.pop('position', None)
        self.orientation = kwargs.pop('orientation', None)
        assert kwargs == {}, 'unrecognized kwargs, %s' % (kwargs,)
        self._vertices = None
        self._colors = None
        self._faces = None

    def add(self, child):
        self.children.append(child)

    @property
    def vertices(self):
        if self._vertices is None:
            matrix = Matrix(self.position, self.orientation)
            self._vertices = [
                matrix.transform(vert)
                for shape in self.children
                for vert in shape.vertices]
        return self._vertices

    @property
    def faces(self):
        if self._faces is None:
            newfaces = []
            index_offset = 0
            for shape in self.children:
                for face in shape.faces:
                    newface = []
                    for index in face:
                        newface.append(index + index_offset)
                    newfaces.append(newface)
                index_offset += len(shape.vertices)
            self._faces = newfaces
        return self._faces

    @property
    def colors(self):
        if self._colors is None:
            self._colors = list(
                chain.from_iterable(shape.colors for shape in self.children))
        return self._colors


def RgbCubeCluster(edge, cluster_edge, cube_count):
    shape = MultiShape()
    for i in xrange(cube_count):
        while True:
            r = randint(1, cluster_edge-1)
            g = randint(1, cluster_edge-1)
            b = randint(1, cluster_edge-1)
            color = (
                int(r / cluster_edge * 255),
                int(g / cluster_edge * 255),
                int(b / cluster_edge * 255),
                255)
            pos = Vec3(
                r - cluster_edge / 2,
                g - cluster_edge / 2,
                b - cluster_edge / 2,
            )
            if pos.length > 8:
                break
        shape.add(Shape(Cube(edge), color=color, position=Vec3(*pos)))
    return shape


def CubeLattice(edge, cluster_edge, freq):
    shape = MultiShape()
    black = (0, 0, 0, 255)
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            shape.add(Shape(Cube(edge), black, Vec3(i, j, -cluster_edge/2)))
            shape.add(Shape(Cube(edge), black, Vec3(i, j, +cluster_edge/2)))
            shape.add(Shape(Cube(edge), black, Vec3(i, -cluster_edge/2, j)))
            shape.add(Shape(Cube(edge), black, Vec3(i, +cluster_edge/2, j)))
            shape.add(Shape(Cube(edge), black, Vec3(-cluster_edge/2, i, j)))
            shape.add(Shape(Cube(edge), black, Vec3(+cluster_edge/2, i, j)))
    return shape


def CubeCross():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), center_color, Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), outer_color, XAxis))
    multi.add(Shape(Cube(1), outer_color, YAxis))
    multi.add(Shape(Cube(1), outer_color, ZAxis))
    multi.add(Shape(Cube(1), outer_color, -XAxis))
    multi.add(Shape(Cube(1), outer_color, -YAxis))
    multi.add(Shape(Cube(1), outer_color, -ZAxis))
    return multi


def CubeCorners():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), center_color, Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), outer_color, (+1, +1, +1)))
    multi.add(Shape(Cube(1), outer_color, (+1, +1, -1)))
    multi.add(Shape(Cube(1), outer_color, (+1, -1, +1)))
    multi.add(Shape(Cube(1), outer_color, (+1, -1, -1)))
    multi.add(Shape(Cube(1), outer_color, (-1, +1, +1)))
    multi.add(Shape(Cube(1), outer_color, (-1, +1, -1)))
    multi.add(Shape(Cube(1), outer_color, (-1, -1, +1)))
    multi.add(Shape(Cube(1), outer_color, (-1, -1, -1)))
    return multi
    

def RgbAxes():
    red = (255, 0, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)
    cube1 = Cube(1)
    multi = MultiShape(
        Shape(
            geometry=cube1,
        ),
        Shape(
            geometry=cube1,
            color=red,
            position=XAxis,
        ),
        Shape(
            geometry=cube1,
            color=green,
            position=YAxis,
        ),
        Shape(
            geometry=Cube(1),
            color=blue,
            position=ZAxis,
        ),
    )
    return multi

