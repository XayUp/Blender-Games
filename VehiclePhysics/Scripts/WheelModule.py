from bge import *
from .FuncClasses import Maths, Transform
from collections import OrderedDict
from mathutils import Vector, Euler
from math import radians, degrees
from .VehiclePhysics import VehiclePhysics

class Wheel(types.KX_PythonComponent):
    args = OrderedDict([
        ("Wheel Name", ""),
        ("Wheel Location", {"Front", "Back"}),
        ("Handlebar", False),
        ("Handlebar angle", 45),
        ("Handlebar angle velocity", 0.2),
        ("Wheel Torque", False),
        ("Wheel Radius (Scale)", 0.5),
        ("Spring Stiffness", 350.0),
        ("Spring Damping", 18000),
        ("Spring Height", 0.5),
        ("Spring Travel", 0.6),
        ("Acceleration", 10.0),
        ("Break", 1.0)
    ])

    def start(self, args):
        self.scene: types.KX_Scene = logic.getCurrentScene()
        self.args = args

        #Finais
        self.keyboard_ad_axis = 0
        self.keyboard_ws_axis = 0
        
        self.is_handlebar = args["Handlebar"]
        self.handlebar_angle = radians(args["Handlebar angle"])
        self.handlebar_velocity = args["Handlebar angle velocity"]
        wheel_location  = args["Wheel Location"]
        wheel_torque    = args["Wheel Torque"]
        wheel_radius    = args["Wheel Radius (Scale)"]
        susp_stiffness  = args["Spring Stiffness"]                            # Rigidez
        susp_damping    = args["Spring Damping"]                              # Suavidez
        susp_travel     = args["Spring Travel"]                               # Viagem da mola
        susp_max_height = args["Spring Height"]                               # Comprimento máximo (Relaxado)        
        susp_min_height = susp_max_height - susp_travel                       # Comprimento mínimo (Comprimido)
        acceleration    = args["Acceleration"]                                # Aceleração
        wheel_break     = args["Break"]                                       # Freio
        
        self.chassi: types.KX_GameObject = self.object.parent                 # Corpo do veículo
        wheel = self.object.childrenRecursive[args["Wheel Name"]]             # Roda
        self.wheel_axis = wheel.parent
        self.VehiclePhysics = VehiclePhysics(self.chassi, self.object, wheel, wheel_location, wheel_torque, wheel_radius, susp_stiffness, susp_damping, susp_travel, susp_max_height, susp_min_height, acceleration, wheel_break)        
        
        pass

    def update(self):
        self.keyboardInputs(logic.keyboard.activeInputs)
        self.__handlebarAngle(self.keyboard_ad_axis)
        self.VehiclePhysics.suspensionPhysics()
        pass

    def keyboardInputs(self, inputs):
        run: bool = False
        for key in inputs:
            key_event = events.EventToCharacter(key, False)
            self.VehiclePhysics.keyboardInput(key_event)
            if key_event == "w":
                pass
            elif key_event == "s":
                pass
            elif key_event == "a":
                self.keyboard_ad_axis = 1
                pass
            elif key_event == "d":
                self.keyboard_ad_axis = -1
                pass
            pass
        pass

    def __handlebarAngle(self, key_axis):
        if self.is_handlebar:
            z = self.object.localOrientation.to_euler().z
            to = self.handlebar_angle * key_axis
            increment = self.handlebar_velocity
            if z != to:               
                if key_axis < 0 and z > -self.handlebar_angle:   #Right
                    if z - increment < -self.handlebar_angle:
                        increment = self.handlebar_angle + z
                        pass
                    pass
                elif key_axis > 0 and z < self.handlebar_angle: #Left
                    if z + increment > self.handlebar_angle:
                        increment = self.handlebar_angle - z
                        pass
                    pass
                elif key_axis == 0: 
                    if z > to: key_axis = -1
                    elif z < to: key_axis = 1
                    pass
                self.object.applyRotation(Vector([0, 0, increment * key_axis * Maths.getDeltaTime()]), True)
            pass
        pass

    pass

