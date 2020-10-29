import typing as tp

def encrypt_caesar(plaintext: str, shift: int=3) -> str:
    ciphertext = ""
    for i in range (len(plaintext)):
        s=plaintext[i]
        if (s.isalpha()):
            if ((ord(s.upper())+shift) > 90):
                ciphertext+=chr(ord(s)-(26-shift))
            else : 
                ciphertext+=chr(ord(s)+shift)
        else:
            ciphertext+=s
    return ciphertext

def decrypt_caesar(ciphertext: str, shift: int=3) -> str:
    plaintext = ""
    for i in range (len(ciphertext)):
        s=ciphertext[i]
        if (s.isalpha()):
            if ((ord(s.upper())-shift) < 65) :
                plaintext += chr(ord(s)+(26-shift))
            else : 
                plaintext +=chr(ord(s)-shift)
        else:
            plaintext+=s
    return plaintext

def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
