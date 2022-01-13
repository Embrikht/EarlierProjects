from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from operator import add


class Pendulum:
    def __init__(self, L=1, M=1, g=9.81):
        self.L = L
        self.M = M
        self.g = g
        self.solve_called = False

    def __call__(self, t, y):
        """
        Returns the right-hand side of ODE.

        Parameters:
        ----------
        t:  float, arraylike
            value(s) of t to be evaluated
        y:  float, arraylike
            value(s) of u to be evaluated
            in order theta, omega

        Returns:
        --------
        dtheta, domega:     floats
            right-hand side of ODE.
        """
        dtheta = y[1]
        domega = -(self.g / self.L) * np.sin(y[0])
        return dtheta, domega

    def solve(self, y0, T, dt, angles="rad"):
        """
        Uses scipy.integrate.solve_ivp to solve initial value problem.
        Stores solution internally in instance of class.

        Parameters:
        ---------
        y0:     float, arraylike
                initial conditions
                in order theta, omega
        T:      float
                end point of integration
        dt:     float
                time discretization
        angles: "rad" or "deg"
                default to rad
                if set to "deg", converts to radians

        """

        self.solve_called = True
        if angles == "deg":
            y0[0] = (y0[0] * 180) / np.pi
        elif angles != "deg" and angles != "rad":
            raise ValueError("Angles must be either rad or deg")

        t = np.linspace(0, T, int(T / dt + 1))
        self._t, self._theta, self._omega = (
            integrate.solve_ivp(self, [0, T], y0, t_eval=t).t,
            integrate.solve_ivp(self, [0, T], y0, t_eval=t).y[0],
            integrate.solve_ivp(self, [0, T], y0, t_eval=t).y[1],
        )

    @property
    def t(self):
        if self.solve_called == False:
            raise NameError(
                "Solve method must be called before calling properties t, theta, omega"
            )
        return self._t

    @property
    def theta(self):
        if self.solve_called == False:
            raise NameError(
                "Solve method must be called before calling properties t, theta, omega"
            )
        return self._theta

    @property
    def omega(self):
        if self.solve_called == False:
            raise NameError(
                "Solve method must be called before calling properties t, theta, omega"
            )
        return self._omega

    @property
    def x(self):
        return self.L * np.sin(self.theta)

    @property
    def y(self):
        return -self.L * np.cos(self.theta)

    @property
    def potential(self):
        return self.M * self.g * (self.y + self.L)

    @property
    def vx(self):
        return np.gradient(self.x, self.t)

    @property
    def vy(self):
        return np.gradient(self.y, self.t)

    @property
    def kinetic(self):
        return 0.5 * self.M * (self.vx ** 2 + self.vy ** 2)


class DampenedPendulum(Pendulum):
    def __init__(self, B, L=1, M=1, g=9.81):
        super().__init__(L=1, M=1, g=9.81)
        self.solve_called = False
        self.B = B

    def __call__(self, t, y):
        dtheta = y[1]
        domega = -(self.g / self.L) * np.sin(y[0]) - (self.B / self.M) * y[1]
        return dtheta, domega


if __name__ == "__main__":

    p = Pendulum(L=5, M=4)
    p.solve([np.pi / 3, 0], 20, 0.01)
    plt.plot(p.t, p.theta)
    plt.title("Motion of pendulum over time")
    plt.xlabel("Time [s]")
    plt.ylabel("\u03b8 [radians]")
    plt.show()

    potential_energy = p.potential
    kinetic_energy = p.kinetic
    total_energy = list(map(add, potential_energy, kinetic_energy))
    plt.plot(p.t, kinetic_energy, label="Kinetic energy")
    plt.plot(p.t, potential_energy, label="Potential energy")
    plt.plot(p.t, total_energy, label="Total energy")
    plt.title("Kinetic, potential and total energy of the pendulum over time")
    plt.xlabel("Time [s]")
    plt.ylabel("Energi [J]")
    plt.legend()
    plt.show()

    dp = DampenedPendulum(0.8, L=5, M=4)
    dp.solve([np.pi / 3, 2], 20, 0.01)
    potential_energy = dp.potential
    kinetic_energy = dp.kinetic
    total_energy = list(map(add, potential_energy, kinetic_energy))
    plt.plot(dp.t, total_energy, label="Total energy")
    plt.title("Total energy of the dampened pendulum")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend()
    plt.show()
