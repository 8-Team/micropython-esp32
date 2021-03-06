# based on https://github.com/python/cpython/blob/3.6/Lib/hmac.py

"""HMAC (Keyed-Hashing for Message Authentication) Python module.

Implements the HMAC algorithm as described by RFC 2104.
"""

import uhashlib as _uhashlib


trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))


class HMAC:
    """RFC 2104 HMAC class.  Also complies with RFC 4231.

    This supports the API for Cryptographic Hash Functions (PEP 247).

    copy() DOES NOT WORK, DO NOT CALL digest() and hexdigest() multiple times
    """
    blocksize = 64  # 512-bit HMAC; can be changed in subclasses.

    def __init__(self, key, msg=None, digestmod=None):
        """Create a new HMAC object.

        key:       key for the keyed hash object.
        msg:       Initial input for the hash, if provided.
        digestmod: A module supporting PEP 247.  *OR*
                   A hashlib constructor returning a new hash object. *OR*
                   A hash name suitable for hashlib.new().
                   Defaults to hashlib.md5.
                   Implicit default to hashlib.md5 is deprecated and will be
                   removed in Python 3.6.

        Note: key and msg must be a bytes or bytearray objects.
        """

        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key: expected bytes or bytearray, but got %r" % type(key).__name__)

        self.digest_cons = _uhashlib.sha256 if digestmod is None else digestmod

        self.outer = self.digest_cons()
        self.inner = self.digest_cons()
        self.digest_size = self.inner.digest_size

        if hasattr(self.inner, 'block_size'):
            blocksize = self.inner.block_size

            if blocksize < 16:
                print('block_size of %d seems too small; using our '
                      'default of %d.' % (blocksize, self.blocksize))
                blocksize = self.blocksize
        else:
            print('No block_size attribute on given digest object; '
                           'Assuming %d.' % (self.blocksize))
            blocksize = self.blocksize

        # self.blocksize is the default blocksize. self.block_size is
        # effective block size as well as the public API attribute.
        self.block_size = blocksize

        if len(key) > blocksize:
            key = self.digest_cons(key).digest()

        key = _ljust_null(key, blocksize - len(key))
        self.outer.update(_translate(key, trans_5C))
        self.inner.update(_translate(key, trans_36))
        if msg is not None:
            self.update(msg)

    @property
    def name(self):
        return "hmac-" + self.inner.name

    def update(self, msg):
        """Update this hashing object with the string msg.
        """
        self.inner.update(msg)

    # def copy(self):
    #     """Return a separate copy of this hashing object.

    #     An update to this copy won't affect the original object.
    #     """
    #     # Call __new__ directly to avoid the expensive __init__.
    #     other = self.__class__.__new__(self.__class__)
    #     other.digest_cons = self.digest_cons
    #     other.digest_size = self.digest_size
    #     other.inner = self.inner.copy()
    #     other.outer = self.outer.copy()
    #     return other

    def _current(self):
        """Return a hash object for the current state.

        To be used only internally with digest() and hexdigest().
        """
        self.outer.update(self.inner.digest())
        return self.outer

    def digest(self):
        """Return the hash value of this hashing object.

        This returns a string containing 8-bit data.  The object is
        not altered in any way by this function; you can continue
        updating the object after calling this function.
        """
        h = self._current()
        return h.digest()

    def hexdigest(self):
        """Like digest(), but returns a string of hexadecimal digits instead.
        """
        h = self._current()
        return h.hexdigest()


def new(key, msg=None, digestmod=None):
    """Create a new hashing object and return it.

    key: The starting key for the hash.
    msg: if available, will immediately be hashed into the object's starting
    state.

    You can now feed arbitrary strings into the object using its update()
    method, and can ask for the hash value at any time by calling its digest()
    method.
    """
    return HMAC(key, msg, digestmod)


# these functions are not in upy yet
def _ljust_null(s, n):
    return s + bytes(n)


def _translate(s, table):
    ret = bytearray(len(s))

    for i, b in enumerate(s):
        ret[i] = table[b]

    return bytes(ret)

