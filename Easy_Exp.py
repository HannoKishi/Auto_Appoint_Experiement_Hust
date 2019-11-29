from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys #需要引入 keys 包
from selenium.webdriver.support.select import Select  ## select 搜索包
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import requests  
import lxml
from io import BytesIO
from bs4 import BeautifulSoup 
import pytesseract ## 要下的包
from PIL import Image,ImageEnhance,ImageOps,ImageFilter
import time
##打开浏览器 使用相应版本的谷歌chrome
def open_webdriver():
    opt=Options()  ##创建参数对象
    #opt.add_argument('--headless')  #无界面化
    #opt.add_argument('--disable-gpu')  #取消gpu
    opt.add_argument('--window-size=1080,720') #窗口大小
    url="http://wn-wnlo.hust.edu.cn/wn/login/?next=/wn/"
    driver=webdriver.Chrome(options=opt)
    driver.get(url)
    return driver

## 验证密码正确与错误与否
def correct_password(username_ui,password_ui):
    opt=Options()  ##创建参数对象
    opt.add_argument('--headless')  #无界面化
    #opt.add_argument('--disable-gpu')  #取消gpu
    #opt.add_argument('--window-size=1080,720') #窗口大小
    url="http://wn-wnlo.hust.edu.cn/wn/login/?next=/wn/"
    driver=webdriver.Chrome(options=opt)
    driver.get(url)
    ## 需要增加是否在当前界面判断
    try:
        submit=driver.find_element_by_class_name('submit-row')
        WebDriverWait(driver,10,0.1).until(EC.visibility_of((submit)))
        print('登陆页面页面存在')
    except:
        print('登陆页面不存在')
        ##可以增加推出等等异常模块判断
    ##
    user=driver.find_element_by_id('id_username')   ##账号
    user.send_keys(username_ui)
    password=driver.find_element_by_id('id_password')  ##密码
    password.send_keys(password_ui)
    password.send_keys(Keys.ENTER)  
    ## 增加登陆成功与否判断
    try:
        add=driver.find_element_by_class_name('addlink')
        WebDriverWait(driver,5,0.5).until(EC.visibility_of((add)))
        print('add页面页面存在')
    except:
        add=None
        print('add页面不存在')
        ##可以增加推出等等异常模块判断
    ##
    return add
## 登陆
def login_next(driver,username_ui,password_ui):
    ## 需要增加是否在当前界面判断
    try:
        submit=driver.find_element_by_class_name('submit-row')
        WebDriverWait(driver,10,0.1).until(EC.visibility_of((submit)))
        print('登陆页面页面存在')
    except:
        print('登陆页面不存在')
        ##可以增加推出等等异常模块判断
    ##
    user=driver.find_element_by_id('id_username')   ##账号
    user.send_keys(username_ui)
    password=driver.find_element_by_id('id_password')  ##密码
    password.send_keys(password_ui)
    password.send_keys(Keys.ENTER)  
    ## 增加登陆成功与否判断

## 进入预约界面
def add_exp(driver):
    ## 需要增加是否在当前界面判断
    try:
        add=driver.find_element_by_class_name('addlink')
        WebDriverWait(driver,10,0.1).until(EC.visibility_of((add)))
        print('add页面页面存在')
    except:
        print('add页面不存在')
        ##可以增加推出等等异常模块判断
    ##
    add_experiment=driver.find_element_by_class_name('addlink')
    add_experiment.click()

## 填写预约信息
def fill_info(driver,device_value,exp_info,appointer,exp_data,time_start,time_end,ebl_1,ebl_2):
    ## ## 需要增加是否在当前界面判断
    try:
        submit=driver.find_element_by_class_name('submit-row')
        WebDriverWait(driver,10,0.1).until(EC.visibility_of((submit)))
        print('info页面页面存在')
    except:
        print('info页面不存在')
        ##可以增加推出等等异常模块判断
    ##
    ## 开始填表
    ## 先找下拉菜单
    sel=driver.find_element_by_id("id_device")
    Select(sel).select_by_value(device_value)
    ##print(sel)
    ## 填写实验描述
    man=driver.find_elements_by_class_name('vTextField')
    man[0].send_keys(exp_info)
    man[1].send_keys(appointer)
    ##  填写时间
    driver.find_element_by_class_name('vDateField').send_keys(exp_data)
    ## 填写time
    time_s_e=driver.find_elements_by_class_name('vTimeField')
    time_s_e[0].send_keys(time_start)
    time_s_e[1].send_keys(time_end)
    ## 人数与备注有待填写
    ## EBL参数填写
    if device_value=='6':
        driver.find_element_by_id('fieldsetcollapser0').click()
        ebl1_text=driver.find_element_by_id('id_count_taoke')
        ebl1_text.clear()
        ebl1_text.send_keys(ebl_1)
        ebl2_text=driver.find_element_by_id('id_count_untaoke')
        ebl2_text.clear()
        ebl2_text.send_keys(ebl_2)
    ## 验证码保存与识别加填写
    crack_code(driver)
    driver.find_element_by_class_name('default').click()  ##点击保存


