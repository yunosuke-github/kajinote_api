from enum import Enum


class HouseUserStatus(Enum):

    INVITING = (1, '招待中')
    LIVE = (2, '住み込み中')
    REJECTION = (3, '拒否')

    def __init__(self, id, ja):
        self.id = id
        self.ja = ja
