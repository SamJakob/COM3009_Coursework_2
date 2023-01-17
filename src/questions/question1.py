import math
from typing import Optional, Tuple

from utils import print_bool, Question


class Question1(Question):
    """
    Solution for Question 1.
    """

    # Settings
    public_exponent = 65537
    """The RSA public exponent used."""

    ciphertext = 19792606470044155211455204150434549948072538336044223694954674364537247475101018812008638353298641469273134687688990436824521982866914567238087017185646832618538036395592603265241964273726601376649962151590308162502072220318764983109427999786154465148990461380776309184213604728577020438154325916782604166322
    """The RSA ciphertext to be decrypted."""

    modulus = 20067674652864705507618478078894371825703299189985229769589511421524535558259570851952511531397245086777923890860793377793308430786064838968878551026724279066734424284905076041579325272841356205633689378811024723012326452461940608315691916435268078174776596788954785347962790386029617883800516764964060553491
    """The RSA modulus n. This modulus has two prime factors, p and q."""

    known_range_bound = 10_000
    """The known upper bound for the range |p - q|."""

    # Methods
    @staticmethod
    def find_modulus_factors(n: int, range_limit=None) -> Optional[Tuple[int, int]]:
        """
        Finds the prime factors for a given integer RSA modulus n, where the range
        between the two prime factors is less than (64n)^1/4.

        :param n: The modulus to factorize.
        :param range_limit: Optionally, a range limit that can be specified to
        show if the assumption will hold.
        :return: Either the integers p and q in a Tuple, or None.
        """

        print(f"n = {format(n, '.32e')}")

        # If the known range limit is specified, we'll also double check that the
        # assumption needed for our simplified version of Fermat holds for that
        # entire range. This can allow us to verify that for any two prime factors
        # in that range, for example, will be correct per this theorem.
        if range_limit is not None:
            print()
            print("Assumption 1. Does |p - q| < (64n)^1/4 hold?")
            print(f"(64n)^1/4 = {format(math.isqrt(math.isqrt(64 * n)), '.32e')}")
            print_bool(range_limit < math.isqrt(math.isqrt(64 * n)))
            print()

        # a is the next square number after n.
        # Let's say (for demonstration purposes only) that sqrt(n) = 2.4, a = 3.
        # isqrt(n) = 2 (because isqrt floors). Thus, when we isqrt and add one,
        # we get the next square number after n.
        # Strictly speaking, we should be doing sqrt & ceil, but as
        # explained in the accompanying submission paper, we know that given
        # n is prime, there will be no exact integer square root (i.e., there
        # will always be a remainder), so that can be optimized into an integer
        # square root (which floors) followed by adding 1 to the result.
        # In other words, we know that isqrt, here, will *always* round down.
        a = math.isqrt(n) + 1
        print(f"a = {format(n, '.32e')}")

        # s is then a^2 - n. Per Fermat's factorization method, this will be the
        # square of some integer, b.
        s = (a ** 2) - n
        print(f"s = {s}")

        # Perform a quick, naive check that s is the square of some integer, by
        # performing integer square root and floating-point square root and
        # comparing them. In other words, this confirms that there is no remainder.
        print()
        print("Assumption 2. Is s the square of some integer?")
        s_is_square_number = math.sqrt(s) == math.isqrt(s)
        print_bool(s_is_square_number)
        if not s_is_square_number: return None
        print()

        # Square root s to get the delta applied to a for the prime factors.
        b = math.isqrt(s)
        print(f"b = {b}")
        print()

        # Compute p and q, which per Fermat's theorem are a + b and a - b.
        p = a + b
        q = a - b
        print(f"p = {p}")
        print(f"q = {q}")

        # Return the prime factors, p and q, as a tuple.
        return p, q

    @staticmethod
    def find_private_exponent(p: int, q: int, public_exponent: int = 65537) -> int:
        """
        Finds the RSA private exponent, d, for two prime factors, p and q using
        the modular inverse (supplied by Python's own standard library in Python
        3.8+).

        :param public_exponent: The RSA public exponent, e.
        :param p: A prime factor of the modulus.
        :param q: A prime factor of the modulus.
        :return: The private exponent, d.
        """
        phi = (p - 1) * (q - 1)
        return pow(public_exponent, -1, phi)

    @staticmethod
    def rsa_encrypt(plaintext: int, public_exponent: int, modulus: int) -> int:
        """
        Encrypts the specified plaintext using the public key (public exponent and
        modulus).
        """

        # Ciphertext = plaintext^d mod n
        return pow(plaintext, public_exponent, modulus)

    @staticmethod
    def rsa_decrypt(ciphertext: int, private_exponent: int, modulus: int) -> int:
        """
        Decrypts the specified ciphertext using hte private key (private exponent
        and modulus).
        """

        # Plaintext = ciphertext^d mod n
        return pow(ciphertext, private_exponent, modulus)

    # Main Method
    # Used to execute the steps necessary to complete Question 1.
    def main(self):
        """Main entry point for the question class."""

        self.begin_step("Get p and q using our find_modulus_factors function.")
        p, q = self.find_modulus_factors(self.modulus, self.known_range_bound)

        self.begin_step("Find private exponent d = d = e^-1 mod (p-1)(q-1)")
        d = self.find_private_exponent(p, q, public_exponent=self.public_exponent)
        print(f"d = {d}")

        self.begin_step("Compute plain text = ciphertext^d mod n")
        plaintext = self.rsa_decrypt(self.ciphertext, d, self.modulus)
        print(f"Decrypted Plaintext = {plaintext}")

        self.begin_step("Confirm that re-encrypting the value yields the same ciphertext...")
        print_bool(self.rsa_encrypt(plaintext, 65537, self.modulus) == self.ciphertext)
