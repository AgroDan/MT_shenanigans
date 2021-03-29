import mersenne


def preseed(seed_array):
    """
        seed_array := a list of numbers of size 624
        Returns a new MT19937 object seeded to the same
    """
    assert type(seed_array) is list
    assert len(seed_array) == 624
    m = mersenne.MT19937(0)
    m.MT = [i for i in seed_array]
    m.index = 624
    return m


def undo_right_shift(number, shift_len, max_len=32):
    """
        This function will un-do the right shift function performed in the
        extract_number() function in the Mersenne Twister. This is integral
        in building the state array to re-create the algorithm.
        number := the original number
        shift_len := the shift length stated in this function
        max_len := the size length of the random number stored. 32 bits is default.
    """
    result = number
    for i in range(0, max_len, shift_len):
        mask = ((1<<shift_len)-1)     # Create a mask of size shift_len
        mask <<= (max_len-shift_len)  # shift mask over specified amount of times
        mask >>= i                    # mask moved over more for specificity
        pulled = result & mask        # Pull the number from the result w/ the mask
        pulled >>= shift_len          # shift pulled over shift_len
        result ^= pulled              # XOR result with pulled
    return result


def undo_left_shift_and(number, and_constant, shift_len, max_len=32):
    """
        This function will un-do the left shift function, which is a little bit
        different from the right shift, mostly because there is also an AND function
        performed with two constants. However, due to some logical magic, this is
        able to be un-done.
    """
    result = number
    for i in range(0, max_len, shift_len):
        mask = (1<<shift_len)-1     # Create a mask of size shift_len
        mask = mask << i                  # Shift it over <i> bits
        part = mask & result        # Create a part var, consisting of bits we masked
        part = part << shift_len          # shift it over another shift_len bits
        anded = part & and_constant # AND the part with the supplied and_constant
        result = result ^ anded             # result is XORd with above anded
    return result

def untemper(number):
    """
        This function works through the process of "untempering" a number
        to place it back into the array to duplicate the (pseudo) random number
        generation.
    """
    res = number
    res = undo_right_shift(res, 18)
    res = undo_left_shift_and(res, 0xefc60000, 15)
    res = undo_left_shift_and(res, 0x9d2c5680, 7)
    res = undo_right_shift(res, 11)
    return res
