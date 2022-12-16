import random
import sys
import Create as cr
import Model as m
import Process as pr
import pandas as pd


def Task1():
    c = cr.Create(2)
    p1 = pr.Process(2)
    maxQueue = 3
    model(c,p1,maxQueue)


def Task3():
    c = cr.Create(3)
    p1 = pr.Process(3)
    p2 = pr.Process(3)
    p3 = pr.Process(3)

    c.next_element = [p1]
    p1.next_element = [p2]
    p2.next_element = [p3]

    p1.max_queue = 3
    p2.max_queue = 3
    p3.max_queue = 3

    c.distribution = 'exp'
    p1.distribution = 'exp'
    p2.distribution = 'exp'
    p3.distribution = 'exp'

    c.name = 'Creator'
    p1.name = 'Processor1'
    p2.name = 'Processor2'
    p3.name = 'Processor3'

    model = m.Model([c, p1, p2, p3])
    model.simulate(1000)


def Task4():
    inputData = pd.read_excel(r'C:\Users\veron\Desktop\Lab2\Lab2\InputData.xlsx')
    df = pd.DataFrame()
    rows = []


    for i in range(len(inputData)):
        distribution = 'exp'
        c = cr.Create(inputData['delay_create'][i])

        p1 = pr.Process(inputData['delay_p1'][i])
        p2 = pr.Process(inputData['delay_p2'][i])
        p3 = pr.Process(inputData['delay_p3'][i])

        p1.max_queue = inputData['max_q1'][i]
        p2.max_queue = inputData['max_q2'][i]
        p3.max_queue = inputData['max_q3'][i]

        c.distribution = distribution
        p1.distribution = distribution
        p2.distribution = distribution
        p3.distribution = distribution

        c.name = 'Creator'
        p1.name = 'Process 1'
        p2.name = 'Process 2'
        p3.name = 'Process 3'

        c.next_element = [p1]
        p1.next_element = [p2]
        p2.next_element = [p3]

        elements = [c, p1, p2, p3]
        model = m.Model(elements)
        res = model.simulate(1000)

        param = {'delay_create': inputData['delay_create'][i],
                 'delay_p1': inputData['delay_p1'][i],
                 'delay_p2': inputData['delay_p2'][i],
                 'delay_p3': inputData['delay_p3'][i],
                 'max_q1': inputData['max_q1'][i],
                 'max_q2': inputData['max_q2'][i],
                 'max_q': inputData['max_q3'][i],
                 'distribution': distribution,
                 'p1_processed': p1.quantity,
                 'p1_failed': p1.failure,
                 'p2_processed': p2.quantity,
                 'p2_failed': p2.failure,
                 'p3_processed': p3.quantity,
                 'p3_failed': p3.failure
                 }

        rows.append({**param})
    df = pd.DataFrame(rows)

    df.to_excel(r'C:\Users\veron\Desktop\Lab2\Lab2\Output.xlsx')


def Task5():
    c = cr.Create(3)
    p1 = pr.Process(3, 3)
    maxQueue = 4
    model(c, p1, maxQueue)


def Task6():
    c = cr.Create(2)
    p1 = pr.Process(1)
    p2 = pr.Process(3)
    p3 = pr.Process(3)
    p4 = pr.Process(3)
    c.next_element = [p1]
    p1.next_element = [p2, p3, p4]

    p1.probability = ([0.3, 0.5, 0.2])
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
    p1.name = 'Processor1'
    p2.name = 'Processor2'
    p3.name = 'Processor3'
    p4.name = 'Processor4'

    model = m.Model([c, p1, p2, p3, p4])
    model.simulate(1000)

def model(c,p1, maxQueue):
    p1.max_queue = maxQueue
    c.distribution = 'exp'
    p1.distribution = 'exp'
    c.name = 'Creator'
    p1.name = 'Processor1'
    c.next_element = [p1]
    model = m.Model([c, p1])
    model.simulate(1000)
 

if __name__ == "__main__":
    #Task1()
    #Task3()
    #Task5()
    Task6()
