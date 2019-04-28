# 导入模块按照以下顺序导入
# 1. 官方标准模块导入
# 2. 第三方模块导入
# 3. 应用程序模块导入
import pygame
from plane_sprites import *


class PlaneGame(object):
    '''飞机大战主游戏'''

    def __init__(self):
        pygame.init()
        print("游戏初始化")
        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建时钟对象
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法 创建精灵组和精灵
        self.__create_sprites()

        # 4. 设置=定时器时间 - 创建敌机 1s(但是这里是以毫秒作单位的)
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)

        # 5. 设置=定时器事件 - 发射子弹 0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵, 和精灵组
        bg1 = BackGround()
        bg2 = BackGround(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        # 把建立的精灵对象放在精灵组里面
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")
        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):
        '''事件监听'''
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                # 调用静态方法用类名, 调用类方法也是用类名
                PlaneGame.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                # 看事件是不是创建敌机时间
                print("敌机出厂...")
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)

            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 这是键盘事件的第一种方式
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右移动...")

        # 使用键盘提供的方法捕获键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        # 用户输入了右方向键
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        # 用户输入了左方向键
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        '''碰撞检查'''
        # 1. 子弹摧毁敌机
        # 子弹精灵组里面的精灵和敌机精灵组里面的精灵发生碰撞时,后面的两个True意思是这两个精灵在他们的
        # 精灵组里面消失
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 2. 敌机装回英雄
        # 英雄精灵和指定的精灵组中的精灵发生碰撞时敌机销毁 返回敌机列表
        enemies = pygame.sprite.spritecollide( self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(enemies) > 0:
            # 让英雄牺牲
            self.hero.kill()

            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):
        '''更新/绘制精灵组'''
        # 这里的update方法就是plane_sprites里面的update方法
        self.back_group.update()
        # 你要把屏幕对象传递过来, 绘制到这个屏幕上
        self.back_group.draw(self.screen)

        # 把敌机的精灵组绘制到屏幕上
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 把英雄的精灵绘制到屏幕上
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 把英雄的子弹精灵组绘制到屏幕上
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        '''退出系统'''
        print("游戏结束")
        pygame.quit()
        exit()



if __name__ == "__main__":
    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()