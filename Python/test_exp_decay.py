from exp_decay import ExponentialDecay


def test_ExponenitalDecay_call():
    P = ExponentialDecay(0.4)
    assert abs(P(0, 3.2) + 1.28) < 1e-12
