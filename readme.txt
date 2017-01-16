一个基于pygame的拼图游戏。
1.支持随机3*3,4*4,
2.支持音效,音效可选择关闭.
3.记录得分数
4.游戏开始自动生成答案（没有移动之前的答案）

界面上三个按键START，NEXT和以个声音标识

点击START开始游戏，否则游戏区（点击区）点击无反应

当拼图完成且正确时，自动切换下一素材

点击NEXT时强制切换新素材


新素材图片可以放到resoureces/images中，以pic+数字命名eg:pic1,...,pic11


模块:
import os,sys,time,random
import Image,pygame


