import pytest
from math import pi
import numpy as np
from pendulum import Pendulum


@pytest.mark.parametrize(
    "args, values",
    [[(2.7, (pi / 6, 0.15)), (0.15, -9.81 / 2.7 * 0.5)], [(2.7, (0, 0)), (0, 0)]],
)
def test_pendulum_call(args, values):
    p = Pendulum(L=args[0])
    dtheta_exp, domega_exp = values[0], values[1]
    dtheta_comp, domega_comp = p(0, args[1])
    tol = 1e-10
    assert abs(dtheta_exp - dtheta_comp) < tol
    assert abs(domega_exp - domega_comp) < tol


@pytest.mark.parametrize("p", ["q.t", "q.theta", "q.omega"])
def test_properties_raise_NameError(p):
    q = Pendulum()
    with pytest.raises(NameError):
        exec(p)


def test_initials_are_zero():
    p = Pendulum()
    p.solve([0, 0], 10, 1)
    assert all(p.theta) == 0
    assert all(p.omega) == 0
    assert all(p.t) == all(np.linspace(0, 10, 11))


def test_translating():
    p = Pendulum()
    p.solve((0.2, 0.3), 5, 0.1)
    tol = 1e-14
    assert abs(all(p.x ** 2 + p.y ** 2 - 1 <= tol))
