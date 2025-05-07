import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funções iniciais disponíveis
def initial_sin_pi_x(x):
    return np.sin(np.pi * x)

def initial_x_1_minus_x(x):
    return x * (1 - x)

initial_functions = {
    "sin(pi*x)": initial_sin_pi_x,
    "x*(1 - x)": initial_x_1_minus_x
}

# Solução por diferenças finitas explícitas
def solve_heat_equation(f, L, alpha, Nx, Nt, T):
    dx = L / Nx
    dt = T / Nt
    x = np.linspace(0, L, Nx+1)
    u = f(x)
    r = alpha * dt / dx**2

    if r > 0.5:
        raise ValueError("O método explícito é instável para r > 0.5")

    U = [u.copy()]
    for n in range(Nt):
        u_new = u.copy()
        u_new[1:-1] = u[1:-1] + r * (u[2:] - 2 * u[1:-1] + u[:-2])
        U.append(u_new)
        u = u_new

    return x, np.array(U)

# App principal
class HeatEquationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador da Equação do Calor")

        # Parâmetros padrão
        self.L = tk.DoubleVar(value=1.0)
        self.alpha = tk.DoubleVar(value=0.01)
        self.Nx = tk.IntVar(value=50)
        self.Nt = tk.IntVar(value=500)
        self.T = tk.DoubleVar(value=0.5)
        self.func_name = tk.StringVar(value="sin(pi*x)")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        ttk.Label(frame, text="Função inicial:").grid(row=0, column=0)
        func_menu = ttk.Combobox(frame, textvariable=self.func_name, values=list(initial_functions.keys()))
        func_menu.grid(row=0, column=1)

        ttk.Label(frame, text="L (tamanho da barra):").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.L).grid(row=1, column=1)

        ttk.Label(frame, text="α (alpha):").grid(row=2, column=0)
        ttk.Entry(frame, textvariable=self.alpha).grid(row=2, column=1)

        ttk.Label(frame, text="Nx (pontos espaciais):").grid(row=3, column=0)
        ttk.Entry(frame, textvariable=self.Nx).grid(row=3, column=1)

        ttk.Label(frame, text="Nt (passos no tempo):").grid(row=4, column=0)
        ttk.Entry(frame, textvariable=self.Nt).grid(row=4, column=1)

        ttk.Label(frame, text="Tempo final T:").grid(row=5, column=0)
        ttk.Entry(frame, textvariable=self.T).grid(row=5, column=1)

        ttk.Button(frame, text="Atualizar gráfico", command=self.update_plot).grid(row=6, column=0, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_plot(self):
        try:
            f = initial_functions[self.func_name.get()]
            x, U = solve_heat_equation(
                f, self.L.get(), self.alpha.get(),
                self.Nx.get(), self.Nt.get(), self.T.get()
            )
            self.ax.clear()
            t_index = int(len(U) * 0.5)
            self.ax.plot(x, U[0], label="t = 0")
            self.ax.plot(x, U[t_index], label=f"t = {self.T.get()/2:.2f}")
            self.ax.plot(x, U[-1], label=f"t = {self.T.get():.2f}")
            self.ax.set_title("Solução da Equação do Calor")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("u(x,t)")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            print("Erro ao atualizar o gráfico:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = HeatEquationApp(root)
    root.mainloop()
