from bge import *
from collections import OrderedDict
from math import radians
from mathutils import Vector, Matrix, Euler
from .FuncClasses import Transform

class ThirdPerson(types.KX_PythonComponent):
    args = OrderedDict([
        ("Parent", "Cube"),
        ("Camera name", "Camera"),
        ("Frame delay after movement", 120)
    ])

    def start(self, args):
        self.args = args
        self.scene: types.KX_Scene = logic.getCurrentScene()

        self.veloc_move = radians(2)

        self.cam_parent = self.scene.objects[args["Parent"]]
        self.cam_axis: types.KX_GameObject = self.object
        self.cam: types.KX_GameObject = self.cam_axis.children[args["Camera name"]]

        self.frame_delay = args["Frame delay after movement"]

        self.cam_dist: Vector = Vector(self.cam.localPosition.xyz)
        self.old_cam_dist: Vector = self.cam_dist       
        
        pass

    def update(self):
        self.__setCamPosition(self.cam_parent)
        #self.__moveToDefault()
        self.__colision()
        pass

        # Rotaciona a camera para a posição noraml, ou seja, atrás do player

    def __setCamPosition(self, obj):
        if self.cam_axis.worldPosition != obj.worldPosition:
            self.cam_axis.worldPosition = obj.worldPosition
        pass

    def __colision(self):
        target = self.cam.worldPosition + Transform.up(self.cam, -self.cam.getDistanceTo(self.cam_axis) + 3)
        hitObj, hitPos, hitNormal = self.cam_axis.rayCast(target, self.cam.worldPosition + Transform.up(self.cam, -1))
        if hitObj:
            self.cam.worldPosition = hitPos - Transform.up(self.cam, -1.1)
            self.old_cam_dist = Vector(self.cam.worldPosition.xyz)
            pass
        else:
            pos = self.cam.localPosition
            if pos != self.cam_dist:
                if pos < self.cam_dist:
                    self.cam.localPosition = self.cam_dist
                    pass
                elif pos > self.cam_dist and self.old_cam_dist != self.cam.worldPosition:
                    self.cam.applyMovement(Vector([0, 0, self.cam.getDistanceTo(self.old_cam_dist)]), True)
                    self.old_cam_dist = Vector(self.cam.worldPosition.xyz)
                    pass
                pass
            pass
        pass

    def __moveToDefault(self):
        frame = self.object["frame"]
        rot_y = self.cam_axis.worldOrientation.to_euler().y
        if rot_y != 0:
            self.cam_axis.applyRotation(Vector([0, -rot_y, 0]), True)
        if frame >= self.frame_delay:
            cam_axis_eule: Euler = self.cam_axis.worldOrientation.to_euler()
            parent_axis: Euler = self.cam_parent.worldOrientation.to_euler()
            add = self.veloc_move
            if cam_axis_eule.z < parent_axis.z:                
                if cam_axis_eule.z + self.veloc_move > parent_axis.z:
                    add = parent_axis.z - cam_axis_eule.z
                    pass
                self.cam_axis.applyRotation(Vector([0, 0, add]), False)
                pass
            elif cam_axis_eule.z > parent_axis.z:
                if cam_axis_eule.z - self.veloc_move < parent_axis.z:
                    add = cam_axis_eule.z - parent_axis.z
                    pass
                self.cam_axis.applyRotation(Vector([0, 0, -add]), False)
                pass
            add = self.veloc_move
            if cam_axis_eule.x < parent_axis.x:
                add = self.veloc_move
                if cam_axis_eule.x + self.veloc_move > parent_axis.x:
                    add = parent_axis.x - cam_axis_eule.x
                    pass
                self.cam_axis.applyRotation(Vector([add, 0, 0]), True)
                pass
            elif cam_axis_eule.x > parent_axis.x:
                if cam_axis_eule.x - self.veloc_move < parent_axis.x:
                    add = cam_axis_eule.x - parent_axis.x
                    pass
                self.cam_axis.applyRotation(Vector([-add, 0, 0]), True)
                pass
            elif cam_axis_eule.z == parent_axis.z and cam_axis_eule.x == parent_axis.x:
                self.object["frame"] = 0
            pass
        else:
             self.object["frame"] += 1
             pass
    pass

class FirstPerson(types.KX_PythonComponent):
    args = OrderedDict([
        
    ])

    def start(self, args):
        self.args = args
        pass

    def update(self):

        pass
    pass