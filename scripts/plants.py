from scripts.entities import Entity

from scripts.utils import make_object_image

class Plant(Entity):
    def __init__(self, permutation, images={'idle': [make_object_image('plant')]}):
        super().__init__(None, permutation, images)



