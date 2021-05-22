class Item:
    def __init__(self, item_id, item_locker_size, item_description):
        self.id = item_id
        self.ls = item_locker_size
        self.des = item_description


# item stored is to check if item is already used by the locker
