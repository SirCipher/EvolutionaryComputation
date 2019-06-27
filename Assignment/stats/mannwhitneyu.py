import scipy.stats as stats

one_range = []
axis_range = []

with open('../one_range.txt') as f:
    one_range = f.read().splitlines()

with open('../axis_range.txt') as f:
    axis_range = f.read().splitlines()

u_statistic, pVal = stats.mannwhitneyu(one_range, axis_range)

print(u_statistic)
print(pVal)
