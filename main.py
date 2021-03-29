"""
    This is a POC of the Mersenne Twister Predictor. More
    information about it is here: https://agrohacksstuff.io/crypto/mt-in-action/
"""

import mersenne
import untwist

print("Here is an example of the Mersenne Twister Pseudo-Random Number Generator.")
print("First, I will initialize the MT19937 object, and seed it with some value.")
print("For the sake of this example, I will use the seed 8080808.")
print("")
m = mersenne.MT19937(8080808)
first_random = m.extract_number()

print(f"An example of a PRNG pulled from this seed: {first_random}")
print("")
print("Now, I will generate a list of random numbers by executing")
print("'extract_number()' 623 more times, filling up the state array.")
print("")
e_nums = [m.extract_number() for _ in range(623)]

# Don't forget to stuff the first random number at the top
e_nums = [first_random] + e_nums

print("Now I will untemper each of these extracted numbers, creating a")
print("new list, which should match up with the state array of the original")
print("PRNG object!")
print("")
u_nums = [untwist.untemper(i) for i in e_nums]

print("If we were successful, these two samples should be the same:")
print(f"PRNG: Index 10: {m.MT[10]}, Index 350: {m.MT[350]}")
print(f"utmp: Index 10: {u_nums[10]}, Index 350: {u_nums[350]}")
print("")

print("Now I can just seed a new random object and start calling random")
print("numbers:")
print("")

x = untwist.preseed(u_nums)

for i in range(10):
    print(f"RND from MT19937: {m.extract_number()}")
    print(f"RND from self: {x.extract_number()}")
    print("")

print("Successfully predicted future iterations of this PRNG by")
print("listening to 624 extracted samples!")