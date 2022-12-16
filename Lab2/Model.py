import numpy as np
import Process


class Model:
    def __init__(self, elements: list):
        self.list = elements
        self.tnext = 0.0
        self.tcurr = self.tnext
        self.event = 0

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
        print('-----RESULTS-----')

        meanqueue_length_sum = 0
        failure_probability_sum = 0
        meanload_sum = 0
        num_of_processors = 0

        for e in self.list:
            e.printResult()
            if isinstance(e, Process.Process):
                num_of_processors += 1

                mean_queue_length = e.mean_queue / self.tcurr
                failure_probability = e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0
                mean_load = e.mean_load / self.tcurr

                print(f"Average queue length: {mean_queue_length}")
                print(f"Failure probability: {failure_probability}")
                print(f"Avarage load: {mean_load}")
                print(' ')

                meanqueue_length_sum += mean_queue_length
                failure_probability_sum += failure_probability
                meanload_sum += mean_load

        meanqueue_length_result = mean_queue_length / num_of_processors
        failure_probability_result = failure_probability / num_of_processors
        meanload_result = mean_load / num_of_processors

        print(f"Global average queue length: {meanqueue_length_result}")
        print(f"Global failure probability: {failure_probability_result}")
        print(f"Global average load: {meanload_result}")

        print()

        return {
            "meanqueue_length_result": meanqueue_length_result,
            "failure_probability_result": failure_probability_result,
            "meanload_result": meanload_result
        }
    
