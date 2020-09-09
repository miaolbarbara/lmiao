import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
mpl.use('QT5Agg')
'''
Matplotlib is very easy to use to plot real time data and animate datas,
If there is one thing to criticize Matplotlib, it is its relative slowness. 
This is a test script uesd to draw some random numbers as quickly as possible, 
and it tests how many plots matplotlib can display with this computer
my computer result: num_plots = 12

with pause function, it helps slightly:
my computer result: num_plots with pause(0.001) = 13

As it turns out, pause() internally calls 
fig.canvas.draw(), 
then plt.show(), 
then fig.canvas.start_event_loop(). T
he default implementation of fig.canvas.start_event_loop() then calls fig.canvas.flush_events(), 
then sleeps for the requested time.
so we can directly call fig.canvas.draw()
here, the result is 39

To optimise fig.canvas.draw() function
What this really is doing is drawing all the artists contained in the ax. 
Those artists can be accessed using ax.get_children().
'''
def speed_test_without_pause():
    fig, ax = plt.subplots()

    tstart = time.time()
    num_plots = 0
    while time.time()-tstart < 1:
        ax.clear()
        ax.plot(np.random.randn(100))
        plt.pause(0.001)
        num_plots += 1
    print(num_plots)


def speed_test_with_pause():
    # creating all the axes and text labels takes a lot of time
    # initialisation of axes should be done first before plotting
    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))

    tstart = time.time()
    num_plots = 0
    while time.time()-tstart < 1:
        line.set_ydata(np.random.randn(100))
        plt.pause(0.001)
        num_plots += 1
    print(num_plots)

def speed_canvas_draw():
    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))

    tstart = time.time()
    num_plots = 0
    while time.time() - tstart < 1:
        line.set_ydata(np.random.randn(100))
        fig.canvas.draw()
        fig.canvas.flush_events()
        num_plots += 1
    print(num_plots)

def optimize_canvas_draw():
    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))
    plt.show(block=False)

    tstart = time.time()
    num_plots = 0
    while time.time() - tstart < 5:
        line.set_ydata(np.random.randn(100))
        ax.draw_artist(line)
        fig.canvas.update()
        fig.canvas.flush_events()
        num_plots += 1
    print(num_plots / 5)

if __name__ == '__main__':

    speed_test_without_pause()
    speed_test_with_pause()
    speed_canvas_draw()
    # optimize_canvas_draw()