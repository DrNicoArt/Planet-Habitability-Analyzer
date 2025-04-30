#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtWidgets import QSlider, QSpinBox, QTabWidget, QGridLayout
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
        
    def plot_correlation(self, x_data, y_data, x_label, y_label, title, color='b'):
        """Rysowanie wykresu korelacji"""
        self.axes.clear()
        self.axes.scatter(x_data, y_data, color=color, alpha=0.7)
        
        # Dodanie linii trendu
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        self.axes.plot(x_data, p(x_data), "r--", alpha=0.7)
        
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.set_title(title)
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()
        
    def plot_habitability_map(self, temp_range, pressure_range, habitability_data, organism):
        """Rysowanie mapy habitabilności"""
        self.axes.clear()
        
        # Tworzenie siatki dla mapy cieplnej
        X, Y = np.meshgrid(temp_range, pressure_range)
        
        # Rysowanie mapy cieplnej
        c = self.axes.pcolormesh(X, Y, habitability_data, cmap='viridis', shading='auto')
        self.fig.colorbar(c, ax=self.axes, label='Indeks habitabilności')
        
        self.axes.set_xlabel('Temperatura (K)')
        self.axes.set_ylabel('Ciśnienie (atm)')
        self.axes.set_title(f'Mapa habitabilności dla {organism}')
        self.fig.tight_layout()
        self.draw()
        
    def plot_simulation_biology(self, time_points, habitability_indices, organism_viability):
        """Rysowanie wyników symulacji biologicznej w czasie"""
        self.axes.clear()
        
        # Główny wykres - indeks habitabilności
        line1 = self.axes.plot(time_points, habitability_indices, 'b-', label='Indeks habitabilności')
        self.axes.set_xlabel('Czas symulacji')
        self.axes.set_ylabel('Indeks habitabilności')
        self.axes.set_ylim(0, 100)
        
        # Dodatkowa oś dla przeżywalności organizmów
        ax2 = self.axes.twinx()
        
        # Rysowanie przeżywalności dla każdego organizmu
        colors = ['r', 'g', 'm', 'c', 'y']
        lines = [line1]
        
        for i, (organism, viability) in enumerate(organism_viability.items()):
            color = colors[i % len(colors)]
            line = ax2.plot(time_points, viability, f'{color}-', label=organism)
            lines.extend(line)
            
        ax2.set_ylabel('Przeżywalność (%)')
        ax2.set_ylim(0, 100)
        
        # Połączenie legend
        labels = [l.get_label() for l in lines]
        self.axes.legend(lines, labels, loc='upper left')
        
        self.axes.set_title('Symulacja biologiczna w czasie')
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()


