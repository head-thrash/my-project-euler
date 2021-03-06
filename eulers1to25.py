from functools import reduce
from math import sqrt, floor, factorial
import string
from timeit import default_timer


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


def sieve2(limit):
    yield 2
    sievebound = int((limit - 1) / 2)
    sieve = [False for i in range(0, sievebound)]
    crosslimit = int((floor(sqrt(limit)) - 1) / 2)
    for i in range(1, crosslimit):
        if not sieve[i]:
            for j in range(2 * i * (i + 1), sievebound, 2 * i + 1):
                sieve[j] = True

    for i in range(1, sievebound):
        if not sieve[i]:
            yield 2 * i + 1


def prime_factors(value):
    crosslimit = int(floor(sqrt(value)) - 1) if value > 100 else value
    primes = sieve2(crosslimit)
    d = []
    prod = 1
    while True:
        if prod >= value:
            break
        y = value
        try:
            p = next(primes)
        except StopIteration:
            if prod < value:
                d.append(int(value / prod))
                break
        while y % p == 0:
            y /= p
            d.append(p)
            prod *= p
    return d


def factors(n):
    yield 1
    if n == 1:
        return
    r = floor(sqrt(n))
    if r * r == n:
        yield r
        r -= 1
    f, step = (3, 2) if n % 2 != 0 else (2, 1)
    while f <= r:
        if n % f == 0:
            yield f
            yield n // f
        f += step
    yield n


def problem1():
    print(sum([x for x in range(1000) if x % 3 == 0 or x % 5 == 0]))


def fib():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b


def problem2():
    N = 4000000

    gen = fib()
    summ = 0
    elem = next(gen)
    while elem < N:
        if elem % 2 == 0:
            summ += elem
        elem = next(gen)
    print(summ)


def problem3():
    N = 600851475143

    def factors(x):
        """
        http://en.wikipedia.org/wiki/Primality_test
        """
        if x % 2 == 0:
            yield 2
        if x % 3 == 0:
            yield 3
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

    known_factors.reverse()     # start with maximum factor
    for factor in known_factors:
        l = list(factors(factor))
        if not l:   # empty list means factor is prime
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
    gen = sieve()
    N = 10001
    prime = 0
    for i in range(1, N + 1):
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
    odds = range(0, 7)  # we don't need smaller digits
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


def problem9():
    N = 1000
    n = 200
    for b in range(n, N):
        for a in range(n, b):
            c = N - b - a
            if c <= b or c <= 0:
                break
            diff = c * c - b * b - a * a
            if diff is 0:
                print("abc = {}".format(a * b * c))
                return


def problem10():
    gen = sieve()
    N = 2000000
    summ = 0
    while True:
        prime = next(gen)
        if prime < N:
            summ += prime
        else:
            break
    print(summ)


def problem11():
    strings = [
        "08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08",
        "49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00",
        "81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65",
        "52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91",
        "22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80",
        "24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50",
        "32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70",
        "67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21",
        "24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72",
        "21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95",
        "78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92",
        "16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57",
        "86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58",
        "19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40",
        "04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66",
        "88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69",
        "04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36",
        "20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16",
        "20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54",
        "01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"]

    mtx = [[int(x) for x in y.split()] for y in strings]
    v_mirrored = [[int(col) for col in list(reversed(rows))] for rows in mtx]
    W = 4

    def max_in_series(r):
        return max([reduce(lambda x, y: x * y, r[i:i + W]) for i in range(len(r) - W + 1)])

    def diag_cuts(_):
        return [[_[row - col][col] for col in range(0, row + 1)] for row in range(W - 1, len(mtx))]

    def maxx(_):
        return max(map(max_in_series, _))

    print(max([
        #rows
        maxx(mtx),
        #cols
        maxx(list(zip(*mtx))),
        # okay, now diagonal cuts
        #diag upper triangle
        maxx(diag_cuts(mtx)),
        #diag lower triangle
        maxx(diag_cuts(list(reversed(mtx)))),
        # okay, now to other bias (we should vertically mirror matrix and apply same functions as above)
        maxx(diag_cuts(v_mirrored)),
        maxx(diag_cuts(list(reversed(v_mirrored))))]))


