import bge
from mathutils import Vector

class PlayerModule(bge.types.KX_PythonComponent):
    
    args = {
        "Walk Forward" : "w",
        "Walk Backward" : "s",
        "Walk Left" : "a",
        "Walk Right" : "d",
        "Pick Object" : "e",
        "Run" : "c"

    }

    def start(self, args):
        #Variais de propriedade
        self.object_dist_multiplier = 0.2
        self.pick_object_default_dist = 3
        #Variaveis 
        self.scene: bge.types.KX_Scene = bge.logic.getCurrentScene()
        self.render = bge.render
        self.mouse = bge.logic.mouse
        self.picked_object = None
        self.item_identifier = "item"
        
        #Objetos
        self.fp_cam: bge.types.KX_GameObject = self.scene.objects["fs_cam"]
        self.raycast_parent = self.scene.objects["cast"]
        self.rayhit = self.scene.objects["raycast_hitPos"]
        self.active_cam = self.fp_cam
        pass

    def update(self):
        self.keyboardInputs(bge.logic.keyboard.activeInputs)
        self.mouseInputs(bge.logic.mouse.activeInputs, self.active_cam)
        pass

    def rayCast(self, fp_cam):
        origin = fp_cam.worldPosition
        target = origin + (fp_cam.worldOrientation * Vector([0, 0, -10]))
        return fp_cam.rayCast(target, origin, 0)
    
    def pickedObjectDist(self, from_object: bge.types.KX_GameObject, to_object: bge.types.KX_GameObject, dist, increment: bool):
        if from_object and to_object != None:
            new_dist = dist
            if increment:
                current_dist = from_object.getDistanceTo(to_object)
                new_dist = current_dist + dist
                pass
            if new_dist > self.pick_object_default_dist:
                to_object.worldPosition = from_object.worldPosition + (from_object.worldOrientation * Vector([0, new_dist, 0]))
                pass
            pass
        pass

    def mouseInputs(self, inputs, cam):
        key: bge.types.SCA_InputEvent
        for key in inputs:
            if key == bge.events.MOUSEX:
                w = self.render.getWindowWidth() / 2
                x = self.mouse.position[0]
                pass
            elif key == bge.events.MOUSEY:
                h = self.render.getWindowHeight() / 2
                y = self.mouse.position[0]
                pass
            elif key == bge.events.LEFTMOUSE:
                print("Esquerdo")
                pass

            elif key == bge.events.RIGHTMOUSE:
                print("direito")
                pass
            elif key == bge.events.WHEELDOWNMOUSE:
                self.pickedObjectDist(self.raycast_parent, self.picked_object, self.object_dist_multiplier*(-1), True)
                pass
            elif key == bge.events.WHEELUPMOUSE:
                self.pickedObjectDist(self.raycast_parent, self.picked_object, self.object_dist_multiplier, True)
                pass
        pass
    
    def keyboardInputs(self, inputs):
        run: bool = False
        for key in inputs:
            key_event = bge.events.EventToCharacter(key, False)
            if self.args["Run"] == key:
                if run:
                    self.object.applyMovement(Vector([0, 0.05, 0]), True)
                    pass
                else:
                    run = True
                pass
            elif self.args["Walk Forward"] == key_event:
                if run:
                    self.object.applyMovement(Vector([0, 0.1, 0]), True)
                    pass
                else:
                    self.object.applyMovement(Vector([0, 0.05, 0]), True)
                    pass
                pass
            elif self.args["Walk Backward"] == key_event:
                self.object.applyMovement(Vector([0, -0.05, 0]), True)
                pass
            elif self.args["Walk Left"] == key_event:
                self.object.applyMovement(Vector([-0.05, 0, 0]), True)
                pass
            elif self.args["Walk Right"] == key_event:
                self.object.applyMovement(Vector([0.05, 0, 0]), True)
                pass
            elif self.args["Pick Object"] == key_event and inputs[key].activated:
                print("E")
                hitObject, hitPos, hitNormal = self.rayCast(self.fp_cam)
                if hitPos: self.rayhit.worldPosition = hitPos
                if self.picked_object == None:
                    if hitObject and self.item_identifier in hitObject:
                        self.picked_object = hitObject
                        self.picked_object.worldOrientation = self.raycast_parent.worldOrientation
                        self.pickedObjectDist(self.raycast_parent, self.picked_object, self.pick_object_default_dist, False)
                        self.picked_object.setParent(self.raycast_parent)
                    pass
                else:
                    self.picked_object.removeParent()
                    self.picked_object = None
                    pass
                pass
            pass
        pass

