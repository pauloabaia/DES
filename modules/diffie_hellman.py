import random  # Importa a biblioteca para geração de números aleatórios

'''
Parâmetros globais usados no Diffie-Hellman:
1. q = Número primo grande
2. a = Raiz primitiva de q

Lógica do protocolo Diffie-Hellman:
1. A chave privada é um número aleatório (chamado x).
2. A chave pública é gerada pela fórmula: (a^x) mod q
3. A chave compartilhada entre duas partes é: (Chave Pública de B) ^ (Chave Privada de A) mod q
'''


def criarNumeroPrimo(menor_limite, limteSuperior):
    '''
    Função utilitária para gerar um número primo grande dentro de um intervalo.
    
    Entrada:
    - lowerLimit: Limite inferior do intervalo
    - upperLimit: Limite superior do intervalo

    Saída:
    - Um número primo escolhido aleatoriamente dentro do intervalo dado
    '''
    p = 2
    # Certifica-se de que o limite superior seja no mínimo 2 (pois 2 é o menor primo)
    limteSuperior = max(limteSuperior, 2)
    # Cria uma lista para verificar a primalidade dos números usando o crivo de Eratóstenes
    primos = [False] * 2 + [True] * (limteSuperior - 1)
    # Verifica a primalidade de todos os números até o limite superior
    while (p ** 2 < limteSuperior):
        if primos[p]:
            # Marca os múltiplos de p como não primos
            for i in range(p ** 2, limteSuperior + 1, p):
                primos[i] = False
        p += 1

    # Retorna um número primo aleatório dentro dos limites
    result = [i for i, check in enumerate(primos) if check and i > menor_limite]
    return random.choice(result)  # Escolhe um número primo aleatório da lista


def raiz_primitivadoprimo(q, reverse=False):
    '''
    Função que encontra uma raiz primitiva de um número primo q.
    A raiz primitiva de um número primo gera todos os restos possíveis
    quando suas potências são calculadas módulo q.

    Exemplo:
    Para q = 7, uma raiz primitiva pode ser o número 3.
    Potências de 3 modulo 7 geram todos os restos: 1, 2, 3, ..., 6.
    
    Entrada:
    - q: O número primo para o qual queremos encontrar a raiz primitiva.
    - reverse: Se verdadeiro, a busca começa em ordem decrescente.

    Saída:
    - A raiz primitiva de q, ou None se q não for primo.
    '''
    if eh_primo(q):  # Verifica se q é primo
        teste = set()  # Armazena os restos gerados
        # Gera uma lista de possíveis raízes primitivas
        pos = [x for x in range(2, q)]
        if reverse:
            # Inverte a lista se a busca for em ordem decrescente
            pos = pos[::-1]

        for num in pos:
            for i in range(1, q):
                val = (num ** i) % q  # Calcula a potência de num modulo q
                if val in teste:  # Se o valor já foi gerado, não é uma raiz primitiva
                    teste = set()  # Reinicia o teste para o próximo número
                    break
                else:
                    teste.add(val)  # Adiciona o valor gerado ao conjunto

                if len(teste) == q - 1:  # Se todos os restos forem gerados, num é uma raiz primitiva
                    return num
    else:
        print("O número inserido não é primo: Não há raiz primitiva")
        return None


def gerarSegredo_e_chavepublica(numero, raiz_primitiva, segredoLimite=101):
    '''
    Gera a chave privada e a chave pública com base nos parâmetros globais.
    
    Entrada:
    - numero: O número primo grande (q)
    - raiz_primitiva: A raiz primitiva de q
    - segredoLimite: Limite superior opcional para o valor da chave privada

    Saída:
    - Chave privada (número aleatório dentro do limite)
    - Chave pública, calculada como (raiz_primitiva ^ segredo)) % numero
    '''
    segredoLimite = max(
        segredoLimite, 101)  # Define o limite mínimo para a chave privada
    # Gera a chave privada aleatoriamente
    segredo = random.randint(segredoLimite - 100, segredoLimite)
    public = (raiz_primitiva ** segredo) % numero  # Calcula a chave pública
    return (segredo, public)  # Retorna as chaves privada e pública


def calcularChaveCompartilhada(PK_outro, meu_segredo, numero_q):
    '''
    Calcula a chave compartilhada entre duas partes no Diffie-Hellman.
    
    Entrada:
    - PK_outro: A chave pública da outra parte
    - meu_segredo: A chave privada da parte atual
    - numero_q: O número primo grande (q)

    Saída:
    - A chave compartilhada calculada como (PK_outro ^ meu_segredo) % number
    '''
    return (PK_outro ** meu_segredo) % numero_q


def eh_primo(number):
    '''
    Verifica se um número é primo. A segurança do Diffie-Hellman
    depende da escolha de um número primo grande.
    
    Entrada:
    - number: O número a ser verificado

    Saída:
    - True se o número for primo, False caso contrário
    '''
    for i in range(2, int(number ** 0.5) + 1):  # Itera até a raiz quadrada de 'number'
        if number % i == 0:  # Se o número for divisível por i, não é primo
            return False
    return True  # Retorna True se não houver divisores


if __name__ == '__main__':
    # Parâmetros globais do Diffie-Hellman
    # Número de bits do primo grande (usaremos um primo pequeno para teste)
    tanhoNPrimo = 16
    q = criarNumeroPrimo(1000, 5000)  # Gera um número primo grande
    print(f"Número primo gerado (q): {q}")

    a = raiz_primitivadoprimo(q)  # Gera uma raiz primitiva de q
    print(f"Raiz primitiva de q (a): {a}")

    # Parte A (Emissor)
    # Gera a chave privada e pública de A
    a_private, a_public = gerarSegredo_e_chavepublica(q, a)
    print(f"Chave privada de A: {a_private}")
    print(f"Chave pública de A: {a_public}")

    # Parte B (Receptor)
    # Gera a chave privada e pública de B
    b_private, b_public = gerarSegredo_e_chavepublica(q, a)
    print(f"Chave privada de B: {b_private}")
    print(f"Chave pública de B: {b_public}")

    # Cálculo da chave compartilhada
    a_chave_compartilhada = calcularChaveCompartilhada(
        b_public, a_private, q)  # Chave compartilhada por A
    b_chave_compartilhada = calcularChaveCompartilhada(
        a_public, b_private, q)  # Chave compartilhada por B

    print(f"Chave compartilhada calculada por A: {a_chave_compartilhada}")
    print(f"Chave compartilhada calculada por B: {b_chave_compartilhada}")

    # Verifica se ambas as chaves compartilhadas são iguais
    assert a_chave_compartilhada == b_chave_compartilhada, "Erro: As chaves compartilhadas não correspondem!"
    print("Chaves compartilhadas coincidem! A troca de chaves foi bem-sucedida.")
