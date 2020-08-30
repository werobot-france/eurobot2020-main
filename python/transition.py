from matplotlib import pyplot
import numpy

def saturation(minX, maxX, minY, maxY, value):
  if value <= minX:
    return minY
  elif value >= maxX:
    return maxY
  else:
    a = (maxY-minY)/(maxX - minX)
    b = minY - a*minX
    return a * value + b

def transition(delta):
  fromD = 20
  return saturation(5, 30, 5, 45, delta)

pyplot.style.use('ggplot')

figure,axes = pyplot.subplots()
axes.set_aspect(1)
axes.set_xlabel("Input delta dist")
axes.set_ylabel("Speed")
axes.set_title("Transition")
axes.set_xlim(left=0,right=50)
axes.set_ylim(bottom=0,top=50)

x_values = numpy.linspace(0,100,1000)
y_values = []
for x in x_values:
  y_values.append(transition(x))

axes.plot(x_values,y_values,label="")

axes.legend()

figure.savefig("wow.png")