import numpy as np
import Element as e

class Process(e.Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0
        self.max_observed_queue = 0
        self.max_queue = float('inf')
        self.mean_queue = 0.0
        self.failure = 0
        self.mean_load = 0
        self.channel = channels
        self.tnext = [np.inf]*self.channel
        self.state = [0]*self.channel
        self.probability = [1]

    def inAct(self):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().get_delay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        current_channel = self.getcurrent_channel()
        for i in current_channel:
            super().outAct()
            self.tnext[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + self.get_delay()
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.inAct()

    def get_free_channels(self):
        free_channels = []
        for i in range(self.channel):
            if self.state[i] == 0:
                free_channels.append(i)

        return free_channels

    def getcurrent_channel(self):
        current_channels = []
        for i in range(self.channel):
            if self.tnext[i] == self.tcurr:
                current_channels.append(i)
        return current_channels

    def printInfo(self):
        super().printInfo()
        print(f'failure = {str(self.failure)}')

    def calculate(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        for i in range(self.channel):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channel
