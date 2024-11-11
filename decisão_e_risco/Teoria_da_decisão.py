# Teoria da decisão existe para facilitar decisão. Esta necessita de ser facilitada devido à quantidade de informação
# complexa que é necessário entender:
# Múltiplos objectivos como minimizar custos, maximizar a satisfação e entre outros
# Estrutura complexa entre alternativas, outros pontos de vista/decisores/objectivos
# Mais do que uma decisão em simultâneo pode ser necessário, pelo que podemos enfrentar menos informação ou
# não tomar em conta as tomadas anteriormente, ou mesmo a influência de uma a ser tomada no resultado de outra

# Este apoio à decisão é feito através da decomposição do problema envolto na decisão em subproblemas,
# com o auxílio de presunções e agregação de decisões sobre os subproblemas, providenciando mecanismos
# formais para tal
# Para além disso, tudo isto garante uma melhor clarificação dos factores decisivos, racionalização do
# problema, justificação fundamentada sobre a decisão e esquemas de análise que definem o nível de abstração
# removendo subjectividades e resolução de conflitos

# Decisão uni-atributo - escolher melhor estratégia com base num conjunto de acontecimentos possíveis
# segundo um determinado ponto de vista. Dois tipos:
# Em situação de incerteza | Em situação de risco

# SITUAÇÃO DE INCERTEZA
# matrix de decisão

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

estrategias = ["A", "B", "C", "D", "E"]
estadosDaNaturezaouAcontecimentos = ["Acontecimento1", "Acontecimento dois", "etc."]
# matrizDeDecisão = valores_resultantes_estrategias_por_acontecimento

# Situação de incerteza - não se deseja ou não é possível saber as probabilidades de ocorrência de
# cada acontecimento
# Ex
estrategias_nova_boneca_lola = ["Lola Rave", "Tia Lola", "O iate da Lola", "Lola Bond"]
tipo_de_procura = estrategias
matriz_decisao = np.array([[35, 30, 20, 10, -15],
                           [30, 50, 25, -20, -10],
                           [-40, 60, 20, -15, 75],
                           [-60, -30, 10, 50, 100]])

matriz_decisao_final = pd.DataFrame(matriz_decisao, estrategias_nova_boneca_lola, tipo_de_procura)
criterio_pessimista = matriz_decisao_final.min(axis=1).rename(
    "Pessimista")  # também conhecido como de wald ou maximin -
criterio_pessimista.idxmax()  # decide com base no máximo do mínimo - conservadores e
# avessos ao risco

criterio_otimista = matriz_decisao_final.max(axis=1).rename("Otimista")  # também conhecido como de Hurwicz ou Maximax
criterio_otimista.idxmax()  # decide com base no máximo do retorno máximo
# decisores propensos ao risco (risco é bom se maiores
# retornos

criterio_savage = pd.concat([criterio_pessimista, criterio_otimista], axis=1)


def criterio_savage_func(x, rowSavageDataframe):
    return rowSavageDataframe["Pessimista"] + (rowSavageDataframe["Otimista"] - rowSavageDataframe["Pessimista"]) * x


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
colors = ['red', 'blue', 'orange', ]
x = np.linspace(criterio_pessimista.min(), criterio_otimista.max(), 10000)
for produto in criterio_savage.index:
    plt.plot(x, criterio_savage_func(x, criterio_savage.loc[produto]))
    plt.show()

plt.close()
# decisão é variada consoante a análise do máximo valor de retorno ao longo das funções e a sua relação
# com o tipo de decisor

criterio_equiprovavel = matriz_decisao_final.mean(axis=1)  # ou de laplace -
criterio_equiprovavel.idxmax()  # assume-se equiprobabilidade entre tipos de procura (acontecimentos)
# decisão realizada consoante maior média

criterio_custo_oportunidade = matriz_decisao_final.max(axis=0) - matriz_decisao_final
criterio_custo_oportunidade = criterio_custo_oportunidade.max(axis=1)
criterio_custo_oportunidade.idxmin()
# maximo de cada coluna(acontecimento) - o valor para cada acontecimento numa dada estratégia - custo de oportunidade
# estratégia é escolhida com base no mínimo do máximo custo de oportunidade
# para cada acontecimento


# SITUAÇÃO DE RISCO
# sabido a priori as probabilidades (pelo menos aproximadamente)
# de cada um dos acontecimentos/estados da natureza

