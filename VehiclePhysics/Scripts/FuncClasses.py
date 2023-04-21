from bge import *
from mathutils import Vector, Matrix

class Maths():
    def clip(value, lower, upper):
        return lower if value < lower else upper if value > upper else value
    pass

    def getDeltaTime():
        deltaTime = logic.getAverageFrameRate()
        if deltaTime > 0:
            return 1 / deltaTime
        return 0
    
    def getLocalFromWorld(obj):
        return obj.worldPosition + obj.worldOrientation
        pass

class Sensors():
    def rayCast(obj, from_position, orientation, distx = 0, disty = 0, distz = 0):
        target = from_position + (orientation * Vector([distx, disty, distz]))
        return obj.rayCast(target, from_position, 0)
    pass

class Transform():   
    def __normalizeOrientation(worldOrientation: Matrix, axis: Vector = Vector([0, 0, 1])) -> Matrix: #Default normalize Z (Vector([0, 0, 1]))
        x = worldOrientation[0]
        y = worldOrientation[1]
        z = worldOrientation[2]
        if axis.x == 1: x = [1, 0, 0]
        if axis.y == 1: y = [0, 1, 0]
        if axis.z == 1: z = [0, 0, 1]        
        return Matrix([x, y, z])
        pass 

    # Local X Axis
    def right(obj, apply = 1) -> Vector:
        return (obj.worldOrientation * Vector([apply, 0, 0]))

    # Local Y Axis
    def forward(obj, apply = 1) -> Vector:
        return (obj.worldOrientation * Vector([0, apply, 0]))
 
    # Local Z Axis
    def up(obj, apply = 1) -> Vector:
        return (obj.worldOrientation * Vector([0, 0, apply]))
    
    def rightZ(obj, apply = 1) -> Vector:
        return (Transform.__normalizeOrientation(obj.worldOrientation) * Vector([apply, 0, 0]))

    # Local Y Axis
    def forwardZ(obj, apply = 1) -> Vector:
        return (Transform.__normalizeOrientation(obj.worldOrientation) * Vector([0, apply, 0]))
 
    # Local Z Axis
    def upZ(obj, apply = 1) -> Vector:
        return (Transform.__normalizeOrientation(obj.worldOrientation) * Vector([0, 0, apply]))

    def localVelocityFrom(obj, point = None) -> Vector:
        obj_point = obj
        if point == None:
            point = Vector([0, 0, 0])
            pass
        elif type(point) == types.KX_GameObject:
            obj_point = point
            point = Vector(point.worldPosition.xyz)
            pass
        world_volocity = obj.getVelocity(obj.worldPosition - point)
        local_x = world_volocity * Transform.right(obj_point)
        local_y = world_volocity * Transform.forward(obj_point)
        local_z = world_volocity * Transform.up(obj_point)
        return Vector([local_x, local_y, local_z])
    
    pass