def problem12():
    def get_div_count(x):
        lim = int(floor(sqrt(x)) - 1)
        count = 0
        for i in range(2, lim):
            if x % i == 0:
                count += 1
        return count * 2

    x = 1
    while True:
        s = int(x * (x + 1) * 0.5)
        div_count = get_div_count(s)
        if div_count > 500:
            print('Found number with divisors = {}'.format(s))
            return
        x += 1


def problem13():
    X = [
        "37107287533902102798797998220837590246510135740250",
        "46376937677490009712648124896970078050417018260538",
        "74324986199524741059474233309513058123726617309629",
        "91942213363574161572522430563301811072406154908250",
        "23067588207539346171171980310421047513778063246676",
        "89261670696623633820136378418383684178734361726757",
        "28112879812849979408065481931592621691275889832738",
        "44274228917432520321923589422876796487670272189318",
        "47451445736001306439091167216856844588711603153276",
        "70386486105843025439939619828917593665686757934951",
        "62176457141856560629502157223196586755079324193331",
        "64906352462741904929101432445813822663347944758178",
        "92575867718337217661963751590579239728245598838407",
        "58203565325359399008402633568948830189458628227828",
        "80181199384826282014278194139940567587151170094390",
        "35398664372827112653829987240784473053190104293586",
        "86515506006295864861532075273371959191420517255829",
        "71693888707715466499115593487603532921714970056938",
        "54370070576826684624621495650076471787294438377604",
        "53282654108756828443191190634694037855217779295145",
        "36123272525000296071075082563815656710885258350721",
        "45876576172410976447339110607218265236877223636045",
        "17423706905851860660448207621209813287860733969412",
        "81142660418086830619328460811191061556940512689692",
        "51934325451728388641918047049293215058642563049483",
        "62467221648435076201727918039944693004732956340691",
        "15732444386908125794514089057706229429197107928209",
        "55037687525678773091862540744969844508330393682126",
        "18336384825330154686196124348767681297534375946515",
        "80386287592878490201521685554828717201219257766954",
        "78182833757993103614740356856449095527097864797581",
        "16726320100436897842553539920931837441497806860984",
        "48403098129077791799088218795327364475675590848030",
        "87086987551392711854517078544161852424320693150332",
        "59959406895756536782107074926966537676326235447210",
        "69793950679652694742597709739166693763042633987085",
        "41052684708299085211399427365734116182760315001271",
        "65378607361501080857009149939512557028198746004375",
        "35829035317434717326932123578154982629742552737307",
        "94953759765105305946966067683156574377167401875275",
        "88902802571733229619176668713819931811048770190271",
        "25267680276078003013678680992525463401061632866526",
        "36270218540497705585629946580636237993140746255962",
        "24074486908231174977792365466257246923322810917141",
        "91430288197103288597806669760892938638285025333403",
        "34413065578016127815921815005561868836468420090470",
        "23053081172816430487623791969842487255036638784583",
        "11487696932154902810424020138335124462181441773470",
        "63783299490636259666498587618221225225512486764533",
        "67720186971698544312419572409913959008952310058822",
        "95548255300263520781532296796249481641953868218774",
        "76085327132285723110424803456124867697064507995236",
        "37774242535411291684276865538926205024910326572967",
        "23701913275725675285653248258265463092207058596522",
        "29798860272258331913126375147341994889534765745501",
        "18495701454879288984856827726077713721403798879715",
        "38298203783031473527721580348144513491373226651381",
        "34829543829199918180278916522431027392251122869539",
        "40957953066405232632538044100059654939159879593635",
        "29746152185502371307642255121183693803580388584903",
        "41698116222072977186158236678424689157993532961922",
        "62467957194401269043877107275048102390895523597457",
        "23189706772547915061505504953922979530901129967519",
        "86188088225875314529584099251203829009407770775672",
        "11306739708304724483816533873502340845647058077308",
        "82959174767140363198008187129011875491310547126581",
        "97623331044818386269515456334926366572897563400500",
        "42846280183517070527831839425882145521227251250327",
        "55121603546981200581762165212827652751691296897789",
        "32238195734329339946437501907836945765883352399886",
        "75506164965184775180738168837861091527357929701337",
        "62177842752192623401942399639168044983993173312731",
        "32924185707147349566916674687634660915035914677504",
        "99518671430235219628894890102423325116913619626622",
        "73267460800591547471830798392868535206946944540724",
        "76841822524674417161514036427982273348055556214818",
        "97142617910342598647204516893989422179826088076852",
        "87783646182799346313767754307809363333018982642090",
        "10848802521674670883215120185883543223812876952786",
        "71329612474782464538636993009049310363619763878039",
        "62184073572399794223406235393808339651327408011116",
        "66627891981488087797941876876144230030984490851411",
        "60661826293682836764744779239180335110989069790714",
        "85786944089552990653640447425576083659976645795096",
        "66024396409905389607120198219976047599490197230297",
        "64913982680032973156037120041377903785566085089252",
        "16730939319872750275468906903707539413042652315011",
        "94809377245048795150954100921645863754710598436791",
        "78639167021187492431995700641917969777599028300699",
        "15368713711936614952811305876380278410754449733078",
        "40789923115535562561142322423255033685442488917353",
        "44889911501440648020369068063960672322193204149535",
        "41503128880339536053299340368006977710650566631954",
        "81234880673210146739058568557934581403627822703280",
        "82616570773948327592232845941706525094512325230608",
        "22918802058777319719839450180888072429661980811197",
        "77158542502016545090413245809786882778948721859617",
        "72107838435069186155435662884062257473692284509516",
        "20849603980134001723930671666823555245252804609722",
        "53503534226472524250874054075591789781264330331690"]

    arr = [reduce(lambda x, y: x + y, [int(x[i - 1:i]) for x in X]) for i in range(1, 51)]
    summ = 0
    for i in range(0, 11):
        summ = summ * 10 + arr[i]
    print(str(summ)[:10])


