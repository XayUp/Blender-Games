from bge import *
from mathutils import Vector
from math import radians, degrees, cos
from .FuncClasses import Maths, Sensors, Transform

class VehiclePhysics():

    def __init__(self, obj_chassi, spring, wheel, wheel_location, wheel_torque, wheel_radius, susp_stiffness, susp_damping, susp_travel, susp_max_height,
                 susp_min_height, acceleration, wheel_break):
        self.chassi: types.KX_GameObject = obj_chassi
        self.spring: types.KX_GameObject = spring
        self.wheel: types.KX_GameObject = wheel
        self.wheel_location = wheel_location
        self.wheel_torque = wheel_torque
        self.wheel_radius = wheel_radius
        self.susp_stiffness = susp_stiffness
        self.susp_damping  = susp_damping
        self.susp_travel = susp_travel
        self.susp_max_height = susp_max_height      
        self.susp_min_height = susp_min_height
        self.acceleration = acceleration
        self.wheel_break = wheel_break

        self.wheel_axis: types.KX_GameObject = self.wheel.parent
        self.spring_lenght = self.susp_max_height
        self.last_lenght = self.spring_lenght
        self.cast_touch = False

        self.direction_keyboard = 0
        self.aceleration_keyboard = 0

        self.friction_velocity: Vector = Vector([0, 0, 0])
        pass

        # Entradas
    def keyboardInput(self, input):
        if input == "w" and self.wheel_torque and self.cast_touch:
            self.aceleration_keyboard = 1
            self.chassi.applyImpulse(self.hitPos, Transform.forward(self.wheel_axis) * self.acceleration * self.chassi.mass * self.aceleration_keyboard * Maths.getDeltaTime(), False)
            #self.chassi.applyImpulse(self.hitPos, (self.spring.worldOrientation * Vector([0, self.acceleration, 0])), False)
            pass
        elif input == "s" and self.wheel_torque and self.cast_touch:
            self.aceleration_keyboard = -1
            self.chassi.applyImpulse(self.hitPos, Transform.forward(self.wheel_axis) * self.acceleration * self.chassi.mass * self.aceleration_keyboard * Maths.getDeltaTime(), False)
            #self.chassi.applyImpulse(self.hitPos, (self.spring.worldOrientation * Vector([0, -self.acceleration, 0])), False)
            pass
        elif input == "a" and not self.wheel_torque and self.cast_touch:
            self.direction_keyboard = 1
            
            pass
        elif input == "d" and not self.wheel_torque and self.cast_touch:
            self.direction_keyboard = -1
            pass
        pass

        # Física
    def suspensionPhysics(self):
        hitObject, self.hitPos, hitNormal = Sensors.rayCast(self.chassi, self.spring.worldPosition,  self.spring.worldOrientation, 0, 0, -(self.susp_max_height+self.wheel_radius)) #self.__rayCast(self.spring, 0, 0, -self.susp_max_height)
        self.cast_touch = self.hitPos != None
        if self.cast_touch:
            delta = Maths.getDeltaTime()

            # Defina a posição da roda
            self.wheel_axis.worldPosition = self.hitPos + (self.wheel_axis.worldOrientation * Vector([0, 0, self.wheel_radius]))
            
            self.last_lenght        = self.spring_lenght
            self.spring_lenght      = Maths.clip((self.spring.getDistanceTo(self.hitPos) - self.wheel_radius), self.susp_min_height, self.susp_max_height)
            self.compression_speed  = (self.last_lenght - self.spring_lenght) * delta               # Velocidade em que a mola foi comprimida
            self.spring_compression = (self.susp_max_height - self.spring_lenght)                   # Tamanho comprido          
            self.spring_force       = self.susp_stiffness * self.spring_compression                 # Força da mola baseada na compressão atual
            self.damping_force      = self.susp_damping * self.compression_speed                    # Força para amortecimento
            self.susp_force         = self.spring_force + self.damping_force                        # Força da suspenção
            
            lFx, lFy                  = self.__direction()  # Aplicar a força de direção ("Curva")
            ang = cos(degrees(self.chassi.worldOrientation.to_euler().y))
            if ang < 0:
                ang *= -1
                pass
            print(ang)
            self.susp_force_vector  = (self.susp_force * ang) * Transform.up(self.spring)                  # Aplicar a força da suspensão no eixo Z da mola
            
            self.chassi.applyImpulse(self.spring.worldPosition, self.susp_force_vector, False)
            #self.chassi.applyImpulse(self.hitPos, lFx + lFy, False)
            self.__wheelFrictionPhysics(self.chassi, self.wheel_axis)
            self.__wheelRotation()
            pass
        elif self.spring_lenght != self.susp_max_height:       # Extenda a Mola     
            self.wheel_axis.worldPosition = self.__extendsSprings()
            self.spring_lenght = self.susp_max_height
        pass

    def __wheelRotation(self):
        self.wheel.applyRotation(Vector([-radians(Transform.localVelocityFrom(self.chassi, self.wheel_axis).y), 0, 0]), True)
        pass

    def __extendsSprings(self):
        return self.spring.worldPosition + (self.spring.worldOrientation * Vector([0, 0, -(self.susp_max_height)]))

    def __direction(self) -> Vector and Vector: 
        velocity: Vector    = Transform.localVelocityFrom(self.chassi, self.wheel_axis)
        Force_x             = self.aceleration_keyboard * (self.spring_force)
        Force_y             = velocity.x * (self.spring_force)
        lFx                 = Force_x * Transform.forward(self.wheel_axis)
        lFy                 = Force_y * -Transform.right(self.wheel_axis)

        return lFx, lFy
        #return Vector([0, 0, 0]), Vector([0, 0, 0])

    def __wheelFrictionPhysics(self, obj, point_obj):
        velocity: Vector = Transform.localVelocityFrom(obj, self.hitPos)
        veloc_x = velocity.x
        veloc_y = velocity.y
        F = -veloc_x**2 * self.spring_force * Maths.getDeltaTime()
        #print(velocity)
        #print("Chassi", self.chassi.getLinearVelocity(True))
        logic.getCurrentScene().objects["Sphere"].worldPosition =  self.hitPos + Transform.rightZ(point_obj, F)
        self.chassi.applyImpulse(obj.worldPosition - self.hitPos, Vector([F, 0, 0]), True)
        pass