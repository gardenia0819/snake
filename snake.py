from tkinter import Canvas
import random

SNAKE_STEP = 10
SNAKE_DEFAULT_DIR = 'Right'
SNAKE_BODY_LEN = 3
SNAKE_HEAD_POS = [50, 50]


class Snake:
    def __init__(self, width: int, height: int, canvas: Canvas):
        self.canvas = canvas
        self.max_x = width - SNAKE_STEP
        self.max_y = height - SNAKE_STEP
        self.step = SNAKE_STEP
        self.direct = SNAKE_DEFAULT_DIR
        self.body_len = SNAKE_BODY_LEN
        self.head_pos = SNAKE_HEAD_POS
        self.element_id = []
        self.food_pos = []
        self.food_id = None

    # 计算小蛇的下一个位置
    def __next_pos(self):
        x, y = 0, 0
        if self.direct == 'Right':
            x = self.head_pos[0] + self.step
            y = self.head_pos[1]
        if self.direct == 'Down':
            x = self.head_pos[0]
            y = self.head_pos[1] + self.step
        if self.direct == 'Left':
            x = self.head_pos[0] - self.step
            y = self.head_pos[1]
        if self.direct == 'Up':
            x = self.head_pos[0]
            y = self.head_pos[1] - self.step

        self.head_pos = [x, y]
        print("snake pos: [{}, {}]".format(x, y))
        return x, y

    # 更新蛇头
    def __draw_head(self):
        cv = self.canvas
        x, y = self.head_pos[0], self.head_pos[1]
        # 如果pos超出了边界返回code -1，否则为0
        if self.__check() == -1:
            return -1

        head_id = cv.create_rectangle(x, y, x + self.step, y + self.step, fill='white', outline='black')
        self.element_id.insert(0, head_id)

        return 0

    # 蛇身体的初始化
    def init_snake(self):
        cv = self.canvas
        self.__draw_head()
        x = self.head_pos[0]
        y = self.head_pos[1]
        for i in range(self.body_len):
            x -= self.step
            self.element_id.append(
                cv.create_rectangle(x, y, x + self.step, y + self.step, fill='white', outline='black'))

        # 初始化食物
        self.update_next_food()
        return self

    # 更新蛇头下一个位置
    def update_next_pos(self):
        cv = self.canvas
        # 计算下一个点的位置
        self.__next_pos()
        # 判断下一个位置是否和食物重合,不重合就删除最后一节
        if self.head_pos != self.food_pos:
            # 删除最后一节
            cv.delete(self.element_id.pop(-1))
        else:
            # 更新食物
            self.update_next_food()
        # 更新第一个节
        return self.__draw_head()

    # 更新食物下一个的位置
    def update_next_food(self):
        # 删除已经被吃掉的元素
        if self.food_id  is not None:
            self.canvas.delete(self.food_id)
        x, y = random.randint(0, self.max_x), random.randint(0, self.max_y)
        x = int(x / self.step) * self.step
        y = int(y / self.step) * self.step
        while True:
            if [x, y] != self.head_pos:
                break
            else:
                x, y = random.randint(0, self.max_x), random.randint(0, self.max_y)
                x = x / self.step * self.step
                y = y / self.step * self.step

        self.food_id = self.canvas.create_rectangle(x, y, x + self.step, y + self.step, fill='red', outline='white')
        print("food pos: [{}, {}]".format(x, y))
        self.food_pos = [x, y]

    # 超出游戏画面校验
    def __check(self):
        head_pos = self.head_pos
        if head_pos[0] >= self.max_x:
            return -1
        elif head_pos[0] < 0:
            return -1
        if head_pos[1] >= self.max_y:
            return -1
        if head_pos[1] < 0:
            return -1
        return 0
