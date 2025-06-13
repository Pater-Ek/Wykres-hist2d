import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

def wczytaj_dane_z_pliku(uzyj_naglowka, custom_label_x='', custom_label_y=''):
    filepath = filedialog.askopenfilename(
        title="Wybierz plik z danymi",
        filetypes=[("Pliki tekstowe", "*.txt *.csv"), ("Wszystkie pliki", "*.*")]
    )
    if not filepath:
        return None, None, None, None

    x = []
    y = []
    label_x = custom_label_x if not uzyj_naglowka else "X"
    label_y = custom_label_y if not uzyj_naglowka else "Y"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                messagebox.showerror("Błąd", "Plik powinien zawierać dane.")
                return None, None, None, None

            if uzyj_naglowka:
                if len(lines) < 2:
                    messagebox.showerror("Błąd", "Plik powinien zawierać nagłówki i dane.")
                    return None, None, None, None
                header = lines[0].strip().replace(';', ' ').replace(',', ' ').replace('\t', ' ').split()
                if len(header) >= 2:
                    label_x, label_y = header[0], header[1]
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
                        continue  # Pomijamy błędne linie
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się odczytać pliku: {e}")
        return None, None, None, None

    if not x or not y or len(x) != len(y):
        messagebox.showerror("Błąd", "Nieprawidłowe lub niekompletne dane w pliku.")
        return None, None, None, None

    return x, y, label_x, label_y

def rysuj_hist2d_z_pliku():
    uzyj_naglowka = var_naglowek.get()
    label_x = entry_label_x.get()
    label_y = entry_label_y.get()
    # Jeśli nagłówek, to ignorujemy wpisane nazwy
    custom_label_x = label_x if not uzyj_naglowka else ""
    custom_label_y = label_y if not uzyj_naglowka else ""
    x, y, label_x, label_y = wczytaj_dane_z_pliku(uzyj_naglowka, custom_label_x, custom_label_y)
    if x is None or y is None:
        return

    plt.figure()
    h = plt.hist2d(x, y, bins=10)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title('Histogram 2D z pliku')
    plt.colorbar(h[3], label='Liczba punktów')
    plt.show()

def on_naglowek_toggle():
    if var_naglowek.get():
        entry_label_x.config(state="disabled")
        entry_label_y.config(state="disabled")
    else:
        entry_label_x.config(state="normal")
        entry_label_y.config(state="normal")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Histogram 2D")
root.geometry("400x150")

label_info = tk.Label(root, text="Wczytaj dane z pliku .csv lub .txt")
label_info.pack(pady=(10,0))

# Checkbox - czy pobierać nazwy zmiennych z pierwszego wiersza
var_naglowek = tk.IntVar(value=1)
frame_check = tk.Frame(root)
check_naglowek = tk.Checkbutton(
    frame_check, text="Pobierz nazwy zmiennych z pierwszego wiersza pliku",
    variable=var_naglowek, command=on_naglowek_toggle
)
check_naglowek.pack(side="left")
frame_check.pack(pady=3)

# Pola do wpisania nazw zmiennych (domyślnie wyłączone, jeśli checkbox zaznaczony)
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

on_naglowek_toggle()  # Ustaw stan pól na podstawie domyślnego wyboru

btn_file = tk.Button(root, text="Wybierz plik i rysuj histogram 2D", command=rysuj_hist2d_z_pliku)
btn_file.pack(pady=10)

root.mainloop()