probAcontecimentos = pd.Series([0.1, 0.2, 0.4, 0.25, 0.05], index=estrategias)  # ou de Bayes
criterio_valor_esperado = matriz_decisao_final.multiply(probAcontecimentos, axis=1)
criterio_valor_esperado.sum(axis=1).idxmax()  # máximo da soma das probabilidades condicionais do acontecimento * valor
# de uma estratégia nesse acontecimento (soma dos valores condicionais de retorno)
# assume que a situação se repetirá um elevado número de vezes, garantindo a aproximação
# com o valor obtido - pode ser erróneo por levar-nos à assunção de que
# um retorno maior com probabilidade reduzida e perdas elevadas com maior
# probabilidade de ocorrência é preferível, ainda que estas probabilidades
# se encontrem naturalmente contra nós

# VALOR ESPERADO DA INFORMAÇÃO PERFEITA
criterioVEIP = criterio_valor_esperado.max(axis=1).sum(axis=0)
# comparação com informação imperfeita
criterio_valor_esperado.sum(axis=1).idxmax()
# valor esperado da informação perfeita :
VEIP = criterioVEIP - criterio_valor_esperado

"""Função de utilidade considera relevância de risco no apoio à decisão
atribui-se um valor de 0 a 1 (Utilidade) à melhor possibilidade (1)
e à pior possibilidade (0):"""

ganhos = pd.Series([60, 30, 11, -10])
utilidade = pd.Series([1, None, None, 0])
tabela = pd.concat([ganhos, utilidade], names=["Ganho", "Utilidade"], axis=1)

"""Para atribuir valor de Utilidade aos valores de ganhos intermédios,
terá que se recorrer a um dos seguintes métodos:"""
tabela.columns = ["Ganho", "Utilidade"]


# MÉTODO DA EQUIVALENCIA PROBABILISTICA
# Proponha-se ao decisor que se opte entre jogar um jogo em que se pode
# receber o pior e o melhor valor, com determinadas probabilidades,ou
# receber um certo valor (se prefere arriscar receber um dado valor por
# receber outro superior(máximo) podendo receber um inferior(mínimo)


def metodoEquivalenciaProbabilisticaPasso1(ganhoUtilidadeaEstimar, tabelaUtilidade):
    prob_superior = 0.70
    prob_inferior = 0.30
    while 1 == 1:
        decisao = input(
            "Probabilidade de ganhar " + str(tabelaUtilidade.head(1)["Ganho"].sum()) + "€ : " + str(prob_superior) + \
            "\ne probabilidade de ganhar " + str(tabelaUtilidade.tail(1)["Ganho"].sum()) + "€ : " + str(prob_inferior) + \
            ".\nDecide arriscar, ficar com os " + str(
                ganhoUtilidadeaEstimar) + "€, ou está indeciso? (Responda 1,2 ou 3)")
        if decisao == "1":
            prob_superior += 0.05
            prob_inferior -= 0.05
        elif decisao == "2":
            prob_superior -= 0.05
            prob_inferior += 0.05
        elif decisao == "3":
            return prob_superior
        else:
            return "Tem de responder 1 ou 2"


for element in tabela[tabela["Utilidade"].isnull()]["Ganho"]:
    tabela.loc[tabela["Ganho"] == element, "Utilidade"] = metodoEquivalenciaProbabilisticaPasso1(element, tabela)

# ajustam-se as probabilidades entre hipotese a(ganho certo) e b
# até decisão ficar 50/50. o valor de utilidade é igual à probabilidade
# de ganhar o melhor valor

# depois de todas as Utilidades serem atribuidas, determina-se a utilidade esperada de cada um dos jogos
# utilidade esperada = probabilidade hipotese * sua utilidade
jogo_1 = pd.DataFrame([[30, 0.6], [11, 0.4]], columns=["Ganho", "Probabilidade"])
jogo_2 = pd.DataFrame([[60, 0.5], [-10, 0.5]], columns=["Ganho", "Probabilidade"])

tabelaUtilidadeProbabilidadeJogo1 = tabela.merge(jogo_1, how='inner', on='Ganho')
tabelaUtilidadeProbabilidadeJogo2 = tabela.merge(jogo_2, how='inner', on='Ganho')

utilidadeEsperadajogo1 = tabelaUtilidadeProbabilidadeJogo1["Utilidade"] * tabelaUtilidadeProbabilidadeJogo1[
    "Probabilidade"]
utilidadeEsperadajogo1 = utilidadeEsperadajogo1.sum()

