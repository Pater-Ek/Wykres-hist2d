import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

current_figure = None

def load_data_from_file():
    use_header = var_header.get()
    custom_label_x = entry_label_x.get() if not use_header else ''
    custom_label_y = entry_label_y.get() if not use_header else ''
    
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

def draw_hist2d():
    global current_figure
    
    x, y, label_x, label_y = load_data_from_file()
    
    if x is None or y is None:
        return

    try:
        bins_count = int(entry_bins.get())
        if bins_count < 2:
            messagebox.showerror("Błąd", "Liczba koszy musi być co najmniej 2!")
            return
    except ValueError:
        messagebox.showerror("Błąd", "Podaj prawidłową liczbę koszy!")
        return

    for widget in frame_plot.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 5))
    h = ax.hist2d(x, y, bins=bins_count)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_title(f'Histogram 2D ({bins_count}x{bins_count} koszy)')
    fig.colorbar(h[3], ax=ax, label='Liczba punktów')
    fig.tight_layout()

    current_figure = fig

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    btn_export.config(state="normal")

def export_to_png():
    global current_figure
    
    filepath = filedialog.asksaveasfilename(
        title="Zapisz histogram jako PNG",
        defaultextension=".png",
        filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")]
    )
    
    if not filepath:
        return
    
    try:
        current_figure.savefig(
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

def on_header_toggle():
    if var_header.get():
        entry_label_x.config(state="disabled")
        entry_label_y.config(state="disabled")
    else:
        entry_label_x.config(state="normal")
        entry_label_y.config(state="normal")

root = tk.Tk()
root.title("Histogram 2D")
root.geometry("800x600")

label_info = tk.Label(root, text="Wczytaj dane z pliku .csv lub .txt")
label_info.pack(pady=(10,0))

var_header = tk.IntVar(value=1)
frame_check = tk.Frame(root)
check_header = tk.Checkbutton(
    frame_check, text="Pobierz nazwy zmiennych z pierwszego wiersza pliku",
    variable=var_header, command=on_header_toggle
)
check_header.pack(side="left")
frame_check.pack(pady=3)

frame_labels = tk.Frame(root)
tk.Label(frame_labels, text="Nazwa osi X:").pack(side="left")
entry_label_x = tk.Entry(frame_labels, width=15)
entry_label_x.insert(0, "X")
entry_label_x.pack(side="left", padx=5)
tk.Label(frame_labels, text="Nazwa osi Y:").pack(side="left")
entry_label_y = tk.Entry(frame_labels, width=15)
entry_label_y.insert(0, "Y")
entry_label_y.pack(side="left", padx=5)
frame_labels.pack(pady=3)

frame_bins = tk.Frame(root)
tk.Label(frame_bins, text="Liczba koszy:").pack(side="left")
entry_bins = tk.Entry(frame_bins, width=8)
entry_bins.insert(0, "10")
entry_bins.pack(side="left", padx=5)
frame_bins.pack(pady=5)

on_header_toggle()

frame_buttons = tk.Frame(root)
btn_file = tk.Button(frame_buttons, text="Wybierz plik i rysuj histogram 2D", command=draw_hist2d)
btn_file.pack(side="left", padx=5)

btn_export = tk.Button(frame_buttons, text="Eksportuj do PNG", command=export_to_png, state="disabled")
btn_export.pack(side="left", padx=5)
frame_buttons.pack(pady=10)

frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True)

root.mainloop()