import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def get_mod_inverse(e, phi):
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("No modular inverse found!")
    return x % phi

def is_prime(num):
    if num < 2: return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_random_prime(min_val, max_val):
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p):
            return p



def generate_keys(p=None, q=None):
    p = p or find_random_prime(1000, 5000)
    q = q or find_random_prime(1000, 5000)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
            
    d = get_mod_inverse(e, phi)
    
    return (e, n), (d, n)

def encrypt(text, pub_key):
    e, n = pub_key
    return [(ord(c) ** e) % n for c in text]

def decrypt(cipher_list, priv_key):
    d, n = priv_key
    chars = [chr((val ** d) % n) for val in cipher_list]
    return "".join(chars)
