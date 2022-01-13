import pytest
from double_pendulum import delta, domega1_dt, domega2_dt, DoublePendulum

M1 = 1
M2 = 1
L1 = 1
L2 = 1
omega1 = 0.15
omega2 = 0.15


@pytest.mark.parametrize(
    "theta1, theta2, expected",
    [
        (0, 0, 0),
        (0, 0.5235987755982988, 0.5235987755982988),
        (0.5235987755982988, 0, -0.5235987755982988),
        (0.5235987755982988, 0.5235987755982988, 0.0),
    ],
)
def test_delta(theta1, theta2, expected):
    assert abs(delta(theta1, theta2) - expected) < 1e-10


@pytest.mark.parametrize(
    "theta1, theta2, expected",
    [
        (0, 0, 0.0),
        (0, 0.5235987755982988, 3.4150779130841977),
        (0.5235987755982988, 0, -7.864794228634059),
        (0.5235987755982988, 0.5235987755982988, -4.904999999999999),
    ],
)
def test_domega1_dt(theta1, theta2, expected):
    assert (
        abs(domega1_dt(M1, M2, L1, L2, theta1, theta2, omega1, omega2) - expected)
        < 1e-10
    )


@pytest.mark.parametrize(
    "theta1, theta2, expected",
    [
        (0, 0, 0.0),
        (0, 0.5235987755982988, -7.8737942286340585),
        (0.5235987755982988, 0, 6.822361597534335),
        (0.5235987755982988, 0.5235987755982988, 0.0),
    ],
)
def test_domega2_dt(theta1, theta2, expected):
    assert (
        abs(domega2_dt(M1, M2, L1, L2, theta1, theta2, omega1, omega2) - expected)
        < 1e-10
    )


def test_initials_are_zero():
    d = DoublePendulum()
    d.solve([0, 0, 0, 0], 10, 1)
    assert all(d.theta1) == 0
    assert all(d.theta2) == 0


def test_solve_raises_IndexError():
    d = DoublePendulum()
    with pytest.raises(IndexError):
        d.solve([1], 10, 1)


def test_DoublePendulum_call():
    d = DoublePendulum()
    assert d(0, [0, 0.1, 0, 0.2])[0] == 0.1
    assert d(0, [0, 0.1, 0, 0.2])[2] == 0.2