class BikeWheel(types.KX_PythonComponent):
    args = OrderedDict([
        ("Wheel Name", ""),
        ("Wheel Location", {"Front", "Back"}),
        ("Handlebar", False),
        ("Handlebar angle", 45),
        ("Handlebar angle velocity", 0.2),
        ("Wheel Torque", False),
        ("Wheel Radius (Scale)", 0.5),
        ("Spring Stiffness", 350.0),
        ("Spring Damping", 18000),
        ("Spring Height", 0.5),
        ("Spring Travel", 0.6),
        ("Acceleration", 10.0),
        ("Break", 1.0)
    ])

    def start(self, args):
        self.scene: types.KX_Scene = logic.getCurrentScene()
        self.args = args

        #Finais
        self.keyboard_ad_axis = 0
        self.keyboard_ws_axis = 0
        
        self.is_handlebar = args["Handlebar"]
        self.handlebar_angle = radians(args["Handlebar angle"])
        self.handlebar_velocity = args["Handlebar angle velocity"]
        wheel_location  = args["Wheel Location"]
        wheel_torque    = args["Wheel Torque"]
        wheel_radius    = args["Wheel Radius (Scale)"]
        susp_stiffness  = args["Spring Stiffness"]                            # Rigidez
        susp_damping    = args["Spring Damping"]                              # Suavidez
        susp_travel     = args["Spring Travel"]                               # Viagem da mola
        susp_max_height = args["Spring Height"]                               # Comprimento máximo (Relaxado)        
        susp_min_height = susp_max_height - susp_travel                       # Comprimento mínimo (Comprimido)
        acceleration    = args["Acceleration"]                                # Aceleração
        wheel_break     = args["Break"]                                       # Freio
        
        self.chassi: types.KX_GameObject = self.object.parent                 # Corpo do veículo
        wheel = self.object.childrenRecursive[args["Wheel Name"]]             # Roda
        self.wheel_axis = wheel.parent
        self.VehiclePhysics = VehiclePhysics(self.chassi, self.object, wheel, wheel_location, wheel_torque, wheel_radius, susp_stiffness, susp_damping, susp_travel, susp_max_height, susp_min_height, acceleration, wheel_break)        
        pass

    def update(self):
        self.keyboardInputs(logic.keyboard.activeInputs)
        self.__handlebarAngle(self.keyboard_ad_axis)
        self.VehiclePhysics.suspensionPhysics()
        #self.__centrifugalForce()
        pass

    def keyboardInputs(self, inputs):        
        run: bool = False
        self.keyboard_ad_axis = 0
        self.keyboard_ws_axis = 0
        for key in inputs:
            key_event = events.EventToCharacter(key, False)
            self.VehiclePhysics.keyboardInput(key_event)
            if key_event == "w":
                pass
            elif key_event == "s":
                pass
            elif key_event == "a":
                self.keyboard_ad_axis = 1
                pass
            elif key_event == "d":
                self.keyboard_ad_axis = -1
                pass
            pass
        pass

    def __handlebarAngle(self, key_axis):
        if self.is_handlebar:
            z = self.object.localOrientation.to_euler().z
            to = self.handlebar_angle * key_axis
            increment = self.handlebar_velocity
            if z != to:               
                if key_axis < 0 and z > -self.handlebar_angle:   #Right
                    if z - increment < -self.handlebar_angle:
                        increment = self.handlebar_angle + z
                        pass
                    pass
                elif key_axis > 0 and z < self.handlebar_angle: #Left
                    if z + increment > self.handlebar_angle:
                        increment = self.handlebar_angle - z
                        pass
                    pass
                elif key_axis == 0: 
                    if z > to: key_axis = -1
                    elif z < to: key_axis = 1
                    pass
                self.object.applyRotation(Vector([0, 0, increment * key_axis * Maths.getDeltaTime()]), True)
            pass
        pass

    def __centrifugalForce(self):
        hitObj, hitPos, hitNormal = self.chassi.rayCast(self.chassi.worldPosition - Vector([0, 0, 5]), self.chassi)
        angle: Euler = self.chassi.localOrientation.to_euler()
        if angle.y != 0:
            #apply = (self.chassi.mass * self.chassi.getLinearVelocity(True).y**2) / 1
            #self.chassi.applyForce(Transform.rightZ(self.chassi) * Vector([apply, 0, 0]), False)
            pass
        pass

    pass
