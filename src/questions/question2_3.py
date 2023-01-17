from typing import Tuple

from utils import Question


class Question2_3(Question):
    """
    Helper for Question 2.3.
    """

    # Main Method
    # Small, simple, (and naive) application used to compute the point where
    # the chance of two IV values colliding exceeds 50% in terms of number of
    # packets communicating.
    def main(self):
        """Main entry point for the question class."""

        # Quick test for birthday paradox
        # n, result = self.determine_packets_for_p(365, 0.5)
        # print(f"In a group of {n} people, chance of birthday collision is {result}")

        n, result = self.determine_packets_for_p(2 ** 24, 0.5)
        print(f"After {n} packets: P = {result}")

        n, result = self.determine_packets_for_p(2 ** 24, 0.75)
        print(f"After {n} packets: P = {result}")

        n, result = self.determine_packets_for_p(2 ** 24, 0.99)
        print(f"After {n} packets: P = {result}")

    @staticmethod
    def determine_packets_for_p(k: int, p: float) -> Tuple[int, float]:
        """
        Naive, brute-force, approach to check the number of packets required
        to get a collision with probability p.

        Essentially, this function calculates the minimum group size to have
        at least 2 collisions per the birthday paradox with probability >= p.

        The "number of days" - practically, in this case, the number of
        possible keys - is k. So, for the original problem, it would be 365.
        """

        n = 1
        """
        The number of packets (group size) required.
        Here, we just start with 1 and count up to make this more dynamic, but
        this can be optimized when a lower bound is known.
        """

        while True:
            # The current fraction that should be subtracted from result.
            frac = 1

            # Quick and dirty way of computing the birthday paradox: compute
            # each fraction involved, and multiply them together.
            for i in range(1, n):
                frac *= ((k - i) / k)

            # Then, our result is 1 - the number of fractions multiplied
            # together.
            result = 1 - frac

            # If our result is >= p, we can exit early and return our result
            # and group size. Otherwise, we increment the group size and check
            # again.
            if result >= p:
                break
            else:
                n += 1

        return n, result
