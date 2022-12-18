import Task1.element as e


class CreateBank(e.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()     
        self.tnext[0] = self.tcurr + super().getDelay()
        p1 = self.next_element[0]
        p2 = self.next_element[1]
        if p1.queue == p2.queue:
            p1.inAct()
        elif p1.queue == 0 and p2.queue == 0:
            p1.inAct()
        elif p1.queue < p2.queue:
            p1.inAct()
        else:
            p2.inAct()