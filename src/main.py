from satisfacao_restricoes import Restricao, SatisfacaoRestricoes, SatisfacaoRestricoesFowardChecking

class RestricaoDiferentes(Restricao):
    def __init__(self, x1, x2, x3, x4):
        super().__init__([x1, x2, x3, x4])
        self.variaveis = [x1, x2, x3, x4]

    def esta_satisfeita(self, atribuicao):
        # Não analise se todos os estados estiverem atribu;idos
        if not all(variavel in atribuicao for variavel in self.variaveis):
          return True
        # cores de estados vizinhos não podem ser igual
        valores = [atribuicao[variavel] for variavel in self.variaveis]
        return len(set(valores)) == 4


class RestricaoNaMesmaJaula(Restricao):
  def __init__(self, a1, a2, junto = False):
    super().__init__([a1, a2])
    self.variaveis = [a1, a2]
    self.junto = junto

  def esta_satisfeita(self, atribuicao):
        # Não analise se todos os estados estiverem atribu;idos
        if not all(variavel in atribuicao for variavel in self.variaveis):
          return True
        # verifica se estão na mesma jaula
        valores = [atribuicao[variavel] for variavel in self.variaveis]
        return (len(set(valores)) == len(valores)) != self.junto

class RestricaoAdjascente(Restricao):
  def __init__(self, a1, a2):
    super().__init__([a1, a2])
    self.variaveis = [a1, a2]

  def esta_satisfeita(self, atribuicao):
        # Não analise se todos os estados estiverem atribu;idos
        if not all(variavel in atribuicao for variavel in self.variaveis):
          return True
        # verifica se estão na mesma jaula
        #valores = [atribuicao[variavel] for variavel in self.variaveis]
        return abs(atribuicao[self.variaveis[0]] - atribuicao[self.variaveis[1]]) > 1

class RestricaoPreferenciaJaula(Restricao):
  def __init__(self, a1, numJaula):
    super().__init__([a1])
    self.variaveis = [a1]
    self.numJaula = numJaula

  def esta_satisfeita(self, atribuicao):
    # Não analise se a variavel esta atribuida
    if not self.variaveis[0] in atribuicao:
      return True
    
    #Verifica se a atribuição é a prefenrência da variavel
    return atribuicao[self.variaveis[0]] == self.numJaula

if __name__ == "__main__":
    variaveis = ["Leão",	"Antílope",	"Hiena",	"Tigre",	"Pavão",	"Suricato",	"Javali"]      
    dominios = {}
    for variavel in variaveis:
      dominios[variavel] = [1, 2, 3, 4]
    problema = SatisfacaoRestricoesFowardChecking(variaveis, dominios)

    #Restrição
    problema.adicionar_restricao(RestricaoPreferenciaJaula("Leão", 1))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Leão","Tigre"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Suricato","Javali", True))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Tigre","Suricato"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Tigre","Javali"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Tigre","Pavão"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Leão","Pavão"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Hiena","Leão"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Hiena","Antílope"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Hiena","Pavão"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Hiena","Suricato"))
    problema.adicionar_restricao(RestricaoNaMesmaJaula("Hiena","Javali"))
    problema.adicionar_restricao(RestricaoAdjascente("Antílope","Leão"))
    problema.adicionar_restricao(RestricaoAdjascente("Antílope","Tigre"))

    # print([v.__str__() + " -> " + len(problema.restricoes[v]).__str__() for v in problema.variaveis])

    
    #resposta = problema.busca_backtracking_foward_checking()
    # resposta = problema.busca_backtracking_foward_checking_MRV()
    resposta = problema.busca_backtracking_foward_checking_MCV()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    else:
        print(resposta)