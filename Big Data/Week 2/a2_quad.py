#!/usr/bin/env python3
import cmath

def solve_quadratic_equation(a, b, c):
    # Find the discriminant
    delta = (b**2) - 4*(a*c)

    # If the discriminant is positive, there are two distinct real roots
    if delta > 0:
        x1 = (-b - delta**0.5) / (2*a)
        x2 = (-b + delta**0.5) / (2*a)
        return x1, x2

    # If the discriminant is zero, there is exactly one real root
    if delta == 0:
        x = (-b - delta**0.5) / (2*a)
        return x

    # If the discriminant is negative, there are two complex roots
    if delta < 0:
        x1 = (-b - cmath.sqrt(delta)) / (2 * a)
        x2 = (-b + cmath.sqrt(delta)) / (2 * a)
        return x1, x2
