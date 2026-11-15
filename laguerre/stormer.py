"""
Smooth numbers and Stormer numbers.

A number is "y-smooth" if all its prime factors are <= y.
We call m a "Stormer number for y" if both m and m - 1 are y-smooth, that is P(m(m-1)) <= y.
Lehmer's Table IA (1964) lists all of them for y <= 41.

WHAT THIS FILE PROVES AND WHAT IT DOES NOT. We simply enumerate all y-smooth numbers up to
a limit and look for consecutive ones. That finds every Stormer number UP TO THE LIMIT.
It says nothing about numbers beyond the limit. The fact that there are none beyond
n_2 = 1,611,308,700 (for y = 31) is IMPORTED from Lehmer, who proved it with Pell equations.
"""

import os

from laguerre.arithmetic import primes_up_to


def smooth_numbers_up_to(limit, largest_prime):
    """
    Return the set of all integers 1 <= m <= limit whose prime factors are all
    <= largest_prime.

    Method: start from {1} and, for each prime in turn, multiply every number found so far
    by every power of that prime that stays within the limit.
    """
    numbers = [1]
    for prime in primes_up_to(largest_prime):
        new_numbers = []
        for number in numbers:
            multiple = number
            while multiple <= limit:
                new_numbers.append(multiple)
                multiple *= prime
        numbers = new_numbers
    return set(numbers)


def ends_of_smooth_blocks(smooth_set, k):
    """
    Return the sorted list of all n >= k such that the k consecutive integers
    n-k+1, ..., n-1, n are all in `smooth_set`.

    In the notation of the paper these are the n with P(Delta(n-k+1, k)) <= y.
    For k = 2 these are exactly the Stormer numbers m = n with P(m(m-1)) <= y.
    """
    ends = []
    for n in sorted(smooth_set):
        if n < k:
            continue
        whole_block_is_smooth = True
        for i in range(1, k):
            if (n - i) not in smooth_set:
                whole_block_is_smooth = False
                break
        if whole_block_is_smooth:
            ends.append(n)
    return ends


def read_lehmer_table(path):
    """
    Read a hand-typed copy of Lehmer's Table IA and return the sorted list of its numbers.

    File format: integers separated by spaces, commas or new lines. Everything after a '#'
    on a line is a comment. Returns an empty list if the file does not exist or has no numbers.

    CONVENTION: the file must contain the values m with P(m(m-1)) <= 31, that is the LARGER
    number of each consecutive smooth pair (the largest entry is 1611308700).
    """
    if not os.path.exists(path):
        return []
    numbers = []
    with open(path) as table_file:
        for line in table_file:
            line = line.split("#")[0]
            for word in line.replace(",", " ").split():
                numbers.append(int(word))
    return sorted(numbers)
