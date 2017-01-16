# _*_coding:utf-8_*_

import os,sys,time,random
import pygame
from imgcrap import *
from tool import *

SCREEN_W,SCREEN_H = 640,500
MARGIN_BTW_PIC = 0

GAME_START=False

PIC_NUM = 0
PIC_INDEX = 0

DIVISION_NUM = 0#默认

#坐标，答案，位置
LOCATION_DICT={}
ANSWERS=[]
ABS_LOCATION_DICT={}

REFER_MARGIN_T = 0
REFER_PIC_SIZE=(0,0)

#打乱次数
MIX_TIMES = 30

#声音背景音乐
SOUND_SWITCH_ON = True

#成绩
SCORE = 0


#模块初始化
pygame.init()
#定义窗口标题
screencaption=pygame.display.set_caption('拼图游戏')

#定义窗口大小
screen=pygame.display.set_mode([SCREEN_W,SCREEN_H])

#用白色填充窗口
screen.fill([255,255,255])
#music
pygame.mixer.init()

#点击
click = pygame.mixer.Sound("resources/audio/click1.wav")
click.set_volume(0.05)

success = pygame.mixer.Sound('resources/audio/success.wav')
success.set_volume(0.25)
#back_ground_music
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.set_volume(0.25)

#--------------------------------更新屏幕内容
def update_fresh_screen_content():
	''' 1:开始按钮
		2：next按钮
		3：音乐btn
		4: 分数显示
	'''
	#请屏幕
	screen.fill([255,255,255])
	#添加按钮--start
	start_im = pygame.image.load('start_btn.jpg')
	screen.blit(start_im,(15,40))
	#添加按钮--next
	next_im = pygame.image.load('next_btn.jpg')
	screen.blit(next_im,(15,140))
	#添加背景音乐按钮
	set_sound_switch_btn()
	#显示分数
	time_label ='Score: '+str(SCORE)
	show_text(screen,(SCREEN_W-80,REFER_MARGIN_T),time_label,(0,255,255),True,20)

#---------------------------------------------------------------------更新游戏图片
def load_next_game(pic_path,division_num):
	global SCREEN_W,SCREEN_H,LOCATION_DICT ,ABS_LOCATION_DICT,ANSWERS
	#更新屏幕内容
	update_fresh_screen_content()
	#1.确定需要进行拼图的图片
	#2.根据division_num和参考图片的大小计算切割的图片的大小cut_size
	pic_width,pic_height = REFER_PIC_SIZE[0]/division_num,REFER_PIC_SIZE[1]/division_num
	cut_size = (pic_width,pic_height)
	#切割图片
	division_pic(pic_path,cut_size,division_num)
	#打乱顺序
	tmp_dict={}
	if division_num == 3:
		for k,v in config_dict[3].items():tmp_dict[k]=v
	else:
		for k,v in config_dict[4].items():tmp_dict[k]=v

	mixed_result = mix_dict(MIX_TIMES,tmp_dict,division_num)
	LOCATION_DICT,ANSWERS = mixed_result[0],mixed_result[1]
	#修正答案--3次
	answers1 = update_answer(ANSWERS)
	answers2 = update_answer(answers1)
	ANSWERS = update_answer(answers2)
	print ANSWERS
	#加载参考图片
	#REFER_MARGIN_T = 40
	refer_pic_location= ((SCREEN_W-REFER_PIC_SIZE[0])/2,REFER_MARGIN_T)
	refer_im = Image.open(pic_path)
	refer_im.thumbnail(REFER_PIC_SIZE,Image.ANTIALIAS)
	refer_im.save(os.path.join('resources/images','refer.png'),'png')
	refer_img = pygame.image.load(os.path.join('resources/images','refer.png'))
	screen.blit(refer_img,refer_pic_location)

	#创建可移动的图片‘0.png’
	#静态0.png
	#create_b_img((pic_width,pic_height),'0',color=(255,255,255))

	#随机o.png
	get_mobile_pic = 'resources/images/mobile'+str(random.randint(1,11))+'.jpg'
	create_thumnail(get_mobile_pic,(pic_width,pic_height),'0')

	#拼图区域margin_left
	margin_left = (SCREEN_W-division_num*pic_width-(division_num-1)*MARGIN_BTW_PIC)/2
	
	#拼图区域margin_top = 屏幕H-距离底部距离(=REFER_MARGIN_T)-division_num*MARGIN_BTW_PIC-pic_height*division_num
	margin_top = SCREEN_H - REFER_MARGIN_T - division_num*MARGIN_BTW_PIC - pic_height*division_num
	#1.清空ABS_LOCATION_DICT
	ABS_LOCATION_DICT={}
	#跟新绝对位置
	update_abs_location_dict(division_num)
	
	#2加载背景图片
	#2.1设置背景图片大小
	back_pic_w=pic_width*division_num+(division_num+1)*MARGIN_BTW_PIC
	back_pic_h=pic_height*division_num+(division_num+1)*MARGIN_BTW_PIC

	#2.2创建背景图
	create_b_img((back_pic_w,back_pic_h),'back_color_pic')
	back_groud_pic = pygame.image.load('resources/images/back_color_pic.png')
	screen.blit(back_groud_pic,(margin_left-1,margin_top-1))

	#3.开始放置拼图，与背景图配合体现边框效果
	for i in range(0,division_num*division_num):
		name = os.path.join('resources/images',str(i)+'.png')
		#if i == 0:name = '0.png'
		pic_nail=pygame.image.load(name)
		pic_location=(margin_left+LOCATION_DICT[i][0]*(pic_width+1),margin_top+LOCATION_DICT[i][1]*(pic_height+1))
		screen.blit(pic_nail,pic_location)
	
	#刷新界面
	pygame.display.flip()


