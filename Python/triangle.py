import matplotlib.pyplot as plt
import numpy as np


def list_corners_and_colors():
    """
    Define a triangle. Corners of triangle stored as NumPy arrays
    which are again stored in a list.

    Also return a list of the basis colors for RGB coloring.
    """

    a = np.array([0, 0])
    b = np.array([1, 0])
    c = np.array([0.5, np.sqrt(3) / 2])  # elementary trigonometry
    r1 = np.array([1, 0, 0])
    r2 = np.array([0, 1, 0])
    r3 = np.array([0, 0, 1])
    return [a, b, c], [r1, r2, r3]


def starting_point():
    """
    Generate a random starting point within the triangle and corresponding
    starting color.

    Parameters
    ----------
    N:      int, number of starting points to be generated

    Returns
    ---------
    X:      NumPy array of size 2, representing the starting point
    C:      NumPy array of size 3, corresponding to the RGB color of the
            starting point
    """

    corners = list_corners_and_colors()[0]
    base_colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    w = np.random.random(size=3)
    X = np.zeros((1, 2))
    C = np.zeros((1, 2))
    w = w / w.sum()
    X = sum(wi * ci for wi, ci in zip(w, corners))
    C = sum(wi * clri for wi, clri in zip(w, base_colors))
    return X, C


def sequence(N):
    """
    Generate a sequence of points within the triangle, given
    a starting point x0, according to formula

    x(k+1) = (x(k) + c(k+1))/2,

    where c(k+1) is one of the triangle's corners selected at random.

    Discard the starting point and the first five points generated.

    Parameters
    ----------
    N:      int, length of sequence to be generate -6

    Returns
    --------
    X:      NumPy array of size (N, 2), containing the sequence of point,
            the first five point excluded
    """

    corners = list_corners_and_colors()[0]
    X = np.zeros((N, 2))
    X[0, :] = starting_point()[0]
    ci = np.array([corners[i] for i in np.random.randint(0, 3, size=N)])
    for i in range(N - 1):
        X[i + 1, :] = (X[i, :] + ci[i + 1]) / 2
    return X[5:, :]


def alternative_sequence(N):
    """
    Generate a sequence of points in the same way as sequence(N).
    Also return the randomly selected corners.

    Discard the starting point and the first five points generated.

    Parameters
    ----------
    N:      int, length of sequence to be generated -6

    Returns
    --------
    X:      NumPy array of size (N, 2), containing the sequence of point,
            the first five point excluded.
    idx:    NumPy array of size N, containing the randomly selected corners
            used in the formula, the first five excluded.
    """

    corners = list_corners_and_colors()[0]
    X = np.zeros((N, 2))
    X[0, :] = starting_point()[0]
    idx = np.random.randint(0, 3, size=N)
    ci = np.array([corners[i] for i in idx])
    for i in range(N - 1):
        X[i + 1, :] = (X[i, :] + ci[i + 1]) / 2
    return X[5:, :], idx[5:]


def fancy_color_sequence(N):
    """
    Generate a sequence of the same kind as sequence(N) accompanied
    by a matrix of RGB colors for each point.

    Parameters
    ----------
    N:      int, length of sequence to generated -6

    Returns
    --------
    X:      NumPy array of size (N, 2), containing the sequence of point,
            the first five point excluded.
    C:      NumPy array of size (N, 3), containing the RGB colors associated
            with each point.
    """

    corners, colors = list_corners_and_colors()
    X = np.zeros((N, 2))
    C = np.zeros((N, 3))
    X[0, :], C[0, :] = starting_point()
    idx = np.random.randint(0, 3, size=N)
    ci = np.array([corners[i] for i in idx])
    for i in range(N - 1):
        X[i + 1, :] = (X[i, :] + ci[i + 1]) / 2
        C[i + 1, :] = (C[i, :] + colors[idx[i + 1]]) / 2
    return X[5:, :], C[5:, :]


def plot_points(N=10006):
    """
    Generate a sequence of N points using alternative_sequence(N+6)
    and plot them in different colors in accordance with the colors
    used when generating.

    Parameters
    ----------
    N:      int, default 10006, number of points to be plotted -6
    """

    seq, colors = alternative_sequence(N)
    red = seq[colors == 0]
    green = seq[colors == 1]
    blue = seq[colors == 2]
    fig, ax = plt.subplots()
    for clr in ["red", "green", "blue"]:
        plt.scatter(eval(clr)[:, 0], eval(clr)[:, 1], s=0.1, marker=".", color=clr)
    ax.axis("equal")
    ax.axis("off")
    plt.show()


def plot_points_fancy_colors(N=10006):
    """
    Generate a sequence of N points and corresponding RGB coloring using
    fancy_color_sequence(N+6) and plot them.

    Parameters
    ----------
    N:      int, default 10006, number of points to be plotted -6
    """
    X, C = fancy_color_sequence(N)
    fig, ax = plt.subplots()
    ax.axis("equal")
    ax.axis("off")
    plt.scatter(*zip(*X), c=C, s=0.2)
    plt.show()


if __name__ == "__main__":
    plot_points()
    plot_points_fancy_colors()
