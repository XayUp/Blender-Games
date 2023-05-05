import bge
from collections import OrderedDict
class AnimationClass(bge.types.KX_PythonComponent):

    args = OrderedDict([])

    def start(self, args):
        self.anim_data = self.object.childrenRecursive['weapon_bones'].components['WeaponData'].args
        print(self.anim_data)
        pass

    def update(self):

        pass

    pass