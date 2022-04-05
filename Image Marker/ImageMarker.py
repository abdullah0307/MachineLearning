# # import the necessary packages
# import argparse
# import csv

import cv2
import os
import csv
import math
import _thread as thread
import tkinter as tk

line = False
edit_line = 1
no_of_lines = 1
circle_radius = 10
color = (255, 0, 0)

base_path = '.\images'
images_path = os.listdir(base_path)
image_points = []
image_points1 = []
last_img = None
editing = False
l_x = 60
l_y = 60
move_point = False
l_x1 = 60
l_y1 = 60
shape_code = 0
thick = 1
current_image = None

img1 = None

all_images_point = []
all_images_point1 = []
l_point = None
l_img_path = None
l_img_path1 = None


def eu_dist(x, y):
    d = 0.0
    for i in range(len(x)):
        d += pow((float(x[i]) - float(y[i])), 2)
    d = math.sqrt(d)
    return d / len(x)


def draw_shape(image, shape_code1, x, y):
    global circle_radius, color, shape_code, thick
    if shape_code == 0:
        image = cv2.circle(image, (x, y), circle_radius, color, thick)
    if shape_code == 1:
        image = cv2.rectangle(image, (x - circle_radius, y - circle_radius), (x + circle_radius, y + circle_radius),
                              color, thick)
        # image=cv2.circle(image, (x, y), circle_radius, color, 2)
    if shape_code == 2:
        p1 = (x, y - circle_radius)
        p2 = (x - circle_radius, y + circle_radius)
        p3 = (x + circle_radius, y + circle_radius)
        image = cv2.line(image, p1, p2, color, thick)
        image = cv2.line(image, p2, p3, color, thick)
        image = cv2.line(image, p1, p3, color, thick)
    return image


def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):
        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


