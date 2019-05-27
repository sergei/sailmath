import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate


class Polars:
    def __init__(self, polars_file):
        with open(polars_file, 'r') as pf:
            x = []
            y = []
            z = []
            for l in pf:
                t = l.split()
                tws = float(t[0])
                for i in range(1, len(t) - 1, 2):
                    twa = float(t[i])
                    bs = float(t[i + 1])
                    x.append(twa)
                    y.append(tws)
                    z.append(bs)
            self.f = interpolate.interp2d(x, y, z)

    def get_boat_speed(self, twa, tws):
        return self.f(twa, tws)


if __name__ == '__main__':
    tws = 6
    twa = 30
    polars = Polars('polars-j105.txt')
    bs = polars.get_boat_speed(twa, tws)
    print bs

    twa = np.arange(0, 180, 1)
    bs = polars.f(twa,bs)
    print bs
    # ax = plt.subplot(111, projection='polar')
    plt.plot(twa, bs)
    plt.show()