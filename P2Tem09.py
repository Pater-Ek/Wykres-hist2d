import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Histogram2DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Histogram 2D")
        self.root.geometry("800x600")

        self.current_figure = None
        self.var_header = tk.IntVar(value=1)

        self._create_widgets()

    def _create_widgets(self):
        # Info label
        self.label_info = tk.Label(self.root, text="Wczytaj dane z pliku .csv lub .txt")
        self.label_info.pack(pady=(10, 0))

        # Header checkbox frame
        self.frame_check = tk.Frame(self.root)
        self.check_header = tk.Checkbutton(
            self.frame_check,
            text="Pobierz nazwy zmiennych z pierwszego wiersza pliku",
            variable=self.var_header,
            command=self._on_header_toggle
        )
        self.check_header.pack(side="left")
        self.frame_check.pack(pady=3)

        # Labels frame
        self.frame_labels = tk.Frame(self.root)
        tk.Label(self.frame_labels, text="Nazwa osi X:").pack(side="left")
        self.entry_label_x = tk.Entry(self.frame_labels, width=15)
        self.entry_label_x.insert(0, "X")
        self.entry_label_x.pack(side="left", padx=5)
        tk.Label(self.frame_labels, text="Nazwa osi Y:").pack(side="left")
        self.entry_label_y = tk.Entry(self.frame_labels, width=15)
        self.entry_label_y.insert(0, "Y")
        self.entry_label_y.pack(side="left", padx=5)
        self.frame_labels.pack(pady=3)

        # Bins frame
        self.frame_bins = tk.Frame(self.root)
        tk.Label(self.frame_bins, text="Liczba koszy:").pack(side="left")
        self.entry_bins = tk.Entry(self.frame_bins, width=8)
        self.entry_bins.insert(0, "10")
        self.entry_bins.pack(side="left", padx=5)
        self.frame_bins.pack(pady=5)

        self._on_header_toggle()

        # Buttons frame
        self.frame_buttons = tk.Frame(self.root)
        self.btn_file = tk.Button(
            self.frame_buttons,
            text="Wybierz plik i rysuj histogram 2D",
            command=self._draw_hist2d
        )
        self.btn_file.pack(side="left", padx=5)

        self.btn_export = tk.Button(
            self.frame_buttons,
            text="Eksportuj do PNG",
            command=self._export_to_png,
            state="disabled"
        )
        self.btn_export.pack(side="left", padx=5)
        self.frame_buttons.pack(pady=10)

        # Plot frame
        self.frame_plot = tk.Frame(self.root)
        self.frame_plot.pack(fill=tk.BOTH, expand=True)

    def _on_header_toggle(self):
        if self.var_header.get():
            self.entry_label_x.config(state="disabled")
            self.entry_label_y.config(state="disabled")
        else:
            self.entry_label_x.config(state="normal")
            self.entry_label_y.config(state="normal")

    def _load_data_from_file(self):
        use_header = self.var_header.get()
        custom_label_x = self.entry_label_x.get() if not use_header else ''
        custom_label_y = self.entry_label_y.get() if not use_header else ''

        filepath = filedialog.askopenfilename(
            title="Wybierz plik z danymi",
            filetypes=[("Pliki tekstowe", "*.txt *.csv"), ("Wszystkie pliki", "*.*")]
        )
        if not filepath:
            return None, None, None, None

        x = []
        y = []
        label_x = custom_label_x if not use_header else "X"
        label_y = custom_label_y if not use_header else "Y"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    messagebox.showerror("Błąd", "Plik powinien zawierać dane.")
                    return None, None, None, None

                if use_header:
                    if len(lines) < 2:
                        messagebox.showerror("Błąd", "Plik powinien zawierać nagłówki i dane.")
                        return None, None, None, None

                    header_line = lines[0].strip()
                    header_parts = header_line.replace(';', '\t').replace(',', '\t').split('\t')

                    if len(header_parts) >= 2:
                        label_x = header_parts[0].strip()
                        label_y = header_parts[1].strip()

                    data_lines = lines[1:]
                else:
                    data_lines = lines

                for line in data_lines:
                    parts = (
                        line.strip()
                        .replace(';', ' ')
                        .replace(',', ' ')
                        .replace('\t', ' ')
                        .split()
                    )
                    if len(parts) >= 2:
                        try:
                            x_val = float(parts[0].replace(',', '.').replace(';', '.'))
                            y_val = float(parts[1].replace(',', '.').replace(';', '.'))
                            x.append(x_val)
                            y.append(y_val)
                        except ValueError:
                            continue

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się odczytać pliku: {e}")
            return None, None, None, None

        if not x or not y or len(x) != len(y):
            messagebox.showerror("Błąd", "Nieprawidłowe lub niekompletne dane w pliku.")
            return None, None, None, None

        return x, y, label_x, label_y

    def _draw_hist2d(self):
        x, y, label_x, label_y = self._load_data_from_file()

        if x is None or y is None:
            return

        try:
            bins_count = int(self.entry_bins.get())
            if bins_count < 2:
                messagebox.showerror("Błąd", "Liczba koszy musi być co najmniej 2!")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Podaj prawidłową liczbę koszy!")
            return

        for widget in self.frame_plot.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 5))
        h = ax.hist2d(x, y, bins=bins_count)
        ax.set_xlabel(label_x)
        ax.set_ylabel(label_y)
        ax.set_title(f'Histogram 2D ({bins_count}x{bins_count} koszy)')
        fig.colorbar(h[3], ax=ax, label='Liczba punktów')
        fig.tight_layout()

        self.current_figure = fig

        canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.btn_export.config(state="normal")

    def _export_to_png(self):
        filepath = filedialog.asksaveasfilename(
            title="Zapisz histogram jako PNG",
            defaultextension=".png",
            filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")]
        )

        if not filepath:
            return

        try:
            self.current_figure.savefig(
                filepath,
                format='png',
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none'
            )
            messagebox.showinfo("Sukces", f"Histogram został zapisany jako:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")

def click_fun(wn, _ml):
    root = tk.Toplevel(wn)
    root.focus()
    app = Histogram2DApp(root)
    root.mainloop()


if __name__ == "__main__":
    click_fun(None, None)