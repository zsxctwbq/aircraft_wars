# 导入模块按照以下顺序导入
# 1. 官方标准模块导入
# 2. 第三方模块导入
# 3. 应用程序模块导入
import random
import pygame

# 屏幕大小常亮
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新的帧率
FRAME_PER_SEC = 60

# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 英雄搭设子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

# 精灵类必须的
# 1> 调用父类的__init__方法
# 2> 创建三个属性
# 3> 从写update方法
class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''

    def __init__(self, image_name, speed=1):
        '''初始化'''
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性 Image.load是加载图像的大小 image_name 是图片的路径
        self.image = pygame.image.load(image_name)
        # get_rect()加载出来的大小就是我们刚刚图片的大小
        self.rect = self.image.get_rect()
        # 速度
        self.speed = speed

    def update(self):
        '''重写父类的update的方法'''
        # 重写rect.y
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class BackGround(GameSprite):
    '''游戏背景精灵'''
    # is_alt==False 创建出来的背景正好是叠加在屏幕的上的
    def __init__(self, is_alt=False):
        # 1.调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./images/background.png")

        # 2.判断是否是交替图像, 如果是, 需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        '''重写父类的update方法'''
        # 1.调用父类的方法实现
        super().update()

        # 2. 判断图像是否移除屏幕, 如果移除屏幕, 将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    '''敌机精灵'''
    def __init__(self):
        # 1. 调用父类方法, 创建敌机精灵, 同时指定敌机图片
        super().__init__("./images/enemy1.png")

        # 2. 指定敌机的初始随机速度 1 ~ 3
        self.speed = random.randint(1,3)
        # 3. 指定敌机的初始随机位置
        # 设置y方向的初始位置提供的bottom属性, 在指定敌机初始位置时, 会比较方便
        # bottom = y + height
        # y = bottom - height(图片底部,连接在窗口的顶部)
        self.rect.bottom = 0
        # 设置x方向的(飞机在最左侧x=0, 飞机在最右侧屏幕的宽度-飞机的宽度)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):
        # 1. 调用父类方法, 保持垂直方向的运行
        super().update()
        # 2. 超出屏幕的敌机, 把它删除
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕, 需要从精灵组删除....")
            # 将精灵从所有组中删除
            # kill方法可以将精灵从所有精灵组中移出, 精灵就会被自动销毁
            self.kill()

    # 当有对象被删除时, 会自动要用此方法
    def __del__(self):
        # print("敌机挂了 %s"%self.rect)
        pass


class Hero(GameSprite):
    '''英雄精灵'''
    # 1. 调用父类方法, 设置image$speed
    def __init__(self):
        super().__init__("./images/me1.png", 0)

        # 2. 设置英雄的初始化位置
        # 把英雄设置在屏幕的中心(x的值)
        self.rect.centerx = SCREEN_RECT.centerx
        # 把英雄的底部设置与屏幕120px距离(y的值)
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        # right = x + width
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        '''发射子弹'''

        # 一次发射3枚子弹
        for i in range(3):
            # 1. 创建子弹精灵
            bullet = Bullet()

            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y -i * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    '''子弹精灵'''

    def __init__(self):
        '''初始化'''

        # 调用父类方法, 设置子弹图片, 设置初始速度
        super().__init__("./images/bullet1.png", -2)

    def update(self):

        # 调用父类方法, 让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")


