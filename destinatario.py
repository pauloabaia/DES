import socket
import time
import string
from modules.diffie_hellman import criarNumeroPrimo, raiz_primitivadoprimo, gerarSegredo_e_chavepublica, calcularChaveCompartilhada
from modules.des import Algoritmo_DES

# Definindo o endereço e porta do remetente
Porta = 8001
IP = "127.0.0.1"

# Função para gerar uma chave para o algoritmo DES a partir da chave compartilhada


def criarchavesDes(p, q, chaveCompartilhada):
    '''
    Esta função gera uma chave de comprimento suficiente para o algoritmo DES,
    utilizando a chave compartilhada formada e os parâmetros globais (p e q).
    '''
    # Mapeamento de caracteres ASCII para os valores da chave
    mapping = {}
    for index, letra in enumerate(string.ascii_letters):
        mapping[index] = letra

    # Multiplica os valores para formar uma string base para gerar a chave
    val = str(chaveCompartilhada * p * q)

    # Converte para uma chave de caracteres a partir do mapeamento
    chave_final = []
    for index in range(0, len(val), 2):
        chave_final.append(mapping[int(val[index:index + 1]) % len(mapping)])

    # Garante que a chave tenha pelo menos 8 caracteres
    while len(chave_final) < 8:
        chave_final += chave_final

    # Retorna a chave final com tamanho apropriado
    return "".join(chave_final[:8])


def main():
    # Criando o socket do servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP, Porta))
    servidor.listen(1)  # Máximo de 1 conexão aguardando

    # Estabelecendo a conexão com o cliente
    print("Aguardando conexão do cliente...")
    client_sock, address = servidor.accept()  # Aceita a conexão do cliente
    print(client_sock.recv(4096).decode())  # Exibe a mensagem de conexão

    # Definindo os parâmetros globais (p e q)
    p = criarNumeroPrimo(1000, 2000)  # Gerando um número primo grande
    q = raiz_primitivadoprimo(p, True)  # Raiz primitiva do número primo

    print("Enviando parâmetros globais para o cliente...\n")
    client_sock.send(str(p).encode())
    time.sleep(2)  # Pausa para garantir sincronização
    client_sock.send(str(q).encode())

    # Gerando o par de chaves pública-privada para o servidor
    privateServer, publicServer = gerarSegredo_e_chavepublica(p, q)
    time.sleep(2)

    # Enviando a chave pública do servidor para o cliente
    client_sock.send(str(publicServer).encode())

    # Recebendo a chave pública do cliente
    publicClient = int(client_sock.recv(4096).decode())

    time.sleep(2)

    # Gerando a chave compartilhada e convertendo-a para chave do DES
    key = int(str(calcularChaveCompartilhada(publicClient, privateServer, p)), 16)
    DES_key = criarchavesDes(p, q, key)
    
    # Loop de recepção de mensagens
    while True:
        # Recebe mensagem criptografada
        mensagem_atual = client_sock.recv(4096).decode()
        # Descriptografa a mensagem
        mensagem = Algoritmo_DES(texto_plano=mensagem_atual,
                                chave=DES_key, encrypt=False).DES()

        # Verifica se a mensagem não é vazia, o que encerraria a comunicação
        if mensagem != "":
            # Exibe a mensagem criptografada
            print(f"Mensagem criptografada recebida transformada em hexadecimal: {mensagem_atual.encode().hex()}")
            # Exibe a mensagem descriptografada
            print(f"Mensagem descriptografada: {mensagem}\n")
        else:
            client_sock.close()  # Fecha a conexão ao receber a mensagem vazia
            break


if __name__ == '__main__':
    main()
