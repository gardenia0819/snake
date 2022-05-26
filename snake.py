from tkinter import Canvas


class Snake:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.step = 10
        self.direct = 'Right'
        self.body_len = 3
        self.head_pos = [50, 50]
        self.element_id = []

    def next_pos(self):
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
        return x, y

    # 画蛇头
    def update_head(self, cv: Canvas):
        head_pos = self.head_pos
        # 如果pos超出了边界返回code -1，否则为0
        if self.check() == -1:
            return -1

        head_id = cv.create_rectangle(head_pos[0],
                                      head_pos[1],
                                      head_pos[0] + self.step,
                                      head_pos[1] + self.step,
                                      fill='white',
                                      outline='black')
        self.element_id.insert(0, head_id)

        return 0

    # 画全部
    def init(self, cv: Canvas):
        self.update_head(cv)
        x = self.head_pos[0]
        y = self.head_pos[1]
        for i in range(self.body_len):
            x -= self.step
            self.element_id.append(
                cv.create_rectangle(x, y, x + self.step, y + self.step, fill='white', outline='black'))
        return self

    # 更新下一个位置
    def update_next(self, cv: Canvas):
        # 计算下一个点的位置
        self.next_pos()
        # 删除最后一节
        cv.delete(self.element_id.pop(-1))
        # 更新第一个节
        return self.update_head(cv)

    # 超出游戏画面校验
    def check(self):
        head_pos = self.head_pos
        if head_pos[0] >= self.max_x:
            return -1
        elif head_pos[0] <= 0:
            return -1
        if head_pos[1] >= self.max_y:
            return -1
        if head_pos[1] <= 0:
            return -1
        return 0