def redraw_point(event, x, y, flags, param):
    global l_x1, l_y1, img1, current_image, image_points, color, circle_radius, l_img_path, all_images_point, move_point, dont_move, last_img, shape_code, edit_line, shape_code
    global all_images_point1, image_points1

    if event == 1:
        if current_image is not None and edit_line == 1:
            last_img = cv2.imread(l_img_path)
            all_images_point.append((x, y))
            img1 = cv2.imread(os.path.join(base_path, current_image))
            all_images_point.append((x, y))
            radius = int(l_x / 12)
            img1 = draw_shape(img1, 0, x, y)
            move_point = False
            dont_move = False
            temp = {current_image: (x, y), 'color': color, 'size': circle_radius, 'shape': shape_code}
            image_points.append(temp)
            cv2.imshow('zoom', img1)

            straight_line = Sort_Tuple(all_images_point)

            for c_point in straight_line:
                last_img = draw_shape(last_img, 0, c_point[0], c_point[1])

            # for point in all_images_point:
            #     img=draw_shape(img,0,point[0],point[1])
            # for i in range(1, len(straight_line)):
            #     last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 2)
            for c_point in straight_line:
                for data in image_points:
                    data_key = list(data.keys())
                    if data[data_key[0]] == c_point:
                        color = data['color']
                        circle_radius = data['size']
                        shape_code = data['shape']
                        last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                        continue
            cv2.imshow('image', last_img)

        if current_image is not None and edit_line == 2:
            last_img = cv2.imread(l_img_path)
            all_images_point1.append((x, y))
            img1 = cv2.imread(os.path.join(base_path, current_image))
            all_images_point1.append((x, y))
            radius = int(l_x / 12)
            img1 = draw_shape(img1, 0, x, y)
            move_point = False
            dont_move = False
            # cv2.imwrite(current_image,img)
            # writer.writerow({'image_name': current_image, 'x': x,'y':y})
            temp = {current_image: (x, y), 'color': color, 'size': circle_radius, 'shape': shape_code}
            image_points1.append(temp)
            cv2.imshow('zoom', img1)

            straight_line = Sort_Tuple(all_images_point1)

            for c_point in straight_line:
                last_img = draw_shape(last_img, 0, c_point[0], c_point[1])

            # for point in all_images_point:
            #     img=draw_shape(img,0,point[0],point[1])
            # for i in range(1, len(straight_line)):
            #     last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 2)
            for c_point in straight_line:
                for data in image_points:
                    data_key = list(data.keys())
                    if data[data_key[0]] == c_point:
                        color = data['color']
                        circle_radius = data['size']
                        shape_code = data['shape']
                        last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                        continue
            cv2.imshow('image', last_img)

    if event == 0 and img1 is not None and move_point and edit_line == 1:
        last_img = cv2.imread(l_img_path)
        img_cp2 = img1.copy()
        temp_points = all_images_point.copy()
        temp_points.append((x, y))
        straight_line = Sort_Tuple(temp_points)
        # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
        img_cp2 = cv2.line(img_cp2, (x, y - 7), (x, y + 7), color, 1)
        img_cp2 = cv2.line(img_cp2, (x - 7, y), (x + 7, y), color, 1)
        crop_image = img_cp2[y - l_y1:y + l_y1, x - l_x1:x + l_x1]
        # img_cp = draw_shape(img_cp, 0, x, y)
        if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
            cv2.imshow('zoom2', crop_image)
            print('zoom')
        # cv2.imshow('zoom2', crop_image)

        for c_point in straight_line:
            for data in image_points:
                data_key = list(data.keys())
                if data[data_key[0]] == c_point:
                    color = data['color']
                    # circle_radius=data['size']
                    # circle_radius=2
                    shape_code = data['shape']
                    last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                    continue

        # for point in all_images_point:
        #     img=draw_shape(img,0,point[0],point[1])
        for i in range(1, len(straight_line)):
            last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)
        cv2.imshow('image', last_img)

    if event == 0 and img1 is not None and move_point and edit_line == 2:
        last_img = cv2.imread(l_img_path)
        img_cp2 = img1.copy()
        temp_points = all_images_point1.copy()
        temp_points.append((x, y))
        straight_line = Sort_Tuple(temp_points)
        # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
        img_cp2 = cv2.line(img_cp2, (x, y - 7), (x, y + 7), color, 1)
        img_cp2 = cv2.line(img_cp2, (x - 7, y), (x + 7, y), color, 1)
        crop_image = img_cp2[y - l_y1:y + l_y1, x - l_x1:x + l_x1]
        # img_cp = draw_shape(img_cp, 0, x, y)
        if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
            cv2.imshow('zoom2', crop_image)
        # cv2.imshow('zoom2', crop_image)

        for c_point in straight_line:
            for data in image_points1:
                data_key = list(data.keys())
                if data[data_key[0]] == c_point:
                    color = data['color']
                    # circle_radius=data['size']
                    circle_radius = 2
                    shape_code = data['shape']
                    last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                    continue

        # for point in all_images_point:
        #     img=draw_shape(img,0,point[0],point[1])
        for i in range(1, len(straight_line)):
            last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)
        cv2.imshow('image', last_img)

    if event == cv2.EVENT_MOUSEWHEEL and flags > 0:
        print('mouse wheel event', x, y)

        if l_x1 >= 20 and l_y1 >= 20 and img1 is not None:
            l_y1 = l_y1 - 10
            l_x1 = l_x1 - 10
            img_cp = img1.copy()
            radius = int(l_x1 / 12)
            circle_radius = radius
            img_cp = cv2.line(img_cp, (x, y - 7), (x, y + 7), color, 1)
            img_cp = cv2.line(img_cp, (x - 7, y), (x + 7, y), color, 1)
            # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
            # img_cp=draw_shape(img_cp,0,x,y)
            crop_image = img_cp[y - l_y1:y + l_y1, x - l_x1:x + l_x1]
            if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
                cv2.imshow('zoom2', crop_image)
            # cv2.waitKey(10)
        else:
            print('Reach maximum zoom')
    elif event == cv2.EVENT_MOUSEWHEEL and flags < 0 and img1 is not None:
        print('mouse wheel event', x, y)
        if l_x1 < 200 and l_y1 < 200:
            l_y1 = l_y1 + 10
            l_x1 = l_x1 + 10
            img_cp = img1.copy()
            radius = int(l_x1 / 12)
            circle_radius = radius
            img_cp = cv2.line(img_cp, (x, y - 7), (x, y + 7), color, 1)
            img_cp = cv2.line(img_cp, (x - 7, y), (x + 7, y), color, 1)
            # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
            # img_cp = draw_shape(img_cp, 0, x, y)
            crop_image = img_cp[y - l_y1:y + l_y1, x - l_x1:x + l_x1]
            if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
                cv2.imshow('zoom2', crop_image)
            # cv2.waitKey(10)
        else:
            print('Reach maximum zoom')


