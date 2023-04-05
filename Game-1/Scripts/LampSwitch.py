from bge import *

from collections import OrderedDict

class Switch(types.KX_PythonComponent):

    args = OrderedDict([
        ("Type", {"Button Click", "Button Rotate"}),
        ("Lamp Object Name", "")
    ])

    def start(self, args):
        self.args = args
        self.lamp : types.KX_GameObject = logic.getCurrentScene().lights[args["Lamp Object Name"]]
        pass

    def update(self):
        pass

    # Função de chamada principal, evitando que quando haja interação de tecla
    # (Clique do "E", por padrão) não haja várias condições para verificar que
    # objeto é esse. Sempre chame startComponent() e dentro da startComponent() faça tudo que for
    # necessário antes de chamar a função que realmente fará tudo.
    
    def startComponent(self):
        self.switchLamp()
        pass

    def switchLamp(self):
        self.lamp.setVisible(not self.lamp.visible)
        pass

    pass