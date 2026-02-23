"""
Compatibility layer for a minimal subset of python-ecdsa APIs.

This module is intentionally small and only implements the methods currently
used by the Behave step definitions in this repository.
"""

from __future__ import annotations

import hashlib
from typing import Callable, Optional

try:
    from coincurve import PrivateKey as CoincurvePrivateKey
    from coincurve import PublicKey as CoincurvePublicKey

    SECP256K1_AVAILABLE = True
except ImportError:
    CoincurvePrivateKey = None
    CoincurvePublicKey = None
    SECP256K1_AVAILABLE = False

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec, utils

    NIST256P_AVAILABLE = True
except ImportError:
    InvalidSignature = None
    hashes = None
    serialization = None
    ec = None
    utils = None
    NIST256P_AVAILABLE = False


SECP256k1 = "SECP256k1"
NIST256p = "NIST256p"


class BadSignatureError(Exception):
    """Compatibility error matching python-ecdsa verify failures."""


def _build_hasher(
    hashfunc: Optional[Callable[[bytes], "hashlib._Hash"]] = None,
) -> Callable[[bytes], bytes]:
    if hashfunc is None:
        return lambda message: hashlib.sha256(message).digest()
    return lambda message: hashfunc(message).digest()


def _hash_algorithm_for(hashfunc: Optional[Callable]) -> "hashes.HashAlgorithm":
    if not NIST256P_AVAILABLE:
        raise ImportError("cryptography library not available")

    if hashfunc is None:
        return hashes.SHA256()

    name = getattr(hashfunc, "__name__", "").lower()
    if "sha512" in name:
        return hashes.SHA512()
    if "sha384" in name:
        return hashes.SHA384()
    if "sha1" in name:
        return hashes.SHA1()
    return hashes.SHA256()


def _raw_signature_to_der(signature: bytes) -> bytes:
    if not NIST256P_AVAILABLE:
        raise ImportError("cryptography library not available")
    if len(signature) != 64:
        raise BadSignatureError("expected 64-byte raw signature")
    r = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:], "big")
    return utils.encode_dss_signature(r, s)


def _der_signature_to_raw(signature: bytes) -> bytes:
    if not NIST256P_AVAILABLE:
        raise ImportError("cryptography library not available")
    r, s = utils.decode_dss_signature(signature)
    return r.to_bytes(32, "big") + s.to_bytes(32, "big")


class VerifyingKey:
    def __init__(self, curve: str, key_obj):
        self.curve = curve
        self._key_obj = key_obj

    @classmethod
    def from_string(cls, key_bytes: bytes, curve: str) -> "VerifyingKey":
        if curve == SECP256k1:
            if not SECP256K1_AVAILABLE:
                raise ImportError("coincurve library not available")
            if len(key_bytes) == 64:
                key_bytes = b"\x04" + key_bytes
            return cls(curve, CoincurvePublicKey(key_bytes))

        if curve == NIST256p:
            if not NIST256P_AVAILABLE:
                raise ImportError("cryptography library not available")
            if len(key_bytes) == 64:
                key_bytes = b"\x04" + key_bytes
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256R1(), key_bytes
            )
            return cls(curve, public_key)

        raise ValueError(f"unsupported curve: {curve}")

    def to_string(self, encoding: Optional[str] = None) -> bytes:
        if self.curve == SECP256k1:
            compressed = encoding == "compressed"
            key_bytes = self._key_obj.format(compressed=compressed)
            return key_bytes if compressed else key_bytes[1:]

        if self.curve == NIST256p:
            if not NIST256P_AVAILABLE:
                raise ImportError("cryptography library not available")
            if encoding == "compressed":
                return self._key_obj.public_bytes(
                    encoding=serialization.Encoding.X962,
                    format=serialization.PublicFormat.CompressedPoint,
                )
            uncompressed = self._key_obj.public_bytes(
                encoding=serialization.Encoding.X962,
                format=serialization.PublicFormat.UncompressedPoint,
            )
            return uncompressed[1:]

        raise ValueError(f"unsupported curve: {self.curve}")

    def verify(
        self,
        signature: bytes,
        message: bytes,
        hashfunc: Optional[Callable[[bytes], "hashlib._Hash"]] = None,
    ) -> bool:
        try:
            if self.curve == SECP256k1:
                if len(signature) == 64:
                    signature = _raw_signature_to_der(signature)
                is_valid = self._key_obj.verify(
                    signature,
                    message,
                    hasher=_build_hasher(hashfunc),
                )
                if not is_valid:
                    raise BadSignatureError("signature verification failed")
                return True

            if self.curve == NIST256p:
                if len(signature) == 64:
                    signature = _raw_signature_to_der(signature)
                self._key_obj.verify(
                    signature,
                    message,
                    ec.ECDSA(_hash_algorithm_for(hashfunc)),
                )
                return True

            raise ValueError(f"unsupported curve: {self.curve}")
        except BadSignatureError:
            raise
        except Exception as exc:
            if InvalidSignature is not None and isinstance(exc, InvalidSignature):
                raise BadSignatureError("signature verification failed") from exc
            if isinstance(exc, (ValueError, TypeError)):
                raise BadSignatureError("invalid signature bytes") from exc
            raise


