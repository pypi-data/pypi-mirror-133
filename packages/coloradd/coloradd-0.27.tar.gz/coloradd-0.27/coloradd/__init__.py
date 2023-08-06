"""
   This is the color increase command that matches the turtle drawing command.
   颜色增加与颜色设定命令,用来在海龟画图中做颜色渐变。
   作者:李兴球 2021/1/8更新
   本程序定义了四个函数，coloradd是用来增加颜色的，参数为RGB的255三元组颜色和一个小数。
   colorset是把一个整数转换成rgb三元色值。
   brightset命令用来设置RGB的255三元组颜色的亮度。
   saturationset命令用来设置RGB的255三元组颜色的饱和度。
   0.27版本主要增加了lerpcolor命令,用来返回过渡颜色
"""
__version__ = 0.27
__author__ = "lixingqiu"
__blog__ = "www.lixingqiu.com"
__date__ = '2022/1/8'

import colorsys

def lerp(fromN,toN,amt):
    """在两个数之间插入一个数,amt是0.0到1.0之间的小数."""
    return fromN + (toN - fromN) * amt

def rgb2int(r,g,b):
    return r*256**2 + g*256 + b

def int2rgb(RGBint):
    b =  RGBint & 255
    g = (RGBint >> 8) & 255
    r =   (RGBint >> 16) & 255
    return r,g,b

def lerpcolor_int(color1,color2,amt):
    """color1:rgb颜色1,如(255,0,0),color2:rgb颜色2,amt:0.0到1.0的小数"""
    n1 =rgb2int(*color1)
    n2 =rgb2int(*color2)
    n = int(lerp(n1,n2,amt))
    return int2rgb(n)
    
def lerpcolor(color1,color2,amt):
    """color1:rgb颜色1,如(255,0,0),color2:rgb颜色2,amt:0.0到1.0的小数"""
    h1,s1,v1 = colorsys.rgb_to_hsv(color1[0]/255,color1[1]/255,color1[2]/255)
    h2,s2,v2 = colorsys.rgb_to_hsv(color2[0]/255,color2[1]/255,color2[2]/255)
     
    h = lerp(h1,h2,amt)  
    s = lerp(s1,s2,amt)   
    v = lerp(v1,v2,amt)
    # 下面是透明度线性插值
    color1len = len(color1)
    color2len = len(color2)    
    if color1len>3:
        a1 = color1[3]
    else:
        a1 = 255
    if color2len>3:
        a2 = color2[3]
    else:
        a2 = 255
    a = lerp(a1,a2,amt)
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    if color1len==3 and color1len==3:
        return int(r*255),int(g*255),int(b*255)
    return int(r*255),int(g*255),int(b*255),a       
    
def coloradd(color,dh):
    """color：three tuple color value，example：(255,255,0)，
       dh：0-1.0       
       此函数把颜色转换成hls模式,对色度h进行增加色度dh的操作
       然后转换回去,dh是小于1的浮点数。
       return three tuple color
    """
    if len(color)==3 :
        h,l,s, = colorsys.rgb_to_hls(color[0]/255,color[1]/255,color[2]/255)
        h =  h + dh
        r,g,b = colorsys.hls_to_rgb(h,l,s)
        return int(r*255),int(g*255),int(b*255)
    else:
        return color
addcolor = coloradd   # define alias name 定义别名

def colorset(color):
    """color：a integer from 1 to 360
       turn a integer to three tuple color value
       把一个整数转换成三元颜色值,返回三元组。
    """
    color = color % 360
    color = color / 360.0    
    r,g,b = colorsys.hsv_to_rgb(color,1.0,1.0)
    
    return int(r*255),int(g*255),int(b*255)
    
setcolor = colorset    # define alias name 定义别名

def brightset(color,light):
    """亮度设置函数
       color:这是RGB255三元组
       light:这是一个从0到1之间小数,值越大亮度越大
       返回RGB255 颜色三元组
    """
    if len(color)==3 :
        h,l,s, = colorsys.rgb_to_hls(color[0]/255,color[1]/255,color[2]/255)
        r,g,b = colorsys.hls_to_rgb(h,light,s)
        r = min(int(r * 255),255)
        g = min(int(g * 255),255)
        b = min(int(b *255),255)
        return max(0,r),max(0,g),max(0,b)
    else:
        return color
lightset = brightset
setbright = brightset

