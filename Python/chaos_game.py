import numpy as np
import matplotlib.pyplot as plt


class ChaosGame:
    """
    Class for simulating the chaos game. Generate n-gon and sequence of points
    within the n-gon, using stochastic simulations.
    """

    def __init__(self, n, r=1 / 2):
        """
        Constructor that ensure the parameters have legal value and calls
        _generate_ngon.

        Parameters
        ----------
        n:      int, number of points
        r:      float, ratio between two points

        Stores
        -------
        n:      int
        r:      float
        list:   generated by _generate_ngon
        """
        try:
            self.n = int(n)
            self.r = float(r)
            if n < 3 or r < 0 or r > 1:
                raise ValueError(
                    "Inacceptable value of n or r! Remember n > 2 and 0 < r < 1!"
                )
            self.list = self._generate_ngon()
        except:
            raise ValueError("n must be int and r must be float!")

    def _generate_ngon(self):
        """
        Generate a n-gon. Takes no parameters and return the corners in the
        n-gon, stored in a list.
        """

        n = self.n
        ci = np.zeros((n, 2))
        theta_i = np.linspace(0, 2 * np.pi, n + 1)
        ci[:, 0] = np.sin(theta_i)[:-1]
        ci[:, 1] = np.cos(theta_i)[:-1]
        return ci

    def plot_ngon(self):
        n = self.n
        list = self.list
        fig, ax = plt.subplots()
        ax.axis("equal")
        ax.axis("off")
        plt.scatter(*zip(*list), s=3)

    def _starting_point(self):
        """
        Select a random starting point.
        """

        n = self.n
        list = self.list
        w = np.random.random(size=n)
        X = np.zeros((1, 2))
        w = w / w.sum()
        X = sum(wi * ci for wi, ci in zip(w, list))
        return X

    def iterate(self, steps, discard=5):
        """
        Generate a list containing points within the n-gon.

        Parameters
        ----------
        steps:      Number of points
        discard:    Discarding the first x points. Default is 5

        Stores
        -------
        points:     List containing the points
        idx:        List of indices selected in each iteration
        """

        n = self.n
        r = self.r
        corners = self._generate_ngon()
        X = np.zeros((steps, 2))
        X[0, :] = self._starting_point()
        idx = np.random.randint(0, n, size=steps)
        ci = np.array([corners[i] for i in idx])
        for i in range(steps - 1):
            X[i + 1, :] = r * X[i, :] + (1 - r) * ci[i + 1]
        self.points, self.idx = X[discard:, :], idx[discard:]

    def plot(self, color=False, cmap="jet"):
        if color:
            colors = self.gradient_color[:, 0]
        else:
            colors = "black"

        fig, ax = plt.subplots()
        ax.axis("equal")
        ax.axis("off")
        ax.scatter(*zip(*self.points), s=0.2, c=colors, cmap=cmap)

    def show(self, color=False, cmap="jet"):
        self.plot(color, cmap)
        plt.show()

    @property
    def gradient_color(self):
        """
        Returns the numpy array C which contains numbers corresponding to color.
        """

        n = self.points.shape[0]
        C = np.zeros((n, 2))
        C[0, :] = self.idx[0]
        for i in range(n - 1):
            C[i + 1, :] = 0.5 * (C[i, :] + self.idx[i + 1])
        return C

    def savepng(self, outfile, color=False, cmap="jet"):
        if outfile.split(".")[-1] == outfile:
            outfile += ".png"
            self.plot(color, cmap)
            plt.savefig(outfile, dpi=300, transparent=True)
        elif outfile.split(".")[-1] == "png":
            self.plot(color, cmap)
            plt.savefig(outfile, dpi=300, transparent=True)
        else:
            raise ValueError("outfile must be a .png.file!")


if __name__ == "__main__":
    rlist = [1/2, 1/3, 1/3, 3/8, 1/3]
    nlist = [3, 4, 5, 5, 6]
    N = 10005
    for i, (r, n) in enumerate(zip(rlist, nlist)):
        a = ChaosGame(n, r)
        a.iterate(N)
        a.savepng(f"figures/chaos{i+1}.png", color=True)
