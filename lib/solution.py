from functions import functions
import numpy as np


class InitialState:
    def __init__(
            self,
            function: str,
            x,
            u0: None | float = None,
            uL: None | float = None):
        if function not in list(functions.keys()):
            raise ValueError(
                f"A função escolhida deve constar na lista {list(functions.keys())}")
        self.x = x
        self.u: list[float] = functions[function](x)
        if u0:
            self.u[0] = u0
        if uL:
            self.u[-1] = uL
        pass

    def get_u(self):
        return self.u


class Solucao:
    def __init__(
            self,
            initial_function: str,
            alpha: float,
            L: float,
            nx: float,
            T: float,
            nt: float,
            u0: float | None = None,
            uL: float | None = None,
    ):
        self.alpha = alpha
        self.L = L
        self.nx = nx
        self.T = T
        self.nt = nt
        self.r = self.calculate_r()
        self.x = np.linspace(0, L, nx)
        self.initial_state = InitialState(initial_function, self.x, u0, uL)
        self.u = self.initial_state.get_u()
        pass
    
    def calculate_r(self):
        dx = self.L / self.nx
        dt = self.T / self.nt
        r = self.alpha * dt / dx ** 2
        if r > 0.5:
            raise ValueError("O método explícito é instável para r > 0.5")
        return r
    
    def get_u(self):
        return self.u

