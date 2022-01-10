from matplotlib import pyplot

def get_y():
    y = 0
    for i in range(1, 100):
        y += i
        yield y

x = range(10)
fig, ax1 = pyplot.subplots(num="Sequence Plot")
ax1.plot(x, y, "ro")
pyplot.show()