import numpy as np
from scipy.stats import norm

class BlackScholes:

    def __init__(self, s0, k, r, sigma, t):

        self.s0 = s0
        self.k = k
        self.r = r
        self.sigma = sigma
        self.t = t

    def call(self):

        d1 = (np.log(self.s0 / self.k) + ((self.r + (self.sigma**2 / 2))*self.t)) / (self.sigma * np.sqrt(self.t))
        d2 = d1 - (self.sigma * np.sqrt(self.t))

        return self.s0*norm.cdf(d1) - (self.k * np.exp(-self.r * self.t) * norm.cdf(d2))

    def put(self):

        d1 = (np.log(self.s0 / self.k) + ((self.r + (self.sigma**2 / 2))*self.t)) / (self.sigma * np.sqrt(self.t))
        d2 = d1 - (self.sigma * np.sqrt(self.t))

        return self.k * np.exp(-self.r * self.t) * norm.cdf(-d2) - (self.s0 * norm.cdf(-d1))
