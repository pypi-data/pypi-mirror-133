from math import sqrt


class FOV():
    def __init__(self, radius):
        self.radius = radius


def is_in_fov(fov, x, y):
    dx = (fov.owner.x-x) ** 2
    dy = (fov.owner.y-y) ** 2
    c = sqrt(dx + dy)

    return c <= fov.radius

