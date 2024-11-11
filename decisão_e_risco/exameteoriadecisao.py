#Exercicio 1


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

niveltensao = ["Tensão Elevada", "Tensão Média", "Tensão Baixa"]
# matrizDeDecisão = valores_resultantes_estrategias_por_acontecimento

# Situação de incerteza - não se deseja ou não é possível saber as probabilidades de ocorrência de
# cada acontecimento
# Ex
estrategias_sobrinhos= ["Urania", "Vitorino", "Ximena", "Zumélia"]
matriz_decisao = np.array([[40,15,0],
                           [15,10,10],
                           [15,15,20],
                           [13,13,13]])

matriz_decisao_final = pd.DataFrame(matriz_decisao, estrategias_sobrinhos, niveltensao)
criterio_pessimista = matriz_decisao_final.min(axis=1).rename("Pessimista")  # também conhecido como de wald ou maximin -
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
colors = ['red', 'blue', 'orange','yellow' ]
x = np.linspace(criterio_pessimista.min(), criterio_otimista.max(), 10000)
for point in x:
    if criterio_savage_func(point,criterio_savage.loc["Vitorino"]) - criterio_savage_func(point,criterio_savage.loc["Zumélia"]) <= 0.00000001:
        print(str(point) + " " + str(criterio_savage_func(point,criterio_savage.loc["Vitorino"])))
for produto in criterio_savage.index:
    plt.plot(x, criterio_savage_func(x, criterio_savage.loc[produto]))
    plt.legend(criterio_savage.index)
    plt.show()

#Exercicio 2 - feito no caderno