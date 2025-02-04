#parâmetros públicos
n = 47  # numero primo 
g = 3   # gerador/base 

# Bob escolhe seu número secreto e calcula a chave pública
bob_secret = 10
bob_public = (g ** bob_secret) % n

print(f"Chave pública de Bob: {bob_public}")

# Bob recebe a chave pública de Alice
alice_public = int(input("Digite a chave pública de Alice recebida: "))

# Bob calcula a chave secreta compartilhada
shared_secret = (alice_public ** bob_secret) % n
key = bin(shared_secret)[2:].zfill(64)[:64]  # Ajustando para 64 bits

print(f"Chave secreta compartilhada (64 bits): {key}")

# ---- Implementação do DES ----
def xor(bin1, bin2):
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bin1, bin2))

def feistel(right, subkey):
    return xor(right, subkey[:32])  # Feistel simplificado

def des_decrypt(ciphertext, key):
    ciphertext = bin(int(ciphertext, 16))[2:].zfill(64)
    
    left, right = ciphertext[:32], ciphertext[32:]
    for _ in range(16):  
        new_right = xor(left, feistel(right, key))
        left, right = right, new_right  

    return int(left + right, 2).to_bytes(8, 'big').decode()

# Bob recebe a mensagem cifrada e a decifra
cifrado = input("Digite a mensagem cifrada recebida: ")
decifrado = des_decrypt(cifrado, key)

print(f"Mensagem decifrada: {decifrado.strip()}")