utilidadeEsperadajogo2 = tabelaUtilidadeProbabilidadeJogo2["Utilidade"] * tabelaUtilidadeProbabilidadeJogo2[
    "Probabilidade"]
utilidadeEsperadajogo2 = utilidadeEsperadajogo2.sum()

# Método da Equivalência em Situação de Certeza
# método anterior obriga a fazer juízos de valor demasiado complexos, tornando a sua execução difícil
# este método permite apresentar questões simplificadas:

# 1 - Propõe que se proponha ao decisor uma lotaria com dois resultados equiprováveis (melhor e pior)

tabelasituacaocerteza = pd.concat([tabela.head(1), tabela.tail(1)])


def lotaria1(tabela_ganhos):
    prob = 0.5
    ponto_utilidade = int(input(
        "A probabilidade de ganhar " + str(tabela_ganhos["Ganho"].max()) + "ou " + str(tabela_ganhos["Ganho"].min()) + \
        "é : \n" + str(prob) + ". \nQuanto é que está disposto a pagar para jogar?"))
    tabela_ganhos = tabela_ganhos.append({"Ganho": ponto_utilidade, "Utilidade": prob}, ignore_index=True)
    return tabela_ganhos.sort_values(by=["Utilidade"], ascending=False, ignore_index=True)


def lotaria2(tabela_ganhos):
    prob = 0.5
    ponto_utilidade = int(input(
        "A probabilidade de ganhar " + str(tabela_ganhos["Ganho"].max()) + "ou " + str(tabela_ganhos["Ganho"].iloc[1]) + \
        "é : \n" + str(prob) + ". \nQuanto é que está disposto a pagar para jogar?"))
    utilidade = 0.75
    tabela_ganhos = tabela_ganhos.append({"Ganho": ponto_utilidade, "Utilidade": utilidade}, ignore_index=True)
    return tabela_ganhos.sort_values(by=["Utilidade"], ascending=False, ignore_index=True)


def lotaria3(tabela_ganhos):
    prob = 0.5
    ponto_utilidade = int(input(
        "A probabilidade de ganhar " + str(tabela_ganhos["Ganho"].iloc[2]) + "ou " + str(tabela_ganhos["Ganho"].min()) + \
        "é : \n" + str(prob) + ". \nQuanto é que está disposto a pagar para jogar?"))
    utilidade = 0.25
    tabela_ganhos = tabela_ganhos.append({"Ganho": ponto_utilidade, "Utilidade": utilidade}, ignore_index=True)
    return tabela_ganhos.sort_values(by=["Utilidade"], ascending=False, ignore_index=True)


tabelasituacaocerteza = lotaria1(tabelasituacaocerteza)
tabelasituacaocerteza = lotaria2(tabelasituacaocerteza)
tabelasituacaocerteza = lotaria3(tabelasituacaocerteza)


def calculoUtilidadeValoresIntermedios(ganhoAUtilizar, tabela_ganhos):
    valoresAcima = tabela_ganhos[tabela_ganhos["Ganho"] >= ganhoAUtilizar]
    valoresAbaixo = tabela_ganhos[tabela_ganhos["Ganho"] <= ganhoAUtilizar]
    valorAcima = valoresAcima["Ganho"].min()
    valorAbaixo = valoresAbaixo["Ganho"].max()
    utilidadeAcima = valoresAcima["Utilidade"].min()
    utilidadeAbaixo = valoresAbaixo["Utilidade"].max()
    if valorAbaixo != valorAcima:
        utilidadevalor = (((ganhoAUtilizar - valorAbaixo) / (valorAcima - valorAbaixo)) * (
                utilidadeAcima - utilidadeAbaixo)) \
                         + utilidadeAbaixo
        tabela_ganhos = tabela_ganhos.append({"Ganho": ganhoAUtilizar, "Utilidade": utilidadevalor}, ignore_index=True)
        return tabela_ganhos.sort_values(by=["Utilidade"], ascending=False, ignore_index=True)

# Função utilidade é dependente do tipo de decisor, pelo que a sua curva(ou falta de) terá uma forma
# associada ao tipo de decisor
# Alguns autores sugerem apenas utilizar funções de utilidade em situações em que o risco é a maior preocupação
# do Decisor (ou seja, avessos ao Risco) - noutros casos, só se recomenda funções de valor


