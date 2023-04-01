from bge import *
from collections import OrderedDict
from mathutils import Vector
from math import radians

class NormalDoor(types.KX_PythonComponent):
    args = OrderedDict([
        ("Openned Num", 90), #Até onde deve ser aberta. Isso depende. Normal (rotação Z)
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende.Normal (rotação Z)
        ("Speed of Movement", 0.01),
        ("Openned", False)
    ])

    def start(self, args):
        self.args = args
        #Finais
        self.open_num: float = radians(args["Openned Num"])                    # A Porta será aberta até esta rotação
        self.close_num: float = args["Closed Num"]                          # A Porta será fechada até essa rotação
        self.move_speed: float = args["Speed of Movement"]                  # Velocidade de movimento da porta
        self.pivot: types.KX_GameObject = self.object.parent                # A ditancia da porta ao pivot determina se ela já está abrta/fechada
        self.open: int = 1
        self.close: int = -1

        #Tipos de Variável
        self.object: types.KX_GameObject
        
        #Identificadores
        self.openned: bool = args["Openned"]
        
        #Propriedades
        self.to_state_num: float = 0
        self.current_state_num = 0

        #Controle
        self.action: int = 1 # -1 para fecha e 1 para abrir
        self.run_anim: bool = False #Definir True para iniciar a animacção
        pass

    def update(self):
        self.animationDoor()
        pass
    
    def openCloseDoor(self):
        if self.openned: #Se estiver Aberta
            self.openned = False
            self.args["Openned"] = False
            self.to_state_num = self.close_num
            self.action = self.close
            pass
        else:            #Se estiver Fechada
            self.openned = True
            self.args["Openned"] = True
            self.to_state_num = self.open_num
            self.action = self.open
            pass
        self.run_anim = True
        pass

    def animationDoor(self):
        if self.run_anim: 
            move = self.move_speed
            if (self.current_state_num * self.action) + self.move_speed >= self.to_state_num * self.action:
                self.run_anim = False
                move = (self.current_state_num - self.to_state_num) * -self.action
                pass
            self.object.applyRotation(Vector([0, 0, move * self.action]), True)
            self.current_state_num += move * self.action
            pass
        pass
        pass
    pass

class SlidingDoor(types.KX_PythonComponent):
   
    args = OrderedDict([
        ("Openned Num", 1.6), #Até onde deve ser aberta. Isso depende. Deslizante (movimento X)
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende. Deslizante (movimento X)
        ("Speed of Movement", 0.2),
        ("Openned", False)
        ])
    def start(self, args):
        self.args = args
        #Finais
        self.pivot: types.KX_GameObject = self.object.parent                # A ditancia da porta ao pivot determina se ela já está abrta/fechada
        self.open_num: float = args["Openned Num"]                          # A Porta será aberta até esta posição
        self.close_num: float = args["Closed Num"]                          # A Porta será fechada até essa posição
        self.move_speed: float = args["Speed of Movement"]                  # Velocidade de puxa/empurra da porta
        self.open: int = -1
        self.close: int = 1

        #Tipos de Variável
        self.object: types.KX_GameObject
        
        #Identificadores
        self.openned: bool = args["Openned"]
        
        #Propriedades
        self.to_state_num: float = 0
        self.current_state_num = 0

        #Controle
        self.action: int = 1 # -1 para fecha e 1 para abrir
        self.run_anim: bool = False #Definir True para iniciar a animacção

        pass

    def update(self):
        self.animationDoor()
        pass

    def openCloseDoor(self):
        if self.openned: #Se estiver Aberta
            self.openned = False
            self.args["Openned"] = False
            self.to_state_num = self.close_num
            self.action = self.close
            pass
        else:            #Se estiver Fechada
            self.openned = True
            self.args["Openned"] = True
            self.to_state_num = self.open_num
            self.action = self.open
            pass
        self.run_anim = True
        pass

    def animationDoor(self):
        if self.run_anim:
            move = self.move_speed
            self.current_state_num = self.object.getDistanceTo(self.pivot)
            if (self.current_state_num * self.action) - self.move_speed <= self.to_state_num * self.action:
                self.run_anim = False
                move = (self.current_state_num - self.to_state_num) * self.action
                pass
            self.object.applyMovement(Vector([move * self.action, 0, 0]), True)
            pass
        pass
    pass