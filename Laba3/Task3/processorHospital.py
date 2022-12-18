import numpy as np
from Task3.elementHospital import ElementHospital


class ProcessHospital(ElementHospital):
    def __init__(self, required_path=None, **kwargs):
        super().__init__(**kwargs)
        self.types = [-1] * self.channel
        self.queue_types = []
        self.required_path = required_path
        self.prior_types = []

        self.delta_t_following_to_the_lab_reception = 0
        self.tprev_following_to_the_lab_reception = 0

        self.t_starts = [-1] * self.channel
        self.t_starts_queue = []

        self.delta_t_finished2_new = 0
        self.type2_new = 0

    def inAct(self, next_type_element, t_start):
        self.next_type_element = next_type_element

        if self.name == 'Go to Laboratory':
            self.delta_t_following_to_the_lab_reception += self.tcurr - self.tprev_following_to_the_lab_reception
            self.tprev_following_to_the_lab_reception = self.tcurr

        if self.name == 'Go to Reception' and next_type_element == 2:
            self.delta_t_finished2_new += self.tcurr - t_start
            self.type2_new += 1


        free_channels = self.getFreeChannels()
        for i in free_channels:
            self.state[i] = 1
            self.tnext[i] = self.tcurr + super().getDelay()
            self.types[i] = self.next_type_element
            self.t_starts[i] = t_start
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                self.queue_types.append(self.next_type_element)
                self.t_starts_queue.append(t_start)
                if self.queue > self.max_observed_queue:
                    self.max_obs_queue_length = self.queue
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()

        current_channels = self.getCurrentChannel()

        for i in current_channels:
            self.tnext[i] = np.inf
            self.state[i] = 0
            prev_next_type_element = self.types[i]
            prev_t_start = self.t_starts[i]
            self.types[i] = -1
            self.t_starts[i] = -1
            if self.queue > 0:
                self.queue -= 1
                prior_index = self.getPriorityIndex()
                self.next_type_element = self.queue_types.pop(prior_index)

                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                self.types[i] = self.next_type_element
                self.t_starts[i] = self.t_starts_queue.pop(prior_index)
            if self.next_element is not None:
                self.next_type_element = 1 if self.name == 'Go to Reception' else prev_next_type_element
                if self.required_path is None:
                    next_element = np.random.choice(self.next_element, p=self.probability)
                    next_element.inAct(self.next_type_element, prev_t_start)
                else:
                    for idx, path in enumerate(self.required_path):
                        if self.next_type_element in path:
                            next_element = self.next_element[idx]
                            next_element.inAct(self.next_type_element, prev_t_start)
                            break

    def getPriorityIndex(self):
        for prior_types_i in self.prior_types:
            for type_i in np.unique(self.queue_types):
                if type_i == prior_types_i:
                    return self.queue_types.index(type_i)
        else:
            return 0

    def print_info(self):
        super().printInfo()
        print(f'queue={self.queue}; failure={self.failure}')
        print(f'types of elements={self.types}')

    def calculate(self, delta):
        self.mean_queue_length = + delta * self.queue
