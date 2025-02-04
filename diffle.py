
#parâmetros públicos
n = 47  # numero primo 
g = 3   # gerador/base 

#Alice setUp
aliceSegredo = 8  #escolhido por Alice (num inteiro)
aliceChavePublica = (g ** aliceSegredo) % n  #chave pública de Alice 
    
#Bob SetUp
bobSegredo = 10  # Escolhido por Bob (num inteiro)
bobChavePublica = (g ** bobSegredo) % n  #chave pública de Bob 

#chave secreta compartilhada usando a chave pública de Bob (Alice)
aliceSegredoCompartilhado = (bobChavePublica ** aliceSegredo) % n

#chave secreta compartilhada usando a chave pública de Alice (Bob)
BobSegredoCompartilhado = (aliceChavePublica ** bobSegredo) % n

# Ambas as chaves devem ser iguais
if aliceSegredoCompartilhado == BobSegredoCompartilhado:
 print("Chave secreta compartilhada:",aliceSegredoCompartilhado)# Exibe o resultado
else:
 print("Erro")

