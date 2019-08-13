import os


def get_animations(name_of_game_entity):
    directory_path = os.path.join(
        os.getcwd(),
        'game_icons',
        name_of_game_entity
    )
    animations = list()
    for filename in os.listdir(directory_path):
        with open(os.path.join(directory_path, filename)) as file:
            animations.append(file.read())
    return animations
