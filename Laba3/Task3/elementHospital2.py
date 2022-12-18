import numpy as np
from Task3.elementHospital import ElementHospital


class ElementH2(ElementHospital):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnext = [np.inf]
        self.delta_t_finished1 = 0
        self.delta_t_finished2 = 0
        self.delta_t_finished3 = 0
        self.type1 = 0
        self.type2 = 0
        self.type3 = 0

    def inAct(self, next_type_element, t_start):
        match next_type_element:
            case 1:
                self.delta_t_finished1 += self.tcurr - t_start
                self.type1 += 1
            case 2:
                self.delta_t_finished2 += self.tcurr - t_start
                self.type2 += 1
            case 3:
                self.delta_t_finished3 += self.tcurr - t_start
                self.type3 += 1
        super().outAct()
