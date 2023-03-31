from bge import *
from collections import OrderedDict

class DoorModule(types.KX_PythonComponent):
   
    args = OrderedDict([
        ("Door type", {"Normal", "Deslizante"}),
        ("Openned Num", 1.0), #Até onde deve ser aberta. Isso depende. Se é deslizante (movimento X) ou normal (rotação Z)
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende. Se é deslizante (movimento X) ou normal (rotação Z)
        ("Openned", False)
        ])
    def start(self, args):
        self.args = args
        #Finais
        self.open_num = args["Openned Num"]
        self.move_speed = 0.05
        self.open = -1
        self.close = 1
        self.object: types.KX_GameObject
        
        #Identificadores
        self.door_type = args["Door type"]
        self.openned = args["Openned"]
        self.closed = 0
        self.deslizante = "Deslizante"
        self.normal = "Normal"
       
        #Propriedades
        self.to_state_num = 0
        self.current_state_num = 0

        #Controle
        self.action = 1 #-1 ou 1
        self.initial_num = 0 #Posição ou rotacão inicial da porta
        self.run_anim = False #Definir True para iniciar a animacção

        pass

    def update(self):
        self.animationDoor()
        pass

    def openCloseDoor(self):
        if self.door_type == self.deslizante:
            self.initial_num =  self.object.position.x
            self.current_state_num = 0
            if self.openned:
                self.current_state_num = self.open_num
            pass
        elif self.door_type == self.normal:
            self.initial_num =  self.object.worldOrientation.to_euler().z - self.initial_num
            pass
        if self.openned: #Se estiver Aberta
            self.openned = False
            self.args["Openned"] = False
            self.to_state_num = 0
            self.action = self.close
            pass
        else:            #Se estiver Fechada
            self.openned = True
            self.args["Openned"] = True
            self.to_state_num = self.open_num
            self.action = self.open
            pass
        print(self.action,
            self.openned,
            self.to_state_num)
        pass

    def animationDoor(self):
        if self.run_anim: 
            print(self.current_state_num, "->", self.to_state_num)
            if self.action == self.open:
                if self.current_state_num <= self.to_state_num + (self.action * self.initial_num):
                    self.run_anim = False
                pass
            elif self.action == self.close:
                if self.current_state_num >= self.to_state_num + (self.action * self.initial_num):
                    self.run_anim = False
                pass                 
            if self.door_type == self.deslizante:
                if self.stop:
                    self.object.position.x = self.to_state_num + self.initial_num
                    print("Current:", self.object.position.x )
                    return
                    pass
                self.object.applyMovement([(self.move_speed * self.action), 0, 0], True)
                self.current_state_num = self.object.position.x
                pass
            elif self.door_type == self.normal:


                self.current_state_num = self.object.localOrientation.to_euler().z - self.initial_num
                pass

            pass
        pass
    pass