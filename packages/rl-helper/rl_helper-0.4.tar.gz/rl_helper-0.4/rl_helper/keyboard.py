
from re import T
from pynput import keyboard
# import keyboard
# from keyboard import keyboard
import time
# from gym.utils import vi
# import cv2


class kb(object):
    """
    an interface for interact env with keyboard
    """
    def __init__(self,key2action:dict={'up':[1,0,0,0],"down":[-1,0,0,0]}) -> None:
        super().__init__()
        
        self.listener = keyboard.Listener(on_release=self.on_press,)
        self.last_action=None
        self.kew2action=key2action

    def on_press(self,key):
        print("received:",key)
        char=key.name if isinstance(key,keyboard.Key) else key.char
        action=self.kew2action.get(char,None)
        if action is None:
            print("input {} not supported in your key2action {}".format(key,self.kew2action.keys()))
        self.last_action=action
        # return False

    def start(self):
        self.listener.start()

    def get_action(self):
        while self.last_action is None:
            time.sleep(0.1)
        action=self.last_action
        self.last_action=None
        return action


class kbinteractor(object):
    def __init__(self,env,key2action:dict) -> None:
        super().__init__()
        # self.k=
        self.env=env
        self.kb=kb(key2action=key2action)
        self.run()
    def run(self):
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots()

        self.env.reset()
        img=self.env.render("rgb_array")
        ax.cla()
        ax.imshow(img)
        plt.pause(0.1)
        self.env.reset()
        self.kb.start()
        while True:
            obs,rew,dones,info=self.env.step(self.kb.get_action())
            print('rew',rew)
            if dones:
                self.env.reset()
            img=self.env.render("rgb_array")
            ax.cla()
            ax.imshow(img)
            plt.pause(0.1)

if __name__=="__main__":

    import gym
    interactor=kbinteractor(env=gym.make('FetchPickAndPlaceDense-v1'),
            key2action={
                    'right':[1,0,0,0],
                    'left':[-1,0,0,0],
                    'up':[0,1,0,0],
                    'down':[0,-1,0,0],
                    "y":[0,0,1,0],
                    "h":[0,0,-1,0],
                    "n":[0,0,0,1],
                    "b":[0,0,0,-1],
                })