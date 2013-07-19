from math import sqrt


def problem1():
    print(sum([x for x in range(1000) if x % 3 == 0 or x % 5 == 0]))

def problem2():
    N = 4000000

    def fib():
        a, b = 0, 1
        while 1:
            yield a
            a, b = b, a + b

    gen = fib()
    sum = 0
    elem = next(gen)
    while elem < N:
        if elem % 2 == 0:
            sum += elem
        elem = next(gen)
    print(sum)


def problem3():
    N = 600851475143

    def factors(x):
        """
        http://en.wikipedia.org/wiki/Primality_test
        """
        if x % 2 == 0: yield 2
        if x % 3 == 0: yield 3
        k = 1
        sqrtx = sqrt(x)
        while True:
            factor1 = 6 * k + 1
            factor2 = 6 * k - 1
            if x % factor1 == 0:
                yield factor1
            if x % factor2 == 0:
                yield factor2
            if factor2 > sqrtx or factor1 > sqrtx:
                break
            k += 1

    gen_factors = factors(N)
    known_factors = list(gen_factors)
    # there is a chance we missed last maximum divisor
    last_factor = int(N / known_factors[-1])
    if last_factor > known_factors[-1]:
        known_factors.append(last_factor)

    known_factors.reverse() # start with maximum factor
    for factor in known_factors:
        l = list(factors(factor))
        if not l: #empty list means factor is prime
            print('largest prime factor is {}'.format(factor))
            break


def problem4():
    M = 900
    N = 1000

    palyndroms = []
    for i in reversed(range(M, N)):
        for j in reversed(range(i, N)):
            s = str(i * j)
            if s == s[::-1]:
                palyndroms.append(s)
    print(palyndroms)
    print(max(palyndroms))


def problem5():
    """
    we got a hint that tells us that [1,2,3,4,5,6,7,8,9,10] all
    divide 2520 with no remainder. 2520 is also divisible by [12,14,15,18,20] with no remainder.
    16 is left. But, 2520 * 2 = 5040 is divisible by 16 with no reminder.
    That means, [1,2,3,4,5,6,7,8,9,10,12,14,15,16,17,18,20] have smallest number 5040 evenly divisible
    by all of them. Only prime divisors are left [11,13,17,19]. Least common multiple for these prime
    numbers is 11 * 13 * 17 * 19.
    So, the smallest number divisible by all of range(1,21) is 11 * 13 * 17 * 19 * 5040 = 232792560
    """

    # BUT THAT DOES NOT SOLVE THE COMMON PROBLEM
    # find the smallest number N divisible by all range(2, K).
    # see http://en.wikipedia.org/wiki/Prime_factor
    print(232792560)


def problem6():
    # okay, I know from Knuth that sum of all squares for N is n*(n+1)(2n+1)/6
    # okay, I know that linear sum of all range(1, N) is N*(1+N)/2
    N = 100

    def all_squares(x):
        return x * (x + 1) * (2 * x + 1) / 6

    def just_sum(x):
        return x * (1 + x) / 2

    sm = int(just_sum(N))
    squares = int(all_squares(N))
    print('Answer is {}'.format(sm * sm - squares))


def problem7():
    def sieve():
        """
        Yields the sequence of prime numbers via the Sieve of Eratosthenes.
        http://stackoverflow.com/questions/1628949/to-find-first-n-prime-numbers-in-python
        """
        D = {}  # map composite integers to primes witnessing their compositeness
        q = 2   # first integer to test for primality
        while True:
            if q not in D:
                yield q        # not marked composite, must be prime
                D[q * q] = [q]   # first multiple of q not already marked
            else:
                for p in D[q]: # move each witness to its next multiple
                    D.setdefault(p + q, []).append(p)
                del D[q]       # no longer need D[q], free memory
            q += 1

    gen = sieve()
    N = 10001
    prime = 0
    for i in range(1, N+1):
        prime = next(gen)
    print(prime)


def problem8():
    """
    More elegant solution
    s = '731...450'
    d = map(int, list(s))
    print max([reduce(lambda x, y: x*y, d[i:i+5]) for i in xrange(len(s)-4)])
    """
    string = "73167176531330624919225119674426574742355349194934" + \
        "96983520312774506326239578318016984801869478851843" + \
        "85861560789112949495459501737958331952853208805511" + \
        "12540698747158523863050715693290963295227443043557" + \
        "66896648950445244523161731856403098711121722383113" + \
        "62229893423380308135336276614282806444486645238749" + \
        "30358907296290491560440772390713810515859307960866" + \
        "70172427121883998797908792274921901699720888093776" + \
        "65727333001053367881220235421809751254540594752243" + \
        "52584907711670556013604839586446706324415722155397" + \
        "53697817977846174064955149290862569321978468622482" + \
        "83972241375657056057490261407972968652414535100474" + \
        "82166370484403199890008895243450658541227588666881" + \
        "16427171479924442928230863465674813919123162824586" + \
        "17866458359124566529476545682848912883142607690042" + \
        "24219022671055626321111109370544217506941658960408" + \
        "07198403850962455444362981230987879927244284909188" + \
        "84580156166097919133875499200524063689912560717606" + \
        "05886116467109405077541002256983155200055935729725" + \
        "71636269561882670428252483600823257530420752963450"

    length = len(string)
    window = 5
    windows = {}
    odds = range(0,7) # we don't need smaller digits
    for i in range(0, length - window + 1):
        cur_window = string[i:i + window]
        windows[cur_window] = 1
        for j in range(0, window):
            int1 = int(string[i + j:i + j + 1])
            if int1 in odds:
                del windows[cur_window]
                break
            windows[cur_window] *= int1

    print(max(windows.values()))


problem8()

