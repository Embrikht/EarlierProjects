import numpy as np
import matplotlib.pyplot as plt
from chaos_game import ChaosGame


class Variations:
    """
    Class for doing transformations on 2D-vectors. Includes four such
    transformations:

    linear
    swirl
    handkerchief
    disc

    Constructor takes three parameters:
    x:      list, arraylike, x-values of vectors to be tranformed
    y:      list, arraylike, y-values of vectors to be tranformed
    name:   string, name of the transformation to be used
    """

    def __init__(self, x, y, name):
        self.x = np.array(x)
        self.y = np.array(y)
        self.name = name

    @staticmethod
    def linear(x, y):
        return x, y

    @staticmethod
    def swirl(x, y):
        r2 = x ** 2 + y ** 2
        return x * np.sin(r2) - y * np.cos(r2), x * np.cos(r2) + y * np.sin(r2)

    @staticmethod
    def handkerchief(x, y):
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return r * np.sin(theta + r), r * np.cos(theta - r)

    @staticmethod
    def disc(x, y):
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return (theta / np.pi) * np.sin(np.pi * r), (theta / np.pi) * np.cos(np.pi * r)

    def transform(self):
        """
        Returns the tranformed vectors.
        """
        _func = getattr(Variations, self.name)
        return _func(self.x, self.y)

    @classmethod
    def from_chaos_game(self, game, name):
        """
        Enables initialization using an instance of class ChaosGame
        """
        return Variations(game.points[:, 0], game.points[:, 1], name)


def plot_black(N=150):
    grid_values = np.linspace(-1, 1, N)
    x, y = np.meshgrid(grid_values, grid_values)
    x_values = x.flatten()
    y_values = y.flatten()

    transformations = ["linear", "handkerchief", "swirl", "disc"]
    variations = [
        Variations(x_values, y_values, version) for version in transformations
    ]

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax, variation in zip(axs.flatten(), variations):
        u, v = variation.transform()
        ax.scatter(u, -v, s=0.2, marker=".", color="black")
        ax.set_title(variation.name)
        ax.axis("equal")
        ax.axis("off")

    plt.savefig("figures/variation_4b.png")
    plt.show()


def plot_color(N=10000, n=4):
    transformations = ["linear", "handkerchief", "swirl", "disc"]
    game = ChaosGame(n)
    game.iterate(N)
    variations = [
        Variations.from_chaos_game(game, version) for version in transformations
    ]
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax, variation in zip(axs.flatten(), variations):
        u, v = variation.transform()
        ax.scatter(u, -v, s=1, marker=".", c=game.gradient_color[:, 0], cmap="jet")
        ax.set_title(variation.name)
        ax.axis("equal")
        ax.axis("off")

    plt.show()


def linear_combination_wrap(v1, v2):
    """
    Method to generate linear combination of transformations

    Parameters:
    ----------
    v1:     Instance of class Variations
    v2:     Instance of class Variations

    Returns:
    --------
    func:   callable function, function that given a weight w returns
            the linear combination of two tranformations
    """

    def func(w):
        u = w * v1.transform()[0] + (1 - w) * v2.transform()[0]
        v = w * v1.transform()[1] + (1 - w) * v2.transform()[1]
        return u, v

    return func


def plot_lincomb():
    ngon = ChaosGame(6)
    ngon.iterate(50000)
    coeffs = np.linspace(0, 1, 4)
    variation1 = Variations.from_chaos_game(ngon, "disc")
    variation2 = Variations.from_chaos_game(ngon, "swirl")
    variation12 = linear_combination_wrap(variation1, variation2)

    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for ax, w in zip(axs.flatten(), coeffs):
        u, v = variation12(w)
        ax.scatter(u, -v, s=0.2, marker=".", c=ngon.gradient_color[:, 0], cmap="jet")
        ax.set_title(f"weight = {w:.2f}")
        ax.axis("off")
        ax.axis("equal")
    plt.show()


if __name__ == "__main__":
    # plot_black()
    # plot_color()
    plot_lincomb()
