"""
@author：kaspar
@data: 201909
@project:play with wechat
@content：玩转微信
@description：做一些与你自己微信有关的好玩事情
"""
from intro import *
from process import *
import shutil
import os

if __name__ == '__main__':
    print(hello())
    choice,lists = choices()
    print(choice)

    while True:
        input_str = input('请选择游戏数字：')
        if input_str == 'z' or input_str == 'Z':
            avatar_dir = os.getcwd() + '\\avatar'
            if  os.path.exists(avatar_dir):
                shutil.rmtree(avatar_dir)
            break

        try:
            number = int(input_str)
            if number in  lists:
                process(number)
                print(choice)
            else:
                print("请输入正确数字{}！".format(lists))
        except:
            print("请输入数字！")
        
      


