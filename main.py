import math
import random

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def find_primes(n):
    for i in range(2, n):
        if is_prime(i) and n % i == 0:
            return i, n // i

def euclidean(divident, divisor):
    while divisor:
        divident, divisor = divisor, divident % divisor
    return divident

def extended_euclidean(divident, divisor):
    prev_x, curr_x, prev_y, curr_y = 1, 0, 0, 1
    while divisor != 0:
        q, divident, divisor = divident // divisor, divisor, divident % divisor
        prev_x, curr_x = curr_x, prev_x - q * curr_x
        prev_y, curr_y = curr_y, prev_y - q * curr_y
    return divident, prev_x, prev_y

def mod_inverse(divident, modulus):
    gcd, x, _ = extended_euclidean(divident, modulus)
    if gcd != 1:
        raise Exception("Modular inverse does not exist")
    return x % modulus

def find_public_key(totient):
    e = random.randrange(2, totient)
    while euclidean(e, totient) != 1:
        e = random.randrange(2, totient)
    return e

def find_private_key(e, totient):
    return mod_inverse(e, totient)

def encrypt(plaintext, public_key):
    n, e = public_key
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(ciphertext, private_key, n):
    return "".join(chr(pow(char, private_key, n)) for char in ciphertext)

def save(ciphertext, public_key):
    with open("ciphertext.txt", "w") as ctfile:
        ctfile.write(" ".join(str(c) for c in ciphertext))
    with open("public_key.txt", "w") as pkfile:
        pkfile.write(f"{public_key[0]} {public_key[1]}")

def read_file():
    with open("ciphertext.txt", "r") as ctfile:
        ciphertext = [int(c) for c in ctfile.read().split()]
    with open("public_key.txt", "r") as pkfile:
        n, e = map(int, pkfile.read().split())
    return ciphertext, (n, e)

def main():
    option = input("Encrypt a message (E) | Decrypt a message from a file (D)? ")

    if option.lower() == "e":
        p = int(input("Enter prime number p: "))
        while not is_prime(p):
            p = int(input("p must be a prime number. Try again: "))

        q = int(input("Enter a prime number q: "))
        while not is_prime(q):
            q = int(input("q must be a prime number. Try again: "))

        x = input("Enter text: ")
        n = p * q
        totient = (p - 1) * (q - 1)

        e = find_public_key(totient)
        public_key = (n, e)
        private_key = find_private_key(e, totient)
        encrypted_text = encrypt(x, public_key)
        print(f"Encrypted text: {encrypted_text}")
        save(encrypted_text, public_key)
        
    elif option.lower() == "d":
        ciphertext, public_key = read_file()
        n, e = public_key
        p, q = find_primes(n)
        totient = (p - 1) * (q - 1)
        private_key = find_private_key(e, totient)
        decrypted_text = decrypt(ciphertext, private_key, n)
        print(f"Decrypted text: {decrypted_text}")

if __name__ == "__main__":
    main()