#---------------------------------------------------------------处理声音按钮
def set_sound_switch_btn():
	if SOUND_SWITCH_ON:
		sound_switch_im = pygame.image.load('resources/images/soundon.png')
		pygame.mixer.music.play(-1, 0.0)
	else:
		sound_switch_im = pygame.image.load('resources/images/soundoff.png')
		pygame.mixer.music.pause()
	screen.blit(sound_switch_im,(305,470))
	

#---------------------------------------初始化----------------------------------------------------------
def game_init():

	global MARGIN_BTW_PIC,SELECT_FINISH,PIC_INDEX,PIC_NUM,DIVISION_NUM,SCREEN_W,SCREEN_H,REFER_MARGIN_T,REFER_PIC_SIZE,SOUND_SWITCH_ON

	#小图片之间的间隔
	MARGIN_BTW_PIC = 1
	#游戏图片参数
	PIC_NUM = 0
	PIC_INDEX = 1
	#默认模式3*3
	DIVISION_NUM = 3
	#参考图设置
	REFER_MARGIN_T = 40
	REFER_PIC_SIZE = (320,200)

	#全局音效
	SOUND_SWITCH_ON = True
	#分数
	SCORE = 0


	#游戏图片选择完成标志
	GAME_START=False
	#更新游戏图片数目
	for i in os.listdir('resources/images'):
		if i.startswith('pic'):PIC_NUM = PIC_NUM+1
		#当前的游戏图片索引
	PIC_INDEX = 1

	update_fresh_screen_content()

	#加载第一张有图片
	load_next_game('resources/images/pic1.jpg',DIVISION_NUM)

def update_abs_location_dict(division_num):
	global SCREEN_W,SCREEN_H,ABS_LOCATION_DICT

	#根据division_num和参考图片的大小
	pic_width,pic_height = REFER_PIC_SIZE[0]/division_num,REFER_PIC_SIZE[1]/division_num
	#拼图区域margin_left
	margin_left = (SCREEN_W-division_num*pic_width-(division_num-1)*MARGIN_BTW_PIC)/2
	#拼图区域margin_top = 屏幕H-距离底部距离(=REFER_MARGIN_T)-division_num*MARGIN_BTW_PIC-pic_height*division_num
	margin_top = SCREEN_H - REFER_MARGIN_T - division_num*MARGIN_BTW_PIC - pic_height*division_num
	
	for k,v in LOCATION_DICT.items():
		v_x,v_y = v[0],v[1]
		rect_l = margin_left+MARGIN_BTW_PIC*(v_x+1)+v_x*pic_width
		rect_r = margin_left+MARGIN_BTW_PIC*(v_x+1)+(v_x+1)*pic_width
		rect_u = margin_top+MARGIN_BTW_PIC*(v_y+1)+v_y*pic_height
		rect_b = margin_top+MARGIN_BTW_PIC*(v_y+1)+(v_y+1)*pic_height
		ABS_LOCATION_DICT[k] = (rect_l,rect_u,rect_r,rect_b)
	#print 'after ABS_LOCATION_DICT',ABS_LOCATION_DICT
	
