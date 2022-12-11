import random
import numpy as np

class Element:
    nextId = 0

    def __init__(self, delay=None, distribution=None):
        self.id_el = Element.nextId
        self.name = 'Element' + str(self.id_el)
        self.tnext = [0]  
        self.delay_mean = delay  
        self.delay_dev = None
        self.distribution = distribution
        self.quantity = 0
        self.tcurr = self.tnext 
        self.state = [0]
        self.next_element = None  
        Element.nextId += 1
        self.probability = [1]

    def get_delay(self):
        #if self.distribution=='exp':
        #    return fn.exp(self.delay_mean)
        #elif self.distribution=='norm':
        #    return fn.norm(self.delay_mean, self.delay_dev)
        #elif self.distribution=='unif':
        #    return fn.uniform(self.delay_mean, self.delay_dev)
        #elif self.distribution=='':
        #    return self.delay_mean

        return self.exp(self.delay_mean)
        


    def exp(self, time_mean):
        a = random.uniform(0.0001, 1)
        a = -time_mean * np.log(a)
        return a

    def inAct(self):  
        pass

    def outAct(self):  
        self.quantity += 1

    def getState(self):
        return self.state

    def setState(self, new_state):
        self.state = new_state

    def setTNext(self, tnext_new):
        self.tnext = tnext_new

    def getTCurr(self):
        return self.tcurr

    def printResult(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def printInfo(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} tnext = {self.tnext}')

    def calculate(self, delta):
        pass

    def calculateMean(self, delta):
        pass