def problem14():
    mem = {}

    def len_collatz(n):
        count = 0
        while n is not 1:
            if n in mem.keys():
                count += mem[n]
                break
            if n % 2 == 0:
                n = int(n / 2)
            else:
                n = 3 * n + 1
            count += 1
        mem[n] = count
        return count

    X = range(13, 1000000)
    counts = []
    xs = []
    for x in X:
        counts.append(len_collatz(x))
        xs.append(x)
    max_length = max(counts)
    print('{} len is {}'.format(xs[counts.index(max_length)], max_length))


def problem15():
    """
    Okay, I'm too dumb to get that right out of my head, so I had to google:
    http://www.robertdickau.com/manhattan.html
    http://www.robertdickau.com/lattices.html

    It is said, that the number of paths that represent the possible paths of
    length 2n from one corner of an n-by-n grid to the opposite corner are
    the central binomial coefficients.

    So, for nxn we have C of 2n by n, (2n)!/n!^2
    """

    def cbc(x):
        return factorial(2 * x) // pow(factorial(x), 2)

    assert cbc(2) == 6
    print('{}'.format(cbc(20)))


def problem16():
    x = pow(2, 1000)
    print(sum([int(i) for i in str(x)]))


def problem15():
    N = 20
    N2 = N * N

    a = reduce(lambda x, y: x * y, range(N2 - N + 1, N2 + 1))
    b = reduce(lambda x, y: x * y, range(1, N + 1))
    print(a // b)


def problem17():
    """


    """
    known = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety',
    }

    def under_100():
        sigs = [(x % 100 // 10,
                 x % 100 % 10)
                for x in range(1, 100)]
        for tens, ones in sigs:
            dec = tens * 10 + ones
            if dec in known.keys():
                yield known[dec]
            else:
                yield '{}{}'.format(known[tens * 10], known[ones])

    lst = list(under_100())
    cnt_hundred = sum(map(lambda x: len(x), lst))

    print(
        sum(
            [len(known[x]) for x in range(1, 10)]) * 100    # 900 lines start with one, two ...
        + (len('hundredand') * 99 + len('hundred')) * 9     # 900 lines continues with hundred or hundred
        + 10 * cnt_hundred                                  # 1000 lines with 99 numbers written
        + len('onethousand')                                # single one thousand
    )