def pressed_croppic(pos):
	'''find press k'''
	pos_x,pos_y = pos[0],pos[1]
	for k1,rect in ABS_LOCATION_DICT.items():
		if rect[0]<=pos_x<=rect[2] and rect[1]<=pos_y<=rect[3]:
			print '点击了:',k1
			#return k1
			exchange_location(k1)

def exchange_location(croppic_key):
	#判断是否有效key
	global LOCATION_DICT
	if LOCATION_DICT[croppic_key][0] == LOCATION_DICT[0][0] or  LOCATION_DICT[croppic_key][1] == LOCATION_DICT[0][1]:
		#print '开始交换'
		tmp_loc = LOCATION_DICT[0]
		LOCATION_DICT[0] = LOCATION_DICT[croppic_key]
		LOCATION_DICT[croppic_key] = tmp_loc
		#print '交换后:',LOCATION_DICT
		#更新绝对位置
		update_abs_location_dict(DIVISION_NUM)
		#-------------------------------------刷新-----------------------------------
		#开始放置拼图，与背景图配合体现边框效果
		pic_width,pic_height = REFER_PIC_SIZE[0]/DIVISION_NUM,REFER_PIC_SIZE[1]/DIVISION_NUM
		margin_left = (SCREEN_W-DIVISION_NUM*pic_width-(DIVISION_NUM-1)*MARGIN_BTW_PIC)/2
		margin_top = SCREEN_H - REFER_MARGIN_T - DIVISION_NUM*MARGIN_BTW_PIC - pic_height*DIVISION_NUM

		for i in range(0,DIVISION_NUM*DIVISION_NUM):
			name = os.path.join('resources/images',str(i)+'.png')
			#if i == 0:name = '0.png'
			pic_nail=pygame.image.load(name)
			pic_location=(margin_left+LOCATION_DICT[i][0]*(pic_width+1),margin_top+LOCATION_DICT[i][1]*(pic_height+1))
			#print i,pic_location
			screen.blit(pic_nail,pic_location)
		pygame.display.flip()
	else:pass#print '无需交换'


#-------------------------------------------main-------------------------------------------------------
#游戏初始化
print u'初始化游戏界面...'
game_init()
deal_success_flag = True
while True:
	#处理胜利
	if LOCATION_DICT == config_dict[DIVISION_NUM] and deal_success_flag == False:
		success.play();
		SCORE = SCORE +1
		#更新内容(几个按钮)
		update_fresh_screen_content()
		deal_success_flag = True;
		#自动进入下一张
		DIVISION_NUM = random.randint(3,4)
		PIC_INDEX += 1
		load_next_game('resources/images/pic'+str(PIC_INDEX)+'.jpg',DIVISION_NUM)
		
	for event in pygame.event.get():
		#退出事件
		if event.type == pygame.QUIT:sys.exit()

		#页面点击	
		elif event.type==pygame.MOUSEBUTTONDOWN:#next 和start可以激活屏幕
			#音效
			if SOUND_SWITCH_ON:click.play()
			#-------------------------------------------背景音乐操作o
			if 305<=event.pos[0]<=305+30 and SCREEN_H-30<=event.pos[1]<SCREEN_H:#点击了音效
				SOUND_SWITCH_ON = not SOUND_SWITCH_ON
				set_sound_switch_btn()
				pygame.display.flip()
			#------------------------------------------start
			if 15<=event.pos[0]<=15+135 and 40<=event.pos[1]<=40+60:
				GAME_START = True;continue
			#-------------------------------------------next
			elif 15<=event.pos[0]<=15+135 and 140<=event.pos[1]<=140+60:
				print 'next'
				PIC_INDEX = PIC_INDEX+1
				if PIC_INDEX >PIC_NUM:
					print 'no more girls...back'
					PIC_INDEX = 1
					continue 
				DIVISION_NUM = random.randint(3,4)
				load_next_game('resources/images/pic'+str(PIC_INDEX)+'.jpg',DIVISION_NUM)

			elif 159<=event.pos[0]<=159+322 and 259<=event.pos[1]<=259+202:
				if GAME_START == True:
					#print u'开始游戏'
					pressed_croppic(event.pos)
					#------------------------防止刷分
					deal_success_flag = False






