import binascii
import random

from utils import Question, print_bool


class Question2_4(Question):
    """
    Solution for Question 2.4.
    """

    # Main Method
    def main(self):
        """Main entry point for the question class."""

        # Fake frame message.
        m = b"Hello, world!"

        # Cannot exceed length of plaintext.
        m2 = b"Howdy partner"

        self.begin_step("Show transitive property of CRC32")

        # We note here that in practice, CRC32 is actually
        # 'affine', not linear. As you can see we can turn
        # this into a linear relationship by computing the
        # base constant for CRC32 and applying it to our
        # XOR operation.

        xor_const = self.xor(self.crc32(self.xor(m, m2)), self.crc32(m), self.crc32(m2))
        print(f'XOR constant: {xor_const.hex()}')

        crc_then_xor = self.xor(self.crc32(m), self.crc32(m2), xor_const).hex()
        print(crc_then_xor)

        xor_then_crc = self.crc32(self.xor(m, m2)).hex()
        print(xor_then_crc)

        print()
        print("Does CRC then XOR == XOR then CRC")
        print_bool(crc_then_xor == xor_then_crc)

        self.begin_step("Replace plain text of packet without key (and without detection).")

        # Fake key-stream. All we do is XOR by the keystream,
        # so the exact value isn't relevant.
        keystream = random.randbytes(64)

        # Generate the cipher text 'organically', as it would
        # be in WEP.
        C = self.wep_encrypt(m, keystream)

        # We artificially compute the plain-text for our own
        # use.
        p = m + Question2_4.crc32(m)

        # Compute the new desired plain text.
        p2 = m2 + Question2_4.crc32(m2)

        # delta = p (XOR) p2
        # Delta is the value that can be applied to p to move
        # to p2. If we apply this same operation to C, we get
        # C' where C' decrypts to our desired plaintext p2.
        delta = self.xor(p, p2)

        # C' = C (XOR) delta
        # Then, we replace the packet (in this case, by just
        # writing it back into the same variable, imagine if
        # MitM was so simple...).
        C = self.xor(C, delta)

        # Now decrypt our packet
        self.wep_decrypt(C, keystream)

    @staticmethod
    def xor(a, b, *args) -> bytes:
        res = Question2_4.raw_xor(a, b)
        for arg in args:
            res = Question2_4.raw_xor(res, arg)
        return res

    @staticmethod
    def raw_xor(a, b) -> bytes:
        # XOR each byte, byte by byte, and convert the resulting
        # list of bytes into a bytes object.
        return bytes(
            [((ord(cA) if isinstance(cA, str) else cA) ^ (ord(cB) if isinstance(cB, str) else cB)) for cA, cB in
             zip(a, b)])

    @staticmethod
    def crc32(x) -> bytes:
        # Compute CRC32 with the binascii library.
        return binascii.crc32(x, 0).to_bytes(4, 'big')

    @staticmethod
    def wep_encrypt(x: bytes, k: bytes):
        # Plain text is (n + 32)-bit M || L(M)
        p = x + Question2_4.crc32(x)
        c = Question2_4.xor(k, p)
        print(f"Computed CRC: {Question2_4.crc32(x).hex()}")
        print(f"Encrypted plaintext: {c.hex()}")
        return c

    @staticmethod
    def wep_decrypt(x: bytes, k: bytes):
        p = Question2_4.xor(x, k)

        plaintext = p[:-4]
        crc = p[-4:]
        print(f"Decrypted plaintext: {plaintext}")
        print(f"Obtained CRC: {crc.hex()}")
        print(f"Computed CRC: {Question2_4.crc32(plaintext).hex()}")

        if Question2_4.crc32(plaintext) == crc:
            print("CRC validated")
        else:
            print("CRC invalid")

        return plaintext

    @staticmethod
    def flip_bit(payload: bytes, bit_number: int) -> bytes:
        target = int(bit_number / 8)
        mask = 1 << (bit_number % 8)

        mask_value = [0] * len(payload)
        mask_value[target] = mask
        mask_value = bytes(mask_value)

        return Question2_4.xor(mask_value, payload)