cv2.namedWindow("zoom2", cv2.WINDOW_NORMAL)

dont_move = False
line2 = True


def click_and_crop(event, x, y, flags, param):
    global img, l_y, l_x, current_image, all_images_point, image_points, editing, base_path, color, circle_radius, dont_move, img1, move_point, last_img, shape_code
    global line2, all_images_point1, image_points1, edit_line
    # img=cv2.imread()

    if event == 1:
        if current_image is not None and not editing:
            if line2:
                last_img = cv2.imread(os.path.join(base_path, current_image))
                all_images_point.append((x, y))
                radius = int(l_x / 12)
                img = draw_shape(last_img, 0, x, y)
                # cv2.imwrite(current_image,img)
                # writer.writerow({'image_name': current_image, 'x': x,'y':y})
                temp = {current_image: (x, y), 'color': color, 'size': circle_radius, 'shape': shape_code}
                image_points.append(temp)
                cv2.imshow('image', img)
                line2 = False
            elif not line2:
                last_img = cv2.imread(os.path.join(base_path, current_image))
                all_images_point1.append((x, y))
                radius = int(l_x / 12)
                img = draw_shape(last_img, 0, x, y)
                # cv2.imwrite(current_image,img)
                # writer.writerow({'image_name': current_image, 'x': x,'y':y})
                temp = {current_image: (x, y), 'color': color, 'size': circle_radius, 'shape': shape_code}
                image_points1.append(temp)
                cv2.imshow('image', img)
                line2 = True

        elif editing and len(image_points) > 0:
            move_point = True
            if edit_line == 1:
                for point in image_points:
                    # print('dict keys',point.keys())
                    # for key in point.keys():
                    img_name = list(point.keys())[0]
                    c_color = list(point.keys())[1]
                    c_size = list(point.keys())[2]
                    c_shape = list(point.keys())[3]
                    img_point = point[img_name]
                    dist = eu_dist((x, y), img_point)
                    if dist < circle_radius:
                        dont_move = True
                        current_image = img_name
                        imge1 = cv2.imread(os.path.join(base_path, img_name))
                        imge1 = draw_shape(imge1, 0, img_point[0], img_point[1])
                        circle_radius = 1
                        imge1 = draw_shape(imge1, 0, img_point[0], img_point[1])

                        cv2.imshow('zoom', imge1)
                        # editing = False
                        image_points.remove(point)
                        all_images_point.remove(img_point)
                        img1 = imge1
            if edit_line == 2:
                for point in image_points1:
                    print('list of point 2', list(point.keys()))
                    # print('dict keys',point.keys())
                    # for key in point.keys():
                    img_name = list(point.keys())[0]
                    c_color = list(point.keys())[1]
                    c_size = list(point.keys())[2]
                    c_shape = list(point.keys())[3]
                    img_point = point[img_name]
                    dist = eu_dist((x, y), img_point)
                    if dist < circle_radius:
                        dont_move = True
                        current_image = img_name
                        imge1 = cv2.imread(os.path.join(base_path, img_name))
                        imge1 = draw_shape(imge1, 0, img_point[0], img_point[1])

                        cv2.imshow('zoom', imge1)
                        # editing = False
                        image_points1.remove(point)
                        all_images_point1.remove(img_point)
                        img1 = imge1

                        # l_img=img

        # cv2.destroyAllWindows()

    if event == 0 and not dont_move:
        img_cp = last_img.copy()
        img_cp2 = last_img.copy()
        radius = int(l_x / 12)
        # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
        img_cp = draw_shape(img_cp, 0, x, y)
        img_cp2 = cv2.line(img_cp2, (x, y - 7), (x, y + 7), color, 1)
        img_cp2 = cv2.line(img_cp2, (x - 7, y), (x + 7, y), color, 1)
        crop_image = img_cp2[y - l_y:y + l_y, x - l_x:x + l_x]
        # img_cp = draw_shape(img_cp, 0, x, y)
        if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
            cv2.imshow('zoom', crop_image)
        cv2.imshow('image', img_cp)

    if event == cv2.EVENT_MOUSEWHEEL and flags > 0 and not dont_move:
        print('mouse wheel event', x, y)

        if l_x >= 20 and l_y >= 20:
            l_y = l_y - 10
            l_x = l_x - 10
            img_cp = img.copy()
            radius = int(l_x / 12)
            img_cp = cv2.line(img_cp, (x, y - 7), (x, y + 7), color, 1)
            img_cp = cv2.line(img_cp, (x - 7, y), (x + 7, y), color, 1)
            # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
            # img_cp=draw_shape(img_cp,0,x,y)
            crop_image = img_cp[y - l_y:y + l_y, x - l_x:x + l_x]
            if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
                cv2.imshow('zoom', crop_image)
            # cv2.waitKey(10)
        else:
            print('Reach maximum zoom')
    elif event == cv2.EVENT_MOUSEWHEEL and flags < 0 and not dont_move:
        print('mouse wheel event', x, y)
        if l_x < 200 and l_y < 200:
            l_y = l_y + 10
            l_x = l_x + 10
            img_cp = img.copy()
            radius = int(l_x / 12)
            img_cp = cv2.line(img_cp, (x, y - 7), (x, y + 7), color, 1)
            img_cp = cv2.line(img_cp, (x - 7, y), (x + 7, y), color, 1)
            # img_cp = cv2.circle(img_cp, (x, y), radius, color, 2)
            # img_cp = draw_shape(img_cp, 0, x, y)
            crop_image = img_cp[y - l_y:y + l_y, x - l_x:x + l_x]
            if crop_image.shape[0] > 0 and crop_image.shape[1] > 0:
                cv2.imshow('zoom', crop_image)
            # cv2.waitKey(10)
        else:
            print('Reach maximum zoom')


