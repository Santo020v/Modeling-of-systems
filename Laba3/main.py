import Task1.model as m
import Task1.create as cr
import Task1.processor  as pr
from Task2.createBank import CreateBank
from Task2.processorbank import ProcessBank
import Task1.element as e
from Task2.modelBank import ModelBank
from Task3.processorHospital import ProcessHospital
from Task3.createHospital import CreateHospital
from Task3.modelHospital import ModelHospital
from Task3.elementHospital2 import ElementH2


def Task1_Multichannel():
    c = cr.Create(3)
    p1 = pr.Process(3, 3)
    maxQueue = 4
    model(c, p1, maxQueue)

def Task1_Probability():
    c = cr.Create(2)
    p1 = pr.Process(1)
    p2 = pr.Process(3)
    p3 = pr.Process(3)
    p4 = pr.Process(3)
    c.next_element = [p1]
    p1.next_element = [p2, p3, p4]

    p1.probability = ([0.1, 0.5, 0.4])
    p1.max_queue = 3
    p2.max_queue = 3
    p3.max_queue = 3
    p4.max_queue = 3
    c.distribution = 'exp'
    p1.distribution = 'exp'
    p2.distribution = 'exp'
    p3.distribution = 'exp'
    p4.distribution = 'exp'
    c.name = 'Creator'
    p1.name = 'Process1'
    p2.name = 'Process2'
    p3.name = 'Process3'
    p4.name = 'Process4'
    model = m.Model([c, p1, p2, p3, p4])
    model.simulate(1000)

def Task1_Priority():
    c = cr.Create(2)
    p1 = pr.Process(1)
    p2 = pr.Process(3)
    p3 = pr.Process(3)
    p4 = pr.Process(3)
    c.next_element = [p1]
    p1.next_element = [p2, p3, p4]

    p1.priority = [2, 1, 3]
    p1.max_queue = 3
    p2.max_queue = 3
    p3.max_queue = 3
    p4.max_queue = 3
    c.distribution = 'exp'
    p1.distribution = 'exp'
    p2.distribution = 'exp'
    p3.distribution = 'exp'
    p4.distribution = 'exp'
    c.name = 'Creator'
    p1.name = 'Process1'
    p2.name = 'Process2'
    p3.name = 'Process3'
    p4.name = 'Process4'

    model = m.Model([c, p1, p2, p3, p4])
    model.simulate(1000)
  
def model(c,p1, maxQueue):
    p1.max_queue = maxQueue
    c.distribution = 'exp'
    p1.distribution = 'exp'
    c.name = 'Creator'
    p1.name = 'Process1'
    c.next_element = [p1]
    model = m.Model([c, p1])
    model.simulate(1000)

def Task2():
    c1 = CreateBank(delay_mean=0.5, name='Creator', distribution='exp')
    p1 = ProcessBank(max_queue=3, delay_mean=0.3, name='Operator1', distribution='exp')
    p2 = ProcessBank(max_queue=3, delay_mean=0.3, name='Operator2', distribution='exp')

    c1.next_element = [p1, p2]
    p1.state[0] = p2.state[0] = 1
    p1.tnext[0] = e.normFn(1, 0.3)
    p2.tnext[0] = e.normFn(1, 0.3)

    c1.tnext[0] = 0.1
    p1.queue = p2.queue = 2
    element_list = [c1, p1, p2]
    bank = ModelBank(element_list, load_cashiers=[p1, p2])
    bank.simulate(1000)

def Task3():  
    names= ['Creator','Reception','Go to the Room','Go to Laboratory','Go to the Registry','Go to Analyzes','Go to Reception']
    c1 = CreateHospital(delay_mean=15.0, name=names[0], distribution='exp')
    p1 = ProcessHospital(max_queue=55, n_channel=2, name=names[1], distribution='exp')
    p2 = ProcessHospital(max_queue=55, delay_mean=3.0, delay_dev=8, n_channel=3, name=names[2],distribution='uniform')
    p3 = ProcessHospital(max_queue=5, delay_mean=2.0, delay_dev=5, n_channel=5, name=names[3],distribution='uniform')
    p4 = ProcessHospital(max_queue=55, delay_mean=4.5, delay_dev=3, n_channel=1, name=names[4],distribution='erlang')
    p5 = ProcessHospital(max_queue=55, delay_mean=4.0, delay_dev=2, n_channel=1, name=names[5],distribution='erlang')
    p6 = ProcessHospital(max_queue=5, delay_mean=2.0, delay_dev=5, n_channel=5, name=names[6],distribution='uniform')

    d1 = ElementH2(name='Exit1')
    d2 = ElementH2(name='Exit2')

    c1.next_element = [p1]
    p1.next_element = [p2, p3]
    p2.next_element = [d1]
    p3.next_element = [p4]
    p4.next_element = [p5]
    p5.next_element = [d2, p6]
    p6.next_element = [p1]

    p1.prior_types = [1]

    p1.required_path = [[1], [2, 3]]
    p5.required_path = [[3], [2]]
    model = ModelHospital([c1, p1, p2, p3, p4, p5, p6, d1, d2])
    model.simulate(1000)

if __name__ == "__main__":
    #Task1_Multichannel()
    #Task1_Probability()
    #Task1_Priority()
    #Task2()
    Task3()