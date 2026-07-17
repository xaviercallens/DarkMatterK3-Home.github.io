import math
import numpy as np

def s10(n):
    return sum(math.comb(n, k)**4 for k in range(n+1))

# We want to find A, B, C such that:
# (n+1)^3 u_{n+1} = (A*n^2 + A*n + B)(2n+1) u_n - C n^3 u_{n-1}
# or similar.
# Actually, the recurrence for s_10 is known. Let's just solve a linear system for the coefficients.
# Let recurrence be: (n+1)^3 u_{n+1} - (a n^2 + a n + b)(2n+1) u_n + c n^3 u_{n-1} = 0
# Let's find a, b, c.

u = [s10(n) for n in range(5)]

# For n=1:
# 2^3 u_2 - 3*(2a + b)*u_1 + c*1^3*u_0 = 0
# 8 u_2 - 6a u_1 - 3b u_1 + c u_0 = 0

# For n=2:
# 3^3 u_3 - 5*(6a + b)*u_2 + c*2^3*u_1 = 0
# 27 u_3 - 30a u_2 - 5b u_2 + 8c u_1 = 0

# For n=3:
# 4^3 u_4 - 7*(12a + b)*u_3 + c*3^3*u_2 = 0
# 64 u_4 - 84a u_3 - 7b u_3 + 27c u_2 = 0

# Let's set up the system:
A_matrix = [
    [-6*u[1], -3*u[1], u[0]],
    [-30*u[2], -5*u[2], 8*u[1]],
    [-84*u[3], -7*u[3], 27*u[2]]
]
B_matrix = [
    -8*u[2],
    -27*u[3],
    -64*u[4]
]

res = np.linalg.solve(A_matrix, B_matrix)
print("a, b, c for s_10:")
print(np.round(res, 4))
