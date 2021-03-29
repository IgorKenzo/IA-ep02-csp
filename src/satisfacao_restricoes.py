class Restricao():
    def __init__(self, variaveis):
        self.variaveis = variaveis

    def esta_satisfeita(self, atribuicao):
      return True

class SatisfacaoRestricoes():
  def __init__(self, variaveis, dominios):
    self.variaveis = variaveis # Variáveis para serem restringidas
    self.dominios = dominios # Domínio de cada variável
    self.restricoes = {}
    for variavel in self.variaveis:
        self.restricoes[variavel] = []
        if variavel not in self.dominios:
            raise LookupError("Cada variávei precisa de um domínio")

  def adicionar_restricao(self, restricao):
    for variavel in restricao.variaveis:
      if variavel not in self.variaveis:
        raise LookupError("Variável não definida previamente")
      else:
        self.restricoes[variavel].append(restricao)

  def esta_consistente(self, variavel, atribuicao):
    for restricoes in self.restricoes[variavel]:
      if not restricoes.esta_satisfeita(atribuicao):
        return False
    return True
  
  def busca_backtracking(self, atribuicao = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]

    primeira_variavel = variaveis_nao_atribuida[0]
    for valor in self.dominios[primeira_variavel]:
      atribuicao_local = atribuicao.copy()
      atribuicao_local[primeira_variavel] = valor
      # estamos consistentes, seguir recursão
      if self.esta_consistente(primeira_variavel, atribuicao_local):
        resultado  = self.busca_backtracking(atribuicao_local)
        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None



class SatisfacaoRestricoesFowardChecking(SatisfacaoRestricoes):
  
  def forward_checking(self, variaveis_nao_atribuida, atribuicao_local, dominio_local):
    for var_nao_att in variaveis_nao_atribuida:
      dominio_novo = dominio_local[var_nao_att].copy()
      for opcao in dominio_local[var_nao_att]:
        atribuicao_local_2 = atribuicao_local.copy()
        atribuicao_local_2[var_nao_att] = opcao
        if not self.esta_consistente(var_nao_att, atribuicao_local_2):
          dominio_novo.remove(opcao)
        dominio_local[var_nao_att] = dominio_novo
      if len(dominio_local[var_nao_att]) == 0:
        return None
    print(f"{atribuicao_local_2} -> {dominio_local}")
    return dominio_local

  def busca_backtracking_foward_checking(self, atribuicao = {}, dominios = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # se dominio for vazio, pega o da classe, senão, usa o da recursão
    if dominios == {} :
      dominios = self.dominios
    
    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]

    primeira_variavel = variaveis_nao_atribuida[0]
    for valor in dominios[primeira_variavel]:
      atribuicao_local = atribuicao.copy()
      dominio_local = dominios.copy()
      variaveis_nao_atribuida_local = variaveis_nao_atribuida.copy()
      atribuicao_local[primeira_variavel] = valor
      
      # estamos consistentes, seguir recursão
      if self.esta_consistente(primeira_variavel, atribuicao_local):

        novo_dominio = self.forward_checking(variaveis_nao_atribuida_local, atribuicao_local, dominio_local)
        resultado = None
        if novo_dominio != None:
          resultado  = self.busca_backtracking_foward_checking(atribuicao_local, novo_dominio)
        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None
      