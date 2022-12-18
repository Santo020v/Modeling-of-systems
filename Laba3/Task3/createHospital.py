import numpy as np

from Task3.elementHospital import ElementHospital


class CreateHospital(ElementHospital):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + super().getDelay()
        self.next_type_element = np.random.choice([1, 2, 3], p=[0.5, 0.1, 0.4])
        next_element = self.chooseNextElement()
        next_element.inAct(self.next_type_element, self.tcurr)