w = 0
h = 0


def main_function():
    global img, base_path, images_path, current_image, all_images_point, all_images_point1, editing, circle_radius, line, l_point, color, l_img_path, last_img, shape_code, image_points1, image_points
    global line2, w, h
    for i in range(0, len(images_path) + 1):
        if i < (len(images_path)):
            img = cv2.imread(os.path.join(base_path, images_path[i]))
            if w == 0 and h == 0:
                w = img.shape[1]
                h = img.shape[0]
            last_img = img
            l_img_path = os.path.join(base_path, images_path[i])
            current_image = images_path[i]
            cv2.namedWindow("zoom", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("zoom", 300, 300)
            cv2.setMouseCallback("zoom", redraw_point)
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("image", w, h)
            cv2.setMouseCallback("image", click_and_crop)
            cv2.imshow('image', last_img)
            # k=cv2.waitKey(0)
            k = cv2.waitKey(0)
            if k == 27:  # Esc key to stop
                break
            elif k == ord('n'):  # normally -1 returned,so don't print it
                line2 = True
                continue
            else:
                print(k)  # else print its value
                line2 = True


        elif i == len(images_path):
            editing = True
            while True:
                last_img = cv2.imread(l_img_path)
                if editing:
                    for point in image_points:
                        c_point = list(point.keys())[0]
                        c_color = list(point.keys())[1]
                        c_size = list(point.keys())[2]
                        c_shape = list(point.keys())[3]
                        c_point = point[c_point]
                        color = point[c_color]
                        circle_radius = point[c_size]
                        shape_code = point[c_shape]
                        last_img = draw_shape(last_img, 0, c_point[0], c_point[1])

                    # for point in all_images_point:
                    #     img=draw_shape(img,0,point[0],point[1])
                    straight_line = Sort_Tuple(all_images_point)
                    for i in range(1, len(straight_line)):
                        last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)
                    if no_of_lines == 2:
                        for point in image_points1:
                            c_point = list(point.keys())[0]
                            c_color = list(point.keys())[1]
                            c_size = list(point.keys())[2]
                            c_shape = list(point.keys())[3]
                            c_point = point[c_point]
                            color = point[c_color]
                            circle_radius = point[c_size]
                            shape_code = point[c_shape]
                            last_img = draw_shape(last_img, 0, c_point[0], c_point[1])

                        # for point in all_images_point:
                        #     img=draw_shape(img,0,point[0],point[1])
                        straight_line = Sort_Tuple(all_images_point1)
                        for i in range(1, len(straight_line)):
                            last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)

                    cv2.imshow('image', last_img)
                    k = cv2.waitKey(0)
                    if k == 27:  # Esc key to stop
                        break
                    elif k == ord('n'):  # normally -1 returned,so don't print it
                        continue
                else:
                    # cv2.imshow('image', img)
                    k = cv2.waitKey(0)
                    editing = True
                    if k == 27:  # Esc key to stop
                        break
                    elif k == ord('n'):  # normally -1 returned,so don't print it
                        continue


