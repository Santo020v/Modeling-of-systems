import numpy as np
from Task3.elementHospital2 import ElementH2
from Task3.processorHospital import ProcessHospital
from Task1.model import Model


class ModelHospital(Model):
    def __init__(self, elements: list):
        super().__init__(elements)
        self.event = elements[0]

    def simulate(self, time):
        while self.tcurr < time:
            self.tnext = float('inf')
            for e in self.list:
                tnext_val = np.min(e.tnext)
                if tnext_val < self.tnext and not isinstance(e, ElementH2):
                    self.tnext = tnext_val
                    self.event = e.id_el
            for e in self.list:
                e.calculate(self.tnext - self.tcurr)
            self.tcurr = self.tnext
            for e in self.list:
                e.tcurr = self.tcurr

            if len(self.list) > self.event:
                self.list[self.event].outAct()
            for e in self.list:
                if self.tcurr in e.tnext:
                    e.outAct()
            self.printInfo()
        return self.printResult()

    def printInfo(self):
        for e in self.list:
            e.printInfo()
    def printResult(self):
        super().printResult()
        meanIntervalLab = 0
        meanFinishTime_ = 0
        num_of_processors = 0
        num_of_finished = 0

        for e in self.list:
            e.result()
            if isinstance(e, ProcessHospital):
                num_of_processors += 1

                if e.name == 'Go to Laboratory':
                    meanIntervalLab = e.delta_t_following_to_the_lab_reception / e.quantity

                if e.name == 'Go to Reception':
                    print(f'Mean time finishing for type 2 = {e.delta_t_finished2_new / e.type2_new if e.type2_new != 0 else np.inf}\n')

            elif isinstance(e, ElementH2):
                meanFinishTime_ += e.delta_t_finished1 + e.delta_t_finished2 + e.delta_t_finished3
                num_of_finished += e.quantity
                print(f'Mean time finishing for type 1 = {e.delta_t_finished1 / e.type1 if e.type1 != 0 else np.inf}')
                print(f'Mean time finishing for type 2 = {e.delta_t_finished2 / e.type2 if e.type2 != 0 else np.inf}')
                print(f'Mean time finishing for type 3 = {e.delta_t_finished3 / e.type3 if e.type3 != 0 else np.inf}')
                print('')

        meanFinishTime = meanFinishTime_ / num_of_finished

        print(f'Mean interval lab: {meanIntervalLab}')
        print(f'Mean finishing time: {meanFinishTime}')
        print('')
