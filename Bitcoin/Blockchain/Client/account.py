import sys
sys.path.append('/Users/matthewdeng/Intro-to-Blockchain-Crypto/Bitcoin')
from Blockchain.Backend.core.EllepticCurve.EllepticCurve import Sha256Point, BASE58_ALPHABET
import secrets
from Blockchain.Backend.util.util import hash160, hash256

class account:
    def createKeys(self):
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        G = Sha256Point(Gx, Gy)

        private_key = secrets.randbits(256)
        unCompressedPublicKey = private_key * G
        xpoint = unCompressedPublicKey.x
        ypoint = unCompressedPublicKey.y

        if ypoint.num % 2 == 0:
            compressedKey = b'\x02' + xpoint.num.to_bytes(32, byteorder='big')
        else:
            compressedKey = b'\x03' + xpoint.num.to_bytes(32, byteorder='big')

        hsh160 = hash160(compressedKey)
        """Prefix for Mainnet"""
        main_prefix = b'\x00'
        newAddr = main_prefix + hsh160

        """Checksum"""
        checksum = hash256(newAddr)[:4]
        newAddr = newAddr + checksum
        BASE58_ALPHABET = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        count = 0

        for c in newAddr:
            if c == 0:
                count += 1
            else:
                break

        num = int.from_bytes(newAddr, byteorder='big')
        prefix = '1' * count

        result = ''

        while num > 0:
            num, mod = divmod(num, 58)
            result = BASE58_ALPHABET[mod] + result

        PublicAddress = prefix + result

        print(f"Private Key: {private_key}")
        print(f"Public Address: {PublicAddress}")

if __name__ == "__main__":
    account = account()
    account.createKeys()