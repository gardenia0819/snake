import sys
from snake import Snake
from tkinter import Tk, Frame, Canvas, Button, Event


class Game:
    def __init__(self, fps, min_fps, fps_step):
        # 游戏参数
        self.FPS = fps
        self.min_fps = min_fps
        self.fps_step = fps_step
        self.snake = Snake(700, 600)

        # 主界面
        self.root = Tk()
        self.root.title("贪吃蛇")
        self.root.geometry("900x600+300+100")
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
        Button(self.frame, text="开始游戏", command=self.__start_game)\
            .place(relx=0.5, rely=0.4, width=80, height=30, anchor="center")

    def draw(self):
        status = self.snake.update_next(self.canvas)
        if status == -1:
            print("游戏结束")
            sys.exit(1)

        if self.FPS >= self.min_fps:
            self.FPS -= self.fps_step
        self.canvas.after(self.FPS, lambda: self.draw())

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
        status = self.snake.update_next(self.canvas)
        if status == -1:
            print("游戏结束")
            sys.exit(1)




    def __start_game(self):
        self.frame.place_forget(),
        self.canvas.place(width=700, height=600),
        self.snake.init(self.canvas)
        self.draw()

    def start(self):
        self.root.mainloop()