def saturationset(color,baohedu):
    """亮度设置函数
       color:这是RGB255三元组
       baohedu:这是一个从0到1之间小数,值越大饱和度越大,
       返回RGB255 颜色三元组
    """
    if len(color)==3 :
        h,l,s, = colorsys.rgb_to_hls(color[0]/255,color[1]/255,color[2]/255)
        r,g,b = colorsys.hls_to_rgb(h,l,baohedu)
        r = min(int(r * 255),255)
        g = min(int(g * 255),255)
        b = min(int(b *255),255)
        return max(0,r),max(0,g),max(0,b)
    else:
        return color
baoheduset = saturationset
satuset = saturationset
setbaohedu = saturationset

if __name__ == "__main__":

    import turtle
    
    def draw_square(length,c):
        turtle.color(c)
        turtle.begin_fill()
        for _ in range(4):
            turtle.fd(length)
            turtle.rt(90)
        turtle.end_fill()
        
    # 测试 rgb2int和int2rgb function
    color1 = (1,0,0)
    print( rgb2int(*color1) )
    
    r,g,b = int2rgb(65536)
    print('r,g,b = ',r,g,b)
    
    ft = ("",12,"normal")
    screen = turtle.getscreen()    
    screen.colormode(255)
    screen.delay(0)
    screen.bgcolor('black')
    screen.title("draw lollipop 画棒棒糖")
    
    c  = (255,0,0)                # RGB红色
    turtle.ht()                   # 隐藏海龟
    turtle.penup()                # 抬起笔来
    turtle.goto(0,100)            # 定位坐标
    turtle.pendown()              # 落下画笔
    for i in range(300):          # 迭代变量
        turtle.width(i/10)        # 画笔笔宽
        turtle.fd(i/10)           # 海龟前进
        turtle.rt(10)             # 海龟右转
        c = coloradd(c,0.01)      # 颜色增加
        turtle.pencolor(c)        # 画笔颜色
        
    turtle.penup()                # 抬起笔来
    turtle.goto(0,100)            # 定位坐标
    turtle.setheading(-90)        # 方向向下
    turtle.color("brown")         # 画笔颜色
    turtle.pendown()              # 落下笔来
    turtle.fd(290)                # 前进300
    turtle.penup()                # 抬起笔来
    turtle.color("gray")          # 画笔颜色
    turtle.write("www.lixingqiu.com",align='center',font=ft)
    
    # 亮度设置
    turtle.goto(-300,-200)
    turtle.write("lightset test (亮度测试)",font=ft)
    turtle.goto(-300,-230)
    c = (255,0,0)
    turtle.setheading(0)
    turtle.pendown()
    for x in range(200):
        ys = lightset(c,x/200)
        turtle.color(ys)
        turtle.fd(3)
    turtle.penup()
    
    # 饱和度设置
    turtle.goto(-300,-280)
    turtle.write("saturation test (饱和度测试)",font=ft)
    turtle.goto(-300,-300)
    c = (255,0,0)
    turtle.setheading(0)
    turtle.pendown()
    for x in range(200):
        ys = saturationset(c,x/200)
        turtle.color(ys)
        turtle.fd(3)
    turtle.penup()
    turtle.color(0,255,255)
    turtle.goto(0,-150)
    turtle.write("请单击",align='center',font=('黑体',32,'normal'))

    # 下面是测试lerpcolor函数@2022/1/8
    def test_lerpcolor(x,y):
        screen.clear()
        screen.delay(0)
        screen.colormode(255)
        fromC = (255,0,0)
        toC = (0,0,255)
        cs = []
        am = 100
        for x in range(1,am):
            cs.append(lerpcolor(fromC,toC,x/am))
        cs.insert(0,fromC)
        cs.append(toC)

        for i in range(len(cs)):
            turtle.dot(10,cs[i])
            turtle.fd(2*(i+1))
            turtle.right(60)
        turtle.penup()
        turtle.color(0,0,255)       
        turtle.goto(0,-240)
        turtle.write("教学档案下载网址:http://www.lixingqiu.com/2020/02/20/coloradd/",
                     align='center',font=('宋体',14,'normal'))        
        turtle.goto(0,240)
        turtle.write("安装方法:  pip install coloradd",
                     align='center',font=('黑体',20,'normal'))

        turtle.ht()
    screen.onclick(test_lerpcolor)
    screen.mainloop()

    
print(f"Version:{__version__},successfully imported,technical support:406273900@qq.com")
