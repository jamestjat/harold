from harold import State, Transfer, bode_plot, nyquist_plot
from numpy import eye
from numpy.random import rand, seed


def test_bode_plot_shape():
    seed(1234)
    # SISO
    f = bode_plot(Transfer(5, dt=0.5))
    # For SISO, expect 2 axes (magnitude and phase)
    assert len(f.axes) == 2
    # MIMO
    a, b, c = -3*eye(5) + rand(5, 5), rand(5, 3), rand(4, 5)
    G = State(a, b, c)
    f = bode_plot(G)
    # For MIMO (p x m), expect p*2 magnitude plots + p*2 phase plots = p*2*m total axes
    assert len(f.axes) == G.shape[0] * 2 * G.shape[1]


def test_nyquist_plot_shape():
    seed(1234)
    # SISO
    H = Transfer(5, dt=0.5)
    f = nyquist_plot(H)
    # For SISO, expect 1 axis
    assert len(f.axes) == 1
    # MIMO
    a, b, c = -3*eye(5) + rand(5, 5), rand(5, 3), rand(4, 5)
    G = State(a, b, c)
    f = nyquist_plot(G)
    # For MIMO (p x m), expect p*m axes (one per transfer function)
    assert len(f.axes) == G.shape[0] * G.shape[1]
