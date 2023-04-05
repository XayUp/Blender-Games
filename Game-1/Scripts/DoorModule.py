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

    def startComponent(self):
        self.args["Openned"] = not self.args["Openned"]
        self.openCloseDoor()
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
        ("move X Axis", {"X", "Y", "Z"}),
        ("Openned Num", 1.6), #Até onde deve ser aberta. Isso depende. Deslizante
        ("Closed Num", 0.0), #Até onde deve ser fechada. Isso depende. Deslizante
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
        self.use_axis = args["move X Axis"]
        self.axis_index: int = 0
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
        self.axis = [0, 0, 0]
        self.axis_index = self.__getAxisIndex()
        print(self.axis_index)
        pass

    def update(self):
        self.__animationDoor()
        pass

    # Função de chamada principal, evitando que quando haja interação de tecla
    # (Clique do "E", por padrão) não haja várias condições para verificar que
    # objeto é esse. Sempre chame startComponent() e dentro da startComponent() faça tudo que for
    # necessário antes de chamar a função que realmente fará tudo

    def startComponent(self): 
        self.args["Openned"] = not self.args["Openned"]
        self.__openCloseDoor()
        pass

    def __getAxisIndex(self) -> int:
        if self.use_axis == "Y": return 1
        elif self.use_axis == "Z": return 2
        else: return 0
        pass

    def __openCloseDoor(self):
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
        self.axis = [0, 0, 0]
        self.run_anim = True
        pass
    
    # Toda a porta deverá ter um parente próprio para, a partir da distância entre eles, fazer
    # os cálculos necessários para reprozuzir a animação

    def __animationDoor(self):
        if self.run_anim:
            move = self.move_speed
            self.current_state_num = self.object.getDistanceTo(self.pivot)
            if (self.current_state_num * self.action) - self.move_speed <= self.to_state_num * self.action:
                self.run_anim = False
                move = (self.current_state_num - self.to_state_num) * self.action
                pass
            self.axis[self.axis_index] = move * self.action
            print(self.axis)
            self.object.applyMovement(Vector(self.axis), True)
            pass
        pass
    pass