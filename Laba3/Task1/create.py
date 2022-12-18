import Task1.element as e
import Task1.processor as p

class Create(e.Element):
    def __init__(self, delay):
        super().__init__(delay)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + self.getDelay()
        next_element = self.chooseNextElement()
        next_element.inAct()