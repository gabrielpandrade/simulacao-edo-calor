import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

from lib.functions import functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from lib.solution import Solution


class HeatEquationApp:
    """
    Aplicação para simulação da equação do calor.
    
    Esta classe implementa uma interface gráfica para visualizar e interagir com
    soluções numéricas da equação do calor unidimensional. Permite ao usuário 
    definir parâmetros de simulação, navegar entre os passos temporais da 
    solução e configurar a apresentação gráfica.
    
    Attributes:
        root (tk.Tk): Janela principal da aplicação Tkinter.
        L (tk.DoubleVar): Comprimento da barra.
        alpha (tk.DoubleVar): Coeficiente de difusão térmica.
        nx (tk.IntVar): Número de pontos espaciais.
        nt (tk.IntVar): Número de passos no tempo.
        T (tk.DoubleVar): Tempo final da simulação.
        boundary_value_left (tk.DoubleVar): Valor de contorno em x=0.
        boundary_value_right (tk.DoubleVar): Valor de contorno em x=L.
        initial_func_name (tk.StringVar): Nome da função de condição inicial.
        current_step (int): Passo atual da simulação sendo visualizado.
        x_axis_min (tk.DoubleVar): Valor mínimo do eixo x no gráfico.
        x_axis_max (tk.DoubleVar): Valor máximo do eixo x no gráfico.
        y_axis_min (tk.DoubleVar): Valor mínimo do eixo y no gráfico.
        y_axis_max (tk.DoubleVar): Valor máximo do eixo y no gráfico.
        use_fixed_limits (tk.BooleanVar): Se True, usa limites fixos no gráfico.
        solution (Solution): Instância da classe Solution com a solução calculada.
        x (numpy.ndarray): Valores de x (coordenadas espaciais).
        U (numpy.ndarray): Matriz com todas as soluções temporais u(x,t).
    """

    def __init__(self, root):
        """
        Inicializa a aplicação da equação do calor.
        
        Args:
            root (tk.Tk): Janela principal da aplicação Tkinter.
        """
        self.root = root
        self.root.title("Simulador da Equação do Calor v0.1")

        self.L = tk.DoubleVar(value=1.0)
        self.alpha = tk.DoubleVar(value=1)
        self.nx = tk.IntVar(value=50)
        self.nt = tk.IntVar(value=500)
        self.T = tk.DoubleVar(value=0.5)
        self.boundary_value_left = tk.DoubleVar(value=None)
        self.boundary_value_right = tk.DoubleVar(value=None)
        self.initial_func_name = tk.StringVar(value="sin(pi*x)")
        self.current_step = 0

        self.x_axis_min = tk.DoubleVar(value=0.0)
        self.x_axis_max = tk.DoubleVar(value=self.L.get())
        self.y_axis_min = tk.DoubleVar(value=-1.5)
        self.y_axis_max = tk.DoubleVar(value=1.5)
        self.use_fixed_limits = tk.BooleanVar(value=False)

        self.create_widgets()
        self.update_solution()

    def set_solution(self):
        """
        Cria uma nova instância da solução com os parâmetros atuais.
        
        Extrai valores das variáveis Tkinter e cria uma nova instância
        da classe Solution com os parâmetros especificados na interface.
        """
        initial_func = self.initial_func_name.get()
        alpha = self.alpha.get()
        L = self.L.get()
        nx = self.nx.get()
        T = self.T.get()
        nt = self.nt.get()

        left_value = None
        right_value = None
        try:
            left_val = self.boundary_value_left.get()
            if left_val is not None and left_val != '':
                left_value = float(left_val)
        except:
            pass

        try:
            right_val = self.boundary_value_right.get()
            if right_val is not None and right_val != '':
                right_value = float(right_val)
        except:
            pass

        self.solution = Solution(initial_func, alpha, L, nx, T, nt, left_value, right_value)

    def create_widgets(self):
        """
        Cria os elementos da interface gráfica.
        
        Configura todos os widgets da interface, incluindo campos de entrada,
        botões, labels e o canvas do gráfico.
        """
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        ttk.Label(frame, text="Função inicial:").grid(row=0, column=0)
        func_menu = ttk.Combobox(
            frame, textvariable=self.initial_func_name, values=list(functions.keys()))
        func_menu.grid(row=0, column=1)

        ttk.Label(frame, text="α (alpha):").grid(row=2, column=0)
        ttk.Entry(frame, textvariable=self.alpha).grid(row=2, column=1)

        ttk.Label(frame, text="L (tamanho da barra):").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.L).grid(row=1, column=1)

        ttk.Label(frame, text="nx (pontos espaciais):").grid(row=3, column=0)
        ttk.Entry(frame, textvariable=self.nx).grid(row=3, column=1)

        ttk.Label(frame, text="Tempo final T:").grid(row=4, column=0)
        ttk.Entry(frame, textvariable=self.T).grid(row=4, column=1)

        ttk.Label(frame, text="nt (passos no tempo):").grid(row=5, column=0)
        ttk.Entry(frame, textvariable=self.nt).grid(row=5, column=1)

        ttk.Label(frame, text="u(0,t):").grid(row=6, column=0)
        ttk.Entry(frame, textvariable=self.boundary_value_left).grid(row=6, column=1)

        ttk.Label(frame, text="u(L,t):").grid(row=7, column=0)
        ttk.Entry(frame, textvariable=self.boundary_value_right).grid(row=7, column=1)

        ttk.Button(frame, text="Atualizar gráfico", command=self.update_solution).grid(
            row=8, column=0, columnspan=2, pady=10)

        nav_frame = ttk.Frame(frame)
        nav_frame.grid(row=9, column=0, columnspan=2, pady=5)

        ttk.Button(nav_frame, text="|<<", command=self.first_step).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="<<", command=self.previous_step).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text=">>", command=self.next_step).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text=">>|", command=self.last_step).pack(
            side=tk.LEFT, padx=5)

        self.step_label = ttk.Label(nav_frame, text="Passo: 0")
        self.step_label.pack(side=tk.LEFT, padx=10)

        jump_frame = ttk.Frame(frame)
        jump_frame.grid(row=10, column=0, columnspan=2, pady=5)

        ttk.Label(jump_frame, text="Ir para passo:").pack(side=tk.LEFT, padx=5)
        self.jump_step_var = tk.IntVar(value=0)
        step_entry = ttk.Entry(
            jump_frame, textvariable=self.jump_step_var, width=8)
        step_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(jump_frame, text="Ir", command=self.jump_to_step).pack(
            side=tk.LEFT, padx=5)

        axis_frame = ttk.LabelFrame(frame, text="Limites dos Eixos")
        axis_frame.grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Checkbutton(axis_frame, text="Usar limites fixos", variable=self.use_fixed_limits).grid(
            row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(axis_frame, text="X Min:").grid(row=1, column=0, sticky="w")
        ttk.Entry(axis_frame, textvariable=self.x_axis_min, width=8).grid(
            row=1, column=1, sticky="w", padx=5)

        ttk.Label(axis_frame, text="X Max:").grid(row=1, column=2, sticky="w")
        ttk.Entry(axis_frame, textvariable=self.x_axis_max, width=8).grid(
            row=1, column=3, sticky="w", padx=5)

        ttk.Label(axis_frame, text="Y Min:").grid(row=2, column=0, sticky="w")
        ttk.Entry(axis_frame, textvariable=self.y_axis_min, width=8).grid(
            row=2, column=1, sticky="w", padx=5)

        ttk.Label(axis_frame, text="Y Max:").grid(row=2, column=2, sticky="w")
        ttk.Entry(axis_frame, textvariable=self.y_axis_max, width=8).grid(
            row=2, column=3, sticky="w", padx=5)

        ttk.Button(axis_frame, text="Aplicar Limites", command=self.apply_axis_limits).grid(
            row=3, column=0, columnspan=4, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_solution(self):
        """
        Atualiza a solução e o gráfico.
        
        Cria uma nova solução com os parâmetros atuais, calcula-a,
        atualiza os limites dos eixos, e exibe o primeiro passo da solução.
        
        Raises:
            Exception: Erro durante o cálculo ou atualização do gráfico.
        """
        try:
            self.set_solution()
            self.x, self.U = self.solution.solve()

            x_min_data = min(self.x)
            x_max_data = max(self.x)
            y_min_data = min(self.U.min(), -0.1)
            y_max_data = max(self.U.max(), 0.1)

            x_margin = (x_max_data - x_min_data) * 0.05
            y_margin = (y_max_data - y_min_data) * 0.05

            self.x_axis_min.set(x_min_data - x_margin)
            self.x_axis_max.set(x_max_data + x_margin)
            self.y_axis_min.set(y_min_data - y_margin)
            self.y_axis_max.set(y_max_data + y_margin)

            self.set_step(0)
            self.plot(self.x, self.U)
        except Exception as e:
            print("Erro ao atualizar o gráfico:", e)

    def plot(self, x, U):
        """
        Plota a solução para o passo atual.
        
        Args:
            x (numpy.ndarray): Coordenadas espaciais.
            U (numpy.ndarray): Matriz de soluções para todos os passos temporais.
        """
        self.ax.clear()
        self.ax.plot(x, U[self.current_step])
        self.ax.set_title(f"Solução da Equação do Calor - Passo {self.current_step}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("u(x,t)")

        if self.use_fixed_limits.get():
            self.ax.set_xlim(self.x_axis_min.get(), self.x_axis_max.get())
            self.ax.set_ylim(self.y_axis_min.get(), self.y_axis_max.get())

        self.canvas.draw()

    def increment_step(self, amount: int):
        """
        Incrementa o passo atual da simulação.
        
        Args:
            amount (int): Quantidade a ser adicionada ao passo atual.
            
        Returns:
            bool: True se o incremento foi bem-sucedido, False caso contrário.
        """
        new_step = self.current_step + amount
        if not hasattr(self, 'U') or new_step >= len(self.U) or new_step < 0:
            return False
        self.set_step(new_step)
        return True

    def next_step(self):
        """
        Avança para o próximo passo da simulação.
        """
        if self.increment_step(1):
            self.plot(self.x, self.U)

    def previous_step(self):
        """
        Retorna ao passo anterior da simulação.
        """
        if self.increment_step(-1):
            self.plot(self.x, self.U)

    def set_step(self, index: int):
        """
        Define o passo atual da simulação.
        
        Args:
            index (int): Índice do passo a ser definido.
        """
        self.current_step = index
        total_steps = len(self.U) if hasattr(self, 'U') else 0
        self.step_label.config(text=f"Passo: {self.current_step}/{total_steps - 1}")
        self.jump_step_var.set(self.current_step)

    def apply_axis_limits(self):
        """
        Aplica os limites dos eixos definidos pelo usuário ao gráfico.
        
        Raises:
            Exception: Erro ao aplicar limites dos eixos.
        """
        try:
            if self.use_fixed_limits.get():
                self.ax.set_xlim(self.x_axis_min.get(), self.x_axis_max.get())
                self.ax.set_ylim(self.y_axis_min.get(), self.y_axis_max.get())
            else:
                self.ax.autoscale(True)

            self.canvas.draw()
        except Exception as e:
            print("Erro ao aplicar limites dos eixos:", e)

    def jump_to_step(self):
        """
        Pula para um passo específico da simulação.
        
        Lê o valor do campo de entrada e tenta ir para o passo correspondente.
        
        Raises:
            Exception: Erro ao pular para o passo.
        """
        try:
            jump_step = self.jump_step_var.get()
            if hasattr(self, 'U'):
                if 0 <= jump_step < len(self.U):
                    self.set_step(jump_step)
                    self.plot(self.x, self.U)
                else:
                    print(
                        f"Valor de passo inválido. Deve estar entre 0 e {len(self.U) - 1}")
            else:
                print("Solução não disponível. Atualize o gráfico primeiro.")
        except Exception as e:
            print(f"Erro ao pular para o passo: {e}")

    def first_step(self):
        """
        Vai para o primeiro passo da simulação.
        """
        if hasattr(self, 'U') and len(self.U) > 0:
            self.set_step(0)
            self.plot(self.x, self.U)
        else:
            print("Solução não disponível. Atualize o gráfico primeiro.")

    def last_step(self):
        """
        Vai para o último passo da simulação.
        """
        if hasattr(self, 'U') and len(self.U) > 0:
            self.set_step(len(self.U) - 1)
            self.plot(self.x, self.U)
        else:
            print("Solução não disponível. Atualize o gráfico primeiro.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HeatEquationApp(root)
    root.mainloop()
