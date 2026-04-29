import rsa
import des
import aes
import sys

def get_valid_prime(prompt):
    while True:
        try:
            p = int(input(prompt))
            if rsa.is_prime(p):
                return p
            print(f" {p} isn't prime. Try another one.")
        except:
            print("enter a valid  integer, please.")

def show_menu():
    print("\n" + "="*40)
    print("      CRYPTOGRAPHY CONSOLE")
    print("="*40)
    print("1) Encrypt")
    print("2) Decrypt")
    print("3) Quit")
    return input("Choice: ")

def run_encryption():
    text = input("\nWhat's the secret message? ")
    
    print("\n--- RSA Encryption ---")
    print("We need two primes where p * q > 255...")
    while True:
        p = get_valid_prime("Enter prime p: ")
        q = get_valid_prime("Enter prime q: ")
        if p * q > 255: break
        print(f"Product is only {p*q}, needs to be > 255. Try larger primes.")
    
    pub, priv = rsa.generate_keys(p, q)
    rsa_cipher = rsa.encrypt(text, pub)
    print(f"Done! Keys: Pub={pub}, Priv={priv}")
    print(f"RSA Ciphertext: {rsa_cipher}")
    
    print("\n--- DES Encryption ---")
    while True:
        dk = input("Enter 8-char DES key: ")
        if len(dk) == 8: break
        print("Key must be exactly 8 characters!")
    des_bits = des.des_encrypt(text, dk)
    d_hex = "".join([hex(int("".join(map(str, des_bits[i:i+4])), 2))[2:] for i in range(0, len(des_bits), 4)])
    print(f"DES Hex: {d_hex}")
    
    print("\n--- AES-128 Encryption ---")
    while True:
        ak = input("Enter 16-char AES key: ")
        if len(ak) == 16: break
        print("Key must be exactly 16 characters!")
    aes_bytes = aes.encrypt_aes(text, ak)
    a_hex = "".join(format(x, '02x') for x in aes_bytes)
    print(f"AES Hex: {a_hex}")

def run_decryption():
    print("\nWhich algorithm do you want to decrypt with?")
    print("1. RSA\n2. DES\n3. AES")
    choice = input("Choice: ")
    
    if choice == "1":
        cipher_str = input("Paste the RSA ciphertext list: ")
        d_val = int(input("Enter private exponent 'd': "))
        n_val = int(input("Enter modulus 'n': "))
        print(f"Decrypted: {rsa.decrypt(eval(cipher_str), (d_val, n_val))}")
        
    elif choice == "2":
        h = input("Paste the DES Hex: ")
        k = input("Enter 8-char key: ")
        b = []
        for char in h:
            b.extend([int(x) for x in format(int(char, 16), '04b')])
        print(f"Decrypted: {des.des_decrypt(b, k)}")
        
    elif choice == "3":
        h = input("Paste the AES Hex: ")
        k = input("Enter 16-char key: ")
        b = list(bytes.fromhex(h))
        print(f"Decrypted: {aes.decrypt_aes(b, k)}")

if __name__ == "__main__":
    while True:
        cmd = show_menu()
        if cmd == "1":
            run_encryption()
        elif cmd == "2":
            run_decryption()
        elif cmd == "3":
            break
        else:
            print("Not an option, try again.")
