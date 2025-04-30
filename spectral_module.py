#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MatplotlibCanvas(FigureCanvas):
    """Klasa do osadzania wykresów matplotlib w interfejsie PyQt5"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        # Ustawienia wykresu
        self.fig.tight_layout()
        
    def plot_spectrum(self, wavelengths, intensities, label="Widmo", color='b'):
        """Rysowanie widma na wykresie"""
        self.axes.clear()
        self.axes.plot(wavelengths, intensities, color=color, label=label)
        self.axes.set_xlabel('Długość fali (nm)')
        self.axes.set_ylabel('Intensywność')
        self.axes.set_title('Analiza Widmowa')
        self.axes.legend()
        self.axes.grid(True)
        self.draw()
        
    def plot_comparison(self, wavelengths, raw_intensities, corrected_intensities):
        """Porównanie widm surowych i skorygowanych"""
        self.axes.clear()
        self.axes.plot(wavelengths, raw_intensities, 'r-', label='Widmo surowe')
        self.axes.plot(wavelengths, corrected_intensities, 'g-', label='Widmo skorygowane')
        self.axes.set_xlabel('Długość fali (nm)')
        self.axes.set_ylabel('Intensywność')
        self.axes.set_title('Porównanie widm')
        self.axes.legend()
        self.axes.grid(True)
        self.draw()
        
    def plot_simulation_results(self, time_points, habitability_indices, temperature_values=None, pressure_values=None):
        """Rysowanie wyników symulacji w czasie"""
        self.axes.clear()
        
        # Główny wykres - indeks habitabilności
        line1 = self.axes.plot(time_points, habitability_indices, 'b-', label='Indeks habitabilności')
        self.axes.set_xlabel('Czas symulacji')
        self.axes.set_ylabel('Indeks habitabilności')
        self.axes.set_ylim(0, 100)
        
        # Dodatkowe osie dla temperatury i ciśnienia, jeśli podane
        if temperature_values is not None:
            ax2 = self.axes.twinx()
            line2 = ax2.plot(time_points, temperature_values, 'r-', label='Temperatura')
            ax2.set_ylabel('Temperatura (K)', color='r')
            ax2.tick_params(axis='y', labelcolor='r')
            
            if pressure_values is not None:
                ax3 = self.axes.twinx()
                ax3.spines['right'].set_position(('outward', 60))
                line3 = ax3.plot(time_points, pressure_values, 'g-', label='Ciśnienie')
                ax3.set_ylabel('Ciśnienie (atm)', color='g')
                ax3.tick_params(axis='y', labelcolor='g')
                
                # Połączenie legend
                lines = line1 + line2 + line3
                labels = [l.get_label() for l in lines]
                self.axes.legend(lines, labels, loc='upper left')
            else:
                # Połączenie legend
                lines = line1 + line2
                labels = [l.get_label() for l in lines]
                self.axes.legend(lines, labels, loc='upper left')
        else:
            self.axes.legend(loc='upper left')
        
        self.axes.set_title('Wyniki symulacji w czasie')
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()


class SpectralModule(QWidget):
    """Moduł analizy widmowej i interferometrycznej"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika modułu widmowego"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Panel kontrolny
        control_layout = QHBoxLayout()
        
        # Wybór typu widma
        spectrum_label = QLabel("Typ widma:")
        self.spectrum_type = QComboBox()
        self.spectrum_type.addItems(["Emisyjne", "Absorpcyjne", "Interferometryczne"])
        control_layout.addWidget(spectrum_label)
        control_layout.addWidget(self.spectrum_type)
        
        # Wybór algorytmu filtrowania
        filter_label = QLabel("Algorytm filtrowania:")
        self.filter_algorithm = QComboBox()
        self.filter_algorithm.addItems(["Filtr Kalmana", "Filtr Gaussa", "Filtr medianowy", "Bez filtrowania"])
        control_layout.addWidget(filter_label)
        control_layout.addWidget(self.filter_algorithm)
        
        # Przycisk analizy
        self.analyze_button = QPushButton("Analizuj")
        self.analyze_button.clicked.connect(self.perform_analysis)
        control_layout.addWidget(self.analyze_button)
        
        # Przycisk porównania
        self.compare_button = QPushButton("Porównaj widma")
        self.compare_button.clicked.connect(self.compare_spectra)
        control_layout.addWidget(self.compare_button)
        
        # Przycisk wyników symulacji
        self.simulation_results_button = QPushButton("Wyniki symulacji")
        self.simulation_results_button.clicked.connect(self.show_simulation_results)
        control_layout.addWidget(self.simulation_results_button)
        
        # Dodanie panelu kontrolnego do głównego układu
        main_layout.addLayout(control_layout)
        
        # Obszar wykresu
        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        main_layout.addWidget(self.canvas)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
        # Wygenerowanie przykładowych danych
        self.generate_sample_data()
        
        # Dane symulacji
        self.simulation_time_points = []
        self.simulation_habitability_indices = []
        self.simulation_temperature_values = []
        self.simulation_pressure_values = []
        
    def generate_sample_data(self):
        """Generowanie przykładowych danych widmowych"""
        # Przykładowe dane widmowe
        self.wavelengths = np.linspace(300, 1000, 500)  # długości fali od 300 do 1000 nm
        
        # Widmo emisyjne (przykład)
        self.emission_spectrum = np.zeros_like(self.wavelengths)
        for peak in [350, 450, 550, 650, 750]:
            self.emission_spectrum += 100 * np.exp(-(self.wavelengths - peak)**2 / (2 * 10**2))
        
        # Dodanie szumu
        self.emission_spectrum += np.random.normal(0, 5, self.wavelengths.shape)
        
        # Widmo absorpcyjne (przykład)
        self.absorption_spectrum = 100 - self.emission_spectrum / 2
        
        # Widmo interferometryczne (przykład)
        self.interferometric_spectrum = 50 + 30 * np.sin(0.1 * self.wavelengths) + np.random.normal(0, 3, self.wavelengths.shape)
        
        # Skorygowane widma
        self.corrected_emission = self.apply_filter(self.emission_spectrum)
        self.corrected_absorption = self.apply_filter(self.absorption_spectrum)
        self.corrected_interferometric = self.apply_filter(self.interferometric_spectrum)
        
        # Wyświetlenie początkowego widma
        self.canvas.plot_spectrum(self.wavelengths, self.emission_spectrum, "Widmo emisyjne", 'r')
        
    def apply_filter(self, spectrum, filter_type="Filtr Kalmana"):
        """Aplikacja wybranego filtra do widma"""
        # Implementacja prostego filtrowania (w rzeczywistej aplikacji byłaby bardziej zaawansowana)
        if filter_type == "Filtr Kalmana":
            # Uproszczona implementacja filtra Kalmana
            filtered = np.zeros_like(spectrum)
            filtered[0] = spectrum[0]
            kalman_gain = 0.75
            for i in range(1, len(spectrum)):
                filtered[i] = filtered[i-1] + kalman_gain * (spectrum[i] - filtered[i-1])
            return filtered
        elif filter_type == "Filtr Gaussa":
            # Uproszczona implementacja filtra Gaussa
            from scipy.ndimage import gaussian_filter
            return gaussian_filter(spectrum, sigma=2)
        elif filter_type == "Filtr medianowy":
            # Uproszczona implementacja filtra medianowego
            from scipy.signal import medfilt
            return medfilt(spectrum, kernel_size=5)
        else:
            # Bez filtrowania
            return spectrum
        
    def perform_analysis(self):
        """Wykonanie analizy widmowej"""
        spectrum_type = self.spectrum_type.currentText()
        filter_type = self.filter_algorithm.currentText()
        
        if spectrum_type == "Emisyjne":
            spectrum = self.emission_spectrum
            label = "Widmo emisyjne"
            color = 'r'
        elif spectrum_type == "Absorpcyjne":
            spectrum = self.absorption_spectrum
            label = "Widmo absorpcyjne"
            color = 'b'
        else:  # Interferometryczne
            spectrum = self.interferometric_spectrum
            label = "Widmo interferometryczne"
            color = 'g'
            
        # Aplikacja filtra
        filtered_spectrum = self.apply_filter(spectrum, filter_type)
        
        # Aktualizacja wykresu
        self.canvas.plot_spectrum(self.wavelengths, filtered_spectrum, label, color)
        
    def compare_spectra(self):
        """Porównanie widm surowych i skorygowanych"""
        spectrum_type = self.spectrum_type.currentText()
        
        if spectrum_type == "Emisyjne":
            raw_spectrum = self.emission_spectrum
            corrected_spectrum = self.corrected_emission
        elif spectrum_type == "Absorpcyjne":
            raw_spectrum = self.absorption_spectrum
            corrected_spectrum = self.corrected_absorption
        else:  # Interferometryczne
            raw_spectrum = self.interferometric_spectrum
            corrected_spectrum = self.corrected_interferometric
            
        # Aktualizacja wykresu
        self.canvas.plot_comparison(self.wavelengths, raw_spectrum, corrected_spectrum)
        
    def show_simulation_results(self):
        """Wyświetlenie wyników symulacji"""
        if len(self.simulation_time_points) > 0:
            self.canvas.plot_simulation_results(
                self.simulation_time_points,
                self.simulation_habitability_indices,
                self.simulation_temperature_values,
                self.simulation_pressure_values
            )
        else:
            # Jeśli nie ma danych symulacji, wygeneruj przykładowe
            time_points = np.linspace(0, 100, 50)
            habitability_indices = 50 + 30 * np.sin(0.1 * time_points) + np.random.normal(0, 5, time_points.shape)
            habitability_indices = np.clip(habitability_indices, 0, 100)
            temperature_values = 300 + 50 * np.sin(0.05 * time_points) + np.random.normal(0, 10, time_points.shape)
            pressure_values = 1 + 0.5 * np.cos(0.1 * time_points) + np.random.normal(0, 0.1, time_points.shape)
            
            self.canvas.plot_simulation_results(
                time_points,
                habitability_indices,
                temperature_values,
                pressure_values
            )
            
    def update_simulation_data(self, time_point, habitability_index, temperature, pressure):
        """Aktualizacja danych symulacji"""
        self.simulation_time_points.append(time_point)
        self.simulation_habitability_indices.append(habitability_index)
        self.simulation_temperature_values.append(temperature)
        self.simulation_pressure_values.append(pressure)
