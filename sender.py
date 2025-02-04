#parâmetros públicos
n = 47  # numero primo 
g = 3   # gerador/base 

# Alice escolhe seu número secreto e calcula a chave pública
alice_secret = 8
alice_public = (g ** alice_secret) % n

print(f"Chave pública de Alice: {alice_public}")

# Alice recebe a chave pública de Bob
bob_public = int(input("Digite a chave pública de Bob recebida: "))

# Alice calcula a chave secreta compartilhada
shared_secret = (bob_public ** alice_secret) % n
key = bin(shared_secret)[2:].zfill(64)[:64]  # Ajustando para 64 bits

print(f"Chave secreta compartilhada (64 bits): {key}")

# ---- Implementação do DES ----
def xor(bin1, bin2):
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bin1, bin2))

def feistel(right, subkey):
    return xor(right, subkey[:32])  # Feistel simplificado

def des_encrypt(plaintext, key):
    plaintext = bin(int.from_bytes(plaintext.encode(), 'big'))[2:].zfill(64)
    
    left, right = plaintext[:32], plaintext[32:]
    for _ in range(16):  
        new_right = xor(left, feistel(right, key))
        left, right = right, new_right  

    return hex(int(left + right, 2))[2:]

# Alice digita a mensagem e a cifra
mensagem = input("Digite a mensagem para enviar (máx. 8 caracteres): ")
cifrado = des_encrypt(mensagem.ljust(8), key)  # Garantindo 8 bytes

print(f"Mensagem cifrada enviada: {cifrado}")
