# based on pyotp

import base64
import uhashlib as hashlib
import hmac

class OTP(object):
    """
    Base class for OTP handlers.
    """
    def __init__(self, s, digits=6, digest=hashlib.sha1):
        """
        :param s: secret in base32 format
        :type s: str
        :param digits: number of integers in the OTP. Some apps expect this to be 6 digits, others support more.
        :type digits: int
        :param digest: digest function to use in the HMAC (expected to be sha256)
        :type digest: callable
        """
        self.digits = digits
        self.digest = digest
        self.secret = s
        self.byte_secret = self._get_byte_secret()

    def generate_otp(self, input):
        """
        :param input: the HMAC counter value to use as the OTP input.
            Usually either the counter, or the computed integer based on the Unix timestamp
        :type input: int
        """
        if input < 0:
            raise ValueError('input must be positive integer')

        hasher = hmac.new(self.byte_secret, self.int_to_bytestring(input), self.digest)
        hmac_hash = bytearray(hasher.digest())

        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))

        str_code = str(code % 10 ** self.digits)
        str_code = '0' * (self.digits - len(str_code)) + str_code

        return str_code

    def _get_byte_secret(self):
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode(self.secret, casefold=True)

    @staticmethod
    def int_to_bytestring(i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        """
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8

        result = bytearray(reversed(result))
        return b'\0' * (padding - len(result)) + result

    def totp(self, for_time, interval=30):
        """
        Accepts a Unix timestamp integer.
        :param for_time: the time to generate an OTP for
        :type for_time: int
        :param interval: the time interval in seconds
            for OTP. This defaults to 30.
        :type interval: int
        :returns: OTP value
        :rtype: str
        """
        for_time = for_time // interval
        return self.generate_otp(for_time)

    # TODO
    # def verify()


