from lib.functions import functions
import numpy as np


class InitialState:
    """
    Classe que representa o estado inicial da equação do calor.
    
    Armazena a condição inicial da equação do calor, aplicando a função inicial
    escolhida e possivelmente sobrescrevendo as condições de contorno.
    
    Attributes:
        x (numpy.ndarray): Coordenadas espaciais discretizadas.
        u (numpy.ndarray): Valores iniciais da temperatura em cada ponto de x.
    """
    
    def __init__(
            self,
            function: str,
            x,
            left_boundary: None | float = None,
            right_boundary: None | float = None):
        """
        Inicializa o estado inicial da equação.
        
        Args:
            function (str): Nome da função inicial a ser aplicada.
            x (numpy.ndarray): Coordenadas espaciais discretizadas.
            left_boundary (float, optional): Valor da temperatura na extremidade esquerda (x=0).
            right_boundary (float, optional): Valor da temperatura na extremidade direita (x=L).
            
        Raises:
            ValueError: Se a função especificada não estiver na lista de funções disponíveis.
        """
        if function not in list(functions.keys()):
            raise ValueError(
                f"A função escolhida deve constar na lista {list(functions.keys())}")
        self.x = x
        self.u: list[float] = functions[function](x)
        if left_boundary is not None:
            self.u[0] = left_boundary
        if right_boundary is not None:
            self.u[-1] = right_boundary

    def get_u(self):
        """
        Retorna os valores iniciais da temperatura.
        
        Returns:
            numpy.ndarray: Valores iniciais da temperatura em cada ponto de x.
        """
        return self.u


class Solution:
    """
    Classe que implementa a solução numérica da equação do calor por diferenças finitas.
    
    Utiliza o método explícito de diferenças finitas para resolver a equação do calor
    unidimensional com as condições iniciais e de contorno especificadas.
    
    Attributes:
        alpha (float): Coeficiente de difusão térmica.
        L (float): Comprimento da barra.
        nx (int): Número de pontos espaciais.
        T (float): Tempo final da simulação.
        nt (int): Número de passos temporais.
        r (float): Fator de estabilidade (alpha*dt/dx²).
        x (numpy.ndarray): Coordenadas espaciais discretizadas.
        initial_state (InitialState): Estado inicial da equação.
        u (numpy.ndarray): Estado atual da temperatura.
        U (list): Lista de todos os estados da temperatura em cada passo temporal.
    """
    
    def __init__(
            self,
            initial_function: str,
            alpha: float,
            L: float,
            nx: float,
            T: float,
            nt: float,
            left_boundary: float | None = None,
            right_boundary: float | None = None,
    ):
        """
        Inicializa a solução da equação do calor.
        
        Args:
            initial_function (str): Nome da função de condição inicial.
            alpha (float): Coeficiente de difusão térmica.
            L (float): Comprimento da barra.
            nx (float): Número de pontos espaciais.
            T (float): Tempo final da simulação.
            nt (float): Número de passos temporais.
            left_boundary (float, optional): Temperatura na extremidade esquerda (x=0).
            right_boundary (float, optional): Temperatura na extremidade direita (x=L).
        """
        self.alpha = alpha
        self.L = L
        self.nx = nx
        self.T = T
        self.nt = nt
        self.r = self.calculate_r()
        self.x = np.linspace(0, L, nx)
        self.initial_state = InitialState(initial_function, self.x, left_boundary, right_boundary)
        self.u = self.initial_state.get_u()
        self.U = [self.u.copy()]
    
    def calculate_r(self):
        """
        Calcula o fator de estabilidade r = alpha*dt/dx².
        
        Returns:
            float: Valor do fator de estabilidade.
            
        Raises:
            ValueError: Se r > 0.5, o que tornaria o método explícito instável.
        """
        dx = self.L / self.nx
        dt = self.T / self.nt
        r = self.alpha * dt / dx ** 2
        if r > 0.5:
            raise ValueError("O método explícito é instável para r > 0.5")
        return r
    
    def solve(self):
        """
        Resolve a equação do calor pelo método de diferenças finitas explícito.
        
        Implementa o esquema explícito de diferenças finitas para resolver a equação
        do calor unidimensional. A solução avança no tempo para cada passo temporal.
        
        Returns:
            tuple: Um par (x, U), onde x são as coordenadas espaciais e 
                  U é uma matriz com todos os estados da temperatura ao longo do tempo.
        """
        for n in range(self.nt):
            u_new = self.u.copy()
            u_new[1:-1] = self.u[1:-1] + self.r * (self.u[2:] - 2 * self.u[1:-1] + self.u[:-2])
            self.U.append(u_new)
            self.u = u_new

        return self.x, np.array(self.U)

