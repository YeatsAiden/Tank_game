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


# everything below is a scrapped function, don't play attention

def merge_able(rect1, rect2):
    edges = {rect1.topleft, rect1.topright, rect1.bottomleft, rect1.bottomright,
             rect2.topleft, rect2.topright, rect2.bottomleft, rect2.bottomright}

    if len(edges) == 6:
        return True

    return False


def merge_rects(rects: list[pg.FRect]):
    unchanged = False

    while unchanged is False:
        old_len = len(rects)

        do_break = False
        for i, rect1 in enumerate(rects):
            if do_break:
                break

            for j, rect2 in enumerate(rects):
                if do_break:
                    break

                if merge_able(rect1, rect2):
                    rects.remove(rect1)
                    rects.remove(rect2)

                    rects.append(rect1.union(rect2))

                    do_break = True


        if old_len == len(rects):
            unchanged = True


    return rects


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
