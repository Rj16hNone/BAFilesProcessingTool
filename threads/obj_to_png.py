# coding: utf-8
from pathlib import Path

import pygame


def getAllFiles(folder: str):
    """
    获取文件夹下的所有文件
    :return: 文件列表
    """
    return list(Path(folder).glob(f'**/*.png'))


def restore_tool(obj_path, png_2d, save):
    """拼图用的函数"""
    # 用于存储相应参数
    blit_place = [None]
    cut_place = [None]
    restore_way = []
    printer = []
    with open(obj_path, mode='r', encoding='utf-8') as fp:
        for msg in fp.readlines():
            if msg[0] == "g":
                continue

            elif msg[0] == "v" and msg[1] != 't':
                msg = msg[:-3]
                msg = msg.split(" ")
                msg = msg[1:]
                msg = [int(msg[0]), int(msg[1])]
                blit_place.append(msg)

            elif msg[0] == "v" and msg[1] == "t":
                msg = msg[:-1]
                msg = msg.split(" ")
                msg = msg[1:]
                msg = [float(msg[0]), float(msg[1])]
                cut_place.append(msg)

            elif msg[0] == 'f':
                msg = msg[:-1]
                msg = msg.split(" ")
                msg = [int(msg[1].split('/')[0]),
                       int(msg[2].split('/')[0]),
                       int(msg[3].split('/')[0]),
                       ]
                restore_way.append(msg)

    # 拼图准备
    temp = ([], [])
    for num in blit_place[1:]:
        temp[0].append(num[0])
        temp[1].append(num[1])

    X = (max(temp[0]) - min(temp[0]))
    Y = (max(temp[1]) - min(temp[1]))

    del temp
    # 背景准备

    bg = pygame.Surface((X, Y), flags=pygame.SRCALPHA, depth=32)

    # 图片加载
    img = pygame.image.load(png_2d)
    width = img.get_width()
    height = img.get_height()
    img_upside_down = pygame.transform.flip(img.copy(), False, True)

    # 坐标镜像处理

    for num in range(len(blit_place) - 1):
        blit_place[num + 1][0] = -blit_place[num + 1][0]

    # 切割模块
    for index in restore_way:
        # 索引，拆分
        blit_p = [blit_place[index[0]], blit_place[index[1]], blit_place[index[2]]]
        cut_p = [cut_place[index[0]], cut_place[index[1]], cut_place[index[2]]]

        blit_area = [min(blit_p[0][0], blit_p[1][0], blit_p[2][0]), min(blit_p[0][1], blit_p[1][1], blit_p[2][1])]

        cut_x = int(min(cut_p[0][0], cut_p[1][0], cut_p[2][0]) * width)
        cut_y = int(min((cut_p[0][1], cut_p[1][1], cut_p[2][1])) * height)

        wide = int((max(cut_p[0][0], cut_p[1][0], cut_p[2][0]) - min(cut_p[0][0], cut_p[1][0], cut_p[2][0])) * width)
        high = int((max(cut_p[0][1], cut_p[1][1], cut_p[2][1]) - min(cut_p[0][1], cut_p[1][1], cut_p[2][1])) * height)

        cut_size = pygame.Rect(cut_x, cut_y, wide, high)

        cut = img_upside_down.subsurface(cut_size)

        cut = pygame.transform.smoothscale(cut, ((max(blit_p[0][0], blit_p[1][0], blit_p[2][0]) -
                                                  min(blit_p[0][0], blit_p[1][0], blit_p[2][0])),
                                                 (max(blit_p[0][1], blit_p[1][1], blit_p[2][1]) -
                                                  min(blit_p[0][1], blit_p[1][1], blit_p[2][1])))
                                           )
        printer.append([blit_area, cut])

    # 开始拼图

    for index in printer:
        bg.blit(index[1], index[0])

    pic = pygame.transform.flip(bg, False, True)

    pygame.image.save(pic, save)

# if __name__ == '__main__':
#     obj = r'E:\PycharmProjects\bilan-add\附件\Mesh\biaoqiang_g-mesh.obj'
#     png_2d = r'E:\PycharmProjects\bilan-add\附件\Texture2D\biaoqiang_g.png'
#     save = r''r'E:\PycharmProjects\bilan-add\附件\合成图片\biaoqiang_g.png'
#     file = Path(save).parent
#     if not file.exists():
#         os.makedirs(file)
#     restore_tool(obj, png_2d, save)