class SigningKey:
    def __init__(self, curve: str, key_obj):
        self.curve = curve
        self._key_obj = key_obj

    @classmethod
    def generate(cls, curve: str) -> "SigningKey":
        if curve == SECP256k1:
            if not SECP256K1_AVAILABLE:
                raise ImportError("coincurve library not available")
            return cls(curve, CoincurvePrivateKey())

        if curve == NIST256p:
            if not NIST256P_AVAILABLE:
                raise ImportError("cryptography library not available")
            return cls(curve, ec.generate_private_key(ec.SECP256R1()))

        raise ValueError(f"unsupported curve: {curve}")

    @classmethod
    def from_string(cls, key_bytes: bytes, curve: str) -> "SigningKey":
        if curve == SECP256k1:
            if not SECP256K1_AVAILABLE:
                raise ImportError("coincurve library not available")
            return cls(curve, CoincurvePrivateKey(key_bytes))

        if curve == NIST256p:
            if not NIST256P_AVAILABLE:
                raise ImportError("cryptography library not available")
            if len(key_bytes) != 32:
                raise ValueError("private key must be 32 bytes")
            private_value = int.from_bytes(key_bytes, "big")
            private_key = ec.derive_private_key(private_value, ec.SECP256R1())
            return cls(curve, private_key)

        raise ValueError(f"unsupported curve: {curve}")

    def get_verifying_key(self) -> VerifyingKey:
        if self.curve == SECP256k1:
            return VerifyingKey(self.curve, self._key_obj.public_key)
        if self.curve == NIST256p:
            return VerifyingKey(self.curve, self._key_obj.public_key())
        raise ValueError(f"unsupported curve: {self.curve}")

    def to_string(self) -> bytes:
        if self.curve == SECP256k1:
            return self._key_obj.secret
        if self.curve == NIST256p:
            private_value = self._key_obj.private_numbers().private_value
            return private_value.to_bytes(32, "big")
        raise ValueError(f"unsupported curve: {self.curve}")

    def sign(
        self,
        message: bytes,
        hashfunc: Optional[Callable[[bytes], "hashlib._Hash"]] = None,
    ) -> bytes:
        if self.curve == SECP256k1:
            der_signature = self._key_obj.sign(
                message,
                hasher=_build_hasher(hashfunc),
            )
            return _der_signature_to_raw(der_signature)

        if self.curve == NIST256p:
            if not NIST256P_AVAILABLE:
                raise ImportError("cryptography library not available")
            der_signature = self._key_obj.sign(
                message,
                ec.ECDSA(_hash_algorithm_for(hashfunc)),
            )
            return _der_signature_to_raw(der_signature)

        raise ValueError(f"unsupported curve: {self.curve}")
