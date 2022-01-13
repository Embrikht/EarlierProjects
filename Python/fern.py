import numpy as np
import matplotlib.pyplot as plt

class AffineTransform:
    """
    An iterated function system, generating a sequence of points by iterating
    them through affine functions.
    """

    def __init__(self, a=0, b=0, c=0, d=0, e=0, f=0):
        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f

    def __call__(self, x, y):
        a, b, c, d, e, f = self.a, self.b, self.c, self.d, self.e, self.f
        return [a*x + b*y + e, c*x + d*y + f]

    def functions(self):
        f1 = AffineTransform(d=0.16)
        f2 = AffineTransform(a=0.85, b=0.04, c=-0.04, d=0.85, f=1.6)
        f3 = AffineTransform(a=0.2, b=-0.26, c=0.23, d=0.22, f=1.6)
        f4 = AffineTransform(a=-0.15, b=0.28, c=0.26, d=0.24, f=0.44)
        func = [f1, f2, f3, f4]
        return func

    def weighted_choice(self):
        """
        A non-uniform draw, using some functions more frequently than others.

        Returns
        -------
        func[j]:    The drawn function based on the list of probabilities.
        """
        prob = [0.01, 0.85, 0.07, 0.07]
        func = self.functions()
        p_cumulative = np.cumsum(prob)
        r = np.random.random()
        for j, p in enumerate(p_cumulative):
            if r < p:
                return func[j]

    def iterating(self):
        X = np.zeros((50000,2))
        for i in range(49999):
            choice = self.weighted_choice()
            X[i+1, 0] = choice(X[i, 0], X[i, 1])[0]
            X[i+1, 1] = choice(X[i, 0], X[i, 1])[1]
        return X

    def plot(self):
        list = self.iterating()
        fig, ax = plt.subplots()
        ax.scatter(*zip(*list), color="forestgreen", s=0.2)
        ax.axis("equal")
        ax.axis("off")
        fig.savefig("figures/barnsley_fern.png", dpi=300)


if __name__ == "__main__":
    a = AffineTransform()
    a.plot()
