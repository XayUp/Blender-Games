import bge
from collections import OrderedDict

class AnimationClass(bge.types.KX_PythonComponent):

    args = OrderedDict([])

    def start(self, args):
        self.anim_data = self.object.childrenRecursive['weapon_bones'].components['WeaponData'].args
        self.player_armature: bge.types.KX_GameObject = self.object.childrenRecursive['Player_Armature']
        pass

    def update(self):
        pass

    def start_walk_forward(self):
        active_act_name = self.player_armature.getActionName()
        if active_act_name in self.anim_data['start_walk_sequence'].keys():
            index_act = list(self.anim_data["start_walk_sequence"]).index(active_act_name)
            current_act = self.anim_data["start_walk_sequence"][active_act_name]
            if self.player_armature.getActionFrame() >= current_act[1]:
                index_act += 1
                if index_act >= len(self.anim_data['start_walk_sequence']): index_act = 0
                play_act_name = list(self.anim_data['start_walk_sequence'].keys())[index_act]
                act = self.anim_data["start_walk_sequence"][play_act_name]
                self.player_armature.playAction(play_act_name, act[0], act[1], play_mode=act[2],)
                pass
            pass
        else:
            play_act_name = list(self.anim_data['start_walk_sequence'].keys())[0]
            act = self.anim_data["start_walk_sequence"][play_act_name]
            self.player_armature.playAction(play_act_name, act[0], act[1], play_mode=act[2])  
            pass
        pass

    def end_walk_back(self):
        act_name = self.player_armature.getActionName()
        pass

    def start_run(self):
        
        pass

    def end_run(self):

        pass

    pass