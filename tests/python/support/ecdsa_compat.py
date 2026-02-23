"""
Compatibility layer for a minimal subset of python-ecdsa APIs.

This module is intentionally small and only implements the methods currently
used by the Behave step definitions in this repository.
"""

from __future__ import annotations

import hashlib
from typing import Callable, Optional

try:
    from coincurve import ecdsa as coincurve_ecdsa
    from coincurve import PrivateKey as CoincurvePrivateKey
    from coincurve import PublicKey as CoincurvePublicKey

    SECP256K1_AVAILABLE = True
except ImportError:
    coincurve_ecdsa = None
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
NIST256P_ORDER = int(
    "FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551",
    16,
)


class BadSignatureError(Exception):
    """Compatibility error matching python-ecdsa verify failures."""


def _build_hasher(
    hashfunc: Optional[Callable[[bytes], "hashlib._Hash"]] = None,
) -> Callable[[bytes], bytes]:
    if hashfunc is None:
        return lambda message: hashlib.sha256(message).digest()
    return lambda message: hashfunc(message).digest()


def _hash_algorithm_for(
    hashfunc: Optional[Callable],
) -> "hashes.HashAlgorithm":
    if not NIST256P_AVAILABLE:
        raise ImportError("cryptography library not available")

    if hashfunc is None:
        return hashes.SHA256()

    known_hashes = {
        hashlib.sha512: hashes.SHA512,
        hashlib.sha384: hashes.SHA384,
        hashlib.sha256: hashes.SHA256,
        hashlib.sha1: hashes.SHA1,
    }
    for known_func, algorithm in known_hashes.items():
        if hashfunc is known_func:
            return algorithm()

    name = getattr(hashfunc, "__name__", "").lower()
    if name == "sha512":
        return hashes.SHA512()
    if name == "sha384":
        return hashes.SHA384()
    if name == "sha1":
        return hashes.SHA1()
    return hashes.SHA256()


def _raw_signature_to_der(signature: bytes, curve: str) -> bytes:
    if len(signature) != 64:
        raise BadSignatureError("expected 64-byte raw signature")

    if curve == SECP256k1:
        if not SECP256K1_AVAILABLE:
            raise ImportError("coincurve library not available")
        try:
            return coincurve_ecdsa.cdata_to_der(
                coincurve_ecdsa.deserialize_compact(signature)
            )
        except (TypeError, ValueError) as exc:
            raise BadSignatureError("invalid signature bytes") from exc

    if curve == NIST256p:
        if not NIST256P_AVAILABLE:
            raise ImportError("cryptography library not available")
        r = int.from_bytes(signature[:32], "big")
        s = int.from_bytes(signature[32:], "big")
        if not (0 < r < NIST256P_ORDER and 0 < s < NIST256P_ORDER):
            raise BadSignatureError("invalid signature bytes")
        return utils.encode_dss_signature(r, s)

    raise ValueError(f"unsupported curve: {curve}")


def _der_signature_to_raw(signature: bytes, curve: str) -> bytes:
    if curve == SECP256k1:
        if not SECP256K1_AVAILABLE:
            raise ImportError("coincurve library not available")
        try:
            return coincurve_ecdsa.serialize_compact(
                coincurve_ecdsa.der_to_cdata(signature)
            )
        except (TypeError, ValueError) as exc:
            raise BadSignatureError("invalid signature bytes") from exc

    if curve == NIST256p:
        if not NIST256P_AVAILABLE:
            raise ImportError("cryptography library not available")

        try:
            r, s = utils.decode_dss_signature(signature)
        except ValueError as exc:
            raise BadSignatureError("invalid signature bytes") from exc

        if not (0 < r < NIST256P_ORDER and 0 < s < NIST256P_ORDER):
            raise BadSignatureError("invalid signature bytes")

        try:
            return r.to_bytes(32, "big") + s.to_bytes(32, "big")
        except OverflowError as exc:
            raise BadSignatureError("signature component too large") from exc

    raise ValueError(f"unsupported curve: {curve}")


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
                    signature = _raw_signature_to_der(
                        signature,
                        curve=self.curve,
                    )
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
                    signature = _raw_signature_to_der(
                        signature,
                        curve=self.curve,
                    )
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
            if (
                InvalidSignature is not None
                and isinstance(exc, InvalidSignature)
            ):
                raise BadSignatureError(
                    "signature verification failed"
                ) from exc
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
            if not 1 <= private_value < NIST256P_ORDER:
                raise ValueError(
                    "private key integer is out of range for NIST256p curve"
                )
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
            return _der_signature_to_raw(der_signature, curve=self.curve)

        if self.curve == NIST256p:
            der_signature = self._key_obj.sign(
                message,
                ec.ECDSA(_hash_algorithm_for(hashfunc)),
            )
            return _der_signature_to_raw(der_signature, curve=self.curve)

        raise ValueError(f"unsupported curve: {self.curve}")