def crack_code(driver):
    current_html=driver.page_source
    soup=BeautifulSoup(current_html,'lxml') #用当前的 html 创建beautifulsoup4 对象
    item=soup.select('img') ## 找到了图像
    ## 用request去爬界面
    pic_html=requests.get('http://wn-wnlo.hust.edu.cn'+item[4].get('src'))
    ## 保存图像 二进制？
    img_new=Image.open(BytesIO(pic_html.content))
    img_new.save('captcha_new.png')
    #.crop((0,0,200,70)
    image = Image.open('captcha_new.png')  ##打开图片
    #width=image.size[0]
    #image=image.crop((0,0,width,70))
    image=image.filter(ImageFilter.GaussianBlur)
    #增加对比度
    pocEnhance = ImageEnhance.Contrast(image)
    #增加255%对比度
    imgOriImg = pocEnhance.enhance(2.0)
    #锐化
    #pocEnhance = ImageEnhance.Sharpness(imgOriImg)
    #锐化200%
    #imgOriImg = pocEnhance.enhance(2.0)
    #增加亮度
    #pocEnhance = ImageEnhance.Brightness(imgOriImg)
    #增加200%
    #imgOriImg = pocEnhance.enhance(2.0)
    ## 高斯模糊
    #imgOriImg=imgOriImg.filter(ImageFilter.GaussianBlur)
    #变成灰度
    imgry = imgOriImg.convert('L')
    table=get_bin_table()
    binary = imgry.point(table,'1')
    noise_point_list = collect_noise_point(binary)
    remove_noise_pixel(binary, noise_point_list)
    ## 高斯模糊
    #remove_noise_pixel(binary, noise_point_list) 
    #binary=binary.filter(ImageFilter.GaussianBlur)
    code = pytesseract.image_to_string(binary).strip()#读取验证码
    binary.save('captcha_new.png')
    #print(code)#输出验证码
    code=code.replace(' ','')
    # 字母J 容易识别出错成为} ]
    code=code.replace('}','J')
    code=code.replace(']','J')
    code=code.upper()
    print(code)#输出验证码
    driver.find_element_by_id('id_captcha_1').send_keys(code)  #输入验证码


def get_bin_table(threshold=10):
	'''
	获取灰度转二值的映射table
	0表示黑色,1表示白色
	'''
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	return table

def sum_9_region_new(img, x, y):
	'''确定噪点 '''
	cur_pixel = img.getpixel((x, y))  # 当前像素点的值
	width = img.width
	height = img.height
 
	if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
		return 0
 
	# 因当前图片的四周都有黑点，所以周围的黑点可以去除
	if y < 3:  # 本例中，前两行的黑点都可以去除
		return 1
	elif y > height - 3:  # 最下面两行
		return 1
	else:  # y不在边界
		if x < 3:  # 前两列
			return 1
		elif x == width - 1:  # 右边非顶点
			return 1
		else:  # 具备9领域条件的
			sum = img.getpixel((x - 1, y - 1)) \
				  + img.getpixel((x - 1, y)) \
				  + img.getpixel((x - 1, y + 1)) \
				  + img.getpixel((x, y - 1)) \
				  + cur_pixel \
				  + img.getpixel((x, y + 1)) \
				  + img.getpixel((x + 1, y - 1)) \
				  + img.getpixel((x + 1, y)) \
				  + img.getpixel((x + 1, y + 1))
			return 9 - sum
 
def collect_noise_point(img):
	'''收集所有的噪点'''
	noise_point_list = []
	for x in range(img.width):
		for y in range(img.height):
			res_9 = sum_9_region_new(img, x, y)
			if (0 < res_9 < 3) and img.getpixel((x, y)) == 0:  # 找到孤立点
				pos = (x, y)
				noise_point_list.append(pos)
	return noise_point_list
 
def remove_noise_pixel(img, noise_point_list):
	'''根据噪点的位置信息，消除二值图片的黑点噪声'''
	for item in noise_point_list:
		img.putpixel((item[0], item[1]), 1)


## main
'''
driver=open_webdriver()
login_next(driver)
add_exp(driver)
fill_info(driver)
'''
## 循环
'''
while driver.find_element_by_class_name('errornote'):
    try:
        submit=driver.find_element_by_class_name('submit-row')
        WebDriverWait(driver,10,0.1).until(EC.visibility_of((submit)))
        print('info页面页面存在')
    except:
        print('info页面不存在')
        ##可以增加推出等等异常模块判断
    crack_code(driver)
    #time.sleep(2)
    driver.find_element_by_class_name('default').click()  ##点击保存

'''