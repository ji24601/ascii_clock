#!/usr/bin/env python
#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import os
import time
import math
import datetime
from asciicanvas import AsciiCanvas
from weather import get_weather
from calendar import calendar
from colorama import init, Fore, Back, Style

init(autoreset=True)
x_scale_ratio = 1.75
location, temperature = get_weather()

def draw_second_hand(ascii_canvas, seconds, length, fill_char):
    """
    Draw second hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 4.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    x1 = x0 + int(math.cos((seconds + 45) * 6 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((seconds + 45) * 6 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_minute_hand(ascii_canvas, minutes, length, fill_char):
    """
    Draw minute hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 4.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    x1 = x0 + int(math.cos((minutes + 45) * 6 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((minutes + 45) * 6 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_hour_hand(ascii_canvas, hours, minutes, length, fill_char):
    """
    Draw hour hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 4.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    total_hours = hours + minutes / 60.0
    x1 = x0 + int(math.cos((total_hours + 45) * 30 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((total_hours + 45) * 30 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_clock_face(ascii_canvas, radius, mark_char):
    """
    Draw clock face with hour and minute marks
    """
    x0 = ascii_canvas.cols // 4
    y0 = ascii_canvas.lines // 2
    # draw marks first
    for mark in range(1, 12 * 5 + 1):
        x1 = x0 + int(math.cos((mark + 45) * 6 * math.pi / 180) * radius * x_scale_ratio)
        y1 = y0 + int(math.sin((mark + 45) * 6 * math.pi / 180) * radius)
        if mark % 5 != 0:
            ascii_canvas.add_text(x1, y1, mark_char)
    # start from 1 because at 0 index - 12 hour
    for mark in range(1, 12 + 1):
        x1 = x0 + int(math.cos((mark + 45) * 30 * math.pi / 180) * radius * x_scale_ratio)
        y1 = y0 + int(math.sin((mark + 45) * 30 * math.pi / 180) * radius)
        ascii_canvas.add_text(x1, y1, '%s' % mark)

def draw_calendar(ascii_canvas, startday, lastday, today):
    x, y = 70, 11

    ascii_canvas.add_text(x, y, Fore.RED + 'Sun' + Fore.WHITE + ' Mon Tue Wed Thu Fri ' + Fore.CYAN + 'Sat' + Fore.WHITE)

    y = 12

    if startday == 6:
        s = 1
    else:
        s = startday + 2

    c = 0
    m = 0

    for k in range(6):
        for i in range(7):
            c = c + 1
            if c < s:
                ascii_canvas.add_text(x, y, ' '.center(3, ' '))
            else:
                ascii_canvas.add_text(x, y, str(m).rjust(3, ' '))
                if lastday > m:
                    m = m + 1
                    ascii_canvas.add_text(x, y, str(m).rjust(3, ' '))
                    # if (c - 1) % 7 == 0:
                    #     ascii_canvas.add_text(x, y, Fore.RED + str(m).rjust(3, ' ') + Fore.WHITE)
                    # elif c % 7 == 0:
                    #     ascii_canvas.add_text(x, y, Fore.CYAN + str(m).rjust(3, ' ') + Fore.WHITE)
                    # else:
                    #     if m == today:
                    #         ascii_canvas.add_text(x, y, Back.GREEN + Fore.WHITE + str(m).rjust(3, ' ') + Back.BLACK)
                    #     else:
                    #         ascii_canvas.add_text(x, y, str(m).rjust(3, ' '))
            x = x + 4
        y = y + 1
        x = 70

def draw_clock(cols, lines):
    """
    Draw clock
    """
    if cols < 25 or lines < 25:
        print('Too little columns/lines for print out the clock!')
        exit()
    # prepare chars
    single_line_border_chars = ('.', '-', '.', '|', ' ', '|', '`', '-', "'")
    second_hand_char = '.'
    minute_hand_char = '#'
    hour_hand_char = '+'
    mark_char = '`'
    if os.name == 'nt':
        single_line_border_chars = ('.', '-', '.', '|', ' ', '|', '`', '-', "'")  # ('\xDA', '\xC4', '\xBF', '\xB3', '\x20', '\xB3', '\xC0', '\xC4', '\xD9')
        second_hand_char = '.'  # '\xFA'
        minute_hand_char = '#'  # '\xF9'
        hour_hand_char = '+'  # 'o'
        mark_char = '`'  # '\xF9'
    # create ascii canvas for clock and eval vars
    ascii_canvas = AsciiCanvas(cols * 2, lines)
    center_x = int(math.ceil(cols / 4.0))
    center_y = int(math.ceil(lines / 2.0))
    radius = center_y - 5
    second_hand_length = int(radius / 1.17)
    minute_hand_length = int(radius / 1.25)
    hour_hand_length = int(radius / 1.95)
    # add clock region and clock face
    ascii_canvas.add_rect(5, 3, int(math.floor(cols / 2.0)) * 2 - 9, int(math.floor(lines / 2.0)) * 2 - 5)
    draw_clock_face(ascii_canvas, radius, mark_char)
    now = datetime.datetime.now()
    # add regions with weekday and day if possible
    if center_x > 25:
        left_pos = int(radius * x_scale_ratio) / 2 - 4
        ascii_canvas.add_nine_patch_rect(int(center_x + left_pos), int(center_y - 1), 5, 3, single_line_border_chars)
        ascii_canvas.add_text(int(center_x + left_pos + 1), int(center_y), now.strftime('%a'))
        ascii_canvas.add_nine_patch_rect(int(center_x + left_pos + 5), int(center_y - 1), 4, 3, single_line_border_chars)
        ascii_canvas.add_text(int(center_x + left_pos + 1 + 5), int(center_y), now.strftime('%d'))
    # add clock hands
    draw_second_hand(ascii_canvas, now.second, second_hand_length, fill_char=second_hand_char)
    draw_minute_hand(ascii_canvas, now.minute, minute_hand_length, fill_char=minute_hand_char)
    draw_hour_hand(ascii_canvas, now.hour, now.minute, hour_hand_length, fill_char=hour_hand_char)

    # draw weather
    ascii_canvas.add_text(70, 5, 'ooooooooooooooooooooooooooooooooooooooooooooooooo')
    ascii_canvas.add_text(70, 6, 'o                                               o')
    ascii_canvas.add_text(70, 7, 'o       ' + location + ' ' + temperature + '\"       o')
    ascii_canvas.add_text(70, 8, 'o                                               o')
    ascii_canvas.add_text(70, 9, 'ooooooooooooooooooooooooooooooooooooooooooooooooo')

    # draw calendar
    startday, lastday, today = calendar()
    draw_calendar(ascii_canvas, startday, lastday, today)

    # print out canvas
    ascii_canvas.print_out()


def main():
    lines = 40
    cols = int(lines * x_scale_ratio)
    # set console window size and screen buffer size
    if os.name == 'nt':
        os.system('mode con: cols=%s lines=%s' % (cols * 2 + 1, lines + 1))
    while True:
       os.system('cls' if os.name == 'nt' else 'clear')
       draw_clock(cols, lines)
       time.sleep(0.2)


if __name__ == '__main__':
    main()
