import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.collections as mcoll
import matplotlib.path as mpath

def colorline(
    x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
        linewidth=3, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

def make_plot(file_path, i):
    data = file_path
    N = 10
    np.random.seed(101)
    x = data["cX"]
    y = data["cY"]
    frame = data["Frame"]

    fig, ax = plt.subplots()
    
    batas = len(data)
    xbegend = []
    ybegend = []
    fbegend = []
    xbeg = x[0]
    ybeg = y[0]
    xend = x[batas-1]
    yend = y[batas-1]
    
    fbeg = frame[0]
    fend = frame[batas-1]
    xbegend.append(xbeg)
    xbegend.append(xend)
    ybegend.append(ybeg)
    ybegend.append(yend)
    fbegend.append(fbeg)
    fbegend.append(fend)

    path = mpath.Path(np.column_stack([x, y]))
    verts = path.interpolated(steps=3).vertices
    x, y = verts[:, 0], verts[:, 1]

    z = np.linspace(0, 1, len(x))
    plt.scatter(x, y, color='white')
    col = plt.scatter(xbegend, ybegend, s=200, c=fbegend, cmap="plasma")
    colorline(x, y, z, cmap=plt.get_cmap('plasma'), linewidth=2)
    plt.colorbar(col, format="%d")

    plt.savefig("static/temp/{}.png".format(i))