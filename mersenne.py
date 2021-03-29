class MT19937():
    # If this is unseeded, I will seed with the C constant
    # of 5489 since you're too lazy to do it yourself you bum
    def __init__(self, seed=5489):
        # HERE BE CONSTANTS
        self.w = 32 # word size, in num of bits. Max length of each number in the array
        self.n = 624 # degree of recurrence
        self.m = 397 # middle word, offset of recurrence relation defining the series
        self.r = 31 # separation point of one word, or num of bits of lower bitmask
        self.a = 0x9908b0df # coefficients of rational normal form twist matrix
        self.u = 11 # additionall MT tempering bit shifts/masks
        self.d = 0xffffffff # additionall MT tempering bit shifts/masks
        self.s = 7 # TGFSR(R) tempering bit shift
        self.b = 0x9d2c5680 # TGRSR(R) tempering bit masks
        self.t = 15 # TGFSR(R) tempering bit shift
        self.c = 0xefc60000 # TGRSR(R) tempering bit masks
        self.l = 18 # additionall MT tempering bit shifts/masks
        self.f = 1812433253 
        # Declare the array of zeroes to start
        self.MT = [0 for _ in range(self.n)]
        self.lower_mask = (1<<self.r)-1
        self.upper_mask = (1<<self.r)
        self.index = self.n+1
        self._seed_mt(seed)

    def _seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            t = self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i
            self.MT[i] = t & 0xffffffff

    def _twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1)%self.n] & self.lower_mask)
            xA = x >> 1
            if not (x%2) == 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i+self.m) % self.n] ^ xA

        self.index = 0

    # extract a tempered value based on MT[index]
    # calling twist() every n numbers
    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                # This was never seeded. So seed with
                # the C constant for unseeded gen
                self._seed_mt(5489)
                # Truthfully though, I don't think we
                # will ever hit here without some serious
                # code-mucking but I'll keep it in here
                # just for those people that do this
            self._twist()

        y = self.MT[self.index]
        y ^= ((y >> self.u) & self.d)
        y ^= ((y << self.s) & self.b)
        y ^= ((y << self.t) & self.c)
        y ^= (y >> self.l)
        self.index += 1
        return y & 0xffffffff
