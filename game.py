import sys
import time

from snake import Snake
from tkinter import Tk, Frame, Canvas, Button, Event, PhotoImage
from PIL import ImageTk, Image


NAME = "贪吃蛇"
START_BUTTON_NAME = "开始游戏"
X = 900
Y = 600
X_OFFSET = 300
Y_OFFSET = 100


class Game:
    def __init__(self, fps, min_fps, fps_step):
        # 游戏参数
        self.FPS = fps
        self.min_fps = min_fps
        self.fps_step = fps_step
        self.bg = None

        # 主界面
        self.root = Tk()
        self.root.title(NAME)
        self.root.geometry("{}x{}+{}+{}".format(X, Y, X_OFFSET, Y_OFFSET))
        self.root.resizable(False, False)

        # start_frame 容器
        self.frame = Frame(self.root)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        # 提供一个游戏画布, 点击开始游戏后进入画布
        self.canvas = Canvas(self.root, bg="grey")

        # 画布控件 绑定 方向键用来控制蛇的方向
        self.canvas.bind("<KeyPress-Up>", self.event_callback)
        self.canvas.bind("<KeyPress-Down>", self.event_callback)
        self.canvas.bind("<KeyPress-Left>", self.event_callback)
        self.canvas.bind("<KeyPress-Right>", self.event_callback)
        self.canvas.focus_set()

        # 加一个按钮(开始游戏),点击时进入游戏
        Button(self.frame, text=START_BUTTON_NAME, command=self.__start_game)\
            .place(relx=0.5, rely=0.4, width=80, height=30, anchor="center")

        # 蛇
        self.snake = Snake(X-200, Y, self.canvas)

    def draw(self):
        status = self.snake.update_next_pos()
        if status == -1:
            print("游戏结束")
            sys.exit(1)
        self.canvas.after(self.FPS, lambda: self.draw())

    # 响应玩家对小蛇的控制
    def event_callback(self,event: Event):
        # 更新方向
        if self.snake.direct == 'Right' and event.keysym == 'Left':
            return
        if self.snake.direct == 'Down' and event.keysym == 'Up':
            return
        if self.snake.direct == 'Left' and event.keysym == 'Right':
            return
        if self.snake.direct == 'Up' and event.keysym == 'Down':
            return

        self.snake.direct = event.keysym
        status = self.snake.update_next_pos()
        if status == -1:
            print("游戏结束")
            sys.exit(1)

    # 更新游戏难度
    def __game_level(self):
        if self.FPS >= self.min_fps:
            self.FPS -= self.fps_step
            print("{}: FPS: {}".format( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),self.FPS))
        self.canvas.after(2000, self.__game_level)

    # 开始游戏触发， 进入游戏界面， 初始化小蛇， 小蛇自动刷新， 游戏难度增加， 食物刷新
    def __start_game(self):
        self.frame.place_forget(),
        width = X - 200
        height = Y
        self.canvas.place(width=width, height=height)

        # 设置背景
        self.bg = ImageTk.PhotoImage(Image.open("img/bg.jpg"))
        self.canvas.create_image(350, 300, image=self.bg)
        # 初始化小蛇
        self.snake.init_snake()
        # 小蛇自动移动
        self.draw()
        # 游戏难度
        self.__game_level()

    def start(self):
        self.root.mainloop()