def increase_circle_size():
    global circle_radius
    circle_radius = circle_radius + 2


def decrease_circle_size():
    global circle_radius
    circle_radius = circle_radius - 2


def increase_thick():
    global thick
    thick = thick + 1


def decrease_thick():
    global thick
    thick = thick - 1


def set_red():
    global color
    color = (0, 0, 255)


def set_green():
    global color
    color = (0, 255, 0)


def set_blue():
    global color
    color = (255, 0, 0)


def set_circle():
    global shape_code
    shape_code = 0


def set_square():
    global shape_code
    shape_code = 1


def set_triangle():
    global shape_code
    shape_code = 2


def save_data():
    global image_points, image_points1, color, circle_radius, shape_code, base_path
    print(image_points)
    if os.path.exists('./Results'):
        csvfile = open('./Results/results.csv', 'w')
    else:
        os.mkdir('./Results')
        csvfile = open('./Results/results.csv', 'w')
    fieldnames = ['image_name', 'x1', 'y1', 'x2', 'y2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer = csv.DictWriter(csvfile)
    writer.writeheader()

    if len(image_points) == len(image_points1):

        for i in range(0, len(image_points)):
            img1_point = image_points[i]
            img2_point = image_points1[i]
            p1_point = img1_point[list(img1_point.keys())[0]]
            img_val = cv2.imread(os.path.join(base_path, list(img1_point.keys())[0]))
            p1_color = img1_point['color']
            p1_shape = img1_point['shape']
            p1_size = img1_point['size']
            color = p1_color
            circle_radius = p1_size
            shape_code = p1_shape
            img_val = draw_shape(img_val, 0, p1_point[0], p1_point[1])

            p2_point = img2_point[list(img2_point.keys())[0]]
            p2_color = img2_point['color']
            p2_shape = img2_point['shape']
            p2_size = img2_point['size']
            color = p2_color
            circle_radius = p2_size
            shape_code = p2_shape

            img_val = draw_shape(img_val, 0, p2_point[0], p2_point[1])
            writer.writerow(
                {'image_name': list(img1_point.keys())[0], 'x1': p1_point[0], 'y1': p1_point[1], 'x2': p2_point[0],
                 'y2': p2_point[1]})
            if os.path.exists('./Results'):
                cv2.imwrite('./Results/' + list(img1_point.keys())[0] + '.jpg', img_val)
            else:
                os.mkdir('./Results')
                cv2.imwrite('./Results/' + list(img1_point.keys())[0] + '.jpg', img_val)


    elif len(image_points) > 0 and len(image_points1) == 0:

        for i in range(0, len(image_points)):
            img1_point = image_points[i]
            p1_point = img1_point[list(img1_point.keys())[0]]
            img_val = cv2.imread(os.path.join(base_path, list(img1_point.keys())[0]))
            p1_color = img1_point['color']
            p1_shape = img1_point['shape']
            p1_size = img1_point['size']
            color = p1_color
            circle_radius = p1_size
            shape_code = p1_shape
            img_val = draw_shape(img_val, 0, int(p1_point[0]), int(p1_point[1]))

            img_val = draw_shape(img_val, 0, p1_point[0], p1_point[1])
            writer.writerow({'image_name': list(img1_point.keys())[0], 'x1': p1_point[0], 'y1': p1_point[1]})
            if os.path.exists('./Results'):
                cv2.imwrite('./Results/' + list(img1_point.keys())[0] + '.jpg', img_val)
            else:
                os.mkdir('./Results')
                cv2.imwrite('./Results/' + list(img1_point.keys())[0] + '.jpg', img_val)
    csvfile.close()


def two_lines():
    global no_of_lines
    no_of_lines = 2


def edit_line_1():
    global edit_line
    edit_line = 1


def edit_line_2():
    global edit_line
    edit_line = 2


def dec_size_shape():
    global image_points, l_img_path, all_images_point, color, shape_code, circle_radius, last_img, no_of_lines, image_points1
    if circle_radius > 1:
        circle_radius = circle_radius - 1
    last_img = cv2.imread(l_img_path)
    if editing:
        i = 0
        for point in image_points:
            c_point = list(point.keys())[0]
            c_color = list(point.keys())[1]
            c_size = list(point.keys())[2]
            c_shape = list(point.keys())[3]
            c_point = point[c_point]
            color = point[c_color]
            image_points[i]['size'] = circle_radius
            shape_code = point[c_shape]
            last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
            i = i + 1

        # for point in all_images_point:
        #     img=draw_shape(img,0,point[0],point[1])
        straight_line = Sort_Tuple(all_images_point)
        for i in range(1, len(straight_line)):
            last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)
        if no_of_lines == 2:
            i = 0
            for point in image_points1:
                c_point = list(point.keys())[0]
                c_color = list(point.keys())[1]
                c_size = list(point.keys())[2]
                c_shape = list(point.keys())[3]
                c_point = point[c_point]
                color = point[c_color]
                image_points1[i]['size'] = circle_radius
                # circle_radius = point[c_size]
                shape_code = point[c_shape]
                last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                i = i + 1

            # for point in all_images_point:
            #     img=draw_shape(img,0,point[0],point[1])
            straight_line = Sort_Tuple(all_images_point1)
            for i in range(1, len(straight_line)):
                last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)

        cv2.imshow('image', last_img)


