import pytest
import numpy as np
from chaos_game import ChaosGame


@pytest.mark.parametrize("n, r", [(2, 0.5), (3, 1.5), (5, -0.3)])
def test_init_raises_ValueError(n, r):
    with pytest.raises(ValueError):
        ChaosGame(n, r)


def test_savepng_raises_ValueError():
    with pytest.raises(ValueError):
        a = ChaosGame(3, 0.5)
        a.savepng("dumt_filnavn.pdf")


def test_generate_n_gon():
    a = ChaosGame(3)
    triangle = np.array(
        [
            (0, 1),
            (np.sin(2 * np.pi / 3), np.cos(2 * np.pi / 3)),
            (np.sin(4 * np.pi / 3), np.cos(4 * np.pi / 3)),
        ]
    )
    assert np.all(np.isclose(a.list, triangle))
