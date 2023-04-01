from bge import *
from collections import OrderedDict
from mathutils import Vector

class NormalDoor(types.KX_PythonComponent):
    args = OrderedDict([
        ("Openned Num", -90), #Até onde deve ser aberta. Isso depende. Normal (rotação Z)
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende.Normal (rotação Z)
        ("Openned", False)
    ])

    def start(self, args):

        pass

    def update(self):

        pass
    
    def openCloseDoor(self):
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
            
            pass
        pass
    pass

class SlidingDoor(types.KX_PythonComponent):
   
    args = OrderedDict([
        ("Openned Num", -1.6), #Até onde deve ser aberta. Isso depende. Deslizante (movimento X)
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende. Deslizante (movimento X)
        ("Openned", False)
        ])
    def start(self, args):
        self.args = args
        #Finais
        self.open_num: float = args["Openned Num"] + self.object.position.x # A Porta será aberta até esta posição
        self.close_num: float = self.object.position.x                      # A Porta será fechada até essa posição
        self.move_speed: float = 0.05                                       # Velocidade de puxa/empurra da porta
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
            self.current_state_num = self.object.worldPosition + (self.object.worldOrientation * Vector([0, 0, 0]))
            print(self.current_state_num)
            self.run_anim = False
            return
            if self.action == self.open:
                pass
            elif self.action == self.close:

                pass
            pass
        pass
    pass