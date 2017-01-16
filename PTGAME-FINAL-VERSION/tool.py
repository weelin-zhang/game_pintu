# _*_coding:utf-8_*_

import Image,pygame
import random





#修正答案
def update_answer(answer_l):
	i,flag=0,0
	newl=[]
	while i<len(answer_l):

		if i == len(answer_l)-1:newl.append(answer_l[i]);break

		if answer_l[i] == 'down' and answer_l[i+1]=='top' or answer_l[i] == 'top' and answer_l[i+1]=='down':
			flag = 1
		elif answer_l[i] == 'right' and answer_l[i+1]=='left' or answer_l[i] == 'left' and answer_l[i+1]=='right':
			flag = 1

		else:
			 flag = 0

		if flag == 1:
			if i+2 <= len(answer_l):
				i = i+2
			else:
				break
		else:
			newl.append(answer_l[i]);i=i+1

	return newl



def create_b_img(size,name,color=(0,255,0),mode='RGBA'):
	random_num_r,random_num_g,random_num_b = random.randint(1,5),random.randint(1,5),random.randint(1,5)
	color = (random_num_r*30+100,random_num_g*30+100,random_num_b*30+100)
	'''(255,0,0)---->red
		(0,255,0)--->green
		(0,0,255)---->blue
	'''
	newImg = Image.new(mode,size,color)
	newImg.save('resources/images/'+name+'.png','PNG')

# create_img(pic_mode,(242,152),'background_red',(0,0,255))
# create_img(pic_mode,(242,152),'background_green',(0,255,0))
# create_img(pic_mode,(242,152),'background_blue',(255,0,0))



def create_thumnail(image,thumsize,thumbnailname):
	'''image----绝对路径
	'''
	tmp_im = Image.open(image)
	tmp_im_rate = tmp_im.size[0]/(tmp_im.size[1]*1.0)
	if thumsize[0]/(thumsize[1]*1.0) != tmp_im_rate:
		max_size_of_thumsize = max(thumsize)
		if tmp_im_rate >=1:
			tmp_im_thumnail_w,tmp_im_thumnail_h = int(tmp_im_rate*max_size_of_thumsize),int(max_size_of_thumsize)
		else:
			tmp_im_thumnail_w,tmp_im_thumnail_h = int(max_size_of_thumsize),int(max_size_of_thumsize/tmp_im_rate)	
			
		tmp_im.thumbnail((tmp_im_thumnail_w,tmp_im_thumnail_h),Image.ANTIALIAS)
		cropbox = ((tmp_im_thumnail_w-thumsize[0])/2,(tmp_im_thumnail_h-thumsize[1])/2,(tmp_im_thumnail_w-thumsize[0])/2+thumsize[0],(tmp_im_thumnail_h-thumsize[1])/2+thumsize[1])
		tmp_im = tmp_im.crop(cropbox)
	else:tmp_im.thumbnail(thumsize,Image.ANTIALIAS);
	try:
		tmp_im.save('resources/images/'+thumbnailname+'.png','jpeg')
	except:
		print 'error'
		tmp_im.save('resources/images/'+thumbnailname+'.png','png')
	



#显示文字

def show_text(surface_handle, pos, text, color, font_bold = False, font_size = 20, font_italic = False):   
    ''''' 
    Function:文字处理函数 
    Input：surface_handle：surface句柄 
           pos：文字显示位置 
           color:文字颜色 
           font_bold:是否加粗 
           font_size:字体大小 
           font_italic:是否斜体 
    Output: NONE 
    author: socrates 
    blog:http://blog.csdn.net/dyx1024 
    date:2012-04-15 
    '''         
    #获取系统字体，并设置文字大小  
    cur_font = pygame.font.SysFont("宋体", font_size)  
      
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)  
      
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)  
      
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
      
    #绘制文字  
    surface_handle.blit(text_fmt, pos)    