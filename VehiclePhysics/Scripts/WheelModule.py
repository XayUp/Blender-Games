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
        #self.susp_min_height = 0.5         # Mola comprimida

        self.pivot: types.KX_GameObject = self.object
        self.chassi = self.pivot.parent
        self.wheel: types.KX_GameObject = self.__startSetWheel(self.scene.addObject(self.scene.objectsInactive["roda"]), args["wheel"])
        self.wheel_radius = self.wheel.localScale[2]
        self.wheel.worldPosition = self.pivot.worldPosition + Vector([0, 0, -self.susp_max_height + self.wheel_radius*2])
        self.wheel.setParent(self.pivot)
        self.back_wheel: bool = args["wheel"] == "Back Left" or args["wheel"] == "Back Right"
        self.front_wheel = self.back_wheel == False

        self.previousLength = self.pivot.getDistanceTo(self.wheel)
        pass

    def update(self):
        self.cast_touch = False
        self.__suspensionPhysics()
        #if self.scene.active_camera in self.chassi.children:
        self.keyboardInputs(logic.keyboard.activeInputs)
        self.__frictionPhysics()
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

    def __frictionPhysics(self):       
        if self.back_wheel:
            velocity = self.chassi.getLinearVelocity(True)
            self.chassi.applyImpulse(self.pivot.worldPosition, (self.pivot.worldOrientation * Vector([-velocity.x*(velocity.y/15), 0, 0])))
        pass

    def __suspensionPhysics(self):
        hitObject, hitPos, hitNormal = self.__rayCast(self.pivot, 0, 0, -self.susp_max_height)
        self.cast_touch = hitObject != None
        if self.cast_touch:
            self.wheel.worldPosition = hitPos + (self.wheel.worldOrientation * Vector([0, 0, self.wheel_radius*2]))
            currentLenght = self.pivot.getDistanceTo(self.wheel)
            susp_force = self.susp_stiffness * ((self.susp_max_height-(self.wheel_radius*2)) - currentLenght) + self.susp_damping * (self.previousLength - currentLenght) / logic.getAverageFrameRate()
            self.pivot.parent.applyImpulse(self.pivot.worldPosition, Vector([0, 0, susp_force]) , False)
            self.previousLength = currentLenght
            pass
        pass

    def keyboardInputs(self, inputs):
        run: bool = False
        for key in inputs:
            key_event = events.EventToCharacter(key, False)
            if key_event == "w" and self.back_wheel and self.cast_touch:
                self.chassi.applyImpulse(self.pivot.worldPosition, (self.pivot.worldOrientation * Vector([0, 10, 0])), False)
                pass
            elif key_event == "s" and self.back_wheel and self.cast_touch:
                self.chassi.applyImpulse(self.pivot.worldPosition, (self.pivot.worldOrientation * Vector([0, -10, 0])), False)
                pass
            elif key_event == "a" and self.front_wheel:
                self.chassi.applyImpulse(self.pivot.worldPosition, (self.pivot.worldOrientation * Vector([-12, 0, 0])), False)
                pass
            elif key_event == "d" and self.front_wheel:
                self.chassi.applyImpulse(self.pivot.worldPosition, (self.pivot.worldOrientation * Vector([12, 0, 0])), False)
                pass
            pass
        pass

    pass

class BikeWheel(types.KX_PythonComponent):
    args = OrderedDict([
        ("Wheel", {"Front", "Back"}),
        ("Final pivot", {"p_b", "p_f"}),
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
        #self.susp_min_height = 0.5         # Mola comprimida

        
        self.pivot: types.KX_GameObject = self.object
        self.chassi: types.KX_GameObject = self.pivot.parent
        self.final_pivot: types.KX_GameObject = self.chassi.children[args["Final pivot"]]
        self.wheel: types.KX_GameObject = self.__startSetWheel(self.scene.addObject(self.scene.objectsInactive["roda_moto"]), args["Wheel"])
        self.wheel_radius = self.wheel.localScale[2]
        self.wheel.worldPosition = self.pivot.worldPosition
        self.wheel.setParent(self.pivot)        
        self.previousLength = self.wheel.getDistanceTo(self.final_pivot)
        
        self.back_wheel = args["Wheel"] == "Back"
        pass

    def update(self):
        self.cast_touch = False
        self.__suspensionPhysics()
        self.keyboardInputs(logic.keyboard.activeInputs)
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
        self.cast_touch = hitObject != None
        if self.cast_touch:
            self.wheel.worldPosition = hitPos + (self.wheel.worldOrientation * Vector([0, 0, self.wheel_radius/2]))
            currentLenght = self.wheel.getDistanceTo(self.final_pivot)
            susp_force = self.susp_stiffness * ((self.susp_max_height) - currentLenght) + self.susp_damping * (self.previousLength - currentLenght) / logic.getAverageFrameRate()
            self.pivot.parent.applyImpulse(self.final_pivot.worldPosition, Vector([0, 0, susp_force]) , False)
            self.previousLength = currentLenght
            pass
        pass

    def keyboardInputs(self, inputs):
        run: bool = False
        for key in inputs:
            key_event = events.EventToCharacter(key, False)
            if key_event == "w" and self.back_wheel and self.cast_touch:
                self.chassi.applyImpulse(self.pivot.worldPosition, Vector([0, 10, 0]), False)
                pass
            elif key_event == "s" and self.back_wheel and self.cast_touch:
                self.chassi.applyImpulse(self.pivot.worldPosition, Vector([0, -10, 0]), True)
                pass
            pass
        pass

    pass
