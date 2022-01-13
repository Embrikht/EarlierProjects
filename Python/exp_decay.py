from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt


class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        return -self.a * u

    def solve(self, u0, T, dt):
        t = np.linspace(0, T, int(T / dt + 1))
        t, u = (
            integrate.solve_ivp(self, [0, T], [u0], t_eval=t).t,
            integrate.solve_ivp(self, [0, T], [u0], t_eval=t).y[0],
        )
        return t, u


if __name__ == "__main__":
    for a in [0.1, 0.4, 0.8]:
        decay_model = ExponentialDecay(a)
        t, u = decay_model.solve(5, 10, 0.1)
        plt.plot(t, u, label=f"a = {a}")
    plt.xlabel("t")
    plt.ylabel("u")
    plt.title("Exponential decay models for different values of a")
    plt.legend()
    plt.show()
