def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    shift=keyword*(round(len(plaintext)/len(keyword))+1)
    for i in range (len(plaintext)):
        s=plaintext[i]
        step=ord(shift[i].upper())-65
        if (s.isalpha()):
            if (ord(s.upper())+step > 90):
                ciphertext+=chr(ord(s)-(26-step))
            else : 
                ciphertext+=chr(ord(s)+step)
        else:
            ciphertext+=s
    return ciphertext    


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    shift=keyword*(round(len(ciphertext)/len(keyword))+1)
    for i in range (len(ciphertext)):
        step=ord(shift[i].upper())-65
        s=ciphertext[i]
        if (s.isalpha()):
            if ((ord(s.upper())-step) < 65) :
                plaintext +=chr(ord(s)+(26-step))
            else : 
                plaintext +=chr(ord(s)-step)
        else:
            plaintext+=s
    return plaintext