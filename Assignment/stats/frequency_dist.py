import math
from decimal import Decimal
import statistics
import matplotlib.pyplot as plt

normal = []
ff = []

with open('../axis_range_normal.txt') as f:
    normal = f.read().splitlines()

with open('../axis_range_ff.txt') as f:
    ff = f.read().splitlines()


def parse(a):
    for i, j in enumerate(a):
        if Decimal(j) < 0:
            a[i] = 0
            continue

        # j = math.sqrt(math.fabs(Decimal(j)))
        a[i] = math.fabs(Decimal(j))

        # a[i] = math.ceil(j)


def plot(a, name):
    parse(a)
    plt.close()

    plt.hist(a, color='blue', edgecolor='black')
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig(name + '.png')


plot(normal, "normal")
plot(ff, "flood_fill")

# print(max(normal))
# print(max(ff))

a = len(ff)
sum = 0

for i in ff:
    sum += i

print(statistics.stdev(ff))
