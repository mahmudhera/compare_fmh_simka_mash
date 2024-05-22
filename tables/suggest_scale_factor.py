"""
Suggest a scale factor given
- num of elements in sets
- desired error
- desired confidence
"""

import math
from scipy.stats import norm


def get_min_scale_factor(n1, n2, error, confidence, c=0.5):
    epsilon = error / (1+c)
    q = 6.0 / (1.0 - confidence)
    log_q = math.log(q)
    min_scale_factor = 3.0 * log_q / ( min(n1, n2) * epsilon**2 )
    return min(min_scale_factor, 1.0)

if __name__ == '__main__':
    n1 = 4800000
    n2 = 4800000
    error = 0.1
    confidence = 0.9
    print(get_min_scale_factor(n1, n2, error, confidence))

