import random
import queue


class cache:
    B = 8  # 8 * 8bytes (8 * 64bit double) in a block
    E = 16  # 16 lines in a set
    S = 2  # 16 sets of the cache

    def __init__(self):

        # self.block = [[None] * 16] * 16 # No need to store the actual contents.
        self.tags = [[None] * self.E] * self.S
        self.hit = 0
        self.miss = 0

    @classmethod
    def matToIdx(self, i, j, col_max):
        '''
        Assume the adr of matrix and cache is matched

        @param i: row index of matrix
        @param j: column index of matrix
        @param col_max
        @return: the *adr index* of the given element
        '''
        res = 0
        res += i * col_max
        res += j
        res //= self.B  # int div
        # res >> 3 # should be the same
        return res  # res % 16: set index

    def _count(self, hit):
        if hit:
            self.hit += 1
        else:
            self.miss += 1
        return

    def _hit(self, set_idx, tag):
        return tag in self.tags[set_idx]

    def _has_empty(self, set_idx):
        return None in self.tags[set_idx]

    def read(self, adr):
        # adr: scaled by the length of double
        # usage: c.read(cache.matToIdx(i, j, col_num))
        set_idx = adr % self.S
        tag = adr // self.S
        if self._has_empty(set_idx):
            self._count(False)
            i = self.tags[set_idx].index(None)
            self.tags[set_idx][i] = tag
            self._update_empty(set_idx, tag, i)
        elif self._hit(set_idx, tag):
            self._count(True)
            i = self.tags[set_idx].index(tag)
            self._update_hit(set_idx, tag, i)
        else:
            self._count(False)
            self._replace(set_idx, tag)

    # least frequently used
    def setLFU(self, T=4):
        self.T = T
        self.queues = [[queue.Queue(self.T)] * self.E] * self.S
        self.queues[0][0].qsize()
        self.freq = [[0] * self.E] * self.S

        self._replace = self.LFU_replace
        self._update_empty = self._update_hit = self.LFU_update
        return

    def LFU_replace(self, set_idx, tag):
        self._update_avg_LFU()
        # find the last frequent one to replace
        i = self.freq[set_idx].index(min(self.freq[set_idx]))
        self.tags[set_idx][i] = tag
        self._update_queue_LFU(set_idx, i)

    def LFU_update(self, set_idx, tag, i):
        self._update_avg_LFU()
        self._update_queue_LFU(set_idx, i)

    def _update_avg_LFU(self):
        for freq_set_idx, queue_set in zip(list(range(self.freq)), self.queues):
            # need to skip the empty queues, where freq are zero
            self.freq[freq_set_idx] = [queue_sum(queue_line) / queue_line.qsize()
                                       for queue_line in queue_set if queue_line.qsize()]
        return

    def _update_queue_LFU(self, set_idx, last_access_line_number):
        i = last_access_line_number
        # set: set of queue
        set = self.queues[set_idx]
        for line in set[:i] + set[i + 1:]:
            if line.qsize() == self.T:
                line.get()
                line.put(0)
            elif line.qsize() < self.T:
                line.put(0)
            else:
                assert False, 'should not run here'
        if set[i].qsize() == self.T:
            set[i].get()
            set[i].put(1)
        else:
            set[i].put(1)
        return

    # not frequently used
    def setNFU(self, max_freq=1 << 8):
        self.MAX_FREQ = max_freq
        self.freq = [[0] * self.E] * self.S
        self._replace = self.NFU_replace
        self._update_hit = self._update_empty = self.NFU_update

        return

    def NFU_replace(self, set_idx, tag):
        self._aging_NFU()
        # find the min frequency
        set = self.freq[set_idx]
        line_idx = set.index(min(set))
        # replace
        self.tags[set_idx][line_idx] = tag
        self.freq[set_idx][line_idx] = self.MAX_FREQ

    def NFU_update(self, set_idx, tag, i):
        self._aging_NFU()
        self.freq[set_idx][i] += self.MAX_FREQ

    def _aging_NFU(self):
        for set_idx in range(len(self.freq)):
            set = self.freq[set_idx]
            # what I did was to change the REFERENCE of the list...
            # even though lists are passed by reference...
            self.freq[set_idx] = [line >> 1 for line in set]

    # least recent used

    def setLRU(self):
        self.last_access = [[0] * self.E] * self.S
        self._update_hit = self._update_empty = self.LRU_update
        self._replace = self.LRU_replace
        return

    def _increment_LRU(self):
        for set_idx in range(len(self.last_access)):
            set = self.last_access[set_idx]
            self.last_access[set_idx] = [line + 1 for line in set]

    def LRU_replace(self, set_idx, tag):
        self._increment_LRU()
        # find the largest last_access
        set = self.last_access[set_idx]
        line_idx = set.index(max(set))
        # replace
        self.tags[set_idx][line_idx] = tag
        self.last_access[set_idx][line_idx] = 0

    def LRU_update(self, set_idx, tag, i):
        self._increment_LRU()
        self.last_access[set_idx][i] = 0

    # random replace
    def setRandom(self):
        self._replace = self.random_replace
        return

    def random_replace(self, set_idx, tag):
        i = random.randint(1, self.E)
        self.tags[set_idx][i - 1] = tag
        return

    def setFIFO(self):
        self.queues = [queue.Queue(self.E)] * self.S
        self._replace = self.FIFO_replace

        self._update_empty = self.FIFO_add_to_empty
        return

    def FIFO_replace(self, set_idx, tag):
        i = self.queues[set_idx].get()
        self.tags[set_idx][i] = tag
        self.queues[set_idx].put(i)

    def FIFO_add_to_empty(self, set_idx, tag, i):
        self.queues[set_idx].put(i)

    def _update_hit(self, set_idx, tag, i):
        return

    def _update_empty(self, set_idx, tag, i):
        return

    def _replace(self, set_idx, tag):
        assert False, 'undefined replacement strategy'

    # Belady strategy, optimal

    def belady(self, adr_seq):
        '''
        adr_seq: all address that will be used in the future
        '''


def queue_sum(q):
    ls = []
    while not q.empty():
        ls.append(q.get())
    for x in ls:
        q.put(x)
    return sum(ls)
