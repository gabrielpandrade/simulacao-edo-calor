"""
Biblioteca de funções iniciais para a equação do calor.

Este módulo define as funções que podem ser usadas como condições iniciais
para a simulação da equação do calor. Cada função toma como entrada um array
de coordenadas espaciais e retorna os valores correspondentes da temperatura inicial.
"""

import numpy as np

# Dicionário de funções disponíveis para condições iniciais
functions = {
    "sin(pi*x)": lambda x: np.sin(np.pi*x),
    "x*(1 - x)": lambda x: x*(1-x),
    "x": lambda x: x
}