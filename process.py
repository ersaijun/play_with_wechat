from wxpy import *
import  math
from  PIL import Image
import matplotlib.pyplot as plt 
import jieba
from wordcloud import WordCloud,STOPWORDS
import numpy as np
import os
import wc2char

friends = None
downloaded_avatar = False

# 创建存放文件夹
def create_filepath(path_name):
	avatar_dir = os.getcwd() + '\\' + path_name + '\\'
	if not os.path.exists(avatar_dir):
		os.mkdir(avatar_dir)
	return  avatar_dir

def login_success():
    print('login success!')

def developing():
    print("功能开发中...")

# 下载头像
def download_avatar():
    global downloaded_avatar
    avatar_dir = create_filepath('avatar')
    
    print("头像下载中，请稍等...")
    if not downloaded_avatar:  
        num = 0
        for friend in friends:
            friend.get_avatar(avatar_dir + '\\' + str(num) + '.jpg')
            # print("昵称 ： %s" % friend.nick_name)
            num+=1

            if num % 20 == 0:
                print("头像读取中，请耐心等待{}%".format(round(num/len(friends)*100,2)),end='\r')

        downloaded_avatar = True
    print('\n')
    return avatar_dir

def process(number):
    if number == 1:
        gen_avatar()
    elif number == 2:
        gen_sex()
    elif number == 3:
        gen_word_cloud()
    elif number == 4 or number == 7:
        developing()
    elif number == 5:
        same_friend() 
    elif number == 6:
        gen_avatar_hanzi()
    else:
        pass

def gen_avatar():
    print("#1 ----生成所有微信好友图片墙----")
    
    # 保存好友头像
	# 初始化机器人，扫码登录
    global friends
    if friends == None:
        bot = Bot(console_qr=True, login_callback=login_success )
        friends = bot.friends(update=True)
    
    avatar_dir = download_avatar()
        

    # 拼接头像
    length = len(os.listdir(avatar_dir))

    image_size = 1920
    each_size = math.ceil(image_size / math.floor(math.sqrt(length)))

    # 计算所需行数和列数的头像数
    x_lines = math.ceil(math.sqrt(length))
    y_lines = math.ceil(math.sqrt(length))

    image = Image.new('RGB',(each_size * x_lines, each_size * y_lines))
    x = 0
    y = 0
    for (_,__,files) in os.walk(avatar_dir):
        for pic_name in files:
            try:
                with Image.open(avatar_dir+pic_name) as img:
                    img = img.resize((each_size,each_size))
                    image.paste(img,(x*each_size,y*each_size))
                    x+=1
                    if x ==  x_lines:
                        x=0
                        y+=1
            except:
                print('读取失败')
    img = image.save(os.getcwd()+'/wechat_avatar.png')
    plt.imread('wechat_avatar.png')
    
    print('wechat_avatar.png已保存至目录。')
    print('#1 Finish!!')
    plt.show()
    
def gen_avatar_hanzi():
      # 初始化机器人，扫码登录
    global friends
    if friends == None:
        bot = Bot( login_callback=login_success,console_qr=True) # 
        friends = bot.friends(update=True) 

    
    print("#6 ----头像拼接汉字----")
    input_str = input('请输入汉字（建议为6个或9个，用于微信六宫格或九宫格；包括标点符号）：')

    #将字转化为汉字库的点阵数据
    outlist = wc2char.char2bit(input_str)
    #获取当前文件夹路径
    workspace = os.getcwd()

    avatar_dir = download_avatar()
     #先读取用户本人头像，存储名为用户名称
    selfHead = avatar_dir + '0.jpg'
    
    avatar_dir = "avatar"
    print("生成中，请稍等...")
     #将头像图片按点阵拼接成单字图片
    wc2char.head2char(workspace,avatar_dir,selfHead,outlist)

    print("完成！ 已输出至目录 avatar_output ")
    print('#6 Finish!!')


