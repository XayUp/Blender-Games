from bge import *
from mathutils import Vector

class PlayerModule(types.KX_PythonComponent):
    
    args = {
        "Walk Forward" : "w",
        "Walk Backward" : "s",
        "Walk Left" : "a",
        "Walk Right" : "d",
        "Pick Object" : "e",
        "Run" : "c"

    }

    def start(self, args):
        #Variais de propriedade (Finais)
        self.pick_object_dist_multiplier = 0.1
        self.raycast_dist = 4
        self.pick_object_min_dist = 3
        self.pick_object_max_dist = 8
        self.open_doctor_door = 1.6
        self.open_normal_door = -90
        #self.anim: types.KX_GameObject = self.object.children["armature"]
        
        #Variaveis 
        self.scene: types.KX_Scene = logic.getCurrentScene()
        self.render = render
        self.mouse = logic.mouse
        self.picked_object = None

        #Identificadores
        self.item_identifier = "item"
        self.porta_deslizante = "deslizante"
        self.porta_normal = "normal"

        #Objetos
        #self.fp_cam: types.KX_GameObject = self.scene.objects["fs_cam"]
        #self.raycast_parent = self.scene.objects["cast"]
        #self.active_cam = self.fp_cam

        # Modulos
        self.animation = None
        if 'AnimationClass' in self.object.components:
            self.animation = self.object.components['AnimationClass']
        pass

    def update(self):
        self.keyboardInputs(logic.keyboard.activeInputs)
        #self.mouseInputs(logic.mouse.activeInputs, self.active_cam)
        pass
    
    def rayCast(self, fp_cam):
        origin = fp_cam.worldPosition
        target = origin + (fp_cam.worldOrientation * Vector([0, 0, -self.raycast_dist]))
        return fp_cam.rayCast(target, origin, 0)
    
    def pickedObjectDist(self, from_object, to_object, dist, min_dist, max_dist):
        # from_object: objeto raíz, geralmente o objeto pai de
        # to_object: objeto de destino, o que vai ser movido. Geralmente o filho de from_object
        # dist: distancia a ser acrescentada (número negativo se quiser puxar para mais perto). Use "0" para manter o objeto na distancia atual
        # min_dist: distância mínima que o objeto pode ser puxado
        # max_dist: distância máxima que o objeto pode ser empurrado
        if from_object and to_object != None:
            new_dist = from_object.getDistanceTo(to_object) + dist
            if new_dist < min_dist:
                new_dist = min_dist
            elif new_dist > max_dist:
                new_dist = max_dist
            to_object.worldPosition = from_object.worldPosition + (from_object.worldOrientation * Vector([0, new_dist, 0]))
            pass
        pass

    def mouseInputs(self, inputs, cam):
        key: types.SCA_InputEvent
        for key in inputs:
            if key == events.MOUSEX:
                w = self.render.getWindowWidth() / 2
                x = self.mouse.position[0]
                pass
            elif key == events.MOUSEY:
                h = self.render.getWindowHeight() / 2
                y = self.mouse.position[0]
                pass
            elif key == events.LEFTMOUSE:
                print("Esquerdo")
                pass
            elif key == events.RIGHTMOUSE:
                print("direito")
                pass
            elif key == events.WHEELDOWNMOUSE:
                self.pickedObjectDist(self.raycast_parent, self.picked_object, self.pick_object_dist_multiplier*(-1), self.pick_object_min_dist, self.pick_object_max_dist)
                pass
            elif key == events.WHEELUPMOUSE:
                self.pickedObjectDist(self.raycast_parent, self.picked_object, self.pick_object_dist_multiplier, self.pick_object_min_dist, self.pick_object_max_dist)
                pass
        pass
    
    def keyboardInputs(self, inputs):
        run: bool = False
        walk: bool = False
        for key in inputs:
            key_event = events.EventToCharacter(key, False)
            if self.args["Run"] == key_event:
                if run:
                    self.object.applyMovement(Vector([0, 0.04, 0]), True)
                    pass
                else:
                    run = True
                pass
            elif self.args["Walk Forward"] == key_event:
                if run:
                    self.object.applyMovement(Vector([0, 0.1, 0]), True)
                    if self.animation != None: self.animation.start_run()
                else:
                    self.object.applyMovement(Vector([0, 0.04, 0]), True)
                    if self.animation != None: self.animation.start_walk_forward()
                pass
            elif self.args["Walk Backward"] == key_event:
                self.object.applyMovement(Vector([0, -0.04, 0]), True)
                if self.animation != None: self.animation.start_walk_forward()

            elif self.args["Walk Left"] == key_event:
                self.object.applyMovement(Vector([-0.05, 0, 0]), True)

            elif self.args["Walk Right"] == key_event:
                self.object.applyMovement(Vector([0.05, 0, 0]), True)

            elif self.args["Pick Object"] == key_event and inputs[key].activated:
                hitObject, hitPos, hitNormal = self.rayCast(self.fp_cam)     
                if hitObject:
                    #print(hitObject)
                    if self.item_identifier in hitObject:   
                        if self.picked_object == None:
                            self.picked_object = hitObject
                            self.picked_object.worldOrientation = self.raycast_parent.worldOrientation
                            self.pickedObjectDist(self.raycast_parent, self.picked_object, 0, self.pick_object_min_dist, self.pick_object_max_dist)
                            self.picked_object.setParent(self.raycast_parent)
                        else:
                            self.picked_object.removeParent()
                            self.picked_object = None
                            pass
                        pass
                    elif len(hitObject.components) > 0:
                        component: types.KX_PythonComponent
                        component = hitObject.components[0]
                        component.startComponent()
                        pass
                    pass
            pass
        pass

