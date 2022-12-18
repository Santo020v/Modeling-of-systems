from Task1.element import Element


class ElementHospital(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_type_element = None

    def getDelay(self):
        if self.name == 'Reception':
            match self.next_type_element:
                case 1:           
                    self.delay_mean = 15
                case 2:
                    self.delay_mean = 40
                case 3:
                    self.delay_mean = 30
        return super().getDelay()

    def inAct(self, next_type_element, t_start):
        pass