# PROCESSO DECISÃO MULTI CRITÉRIO
# processo de decisão pode envolver obtetivos antagónicos -  Q como resolver?
# R 1 - Dividir o problema em subproblemas
# 2 - agregar soluções de subproblemas sobre única medida
# 3 - tomar decisão com base no resultado de 2
# TÉCNICA S(imple)M(ulti)A(trribute)R(ating)T(echnique) - proposta por Edwards 1971
# conceitos :
# objectivo/ponto de vista - desejos dos decisores (pontos a satisfazer), indicando o sentido de preferencia
# alternativas - soluções possíveis
# atributo - medida de avaliação de alternativas face aos objetivos
# (que componentes levam no sentido de satisfação dos objectivos)
# critério - atributo convertido a uma escala numérica
# exige diálogo constante entre analista e decisor
# produz soluções robustas
# baseia-se num conjunto de axiomas que não são necessariamente factuais
# simplicidade pode não refletir correctamente problemas mais complexos
# METODOLOGIA:
# 1- Identificação dos decisores
# 2- Identificação das alternativas
# 3- Identificação dos objetivos e alternativas respectivas
# 4- Avaliação do desempenho de cada alternativa com base nos atributos
# 5- Conversão de atributos a critérios
# 6- Análise de Dominâncias
# 7- Determinação de peso para cada critério de forma a estabelecer importância relativa
# 8- Cálculo média ponderada dos critérios por alternativa
# 9- Realização de uma análise de sensibilidade para avaliar a robustez
#       da alternativa resultante(TRIDENT)

# Identificação dos atributos : Árvores de valor

#Conversão de objectivos a uma escala - dois métodos
#1 Escala qualitativa (ex. de Muito Fraco a Muito Forte / de Muito Mau a Muito Bom)
#2 Direct Rating
    # DIRECT RATING
    #Solicitar ao decisor que ordene as alternativas por ordem decrescente em relação
    #ao atributo -> Atribui-se pontuação 100 à melhor e 0 à pior -> pede-se ao decisor
    #que pontue as restantes a partir da penúltima, dividindo pelo valor máximo da pontuação
    #realizada por este e multiplicando por 100.
    #Nota: Direct Rating pode ser usado para converter método 1 em escala numérica

#FUNÇÕES DE VALOR - funções aplicadas a atributos quantitativos de forma a efetivamente
#associar as diferenças entre alternativas com o valor subjetivo dado ao atributo pelo
#decisor
#1 - ASSUME-SE TODAS AS ALTERNATIVAS ESTÃO DISPONÍVEIS, AVALIAÇÃO DESTAS É UM PROCESSO
#DETERMINISTICO
#Duas opções :
#1 Utilizar pontuações das alternativas - novas alternativas a posteriori obrigam ao
#recalculo

valor_melhor_alternativa = 100
valor_pior_alternativa = 0
#2 Utilizar bitola externa ao problema - encontra-se os valores no extremo do atributo que o decisor
#que o decisor ainda está interessado em pagar - exige juízos de valor mas não recálculo
pior_nivel_atributo = 30
#então
valor_de_30 = 0
melhor_nivel_atributo = 180
#então
valor_de_180 = 100

#PARA OS NÍVEIS INTERMÉDIOS - MÉTODO DE BISSECÇÃO
#solicita-se ao decisor que indique qual o valor (aprox. ou não) que corresponde ao meio
#termo. Atribui-se a este o valor 50. De seguida procuram-se os pontos 25 e 75, e depois
#os valores das alternativas por interpolação linear

#OU ENTÃO FUNÇÕES DE VALOR PRÉ ESTABELECIDAS
#SE CRESCENTE
def v_cresc(tabela,x,alpha):
    v = ((tabela.max() - x) / (tabela.max() - tabela.min()))**alpha
    return v

def v_decresc(tabela,x,alpha):
    v = ((x - tabela.min()) / (tabela.max() - tabela.min()))**alpha
    return v

#2- NÃO SE ASSUME COMPLETA DISPONIBILIDADE E AVALIAÇÃO DETERMINISTICA DE 1 - SITUAÇÃO DE RISCO
#NESTE CASO SERÁ VALIOSO SUBSTITUIR A FUNÇÃO DE VALOR POR UMA DE UTILIDADE

#ANALISE DE DOMINANCIA
#Permite descartar alternativas do processo de decisão que nunca poderão ser as melhores
#alternativas dominadas - outras alternativas são melhores em todos os critérios
#removem-se do processo de decisão completamente