def inc_size_shape():
    global image_points, l_img_path, all_images_point, color, shape_code, circle_radius, editing, last_img, no_of_lines, image_points1
    circle_radius = circle_radius + 1
    last_img = cv2.imread(l_img_path)
    if editing:
        i = 0
        for point in image_points:
            c_point = list(point.keys())[0]
            c_color = list(point.keys())[1]
            c_size = list(point.keys())[2]
            c_shape = list(point.keys())[3]
            c_point = point[c_point]
            color = point[c_color]
            image_points[i]['size'] = circle_radius
            # circle_radius = point[c_size]
            shape_code = point[c_shape]
            last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
            i = i + 1

        # for point in all_images_point:
        #     img=draw_shape(img,0,point[0],point[1])
        straight_line = Sort_Tuple(all_images_point)
        for i in range(1, len(straight_line)):
            last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)

        if no_of_lines == 2:
            i = 0
            for point in image_points1:
                c_point = list(point.keys())[0]
                c_color = list(point.keys())[1]
                c_size = list(point.keys())[2]
                c_shape = list(point.keys())[3]
                c_point = point[c_point]
                color = point[c_color]
                image_points1[i]['size'] = circle_radius
                # circle_radius = point[c_size]
                shape_code = point[c_shape]
                last_img = draw_shape(last_img, 0, c_point[0], c_point[1])
                i = i + 1

            # for point in all_images_point:
            #     img=draw_shape(img,0,point[0],point[1])
            straight_line = Sort_Tuple(all_images_point1)
            for i in range(1, len(straight_line)):
                last_img = cv2.line(last_img, straight_line[i - 1], straight_line[i], color, 1)

        cv2.imshow('image', last_img)


