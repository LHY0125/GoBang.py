# -*- coding: gbk -*-

# python python����/chaogao2.py

import sys
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from collections import namedtuple

Chessman = namedtuple("Chessman", "Name Value Color")
Point = namedtuple("Point", "X Y")

BLACK_CHESSMAN = Chessman("����", 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman("����", 2, (219, 219, 219))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Checkerboard:
    def __init__(self, line_points):
        self._line_points = line_points
        self._checkerboard = [[0] * line_points for _ in range(line_points)]
        # ��¼�����ʷ��ÿ��Ԫ��Ϊ(chessman, point)Ԫ��
        self._history = []

    def _get_checkerboard(self):
        return self._checkerboard
        
    def _get_history(self):
        return self._history
        
    checkerboard = property(_get_checkerboard)
    history = property(_get_history)

    # �ж��Ƿ������
    def can_drop(self, point):
        return self._checkerboard[point.Y][point.X] == 0

    def drop(self, chessman, point):
        """
        ����
        :param chessman:
        :param point:����λ��
        :return:����������֮�󼴿ɻ�ʤ���򷵻ػ�ʤ�������򷵻� None
        """
        print(f"{chessman.Name} ({point.X}, {point.Y})")
        self._checkerboard[point.Y][point.X] = chessman.Value
        self._history.append((chessman, point))

        if self._win(point):
            print(f"{chessman.Name}��ʤ")
            return chessman

    def undo(self):
        """������һ��"""
        if self._history:
            last_move = self._history.pop()
            self._checkerboard[last_move[1].Y][last_move[1].X] = 0
            return True
        return False

    def replay_to(self, step):
        """
        ���̵�ָ������
        :param step: Ŀ�경������1��ʼ��
        :return: �Ƿ�ɹ�
        """
        if step < 0 or step > len(self._history):
            return False
            
        # �������
        self._checkerboard = [[0] * self._line_points for _ in range(self._line_points)]
        
        # �����µ�ָ������
        for i in range(step):
            chessman, point = self._history[i]
            self._checkerboard[point.Y][point.X] = chessman.Value
            
        return True

    # �ж��Ƿ�Ӯ��
    def _win(self, point):
        cur_value = self._checkerboard[point.Y][point.X]
        for os in offset:
            if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                return True

    def _get_count_on_direction(self, point, value, x_offset, y_offset):
        count = 1
        for step in range(1, 5):
            x = point.X + step * x_offset
            y = point.Y + step * y_offset
            if (
                0 <= x < self._line_points
                and 0 <= y < self._line_points
                and self._checkerboard[y][x] == value
            ):
                count += 1
            else:
                break
        for step in range(1, 5):
            x = point.X - step * x_offset
            y = point.Y - step * y_offset
            if (
                0 <= x < self._line_points
                and 0 <= y < self._line_points
                and self._checkerboard[y][x] == value
            ):
                count += 1
            else:
                break

        return count >= 5


SIZE = 30  # ����ÿ����ʱ��ļ��
Line_Points = 19  # ����ÿ��/ÿ�е���
Outer_Width = 20  # ��������
Border_Width = 4  # �߿���
Inside_Width = 4  # �߿��ʵ�ʵ�����֮��ļ��
Border_Length = (
    SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
)  # �߿��ߵĳ���
Start_X = Start_Y = (
    Outer_Width + int(Border_Width / 2) + Inside_Width
)  # ��������㣨���Ͻǣ�����
SCREEN_HEIGHT = (
    SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
)  # ��Ϸ��Ļ�ĸ�
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # ��Ϸ��Ļ�Ŀ�

Stone_Radius = SIZE // 2 - 3  # ���Ӱ뾶
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xE3, 0x92, 0x65)  # ������ɫ
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10

# ���̿��ư�ť��λ�úʹ�С
REPLAY_BUTTON_WIDTH = 80
REPLAY_BUTTON_HEIGHT = 30
REPLAY_BUTTON_MARGIN = 10
REPLAY_BUTTON_START_Y = SCREEN_HEIGHT - 200

