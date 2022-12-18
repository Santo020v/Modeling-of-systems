from Task2.processorbank import *
from Task1.model import Model


class ModelBank(Model):

    def __init__(self, elements: list, load_cashiers=None):
        super().__init__(elements)
        self.time = 0
        self.load_cashiers = load_cashiers
        self.all_clients = 0
        self.out_clients = 0
        self.lane_change = 0 
        self.meanBankClients = 0

    def averageBankClients(self, delta):
        a = self.load_cashiers[0].queue + self.load_cashiers[1].queue + self.load_cashiers[0].state[0] + self.load_cashiers[1].state[0]
        self.meanBankClients += delta * a

    def simulate(self, time):
        while self.tcurr < time:
            self.tnext = float('inf')
            for e in self.list:
                tnext_val = np.min(e.tnext)
                if tnext_val < self.tnext:
                    self.tnext = tnext_val
                    self.event = e.id_el
            for e in self.list:
                e.calculate(self.tnext - self.tcurr)
            self.averageBankClients(self.tnext - self.tcurr)
            self.tcurr = self.tnext
            for e in self.list:
                e.tcurr = self.tcurr
            if len(self.list) > self.event:
                self.list[self.event].outAct()
            for e in self.list:
                if self.tcurr in e.tnext:
                    e.outAct()
            self.printInfo()
            self.changeQueue()
        self.printResult()

    def changeQueue(self):
        queue_list = list()
        for element in self.list:
            if isinstance(element, ProcessBank):
                queue_list.append(element.queue)
        q_1 = queue_list[0] - queue_list[1]
        q_2 = queue_list[1] - queue_list[0]
        if q_1 >= 2:
            self.list[1].queue -= 1
            self.list[2].queue += 1
            print("From Operator1 to Operator2.")
            self.lane_change += 1
        elif q_2 >= 2:
            self.list[1].queue += 1
            self.list[2].queue -= 1 
            print("From Operator2 to Operator1.")
            self.lane_change += 1

    def printInfo(self):
        for e in self.list:
            e.printInfo()

    def printResult(self):
        super().printResult()
        meanOutgoingTime_a = 0
        meanTimeInBank_a = 0
        num_of_processors = 0

        for e in self.list:
            e.result()
            if isinstance(e, ProcessBank):
                num_of_processors += 1
                meanOutgoingTime_a += e.delta_t_departure / e.quantity
                meanTimeInBank_a += e.delta_t_in_bank / e.quantity
                print(f'Mean time of outgoing = {e.delta_t_departure / e.quantity}')

        meanBankClients = self.meanBankClients / self.tcurr
        meanOutgoingTime = meanOutgoingTime_a / num_of_processors
        meanTimeInBank = meanTimeInBank_a / num_of_processors

        print(f"Global mean clients in bank: {meanBankClients}")
        print(f"Global mean time of outgoing: {meanOutgoingTime}")
        print(f"Global mean time in bank: {meanTimeInBank}")
        print(f"Global changed lines: {self.lane_change}")
        print()
