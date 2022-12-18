import random
import numpy as np

from copy import deepcopy

class Element:
    nextId = 0

    def __init__(self, name=None, delay_mean=1., delay_dev=0., distribution='', probability=1, n_channel=1, max_queue=float('inf')):
        self.tnext = [0] * n_channel  
        self.delay_mean = delay_mean 
        self.delay_dev = delay_dev 
        self.quantity = 0
        self.tcurr = 0  
        self.state = [0] * n_channel
        self.next_element = None  
        self.id_el = Element.nextId
        Element.nextId += 1
        self.name = f'Element_{self.id_el}' if name is None else name
        self.distribution = distribution
        self.probability = [1]
        self.priority = [1]  
        self.queue = 0
        self.max_observed_queue = 0
        self.max_queue = max_queue
        self.mean_queue = 0.0
        self.channel = n_channel
        self.mean_load = 0
        self.failure = 0

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
            raise Exception('We cannot choose a route. Please specify probability OR priority value (not both)')

    def chooseByPriority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        min_queue_index = 0

        for i in range(len(priorities)):
            if min(priorities) == 100000:
                break

            max_priorities_index = priorities.index(min(priorities))

            if 0 in self.next_element[max_priorities_index].state:
                return self.next_element[max_priorities_index]
            else:
                if self.next_element[max_priorities_index].queue < min_queue:
                    min_queue = self.next_element[max_priorities_index].queue
                    min_queue_index = self.next_element.index(self.next_element[max_priorities_index])

            priorities[max_priorities_index] = 100000

        return self.next_element[min_queue_index]

    def getDelay(self):      
        match self.distribution:
            case 'exp':
                return self.expFn(self.delay_mean)
            case 'norm':
                return normFn(self.delay_mean, self.delay_dev)
            case 'uniform':
                return self.uniformFn(self.delay_mean, self.delay_dev)
            case 'erlang':
                return self.erlangFn(self.delay_mean, self.delay_dev)
            case _:
                return self.delay_mean

    def inAct(self):  
        pass

    def getState(self):
        return self.state

    def setState(self, new_state):
        self.state = new_state

    def setTNext(self, tnext_new):
        self.tnext = tnext_new

    def getTCurr(self):
        return self.tcurr

    def outAct(self):  
        self.quantity += 1

    def printResult(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def printInfo(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} tnext = {self.tnext}')

    def calculate(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        for i in range(self.channel):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channel
    
    def calculateMean(self, delta):
        pass
    
    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')
    
    def expFn(self, time_mean):
        a = random.uniform(0.0001, 1)
        a = -time_mean * np.log(a)
        return a

    def erlangFn(self,time_mean, time_deviation):
        a = 1
        for i in range(time_deviation):
            a *= random.random()
        return - np.log(a) / (time_deviation * time_mean)

    def uniformFn(self,time_min, time_max):
        a = random.uniform(0.0001, 1)
        a = time_min + a * (time_max - time_min)
        return a

    def getFreeChannels(self):
        free_channels = []
        for i in range(self.channel):
            if self.state[i] == 0:
                free_channels.append(i)

        return free_channels

    def getCurrentChannel(self):
        current_channels = []
        for i in range(self.channel):
            if self.tnext[i] == self.tcurr:
                current_channels.append(i)
        return current_channels


def normFn(time_mean, time_deviation):
        return time_mean + time_deviation * random.gauss(0.0, 1.0)