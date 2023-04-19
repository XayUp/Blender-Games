from bge import *
from collections import OrderedDict
from mathutils import Vector

class Sun(types.KX_PythonComponent):

    args = OrderedDict([
        ("Distance", Vector([0, 0, 0]))
    ])

    def start(self, args):
        self.args = args
        self.scene: types.KX_Scene = logic.getCurrentScene()   
        pass
    
    def update(self):
        cam = self.scene.active_camera
        new_sun = cam.worldPosition + self.args["Distance"]
        sun = self.object.worldPosition
        if cam and sun != new_sun:
            sun = new_sun
            pass
        pass
    pass