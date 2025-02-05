import socket
import time
import string
from modules.diffie_hellman import gerarSegredo_e_chavepublica, calcularChaveCompartilhada
from modules.des import Algoritmo_DES

# Definindo o endereço e porta do servidor ao qual vamos nos conectar
portaDestinatario = 8001
ipDestinatario = "127.0.0.1"

# Função para gerar uma chave para o algoritmo DES a partir da chave compartilhada


def gerarChavesparaoDes(p, q, a):
    '''
    Esta função gera uma chave de comprimento suficiente para o algoritmo DES,
    utilizando a chave compartilhada formada e os parâmetros globais (p e q).
    '''
    # Mapeamento de caracteres ASCII para os valores da chave
    mapping = {}
    for index, letter in enumerate(string.ascii_letters):
        mapping[index] = letter

    # Multiplica os valores para formar uma string base para gerar a chave
    val = str(a * p * q)

    # Converte para uma chave de caracteres a partir do mapeamento
    finalKey = []
    for index in range(0, len(val), 2):
        finalKey.append(mapping[int(val[index:index + 1]) % len(mapping)])

    # Garante que a chave tenha pelo menos 8 caracteres
    while len(finalKey) < 8:
        finalKey += finalKey

    # Retorna a chave final com tamanho apropriado
    return "".join(finalKey[:8])


def main():
    # Criando o socket do cliente
    remetente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Estabelecendo a conexão com o servidor
    print("Estabelecendo conexão com o servidor...")
    remetente.connect((ipDestinatario, portaDestinatario))
    remetente.send("Conectado!".encode())  # Envia uma mensagem inicial
    print("Conectado!")

    # Recebendo os parâmetros globais p (número primo) e q (raiz primitiva)
    p = int(remetente.recv(4096).decode())
    q = int(remetente.recv(4096).decode())

    print(f"Número primo grande: {p}")
    print(f"Raiz primitiva: {q}\n")

    # Gerando o par de chaves pública-privada para o cliente
    segredoRemetente, publicoRemetente = gerarSegredo_e_chavepublica(p, q)
    time.sleep(2)  # Pausa para garantir sincronização

    # Recebendo a chave pública do servidor
    param_publico_destinatario = int(remetente.recv(4096).decode())

    # Enviando a chave pública do cliente para o servidor
    remetente.send(str(publicoRemetente).encode())

    time.sleep(2)

    # Gerando a chave compartilhada e convertendo-a para chave do DES
    key = int(str(calcularChaveCompartilhada(param_publico_destinatario, segredoRemetente, p)), 16)
    DES_key = gerarChavesparaoDes(p, q, key)
    
    print("Quando quiser encerrar a comunicação, envie uma mensagem vazia!\n")

    # Loop de envio de mensagens
    while True:
        mensagem = input("Digite sua mensagem: ")  # Entrada de mensagem do usuário
        print("\n")

        # Criptografando a mensagem com o DES
        mensagemCifrada = Algoritmo_DES(
            texto_plano=mensagem, chave=DES_key, encrypt=True).DES()
        # Envia a mensagem criptografada
        remetente.send(mensagemCifrada.encode())

        if mensagem == "":
            time.sleep(2)
            remetente.close()  # Fecha a conexão ao mandar mensagem vazia
            break


if __name__ == '__main__':
    main()
