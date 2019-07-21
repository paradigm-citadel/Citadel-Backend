from random import choice

# https://www.artlebedev.ru/colors/
SAFE_GRADATIONS = [51, 102, 153, 204]

def get_random_color():
    rgb_values = [choice(SAFE_GRADATIONS) for i in range(0,3)]
    return u'#{:02x}{:02x}{:02x}'.format(*rgb_values)

def get_new_color(exclude=None):
    rgb_hex = None
    for i in range(0, 100):
        rgb_hex = get_random_color()
        if exclude and rgb_hex not in exclude:
            break

    return rgb_hex

