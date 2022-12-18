import numpy as np
import Task1.element as e


class ProcessBank(e.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnext = [np.inf] * self.channel
        self.state = [0] * self.channel
        self.delta_t_in_bank = 0
        self.tprev_in_bank = 0
        self.delta_t_departure = 0
        self.tprev_departure = 0
        

    def inAct(self):
        free_route = self.getFreeChannels()
        if len(free_route) > 0:
            for i in free_route:
                self.tprev_in_bank = self.tcurr
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()
        current_channel = self.getCurrentChannel()
        for i in current_channel:

            self.tnext[i] = np.inf
            self.state[i] = 0
            self.delta_t_departure += self.tcurr - self.tprev_departure
            self.tprev_departure = self.tcurr
            self.delta_t_in_bank = + self.tcurr - self.tprev_in_bank
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.inAct()
