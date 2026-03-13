P2Tem09
Adrian Paterek, Kacper Piwosz
Adrian Paterek developed:
Code for generating the chart,
Tkinter window,
Option to select a .csv or .txt file to import for chart generation,
Options for naming axes in the window.

Kacper Piwosz developed:
GUI design,
Chart generation in the window,
Option to export a .png file,
API implementation,
Selection of the number of generated baskets,
Documentation.

System requirements
Python 3.6 or newer

Libraries (install via pip install -r requirements.txt):
matplotlib>=3.5.0

Installation
Download the file containing the application code (e.g., histogram2d.py)

Install the required libraries:

bash
pip install -r P2Tem09_requirements.txt

Functionality description
The application allows you to:

Load two-dimensional data from text files (CSV/TXT)

Creating 2D histograms

Exporting results to PNG files

Step-by-step instructions
1. Loading data
Click the “Select file and draw 2D histogram” button

Select a file with data:

Supported formats: .txt, .csv

Data should be separated by spaces, tabs, commas, or semicolons

Sample data format:

text
x1 y1
x2 y2
x3 y3

2. Configuration Options
Column Headings:

Check the “Get variable names from the first row of the file” checkbox if the first row of the file contains column names

Or enter your own axis names in the “X-axis Name” and “Y-axis Name” fields

Number of bins:

Enter the number of bins (default 10) for the histogram

3. Generating the histogram
After selecting a file, the application will automatically generate the histogram

On the graph, you will see:

The distribution of data on the XY plane

A color scale representing the density of points

Axis labels according to the selected settings

4. Exporting results
After the histogram is generated, the “Export to PNG” button will become active

Click it to save the histogram as a PNG image

Select the location and file name

Error handling
Invalid data format: The application will display a message about invalid data

No file: You will receive a notification if no file is selected

Invalid number of bins: The value must be an integer ≥ 2
-----------------------------------------------------------------------------------------------------------------------
P2Tem09
Adrian Paterek, Kacper Piwosz
Adrian Paterek wykonał:
Kod generujący wykres,
Okno tkintera,
Wybór pliku do importu .csv lub .txt do wygenerowania wykresu,
Opcje nazwania osi w oknie.

Kacper Piwosz wykonał:
Wygląd GUI,
Generowanie wykresu w oknie,
Opcja eksportu pliku .png,
Implementacja API,
Wybór liczby generowanych koszy,
Dokumentacja.

Wymagania systemowe
Python 3.6 lub nowszy

Biblioteki (zainstaluj przez pip install -r requirements.txt):
matplotlib>=3.5.0

Instalacja
Pobierz plik z kodem aplikacji (np. histogram2d.py)

Zainstaluj wymagane biblioteki:

bash
pip install -r P2Tem09_requirements.txt

Opis funkcjonalności
Aplikacja umożliwia:

Wczytywanie danych dwuwymiarowych z plików tekstowych (CSV/TXT)

Tworzenie histogramów 2D

Eksport wyników do plików PNG

Instrukcja krok po kroku
1. Wczytywanie danych
Kliknij przycisk "Wybierz plik i rysuj histogram 2D"

Wybierz plik z danymi:

Obsługiwane formaty: .txt, .csv

Dane powinny być oddzielone spacjami, tabulatorami, przecinkami lub średnikami

Przykładowy format danych:

text
x1 y1
x2 y2
x3 y3
2. Opcje konfiguracji
Nagłówki kolumn:

Zaznacz checkbox "Pobierz nazwy zmiennych z pierwszego wiersza pliku", jeśli pierwszy wiersz pliku zawiera nazwy kolumn

Lub wpisz własne nazwy osi w polach "Nazwa osi X" i "Nazwa osi Y"

Liczba koszy:

Wpisz liczbę przedziałów (domyślnie 10) dla histogramu

3. Generowanie histogramu
Po wybraniu pliku, aplikacja automatycznie wygeneruje histogram

Na wykresie zobaczysz:

Rozkład danych na płaszczyźnie XY

Skalę kolorów reprezentującą gęstość punktów

Podpisy osi zgodne z wybranymi ustawieniami

4. Eksport wyników
Po wygenerowaniu histogramu przycisk "Eksportuj do PNG" stanie się aktywny

Kliknij go, aby zapisać histogram jako obraz PNG

Wybierz lokalizację i nazwę pliku

Obsługa błędów
Błędny format danych: Aplikacja wyświetli komunikat o nieprawidłowych danych

Brak pliku: Otrzymasz powiadomienie, jeśli plik nie zostanie wybrany

Nieprawidłowa liczba koszy: Wartość musi być liczbą całkowitą ≥ 2
