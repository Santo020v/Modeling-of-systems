import Element as e

class Create(e.Element):
    def __init__(self, delay):
        super().__init__(delay)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + self.get_delay()
        self.next_element[0].inAct()