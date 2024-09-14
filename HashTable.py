class HashMap:
    def __init__(self, initial_size=20):
        self.table = [[] for _ in range(initial_size)]

    def add(self, key, value):  # Inserts or updates an item
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return True

        bucket.append([key, value])
        return True

    def get(self, key):
        index = hash(key) % len(self.table)
        bucket = self.table[index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def remove(self, key):
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                bucket.remove(pair)
                return True
        return False
