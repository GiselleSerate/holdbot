class RingBuffer:
    def __init__(self, size):
        self.buffer = []
        self.cur_idx = 0
        self.num_items = 0
        self.max_size = size

    def add(self, value):
        if self.num_items == self.max_size:
            return None
        self.buffer[self.cur_idx % self.max_size] = value
        self.cur_idx += 1
        self.num_items += 1

    def pop(self):
        ret_val = self.buffer[self.cur_idx]
        self.buffer[self.cur_idx] = None
        self.num_items -= 1

    def is_full(self):
        return self.num_items == self.max_size