def dec_size_win():
    global w, h
    w = w - 10
    h = h - 10
    cv2.resizeWindow("image", w, h)


def inc_size_win():
    global w, h
    w = w + 10
    h = h + 10
    # x,y,w,h=cv2.getWindowImageRect('image')
    cv2.resizeWindow("image", w, h)


def GUI():
    r = tk.Tk()
    r.title('Tool')
    r.geometry("150x500")
    button1 = tk.Button(r, text='size +', width=10, command=increase_circle_size)
    button2 = tk.Button(r, text='size -', width=10, command=decrease_circle_size)
    thick_inc = tk.Button(r, text='Thickness +', width=10, command=increase_thick)
    thick_dec = tk.Button(r, text='Thickness -', width=10, command=decrease_thick)
    button3 = tk.Button(r, text='Red', width=10, command=set_red)
    button4 = tk.Button(r, text='Green', width=10, command=set_green)
    button5 = tk.Button(r, text='Blue', width=10, command=set_blue)
    button6 = tk.Button(r, text='Circle', width=10, command=set_circle)
    button7 = tk.Button(r, text='Square', width=10, command=set_square)
    triangle = tk.Button(r, text='Triangle', width=10, command=set_triangle)
    two_lines_btn = tk.Button(r, text='Mark 2', width=10, command=two_lines)
    edit1_btn = tk.Button(r, text='Edit line1', width=10, command=edit_line_1)
    edit2_btn = tk.Button(r, text='Edit line2', width=10, command=edit_line_2)
    button8 = tk.Button(r, text='Save Data', width=10, command=save_data)

    dec_size = tk.Button(r, text='Markers size -', width=10, command=dec_size_shape)
    inc_size = tk.Button(r, text='Markers size +', width=10, command=inc_size_shape)

    dec_win_size = tk.Button(r, text='window size -', width=10, command=dec_size_win)
    inc_win_size = tk.Button(r, text='window size +', width=10, command=inc_size_win)
    button1.pack()
    button2.pack()
    thick_inc.pack()
    thick_dec.pack()
    button3.pack()
    button4.pack()
    button5.pack()
    button6.pack()
    button7.pack()
    triangle.pack()
    two_lines_btn.pack()
    edit1_btn.pack()
    edit2_btn.pack()
    inc_size.pack()
    dec_size.pack()
    inc_win_size.pack()
    dec_win_size.pack()
    button8.pack()
    r.mainloop()


import time

# thread.start_new_thread(main_function,())
thread.start_new_thread(GUI, ())
# time.sleep(2000)

main_function()