class BiologicalModule(QWidget):
    """Moduł analizy danych biologicznych"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_biological_data()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika modułu biologicznego"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Panel kontrolny
        control_layout = QHBoxLayout()
        
        # Wybór organizmu
        organism_label = QLabel("Wybierz organizm:")
        self.organism_combo = QComboBox()
        control_layout.addWidget(organism_label)
        control_layout.addWidget(self.organism_combo)
        
        # Wybór parametru
        parameter_label = QLabel("Parametr:")
        self.parameter_combo = QComboBox()
        self.parameter_combo.addItems(["Temperatura", "Ciśnienie", "Promieniowanie", "pH"])
        control_layout.addWidget(parameter_label)
        control_layout.addWidget(self.parameter_combo)
        
        # Przycisk analizy
        self.analyze_button = QPushButton("Analizuj korelację")
        self.analyze_button.clicked.connect(self.analyze_correlation)
        control_layout.addWidget(self.analyze_button)
        
        # Przycisk mapy habitabilności
        self.map_button = QPushButton("Mapa habitabilności")
        self.map_button.clicked.connect(self.show_habitability_map)
        control_layout.addWidget(self.map_button)
        
        # Przycisk wyników symulacji
        self.simulation_results_button = QPushButton("Wyniki symulacji")
        self.simulation_results_button.clicked.connect(self.show_simulation_results)
        control_layout.addWidget(self.simulation_results_button)
        
        # Dodanie panelu kontrolnego do głównego układu
        main_layout.addLayout(control_layout)
        
        # Panel parametrów środowiskowych
        env_layout = QHBoxLayout()
        
        # Temperatura
        temp_label = QLabel("Temperatura (K):")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 500)
        self.temp_slider.setValue(300)
        self.temp_spin = QSpinBox()
        self.temp_spin.setRange(0, 500)
        self.temp_spin.setValue(300)
        self.temp_slider.valueChanged.connect(self.temp_spin.setValue)
        self.temp_spin.valueChanged.connect(self.temp_slider.setValue)
        
        env_layout.addWidget(temp_label)
        env_layout.addWidget(self.temp_slider)
        env_layout.addWidget(self.temp_spin)
        
        # Ciśnienie
        pressure_label = QLabel("Ciśnienie (atm):")
        self.pressure_slider = QSlider(Qt.Horizontal)
        self.pressure_slider.setRange(0, 100)
        self.pressure_slider.setValue(1)
        self.pressure_spin = QSpinBox()
        self.pressure_spin.setRange(0, 100)
        self.pressure_spin.setValue(1)
        self.pressure_slider.valueChanged.connect(self.pressure_spin.setValue)
        self.pressure_spin.valueChanged.connect(self.pressure_slider.setValue)
        
        env_layout.addWidget(pressure_label)
        env_layout.addWidget(self.pressure_slider)
        env_layout.addWidget(self.pressure_spin)
        
        # Promieniowanie
        radiation_label = QLabel("Promieniowanie (Sv/h):")
        self.radiation_slider = QSlider(Qt.Horizontal)
        self.radiation_slider.setRange(0, 1000)
        self.radiation_slider.setValue(1)
        self.radiation_spin = QSpinBox()
        self.radiation_spin.setRange(0, 1000)
        self.radiation_spin.setValue(1)
        self.radiation_slider.valueChanged.connect(self.radiation_spin.setValue)
        self.radiation_spin.valueChanged.connect(self.radiation_slider.setValue)
        
        env_layout.addWidget(radiation_label)
        env_layout.addWidget(self.radiation_slider)
        env_layout.addWidget(self.radiation_spin)
        
        main_layout.addLayout(env_layout)
        
        # Zakładki z wykresami
        self.tabs = QTabWidget()
        
        # Zakładka korelacji
        self.correlation_tab = QWidget()
        correlation_layout = QVBoxLayout()
        self.correlation_canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        correlation_layout.addWidget(self.correlation_canvas)
        self.correlation_tab.setLayout(correlation_layout)
        self.tabs.addTab(self.correlation_tab, "Korelacje")
        
        # Zakładka mapy habitabilności
        self.map_tab = QWidget()
        map_layout = QVBoxLayout()
        self.map_canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        map_layout.addWidget(self.map_canvas)
        self.map_tab.setLayout(map_layout)
        self.tabs.addTab(self.map_tab, "Mapa habitabilności")
        
        # Zakładka porównania widm
        self.spectra_tab = QWidget()
        spectra_layout = QVBoxLayout()
        self.spectra_canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        spectra_layout.addWidget(self.spectra_canvas)
        self.spectra_tab.setLayout(spectra_layout)
        self.tabs.addTab(self.spectra_tab, "Widma biologiczne")
        
        # Zakładka symulacji
        self.simulation_tab = QWidget()
        simulation_layout = QVBoxLayout()
        self.simulation_canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        simulation_layout.addWidget(self.simulation_canvas)
        self.simulation_tab.setLayout(simulation_layout)
        self.tabs.addTab(self.simulation_tab, "Symulacja biologiczna")
        
        main_layout.addWidget(self.tabs)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
        # Dane symulacji
        self.simulation_time_points = []
        self.simulation_habitability_indices = []
        self.simulation_organism_viability = {}
        
    def load_biological_data(self):
        """Ładowanie danych biologicznych"""
        # Przykładowe dane o organizmach (w rzeczywistej aplikacji byłyby pobierane z bazy danych)
        self.organisms = {
            "Niesporczak (Tardigrade)": {
                "temp_range": (0, 150),  # K
                "pressure_range": (0, 60),  # atm
                "radiation_tolerance": 5000,  # Sv
                "pH_range": (3, 10),
                "cell_composition": {
                    "water": 85,
                    "protein": 10,
                    "lipids": 3,
                    "nucleic_acids": 1,
                    "other": 1
                }
            },
            "Deinococcus radiodurans": {
                "temp_range": (10, 45),  # K
                "pressure_range": (1, 5),  # atm
                "radiation_tolerance": 15000,  # Sv
                "pH_range": (5, 11),
                "cell_composition": {
                    "water": 80,
                    "protein": 12,
                    "lipids": 4,
                    "nucleic_acids": 2,
                    "other": 2
                }
            },
            "Thermococcus litoralis": {
                "temp_range": (55, 100),  # K
                "pressure_range": (1, 20),  # atm
                "radiation_tolerance": 200,  # Sv
                "pH_range": (5, 9),
                "cell_composition": {
                    "water": 75,
                    "protein": 15,
                    "lipids": 5,
                    "nucleic_acids": 3,
                    "other": 2
                }
            },
            "Escherichia coli": {
                "temp_range": (15, 45),  # K
                "pressure_range": (1, 2),  # atm
                "radiation_tolerance": 20,  # Sv
                "pH_range": (4.5, 9),
                "cell_composition": {
                    "water": 70,
                    "protein": 15,
                    "lipids": 10,
                    "nucleic_acids": 3,
                    "other": 2
                }
            },
            "Homo sapiens (komórka)": {
                "temp_range": (35, 42),  # K
                "pressure_range": (0.8, 1.2),  # atm
                "radiation_tolerance": 4,  # Sv
                "pH_range": (7.35, 7.45),
                "cell_composition": {
                    "water": 65,
                    "protein": 20,
                    "lipids": 12,
                    "nucleic_acids": 2,
                    "other": 1
                }
            }
        }
        
        # Wypełnienie combobox
        self.organism_combo.addItems(self.organisms.keys())
        
        # Wyświetlenie początkowej korelacji
        self.analyze_correlation()
        
    def analyze_correlation(self):
        """Analiza korelacji między parametrami środowiskowymi a właściwościami organizmów"""
        organism = self.organism_combo.currentText()
        parameter = self.parameter_combo.currentText()
        
        # Generowanie danych dla korelacji (przykład)
        if parameter == "Temperatura":
            x_data = np.linspace(0, 150, 50)
            
            # Symulacja przeżywalności w zależności od temperatury
            min_temp, max_temp = self.organisms[organism]["temp_range"]
            y_data = 100 * np.exp(-0.5 * ((x_data - (min_temp + max_temp) / 2) / ((max_temp - min_temp) / 4))**2)
            
            x_label = "Temperatura (K)"
            y_label = "Przeżywalność (%)"
            title = f"Korelacja temperatury i przeżywalności dla {organism}"
            
        elif parameter == "Ciśnienie":
            x_data = np.linspace(0, 60, 50)
            
            # Symulacja przeżywalności w zależności od ciśnienia
            min_pressure, max_pressure = self.organisms[organism]["pressure_range"]
            y_data = 100 * np.exp(-0.5 * ((x_data - (min_pressure + max_pressure) / 2) / ((max_pressure - min_pressure) / 4))**2)
            
            x_label = "Ciśnienie (atm)"
            y_label = "Przeżywalność (%)"
            title = f"Korelacja ciśnienia i przeżywalności dla {organism}"
            
        elif parameter == "Promieniowanie":
            x_data = np.linspace(0, 5000, 50)
            
            # Symulacja przeżywalności w zależności od promieniowania
            max_radiation = self.organisms[organism]["radiation_tolerance"]
            y_data = 100 * np.exp(-x_data / max_radiation)
            
            x_label = "Promieniowanie (Sv)"
            y_label = "Przeżywalność (%)"
            title = f"Korelacja promieniowania i przeżywalności dla {organism}"
            
        else:  # pH
            x_data = np.linspace(0, 14, 50)
            
            # Symulacja przeżywalności w zależności od pH
            min_ph, max_ph = self.organisms[organism]["pH_range"]
            y_data = 100 * np.exp(-0.5 * ((x_data - (min_ph + max_ph) / 2) / ((max_ph - min_ph) / 4))**2)
            
            x_label = "pH"
            y_label = "Przeżywalność (%)"
            title = f"Korelacja pH i przeżywalności dla {organism}"
            
        # Dodanie szumu do danych
        y_data += np.random.normal(0, 5, size=y_data.shape)
        y_data = np.clip(y_data, 0, 100)  # Ograniczenie wartości do zakresu 0-100%
            
        # Aktualizacja wykresu
        self.correlation_canvas.plot_correlation(x_data, y_data, x_label, y_label, title)
        
        # Przełączenie na zakładkę korelacji
        self.tabs.setCurrentWidget(self.correlation_tab)
        
    def show_habitability_map(self):
        """Wyświetlenie mapy habitabilności"""
        organism = self.organism_combo.currentText()
        
        # Generowanie danych dla mapy habitabilności
        temp_range = np.linspace(0, 150, 50)
        pressure_range = np.linspace(0, 60, 50)
        
        # Symulacja indeksu habitabilności w zależności od temperatury i ciśnienia
        min_temp, max_temp = self.organisms[organism]["temp_range"]
        min_pressure, max_pressure = self.organisms[organism]["pressure_range"]
        
        habitability_data = np.zeros((len(pressure_range), len(temp_range)))
        
        for i, p in enumerate(pressure_range):
            for j, t in enumerate(temp_range):
                # Obliczenie indeksu habitabilności (przykład)
                temp_factor = np.exp(-0.5 * ((t - (min_temp + max_temp) / 2) / ((max_temp - min_temp) / 4))**2)
                pressure_factor = np.exp(-0.5 * ((p - (min_pressure + max_pressure) / 2) / ((max_pressure - min_pressure) / 4))**2)
                
                habitability_data[i, j] = temp_factor * pressure_factor
                
        # Aktualizacja wykresu
        self.map_canvas.plot_habitability_map(temp_range, pressure_range, habitability_data, organism)
        
        # Przełączenie na zakładkę mapy habitabilności
        self.tabs.setCurrentWidget(self.map_tab)
        
    def show_simulation_results(self):
        """Wyświetlenie wyników symulacji biologicznej"""
        if len(self.simulation_time_points) > 0 and self.simulation_organism_viability:
            self.simulation_canvas.plot_simulation_biology(
                self.simulation_time_points,
                self.simulation_habitability_indices,
                self.simulation_organism_viability
            )
        else:
            # Jeśli nie ma danych symulacji, wygeneruj przykładowe
            time_points = np.linspace(0, 100, 50)
            habitability_indices = 50 + 30 * np.sin(0.1 * time_points) + np.random.normal(0, 5, time_points.shape)
            habitability_indices = np.clip(habitability_indices, 0, 100)
            
            organism_viability = {}
            for organism in self.organisms.keys():
                # Różne wzorce przeżywalności dla różnych organizmów
                if "Niesporczak" in organism:
                    viability = 80 + 10 * np.sin(0.05 * time_points) + np.random.normal(0, 3, time_points.shape)
                elif "Deinococcus" in organism:
                    viability = 60 + 20 * np.sin(0.1 * time_points) + np.random.normal(0, 5, time_points.shape)
                elif "Thermococcus" in organism:
                    viability = 40 + 30 * np.sin(0.15 * time_points) + np.random.normal(0, 7, time_points.shape)
                elif "coli" in organism:
                    viability = 30 + 20 * np.sin(0.2 * time_points) + np.random.normal(0, 5, time_points.shape)
                else:  # Homo sapiens
                    viability = 20 + 10 * np.sin(0.25 * time_points) + np.random.normal(0, 3, time_points.shape)
                    
                viability = np.clip(viability, 0, 100)
                organism_viability[organism] = viability
                
            self.simulation_canvas.plot_simulation_biology(
                time_points,
                habitability_indices,
                organism_viability
            )
            
        # Przełączenie na zakładkę symulacji
        self.tabs.setCurrentWidget(self.simulation_tab)
        
    def update_simulation_data(self, time_point, habitability_index, organism_data):
        """Aktualizacja danych symulacji biologicznej"""
        self.simulation_time_points.append(time_point)
        self.simulation_habitability_indices.append(habitability_index)
        
        # Inicjalizacja słownika przeżywalności organizmów przy pierwszym wywołaniu
        if not self.simulation_organism_viability:
            for organism in self.organisms.keys():
                self.simulation_organism_viability[organism] = []
                
        # Aktualizacja przeżywalności organizmów
        for organism in self.simulation_organism_viability.keys():
            if organism in organism_data:
                self.simulation_organism_viability[organism].append(organism_data[organism])
            else:
                # Jeśli brak danych dla danego organizmu, użyj ostatniej wartości lub 0
                last_value = self.simulation_organism_viability[organism][-1] if self.simulation_organism_viability[organism] else 0
                self.simulation_organism_viability[organism].append(last_value)