#统计好友的性别，微信中男性为1，女性为2，未知为0
def gen_sex():
    print("#2 ----好友男女比例和地区统计----")

    # 初始化机器人，扫码登录
    global friends
    if friends == None:
        bot = Bot( login_callback=login_success) # console_qr=True,
        friends = bot.friends(update=True)
   
    # result = friends.stats_text()
    # print(result)
    stat = friends.stats()
    # print(stat)
    
    plt.figure(figsize=(8,5), dpi=80)
    plt.axes(aspect=1) 
    plt.pie([stat['sex'][1], stat['sex'][2], stat['sex'][0]],
            labels=['男','女','未知'],
            labeldistance = 1.1,
            autopct = '%3.1f%%',
            shadow = False,
            startangle = 90,
            pctdistance = 0.6 
    )

    plt.legend(loc='upper left',)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('微信中的男女比例')
    plt.show()
    
    top_n = list(filter(lambda x: x[0], stat['city'].most_common()))[:10]
    top_n_list = ['{}'.format(k) for k, v in top_n]
    top_n_number_list = ['{:.2}'.format(v/len(friends)) for k, v in top_n]

    plt.title('好友城市分布TOP10')
    plt.bar(range(len(top_n_list)),top_n_number_list,tick_label=top_n_list,color="blue")
    plt.show()

    top_n = list(filter(lambda x: x[0], stat['province'].most_common()))[:10]
    top_n_list = ['{}'.format(k) for k, v in top_n]
    top_n_number_list = ['{:.2}'.format(v/len(friends)) for k, v in top_n]
    plt.title('好友省份分布TOP10')
    plt.bar(range(len(top_n_list)),top_n_number_list,tick_label=top_n_list,color="blue")
    plt.show()

    print('#2 Finish!!')

# 生成签名词云
def gen_word_cloud():
    print("#3 ----好友签名制作词云和情感分析----")

     # 初始化机器人，扫码登录
    global friends
    if friends == None:
        bot = Bot(console_qr=True, login_callback=login_success) #cache_path=True,
        friends = bot.friends(update=True)
    
    # 获取好友签名信息并储存在 siglist 中
    siglist = []
    for _,friend in enumerate(friends):
        sigture = friend.signature
        # 如果存在签名的话
        if len(sigture) > 0:
            # 将个性签名中的表情符号去掉（这里没有去除干净，利用正则表达式）
            sigture = sigture.replace('span','').replace('class','').replace('emoji','').replace('< =','').replace('"','').replace('</>','').replace('>','')
            siglist.append(sigture)

    # 将siglist中的元素拼接为一个字符串
    text = ''.join(siglist)

    # jieba(结巴分词：有全模式、精确模式、默认模式、新词识别、搜索引擎模式）
    # jieba.cut()所接收的两个参数，第一个参数为需要分词的字符串，第二个为是否采用全模式
    word_list = jieba.cut(text, cut_all=True)
    # 空格拼接
    word_space_split = ' '.join(word_list)
    # 字体的颜色为对应路径的背景图片的颜色
    coloring = plt.imread('bg.jpg')
    # coloring = np.array(Image.open("wechat.jpg"))
    # font_path: 字体路径；  random_state: 为每个字体返回一个PIL颜色；  scale：按照比例放大画布；max_font_size:显示的最大字体的大小
    # 如果参数 mask 为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 取代
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
                            mask=coloring, max_font_size=120, random_state=42, scale=3,
                            font_path="./simkai.ttf").generate(word_space_split)

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
    my_wordcloud.to_file(os.path.join("wechatfriends_wordcloud.png"))
    print('#3 Finish!!')
    print('wechatfriends_wordcloud.png 已保存至目录。')


# 共同好友检测
def same_friend():
    print("#5 ----共同好友检测----")
    
     # 初始化机器人，扫码登录
    global friends
    if friends == None:
        bot = Bot(console_qr=True, login_callback=login_success)
        friends = bot.friends(update=True)
    
    print("请另一位同学扫码登录")
    bot_tmp = Bot( login_callback=login_success,cache_path=False,console_qr=True) #,console_qr=True
    other_friend = bot_tmp.friends(update=True)

    result = mutual_friends(friends,other_friend)

    print("共同好友有{}个".format(len(result)))
    for i in result:
        print(i)

    print('#5 Finish!!')
    



