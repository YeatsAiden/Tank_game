from settings import *


def clip_img(surf, x, y, width, height):
    # It makes clips of all your FAILURES
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())


def calculate_angle_to_point(point1, point2):
    x_change = point1[0] - point2[0]
    y_change = point1[1] - point2[1]

    return degrees(atan2(-y_change, x_change))


def calculate_smallest_angle(A, B):
    # given angles A and B find the smallest value to append to angle A and make it become angle B
    diff = B - A
    diff = (diff + 180) % 360 - 180  # magic of chatGPT
    return diff  # i promise, this is one of the only occasions where i had to use it


def rotate_to(current_angle, target_angle, rotation_step):
    smallest_angle = calculate_smallest_angle(current_angle, target_angle)

    rotation_change = rotation_step * (-1 if smallest_angle < 0 else 1)

    if abs(rotation_change) > abs(smallest_angle):
        current_angle = target_angle
    else:
        current_angle += rotation_change

    return current_angle
