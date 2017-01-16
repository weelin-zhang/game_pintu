#_*_ coding:utf-8 _*_

import Image
import time,os,random

config_dict = {
					3:
					{
						1:(0,0),
						2:(1,0),
						3:(2,0),
						4:(0,1),
						5:(1,1),
						6:(2,1),
						7:(0,2),
						8:(1,2),
						0:(2,2)
					},
					4:
					{
						1:(0,0),
						2:(1,0),
						3:(2,0),
						4:(3,0),
						5:(0,1),
						6:(1,1),
						7:(2,1),
						8:(3,1),
						9:(0,2),
						10:(1,2),
						11:(2,2),
						12:(3,2),
						13:(0,3),
						14:(1,3),
						15:(2,3),
						0:(3,3)
					}
					
				}

num_direction_map = {0:'top',1:'down',2:'left',3:'right'}

route = []
back_route = []
fuck = []
#切割图片
def division_pic(image,cut_size,division_num=3):
	im = Image.open(image)
	sub_width,sub_eight = im.size[0]/division_num,im.size[1]/division_num
	for row in range(0,division_num):
		for col in range(0,division_num):
			sub_l,sub_u,sub_r,sub_b = col*sub_width,row*sub_eight,(col+1)*sub_width,(row+1)*sub_eight
			sub_box = (sub_l,sub_u,sub_r,sub_b)
			im_crop = im.crop(sub_box)
			im_crop.thumbnail(cut_size,Image.ANTIALIAS)
			im_crop.save(os.path.join(os.path.dirname(image),str(row*division_num+col+1)+'.png'),'PNG')


def moveOneStep(direction,division_num,tmp_dict,key=0):
	
	'''division_num-----行、列
		loc_dict--------位置字典
		key-------------移动的对象
		direction-------left,top,right,down
		返回----移动后的字典
	'''
	global route,back_route,fuck
	hor_limit,ver_limit = division_num-1,division_num-1
	fuck.append(direction)
	#判断是否可以移动
	#print tmp_dict[key] #打乱历程
	if direction == 'top':
		if tmp_dict[key][1] == 0:return tmp_dict
		move_before = tmp_dict[key]
		move_after = (tmp_dict[key][0],tmp_dict[key][1] - 1)

	elif direction == 'down':
		if tmp_dict[key][1] == ver_limit:return tmp_dict
		move_before = tmp_dict[key]
		move_after = (tmp_dict[key][0],tmp_dict[key][1] + 1)

	elif direction == 'left':
		if tmp_dict[key][0] == 0:return tmp_dict
		move_before = tmp_dict[key]
		move_after = tmp_dict[key][0]-1,tmp_dict[key][1]
		
	elif direction == 'right':
		if tmp_dict[key][0] == hor_limit:return tmp_dict
		move_before = tmp_dict[key]
		move_after = (tmp_dict[key][0]+1,tmp_dict[key][1])

	#记录路径
	route.append(direction)
	#生成答案

	if direction == 'top':back_direction = 'down'
	elif direction == 'down':back_direction ='top'
	elif direction == 'right':back_direction = 'left'
	elif direction == 'left':back_direction = 'right'
	back_route.append(back_direction)
	#更新location_dict
	#找到tmp_tuple对应的key
	for k,v in tmp_dict.items():
		if v == move_after:
			tmp_dict[k] = move_before
	#一定放下面
	tmp_dict[0]=move_after
	
	return tmp_dict
		

#打乱次序
def mix_dict(times,tmp_dict,division_num):
	'''返回打乱后的字典
	0-top
	1-down
	2-left
	3-right
	'''	
	# print '需要弄混乱的:',tmp_dict
	global fuck,route,back_route
	fuck,route,back_route=[],[],[]
	for i in range(0,times):
		direction = num_direction_map[random.randint(0,20)%4]
		tmp_dict_update = moveOneStep(direction,division_num,tmp_dict)
	
	# print 'fuck:',fuck
	# print '路由:',route
	# print '转置before:',back_route
	back_route.reverse()
	# print '转置after:',back_route
	# print 'mix_after:',tmp_dict_update
	return (tmp_dict_update,back_route)

# def test():
# 	#print 'ori:',location_dict
# 	#print u'开始切割'
# 	division_pic('resources/pic1.jpg',(106,67),3)
# 	mix_dict(5,config_dict[3],3)
# 	print '路由:',route
# 	print '回去的路由:',back_route


# if __name__ == '__main__':
# 	pass
# 	test()
