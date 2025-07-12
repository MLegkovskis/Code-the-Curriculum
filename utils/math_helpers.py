import math
from fractions import Fraction


def get_gcd(a, b):
    """Return the greatest common divisor of a and b."""
    return math.gcd(int(a), int(b))


def get_lcm(a, b):
    """Return the lowest common multiple of a and b."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // get_gcd(a, b)


def get_lcm_for_list(numbers):
    """Return LCM for a list of integers."""
    if not numbers:
        return 1
    lcm = numbers[0]
    for n in numbers[1:]:
        lcm = get_lcm(lcm, n)
    return lcm


def get_simplification_steps(n, d):
    """Return a list of steps to simplify n/d."""
    if d == 0:
        return ["Denominator cannot be zero"]

    n = int(n)
    d = int(d)
    steps = [f"{n}/{d}"]

    gcd = get_gcd(n, d)
    p = 2
    while gcd > 1:
        if gcd % p == 0:
            n //= p
            d //= p
            steps.append(f" \u2192 \u00F7{p} \u2192 {n}/{d}")
            gcd //= p
        elif p * p > gcd:
            if gcd > 1:
                p = gcd
        elif p == 2:
            p = 3
        else:
            p += 2
    if len(steps) == 1:
        steps.append(" (already in simplest form)")
    return steps


def get_multiplication_steps(f1: Fraction, f2: Fraction):
    result = f1 * f2
    return [f"{f1} × {f2} = {result}"]


def get_division_steps(f1: Fraction, f2: Fraction):
    result = f1 / f2
    return [f"{f1} ÷ {f2} = {result}"]


def get_add_subtract_steps(f1: Fraction, f2: Fraction, op: str):
    if op == '+':
        result = f1 + f2
        return [f"{f1} + {f2} = {result}"]
    else:
        result = f1 - f2
        return [f"{f1} - {f2} = {result}"]
