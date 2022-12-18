import numpy as np
from copy import deepcopy
import Task1.element as e


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
        self.priority = [1]

    def inAct(self):
        free_route = self.getFreeChannels()
        if len(free_route) > 0:
            for i in free_route:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        current_channel = self.getCurrentChannel()
        for i in current_channel:
            super().outAct()
            self.tnext[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + self.getDelay()
            if self.next_element is not None:
                next_el = self.chooseNextElement()
                next_el.inAct()

    def getFreeChannels(self):
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
        print(f'failure = {str(self.failure)}, queue_length = {str(self.queue)}')

    def calculate(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        for i in range(self.channel):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channel

    def chooseNextElement(self):
        if self.probability != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probability)
            return next_element
        elif self.priority != [1]:
            next_element = self.chooseByPriority()
            return next_element
        elif self.probability == [1] and self.priority == [1]:
            return self.next_element[0]
        elif self.probability != [1] and self.priority != [1]:
            raise Exception('Please specify probability OR priority value (not both)')

    def chooseByPriority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        min_queue_index = 0

        for i in range(len(priorities)):
            if min(priorities) == float('inf'):
                break
            max_pr_index = priorities.index(min(priorities))
            if 0 in self.next_element[max_pr_index].state:
                return self.next_element[max_pr_index]
            else:
                if self.next_element[max_pr_index].queue < min_queue:
                    min_queue = self.next_element[max_pr_index].queue
                    min_queue_index = self.next_element.index(self.next_element[max_pr_index])
            priorities[max_pr_index] = float('inf')

        return self.next_element[min_queue_index]