#DETERMINAÇÃO HIERARQUIA DE CRITÉRIOS
#TÉCNICA DE SWING WEIGHTS
#Consiste em:
    #1 Ordenar os critérios (desc)
    #2 Considerar primeiro com peso 1
    #3 Apresentam-se alternativas ficticias ao decisor (A e B) em tudo iguais, excepto:
    #A tem 100 no melhor critério (o de peso 1) e 0 nos restantes
    #B tem 100 no critério em análise e 0 no resto;
    #e requer-se que decida até que nível estará interessado na opção B.
    #4 Normalizam-se os pesos (para se conterem entre 0 e 1)
    #5 Realiza-se a média ponderada dos vários critérios por alternativa
    #6 Determina-se a melhor alternativa como a alternativa com maior média ponderada

#ANÁLISE DE SENSIBILIDADE - TÉCNICA TRIDENT
#Permite uma análise de sensibilidade simultânea de três critérios
#valor alternativa = pesocritério1 * valorcritério1 + pesocritério1 * valorcritério1 + pesocritério2 * valorcritério2
# + pesocritério3 * valorcritério3 (peso total = 1)
#utilizando esta função de valor, traçam-se retas de indiferença (entre duas alternativas,
#encontra-se as combinações de pesos que permitam igualar o valor) -
#valor alternativa 1 = valor alternativa 2
# n alternativas - combinações de n a cada 2 retas de indiferença

#Permite descobrir :
#solução escolhida de acordo com pesos
#ordenação de acordo com pesos
#combinação de k alternativas nos primeiros k lugares
#robustez da solução adoptada
# Decidibilidade: O Decisor é sempre capaz de tomar uma
# decisão face a uma questão com duas opções;
# Transitividade: Se o Decisor preferir A a B, e preferir B a C,
# então prefere A a C
# Soma: Se o Decisor preferir A a B, e preferir B a C, então a
# intensidade da preferência de A, relativamente a C, é
# superior à intensidade das preferências de A, relativamente
# a B, e de B, relativamente a C
# Solvabilidade: (Método da Bisecção) Dado um critério, o pior e
# o melhor caso, o valor intermédio é uma opção válida para o
# Decisor
# Limites Finitos: Os limites para a função de Valor são finitos
# (para poderem ser convertidos a [0,100]

#MÉTODOS EL(imination)E(t)C(hoix)T(raduisant la)RE(alité)
#Existem vários que se baseiam na mesma filosofia
#Abordagem não compensatória (alternativa com um critério muito bom não compensa critério muito mau)
#Não é baseado em ordenação. Pretende-se saber de base o conjunto de melhores alternativas (Núcleo)
#ELECTRE 1
#Baseia-se na definição de relação de Prevalência S (Subordinação)
#Dado duas alternativas (a,b) diz-se que aSb (a prevalece sobre b) se a é pelo menos tão
#boa quanto b(a não é pior que b) - se aSb e bSa - indiferença, se ~(aSb) e ~(bSa) - incomparabilidade
#dois principios :
    #CONCORDANCIA - aSB : a tem que ser melhor que b para uma maioria de critérios
    #NÃO DISCORDANCIA - não existe uma rejeição forte na minoria de critérios
#1- Atribuem-se pesos que não tem necessariamente que somar para 1
#2 - C(I,J) - valor de concordancia da afirmação ISJ = soma pesos concordantes (critérios onde I > J)
#3 Discordância - condições de veto (dado limite num critério que impede ISJ)
#4 Limiar da concordância - valor ^C entre 0 e 1 (C(IJ) tem que ser maior que ^C
#5 Diz-se que ISJ se C(IJ) > ^C & não há veto em nenhum critério
#Núcleo N - subconjunto de alternativas não subordinadas pelas alternativas não pertencentes
#6 Encontrar o núcleo com menor alternativas

#ELECTRE 2 - PERMITE ORDENAÇÃO
#Introduz subordinação Fraca e Forte
#Introduz relação de indiferença entre duas alternativas e limiar à preferencia
#limiar qi de indiferença - vparaa(critério) - vparab(critério) > qi - então é preferivel,
#de resto é indiferente
#limiar de preferencia - adiciona realismo - pi > qi
#  vparaa(critério) - vparab(critério) > pi = fortemente preferivel
# qi < vparaa(critério) - vparab(critério) <= pi = fracamente preferivel
# qi> vparaa(critério) - vparab(critério) = indiferente