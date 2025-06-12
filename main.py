import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def rysuj_hist2d():
    try:
        x_str = entry_x.get()
        y_str = entry_y.get()
        x = [float(i.replace(',', '.')) for i in x_str.replace(',', ' ').split()]
        y = [float(i.replace(',', '.')) for i in y_str.replace(',', ' ').split()]
        if len(x) != len(y):
            messagebox.showerror("Błąd", "Liczba wartości X i Y musi być taka sama!")
            return
    except ValueError:
        messagebox.showerror("Błąd", "Podano nieprawidłowe dane.")
        return

    # Tworzenie histogramu 2D w osobnym oknie matplotlib
    plt.figure()
    h = plt.hist2d(x, y, bins=10)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Histogram 2D')
    plt.colorbar(h[3], label='Liczba punktów')
    plt.show()

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Histogram 2D - aplikacja")

label_x = tk.Label(root, text="Dane X (oddziel spacją lub przecinkiem):")
label_x.pack()
entry_x = tk.Entry(root, width=50)
entry_x.pack()

label_y = tk.Label(root, text="Dane Y (oddziel spacją lub przecinkiem):")
label_y.pack()
entry_y = tk.Entry(root, width=50)
entry_y.pack()

btn = tk.Button(root, text="Rysuj histogram 2D", command=rysuj_hist2d)
btn.pack(pady=10)

root.mainloop()