# ���̰�ť��ɫ
BUTTON_COLOR = (180, 180, 180)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (50, 50, 50)

def draw_button(screen, font, text, rect, color):
    """���ư�ť"""
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def is_point_in_rect(point, rect):
    """�жϵ��Ƿ��ھ�����"""
    return rect.left <= point[0] <= rect.right and rect.top <= point[1] <= rect.bottom

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("������")

    font1 = pygame.font.SysFont("SimHei", 32)
    font2 = pygame.font.SysFont("SimHei", 72)
    font3 = pygame.font.SysFont("SimHei", 24)  # ���ڰ�ť����
    fwidth, fheight = font2.size("�ڷ���ʤ")

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None
    computer = AI(Line_Points, WHITE_CHESSMAN)

    black_win_count = 0
    white_win_count = 0
    
    # ����ģʽ��ر���
    replay_mode = False
    current_step = 0
    auto_replay = False
    auto_replay_timer = 0
    auto_replay_interval = 1000  # �Զ����ż��������
    
    # ��ʱ��ʾ��Ϣϵͳ
    temp_message = ""
    temp_message_time = 0
    temp_message_duration = 2000  # ��Ϣ��ʾʱ�䣬����
    
    # �������̿��ư�ť
    replay_buttons = {
        'start': pygame.Rect(SCREEN_HEIGHT + 20, REPLAY_BUTTON_START_Y, 
                           REPLAY_BUTTON_WIDTH, REPLAY_BUTTON_HEIGHT),
        'prev': pygame.Rect(SCREEN_HEIGHT + 20, REPLAY_BUTTON_START_Y + REPLAY_BUTTON_HEIGHT + REPLAY_BUTTON_MARGIN, 
                          REPLAY_BUTTON_WIDTH, REPLAY_BUTTON_HEIGHT),
        'next': pygame.Rect(SCREEN_HEIGHT + 20, REPLAY_BUTTON_START_Y + (REPLAY_BUTTON_HEIGHT + REPLAY_BUTTON_MARGIN) * 2, 
                          REPLAY_BUTTON_WIDTH, REPLAY_BUTTON_HEIGHT),
        'end': pygame.Rect(SCREEN_HEIGHT + 20, REPLAY_BUTTON_START_Y + (REPLAY_BUTTON_HEIGHT + REPLAY_BUTTON_MARGIN) * 3, 
                         REPLAY_BUTTON_WIDTH, REPLAY_BUTTON_HEIGHT),
        'auto': pygame.Rect(SCREEN_HEIGHT + 20, REPLAY_BUTTON_START_Y + (REPLAY_BUTTON_HEIGHT + REPLAY_BUTTON_MARGIN) * 4, 
                          REPLAY_BUTTON_WIDTH, REPLAY_BUTTON_HEIGHT)
    }

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        cur_runner = BLACK_CHESSMAN
                        checkerboard = Checkerboard(Line_Points)
                        computer = AI(Line_Points, WHITE_CHESSMAN)
                        replay_mode = False
                        current_step = 0
                        auto_replay = False
                elif event.key == K_u:  # ��U��������һ��
                    if winner is None and not replay_mode:
                        # ��Ҫ������������ҵ�һ���͵��Ե�һ��
                        if checkerboard.undo():  # �������Ե�һ��
                            computer.reset_checkerboard(checkerboard.checkerboard)
                            if checkerboard.undo():  # ������ҵ�һ��
                                computer.reset_checkerboard(checkerboard.checkerboard)
                elif event.key == K_r:  # ��R�����븴��ģʽ
                    if winner is not None:
                        replay_mode = True
                        current_step = len(checkerboard.history)
                        checkerboard.replay_to(current_step)
                        print("�ѽ��븴��ģʽ")
                    else:
                        print("ֻ������Ϸ��������ܽ��븴��ģʽ")
                        # ������ʱ��ʾ��Ϣ
                        temp_message = "ֻ������Ϸ��������ܽ��븴��ģʽ"
                        temp_message_time = pygame.time.get_ticks()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if winner is not None and replay_mode:
                    # �����̰�ť���
                    if is_point_in_rect(mouse_pos, replay_buttons['start']):
                        current_step = 0
                        checkerboard.replay_to(current_step)
                        computer.reset_checkerboard(checkerboard.checkerboard)
                    elif is_point_in_rect(mouse_pos, replay_buttons['prev']):
                        if current_step > 0:
                            current_step -= 1
                            checkerboard.replay_to(current_step)
                            computer.reset_checkerboard(checkerboard.checkerboard)
                    elif is_point_in_rect(mouse_pos, replay_buttons['next']):
                        if current_step < len(checkerboard.history):
                            current_step += 1
                            checkerboard.replay_to(current_step)
                            computer.reset_checkerboard(checkerboard.checkerboard)
                    elif is_point_in_rect(mouse_pos, replay_buttons['end']):
                        current_step = len(checkerboard.history)
                        checkerboard.replay_to(current_step)
                        computer.reset_checkerboard(checkerboard.checkerboard)
                    elif is_point_in_rect(mouse_pos, replay_buttons['auto']):
                        auto_replay = not auto_replay
                        if auto_replay:
                            auto_replay_timer = pygame.time.get_ticks()
                elif winner is None and not replay_mode:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        click_point = _get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:
                                    cur_runner = _get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    AI_point = computer.AI_drop()
                                    winner = checkerboard.drop(cur_runner, AI_point)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = _get_next(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print("������������")

        # ������
        _draw_checkerboard(screen)

        # �����������е�����
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

        _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count, replay_mode, winner)
        
        # ��ʾ����ģʽ״ָ̬ʾ��
        if replay_mode:
            mode_text = "������ģʽ��"
            mode_font = pygame.font.SysFont("SimHei", 36)
            text_surface = mode_font.render(mode_text, True, (200, 50, 50))
            text_rect = text_surface.get_rect(center=(SCREEN_HEIGHT // 2, 30))
            screen.blit(text_surface, text_rect)

        if winner:
            print_text(
                screen,
                font2,
                (SCREEN_WIDTH - fwidth) // 2,
                (SCREEN_HEIGHT - fheight) // 2,
                winner.Name + "��ʤ",
                RED_COLOR,
            )
            
            # ����Ϸ��������ʾ������ʾ
            if not replay_mode:
                print_text(
                    screen,
                    font3,
                    SCREEN_HEIGHT + 20,
                    REPLAY_BUTTON_START_Y - 40,
                    "��R�����븴��ģʽ",
                    BLUE_COLOR,
                )
            
            # �ڸ���ģʽ����ʾ���ư�ť�͵�ǰ����
            if replay_mode:
                # ��ʾ��ǰ����
                print_text(
                    screen,
                    font3,
                    SCREEN_HEIGHT + 20,
                    REPLAY_BUTTON_START_Y - 70,
                    f"��ǰ����: {current_step}/{len(checkerboard.history)}",
                    BLUE_COLOR,
                )
                
                # ��ʾ��ǰ�غ�
                if current_step > 0 and current_step <= len(checkerboard.history):
                    current_player = checkerboard.history[current_step - 1][0]
                    next_player = BLACK_CHESSMAN if current_player == WHITE_CHESSMAN else WHITE_CHESSMAN
                    print_text(
                        screen,
                        font3,
                        SCREEN_HEIGHT + 20,
                        REPLAY_BUTTON_START_Y - 100,
                        f"��һ��: {next_player.Name}",
                        BLUE_COLOR,
                    )
                
                # ������ʾ���һ����
                if current_step > 0 and current_step <= len(checkerboard.history):
                    last_move = checkerboard.history[current_step - 1]
                    last_point = last_move[1]
                    pygame.draw.circle(
                        screen,
                        RED_COLOR,
                        (Start_X + SIZE * last_point.X, Start_Y + SIZE * last_point.Y),
                        Stone_Radius + 2,
                        2
                    )
                
                # ���Ƹ��̿��ư�ť
                button_texts = {
                    'start': '��ʼ',
                    'prev': '��һ��',
                    'next': '��һ��',
                    'end': '����',
                    'auto': '�Զ�����' if not auto_replay else 'ֹͣ����'
                }
                
                for button_name, rect in replay_buttons.items():
                    # �������Ƿ���ͣ�ڰ�ť��
                    if is_point_in_rect(pygame.mouse.get_pos(), rect):
                        color = BUTTON_HOVER_COLOR
                    else:
                        color = BUTTON_COLOR
                    
                    # �Զ����Ű�ť�ڼ���ʱʹ�ò�ͬ��ɫ
                    if button_name == 'auto' and auto_replay:
                        color = (150, 200, 150)
                    
                    draw_button(screen, font3, button_texts[button_name], rect, color)

        # �����Զ������߼�
        if replay_mode and auto_replay and current_step < len(checkerboard.history):
            current_time = pygame.time.get_ticks()
            if current_time - auto_replay_timer >= auto_replay_interval:
                current_step += 1
                checkerboard.replay_to(current_step)
                computer.reset_checkerboard(checkerboard.checkerboard)
                auto_replay_timer = current_time
                
                # ����������һ����ֹͣ�Զ�����
                if current_step >= len(checkerboard.history):
                    auto_replay = False

        pygame.display.flip()


def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN


# ������
def _draw_checkerboard(screen):
    # ������̱���ɫ
    screen.fill(Checkerboard_Color)
    # ��������������ı߿�
    pygame.draw.rect(
        screen,
        BLACK_COLOR,
        (Outer_Width, Outer_Width, Border_Length, Border_Length),
        Border_Width,
    )
    # ��������
    for i in range(Line_Points):
        pygame.draw.line(
            screen,
            BLACK_COLOR,
            (Start_Y, Start_Y + SIZE * i),
            (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
            1,
        )
    for j in range(Line_Points):
        pygame.draw.line(
            screen,
            BLACK_COLOR,
            (Start_X + SIZE * j, Start_X),
            (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
            1,
        )
    # ����λ����Ԫ
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            # pygame.draw.circle(screen, BLACK, (Start_X + SIZE * i, Start_Y + SIZE * j), radius)
            pygame.gfxdraw.aacircle(
                screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR
            )
            pygame.gfxdraw.filled_circle(
                screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR
            )


# ������
def _draw_chessman(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(
        screen,
        Start_X + SIZE * point.X,
        Start_Y + SIZE * point.Y,
        Stone_Radius,
        stone_color,
    )
    pygame.gfxdraw.filled_circle(
        screen,
        Start_X + SIZE * point.X,
        Start_Y + SIZE * point.Y,
        Stone_Radius,
        stone_color,
    )


# �������Ϣ��ʾ
def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count, replay_mode=False, winner=None):
    _draw_chessman_pos(
        screen,
        (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2),
        BLACK_CHESSMAN.Color,
    )
    _draw_chessman_pos(
        screen,
        (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4),
        WHITE_CHESSMAN.Color,
    )

    print_text(screen, font, RIGHT_INFO_POS_X, Start_X + 3, "���", BLUE_COLOR)
    print_text(
        screen,
        font,
        RIGHT_INFO_POS_X,
        Start_X + Stone_Radius2 * 3 + 3,
        "����",
        BLUE_COLOR,
    )

    print_text(
        screen,
        font,
        SCREEN_HEIGHT,
        SCREEN_HEIGHT - Stone_Radius2 * 8,
        "ս����",
        BLUE_COLOR,
    )
    _draw_chessman_pos(
        screen,
        (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)),
        BLACK_CHESSMAN.Color,
    )
    _draw_chessman_pos(
        screen,
        (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2),
        WHITE_CHESSMAN.Color,
    )
    print_text(
        screen,
        font,
        RIGHT_INFO_POS_X,
        SCREEN_HEIGHT - int(Stone_Radius2 * 5.5) + 3,
        f"{black_win_count} ʤ",
        BLUE_COLOR,
    )
    print_text(
        screen,
        font,
        RIGHT_INFO_POS_X,
        SCREEN_HEIGHT - Stone_Radius2 * 3 + 3,
        f"{white_win_count} ʤ",
        BLUE_COLOR,
    )
    
    # ��Ӳ�����ʾ
    if not replay_mode:
        if winner is None:
            # ��Ϸ��������ʾ������ʾ
            print_text(
                screen,
                pygame.font.SysFont("SimHei", 24),
                SCREEN_HEIGHT + 20,
                SCREEN_HEIGHT - Stone_Radius2 * 10,
                "��U��������һ��",
                BLUE_COLOR,
            )
            # ��Ϸ��������ʾR����ʾ
            print_text(
                screen,
                pygame.font.SysFont("SimHei", 24),
                SCREEN_HEIGHT + 20,
                SCREEN_HEIGHT - Stone_Radius2 * 12,
                "��Ϸ������R�����븴��ģʽ",
                (150, 150, 150),  # ʹ�û�ɫ��ʾ����ʾ��ǰ������
            )
        else:
            # ��Ϸ��������ʾR����ʾ��ʹ����ɫͻ����ʾ��
            print_text(
                screen,
                pygame.font.SysFont("SimHei", 24),
                SCREEN_HEIGHT + 20,
                SCREEN_HEIGHT - Stone_Radius2 * 10,
                "��R�����븴��ģʽ",
                BLUE_COLOR,
            )


def _draw_chessman_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)


# ���������λ�ã�������Ϸ������
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    if pos_x < -Inside_Width or pos_y < -Inside_Width:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > Stone_Radius:
        x += 1
    if pos_y % SIZE > Stone_Radius:
        y += 1
    if x >= Line_Points or y >= Line_Points:
        return None

    return Point(x, y)


class AI:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman
        self._opponent = (
            BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        )
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def get_opponent_drop(self, point):
        self._checkerboard[point.Y][point.X] = self._opponent.Value
        
    def reset_checkerboard(self, checkerboard):
        """����AI������״̬�����ڸ���ģʽ"""
        for i in range(self._line_points):
            for j in range(self._line_points):
                self._checkerboard[i][j] = checkerboard[i][j]

    def AI_drop(self):
        point = None
        score = 0
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Point(i, j)
        self._checkerboard[point.Y][point.X] = self._my.Value
        return point

    def _get_point_score(self, point):
        score = 0
        for os in offset:
            score += self._get_direction_score(point, os[0], os[1])
        return score

    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0  # ���Ӵ��ҷ���������
        _count = 0  # ���Ӵ��Է���������
        space = None  # �ҷ������������޿ո�
        _space = None  # �Է������������޿ո�
        both = 0  # �ҷ����������������赲
        _both = 0  # �Է����������������赲

        # ����� 1 ��ʾ�Ǳ������ҷ��ӣ�2 ��ʾ�з���
        flag = self._get_stone_color(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # �����ڶ����ո��˳�
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # ������Ҳ�����赲
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # �����ڶ����ո��˳�
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # ������Ҳ�����赲
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    # �ж�ָ��λ�ô���ָ�����������ҷ��ӡ��Է��ӡ���
    def _get_stone_color(self, point, x_offset, y_offset, next):
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else:
                if next:
                    return self._get_stone_color(Point(x, y), x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0


if __name__ == "__main__":
    main()
