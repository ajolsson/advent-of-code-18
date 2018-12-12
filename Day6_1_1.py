import numpy as np
import matplotlib.pyplot as plt

#with open('day6Data_test1.txt') as f:
with open('day6Data.txt') as f:
    data = f.readlines()

system = {}
for line, val in zip(data, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    x, y = map(int, line.split(','))
    system[(x, y)] = val

ymax = max([y for x, y in system]) + 1
xmax = max([x for x, y in system]) + 1

board = np.zeros([xmax, ymax], dtype=int)
for x in range(xmax):
    for y in range(ymax):
        dmax = xmax + ymax
        letter = ord('@')
        for x0, y0 in system:
            d = abs(x - x0) + abs(y - y0)
            if d < dmax:
                dmax = d
                letter = ord(system[(x0, y0)])
            elif d == dmax:
                letter = ord('@')
        board[x, y] = letter

unique, counts = map(list, np.unique(board, return_counts=True))
border = list(set([board[0, y] for y in range(ymax)] +
                  [board[-1, y] for y in range(ymax)] +
                  [board[x, 0] for x in range(xmax)] +
                  [board[x, -1] for x in range(xmax)]))

for element in border:
    index = unique.index(element)
    del unique[index]
    del counts[index]

unique, counts = map(np.array, [unique, counts])
order = counts.argsort()
for unique, count in zip(unique[order], counts[order]):
    print(chr(unique), count)


plt.imshow(board.T, origin='lower')

for point in system:
     plt.annotate(xy=point, s=system[point], ha='center', va='center')
plt.xticks([])
plt.yticks([])

plt.show()