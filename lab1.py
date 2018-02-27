import sys, os
import csv, math
from random import Random

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class DataGenerator:
    def __init__(self, input_file, output_file, seed, period):
        self.input_file = input_file
        self.output_file = output_file
        self.__r = Random()
        self.__r.seed(seed)
        self.__iter_num = 1000
        self.per = period
        self.avr = []

    def __func_x1(self, x1_list):
        for x in x1_list:
            yield (2 * x + x ** 2 + 0.5 * x ** 3 + x ** 4 + 2 * x ** 5)
            # yield math.sin(x)

    def get_f1(self, xstrm):
        return self.__func_x1(xstrm)

    def __func_x2(self, x2_list):
        for x in x2_list:
            yield 20000 * math.sin(x)
            # yield math.cos(x)

    def get_f2(self, xstrm):
        return self.__func_x2(xstrm)

    def __func_y(self):
            return self.__r.uniform(self.per[0], self.per[1])

    def get_y(self):
        yield from [self.__func_y() for _ in range(self.__iter_num)]

    def __x_stream(self):
        step = (self.per[1] - self.per[0])/self.__iter_num
        result = self.per[0]
        for _ in range(self.__iter_num):
            yield result
            result += step

    def get_x_stream(self):
        return self.__x_stream()

    def __params(self):
        xstrm1 = self.get_x_stream()
        xstrm2 = self.get_x_stream()
        f1 = self.__func_x1(xstrm1)
        f2 = self.__func_x2(xstrm2)
        yield from [[x1, x2, self.__func_y()] for x1, x2 in zip(f1, f2)]

    def get_params(self):
        return self.__params()

    def get_extr(self):
        minimum = [
            min(self.get_f1(self.get_x_stream())),
            min(self.get_f2(self.get_x_stream())),
            min(self.get_y())
        ]
        maximum = [
            max(self.get_f1(self.get_x_stream())),
            max(self.get_f2(self.get_x_stream())),
            max(self.get_y())]
        average = [
            sum(self.get_f1(self.get_x_stream()))/self.__iter_num,
            sum(self.get_f2(self.get_x_stream()))/self.__iter_num,
            sum(self.get_y())/self.__iter_num
        ]
        self.avr = average
        return (minimum, maximum, average)

    def get_matched_condition(self, value_list):
        for value_trio in value_list:
            if value_trio[0] < self.avr[0] or value_trio[1] < self.avr[1]:
                yield value_trio


    def write_to_csv_file(self, value_list):
        with open(self.output_file, 'w', newline='') as csv_file:
            fwriter = csv.writer(csv_file, dialect='unix', delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for value_trio in value_list:
                fwriter.writerow(map(str, value_trio))
            csv_file.close()

    def read_from_csv_file(self):
        with open(self.input_file, 'r', newline='') as csv_file:
            freader = csv.reader(csv_file, dialect='unix', delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for value_trio in freader:
                yield map(float, value_trio)


if __name__ == '__main__':
    dg = DataGenerator(None, 'output.csv', 13, [-3,3])
    # params = list(dg.get_params())
    # x = list(dg.get_x_stream())

    dg.write_to_csv_file(dg.get_params())
    mn, mx, avr = dg.get_extr()

    print('Min \n->\n X1: {0}\nX2: {1}\n Y: {2}\n'.format(mn[0], mn[1], mn[2]))
    print('Max \n->\n X1: {0}\nX2: {1}\n Y: {2}\n'.format(mx[0], mx[1], mx[2]))
    print('Average \n->\n X1: {0}\nX2: {1}\n Y: {2}\n'.format(avr[0], avr[1], avr[2]))

    dg.output_file = 'cond_output.csv'

    dg.write_to_csv_file(dg.get_matched_condition(dg.get_params()))

    x = list(dg.get_x_stream())
    x1 = list(dg.get_f1(dg.get_x_stream()))
    x2 = list(dg.get_f2(dg.get_x_stream()))
    y = list(dg.get_y())
    x1y = list(dg.get_f1(dg.get_y()))
    x2y = list(dg.get_f2(dg.get_y()))

    plt.plot(x, x1, 'r-', x, x2, 'b-')
    plt.axis([-40,40,-40,40])
    plt.grid(True, linestyle='-.')
    plt.show()

    plt.plot(y, x1y, 'rs', y, x2y, 'b^')
    plt.axis([-40, 40, -40, 40])
    plt.grid(True, linestyle='-.')
    plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_trisurf(x1, x2, y)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # plt.grid(True, linestyle='-.')
    plt.show()