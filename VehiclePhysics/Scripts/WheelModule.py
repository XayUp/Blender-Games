from bge import *
from collections import OrderedDict
from mathutils import Vector
from math import radians

class Wheel(types.KX_PythonComponent):
    args = OrderedDict([
        ("wheel", {"Front Left", "Front Right", "Back Left", "Back Right"}),
        ("Stiffness", 50.0),
        ("Damping", 5000),
        ("Height", 0.92)
    ])

    def start(self, args):
        self.scene: types.KX_Scene = logic.getCurrentScene()
        self.args = args

        #Finais
        self.susp_stiffness = args["Stiffness"]         # Rigidez
        self.susp_damping  = args["Damping"]
        self.susp_max_height = args["Height"]
        self.susp_min_height = 0.5         # Mola comprimida

        self.pivot: types.KX_GameObject = self.object
        self.wheel: types.KX_GameObject = self.__startSetWheel(self.scene.addObject(self.scene.objectsInactive["roda"]), args["wheel"])
        self.wheel_radius = self.wheel.localScale[2]
        self.wheel.worldPosition = self.pivot.worldPosition + Vector([0, 0, -self.susp_max_height + self.wheel_radius*2])
        self.wheel.setParent(self.pivot)
        

        self.previousLength = self.pivot.getDistanceTo(self.wheel)
        pass

    def update(self):
        self.__suspensionPhysics()
        pass

    def __startSetWheel(self, wheel_obj, wheel_type: str):
        if wheel_type == "Front Left" or wheel_type == "Back Left":
            wheel_obj.applyRotation(Vector([0, 0, radians(180)]), False)
            pass
        return wheel_obj

    def __rayCast(self, obj, dist_x: float, dist_y: float, dist_z: float):
        origin = obj.worldPosition
        target = origin + (obj.worldOrientation * Vector([dist_x, dist_y, dist_z]))
        return obj.rayCast(target, origin, 0)

    def __suspensionPhysics(self):
        hitObject, hitPos, hitNormal = self.__rayCast(self.pivot, 0, 0, -self.susp_max_height)
        if hitObject != None:
            self.wheel.worldPosition = hitPos + (self.wheel.worldOrientation * Vector([0, 0, self.wheel_radius*2]))
            currentLenght = self.pivot.getDistanceTo(self.wheel)
            susp_force = self.susp_stiffness * ((self.susp_max_height-(self.wheel_radius*2)) - currentLenght) + self.susp_damping * (self.previousLength - currentLenght) / logic.getAverageFrameRate()
            self.pivot.parent.applyImpulse(self.pivot.worldPosition, Vector([0, 0, susp_force]) , False)
            self.previousLength = currentLenght
            pass
        pass

    pass
