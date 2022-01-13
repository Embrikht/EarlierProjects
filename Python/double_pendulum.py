import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.81


def delta(theta1, theta2):
    return theta2 - theta1


def domega1_dt(M1, M2, L1, L2, theta1, theta2, omega1, omega2):
    d = delta(theta1, theta2)
    num = (
        M2 * L1 * omega1 ** 2 * np.sin(d) * np.cos(d)
        + M2 * g * np.sin(theta2) * np.cos(d)
        + M2 * L2 * omega2 ** 2 * np.sin(d)
        - (M1 + M2) * g * np.sin(theta1)
    )
    den = (M1 + M2) * L2 - M2 * L1 * (np.cos(d)) ** 2
    return num / den


def domega2_dt(M1, M2, L1, L2, theta1, theta2, omega1, omega2):
    d = delta(theta1, theta2)
    num = (
        -M2 * L2 * omega2 ** 2 * np.sin(d) * np.cos(d)
        + (M1 + M2) * g * np.sin(theta1) * np.cos(d)
        - (M1 + M2) * L2 * omega1 ** 2 * np.sin(d)
        - (M1 + M2) * g * np.sin(theta2)
    )
    den = (M1 + M2) * L2 - M2 * L2 * (np.cos(d)) ** 2
    return num / den


class DoublePendulum:
    def __init__(self, M1=1, L1=1, M2=1, L2=1):
        self.M1 = M1
        self.L1 = L1
        self.M2 = M2
        self.L2 = L2

    def __call__(self, t, y):
        """
        Returns right-hand side of equation using functions
        domega1_dt and domega2_dt

        Parameters:
        -----------
        t:  float, arraylike
            value of t to be evaluated
        y:  float, arraylike
            value of y to be evaluated
            in order theta1, omega1, theta2, omega2

        Returns:
        --------
        Tuple consisting of right-hand side of ODE
        in the same order as y was given
        """

        return (
            y[1],
            domega1_dt(self.M1, self.M2, self.L1, self.L2, y[0], y[2], y[1], y[3]),
            y[3],
            domega2_dt(self.M1, self.M2, self.L1, self.L2, y[0], y[2], y[1], y[3]),
        )

    def solve(self, y0, T, dt, angles="rad"):
        if angles == "deg":
            y0[0] = (y0[0] * 180) / np.pi
        elif angles != "deg" and angles != "rad":
            raise ValueError("Angles must be either rad or deg")

        if not len(y0) == 4:
            raise IndexError("Initial condition y0 must be of length 4!")

        t = np.linspace(0, T, int(T / dt + 1))
        self._t, self._theta1, self._omega1, self._theta2, self._omega2 = (
            integrate.solve_ivp(self, [0, T], y0, method="Radau", t_eval=t).t,
            integrate.solve_ivp(self, [0, T], y0, method="Radau", t_eval=t).y[0],
            integrate.solve_ivp(self, [0, T], y0, method="Radau", t_eval=t).y[1],
            integrate.solve_ivp(self, [0, T], y0, method="Radau", t_eval=t).y[2],
            integrate.solve_ivp(self, [0, T], y0, method="Radau", t_eval=t).y[3],
        )

    @property
    def theta1(self):
        return self._theta1

    @property
    def theta2(self):
        return self._theta2

    @property
    def t(self):
        return self._t

    @property
    def x1(self):
        return self.L1 * np.sin(self.theta1)

    @property
    def y1(self):
        return -self.L1 * np.cos(self.theta1)

    @property
    def x2(self):
        return self.x1 + self.L2 * np.sin(self.theta2)

    @property
    def y2(self):
        return self.y1 - self.L2 * np.cos(self.theta2)

    @property
    def potential(self):
        P1 = self.M1 * g * (self.y1 + self.L1)
        P2 = self.M2 * g * (self.y2 + self.L1 + self.L2)
        return P1 + P2

    @property
    def vx1(self):
        return np.gradient(self.x1, self.t)

    @property
    def vy1(self):
        return np.gradient(self.y1, self.t)

    @property
    def vx2(self):
        return np.gradient(self.x2, self.t)

    @property
    def vy2(self):
        return np.gradient(self.y2, self.t)

    @property
    def kinetic(self):
        K1 = 0.5 * self.M1 * (self.vx1 ** 2 + self.vy1 ** 2)
        K2 = 0.5 * self.M2 * (self.vx2 ** 2 + self.vy2 ** 2)
        return K1 + K2

    def create_animation(self):
        fig = plt.figure()

        plt.axis("equal")
        plt.axis("off")
        plt.axis((-3, 3, -3, 3))

        (self.pendulums,) = plt.plot([], [], "o-", lw=2)

        self.animation = animation.FuncAnimation(
            fig,
            self._next_frame,
            interval=100,
            frames=600,
            repeat=None,
            blit=True,
        )

    def _next_frame(self, i):
        self.pendulums.set_data(
            (0, self.x1[i], self.x2[i]), (0, self.y1[i], self.y2[i])
        )
        return (self.pendulums,)

    def show_animation(self):
        self.create_animation()
        plt.show()

    def save_animation(self, filename):
        self.create_animation()
        self.animation.save(filename + ".mp4", fps=60)


if __name__ == "__main__":
    p_double = DoublePendulum(M1=2.5, L1=1, M2=0.4, L2=1)
    p_double.solve([np.pi / 2, 0, np.pi / 4, 0], 10, 0.01)
    potential_energy = p_double.potential
    kinetic_energy = p_double.kinetic
    total_energy = potential_energy + kinetic_energy
    plt.plot(p_double.t, kinetic_energy, label="Kinetic energy")
    plt.plot(p_double.t, potential_energy, label="Potential energy")
    plt.plot(p_double.t, total_energy, label="Total energy")
    plt.title(
        "The potential, kinetic and total energy of the double pendulum over time"
    )
    plt.legend()
    plt.ylabel("Energy [J]")
    plt.xlabel("Time [s]")
    plt.show()

    p_double.save_animation("pendulum_motion")
    plt.show()

    for i, col in zip([0, 1, 2], ["red", "blue", "green"]):
        q_double = DoublePendulum()
        q_double.solve([1.7 + 0.1 * i, 0, np.pi / 4, 0], 10, 0.01)
        plt.plot(
            q_double.x2[500:],
            q_double.y2[500:],
            color=col,
            label=f"\u03b8 _1 = {1.7+0.1*i}",
        )

    plt.title("Trajectories of pendulum 2 for different values of theta1")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig("chaotic_pendulum.png")
    plt.show()