def problem18():
    X = [[75],
         [95, 64],
         [17, 47, 82],
         [18, 35, 87, 10],
         [20, 4, 82, 47, 65],
         [19, 1, 23, 75, 3, 34],
         [88, 2, 77, 73, 7, 63, 67],
         [99, 65, 4, 28, 6, 16, 70, 92],
         [41, 41, 26, 56, 83, 40, 80, 70, 33],
         [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
         [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
         [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
         [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
         [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
         [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]]

    Y = [[3],
         [7, 4],
         [2, 4, 6],
         [8, 5, 9, 3]]

    def binary_tree_max_path(data, row, col):
        vertex = data[row][col]
        if row is len(data) - 1:
            return vertex
        left = binary_tree_max_path(data, row + 1, col)
        right = binary_tree_max_path(data, row + 1, col + 1)
        res = max(left, right) + vertex
        return res

    print(binary_tree_max_path(X, 0, 0))


def problem19():
    def is_leap(x):
        if x % 400 == 0:
            return True
        if x % 100 == 0:
            return False
        if x % 4 == 0:
            return True
        return False

    m_dur = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m_leap = list(m_dur)
    m_leap[1] = 29

    def get_dur(y):
        return m_leap if is_leap(y) else m_dur

    year = 1901
    day_counter = sum(get_dur(year - 1)) + 1  # starting with monday
    res = 0
    while year <= 2000:
        for dur in get_dur(year):
            day_counter += dur
            if day_counter % 7 == 0:
                res += 1
        year += 1

    print(res)


def problem20():
    print(sum([int(x) for x in str(factorial(100))]))


def problem21():
    def amicable_sum(x):
        return sum(factors(x)) - x

    res = []
    upper = 10001
    for value in range(2, upper):
        other = amicable_sum(value)
        if other < upper and value == amicable_sum(other) and other != value:
            res.append(value)
            res.append(other)

    print(sum(set(res)))


def problem22():
    import urllib.request

    url = 'http://projecteuler.net/project/names.txt'
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    values = sorted([x.strip('\"') for x in text.split(',')])

    print(sum(
        [sum([string.ascii_lowercase.index(c) + 1 for c in value.lower()]) * (values.index(value) + 1) for value in
         values]))


def problem23():
    def is_abundant(x):
        return sum(factors(x)) > 2 * x

    UPPER = 23123
    ab = []
    arr = range(1, UPPER + 1)
    for n in arr:
        if is_abundant(n):
            ab.append(n)

    sm = sum(arr)
    vals = set()
    for a in ab:
        for b in ab:
            a_b = a + b
            if a_b <= UPPER:
                vals.add(a_b)

    print(sm - sum(vals))


def problem24():
    """
    http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
    """

    def find_largest_k(a):
        k = 0
        for i in range(0, len(a) - 1):
            if a[i] < a[i + 1]:
                k = i
        return k

    def find_largest_l(a, k):
        l = 0
        ak = a[k]
        for i in range(0, len(a)):
            if ak < a[i]:
                l = i
        return l

    arr = list(map(str, range(0, 10)))
    count = 1000000
    for i in range(1, count):
        k = find_largest_k(arr)
        l = find_largest_l(arr, k)
        arr[k], arr[l] = arr[l], arr[k]
        arr[k + 1:] = arr[-1:k:-1]
        print('{}:{}'.format(i, ''.join(arr)))


def problem25():
    gen = fib()

    cur_fib = next(gen)
    count = 0
    while len(str(cur_fib)) < 1000:
        count += 1
        cur_fib = next(gen)
    print(count)


start = default_timer()

problem25()

print('Elapsed:{}'.format(default_timer() - start))