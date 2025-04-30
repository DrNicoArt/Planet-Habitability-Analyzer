#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QPushButton, QComboBox, QSlider, QSpinBox, QHeaderView
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
        
    def plot_decay(self, elements, half_lives, label="Okresy połowicznego rozpadu", color='b'):
        """Rysowanie wykresu okresów połowicznego rozpadu"""
        self.axes.clear()
        self.axes.bar(elements, half_lives, color=color)
        self.axes.set_xlabel('Pierwiastek')
        self.axes.set_ylabel('Okres połowicznego rozpadu (lata)')
        self.axes.set_title(label)
        self.axes.tick_params(axis='x', rotation=45)
        self.fig.tight_layout()
        self.draw()
        
    def plot_property_change(self, temperatures, property_values, element_name, property_name):
        """Rysowanie wykresu zmian właściwości w zależności od temperatury"""
        self.axes.clear()
        self.axes.plot(temperatures, property_values, 'r-o')
        self.axes.set_xlabel('Temperatura (K)')
        self.axes.set_ylabel(property_name)
        self.axes.set_title(f'Zmiana {property_name} dla {element_name}')
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()
        
    def plot_simulation_elements(self, time_points, element_concentrations, element_names):
        """Rysowanie zmian stężeń pierwiastków podczas symulacji"""
        self.axes.clear()
        
        for i, element in enumerate(element_names):
            self.axes.plot(time_points, element_concentrations[i], label=element)
            
        self.axes.set_xlabel('Czas symulacji')
        self.axes.set_ylabel('Względne stężenie')
        self.axes.set_title('Zmiany stężeń pierwiastków podczas symulacji')
        self.axes.legend()
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()


class ElementModule(QWidget):
    """Moduł analizy właściwości pierwiastków"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_element_data()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika modułu pierwiastkowego"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Panel kontrolny
        control_layout = QHBoxLayout()
        
        # Wybór pierwiastka
        element_label = QLabel("Wybierz pierwiastek:")
        self.element_combo = QComboBox()
        control_layout.addWidget(element_label)
        control_layout.addWidget(self.element_combo)
        
        # Wybór właściwości
        property_label = QLabel("Właściwość:")
        self.property_combo = QComboBox()
        self.property_combo.addItems(["Okres połowicznego rozpadu", "Energia aktywacji", "Temperatura topnienia", "Temperatura wrzenia"])
        control_layout.addWidget(property_label)
        control_layout.addWidget(self.property_combo)
        
        # Przycisk analizy
        self.analyze_button = QPushButton("Analizuj")
        self.analyze_button.clicked.connect(self.analyze_element)
        control_layout.addWidget(self.analyze_button)
        
        # Przycisk symulacji
        self.simulate_button = QPushButton("Symuluj zmiany")
        self.simulate_button.clicked.connect(self.simulate_property_changes)
        control_layout.addWidget(self.simulate_button)
        
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
        self.temp_slider.setRange(0, 5000)
        self.temp_slider.setValue(300)
        self.temp_spin = QSpinBox()
        self.temp_spin.setRange(0, 5000)
        self.temp_spin.setValue(300)
        self.temp_slider.valueChanged.connect(self.temp_spin.setValue)
        self.temp_spin.valueChanged.connect(self.temp_slider.setValue)
        
        env_layout.addWidget(temp_label)
        env_layout.addWidget(self.temp_slider)
        env_layout.addWidget(self.temp_spin)
        
        # Ciśnienie
        pressure_label = QLabel("Ciśnienie (atm):")
        self.pressure_slider = QSlider(Qt.Horizontal)
        self.pressure_slider.setRange(0, 1000)
        self.pressure_slider.setValue(1)
        self.pressure_spin = QSpinBox()
        self.pressure_spin.setRange(0, 1000)
        self.pressure_spin.setValue(1)
        self.pressure_slider.valueChanged.connect(self.pressure_spin.setValue)
        self.pressure_spin.valueChanged.connect(self.pressure_slider.setValue)
        
        env_layout.addWidget(pressure_label)
        env_layout.addWidget(self.pressure_slider)
        env_layout.addWidget(self.pressure_spin)
        
        main_layout.addLayout(env_layout)
        
        # Układ dla tabeli i wykresu
        content_layout = QHBoxLayout()
        
        # Tabela pierwiastków
        self.element_table = QTableWidget()
        self.element_table.setColumnCount(5)
        self.element_table.setHorizontalHeaderLabels(["Symbol", "Nazwa", "Okres połowicznego rozpadu", "Stan skupienia", "Energia aktywacji"])
        self.element_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        content_layout.addWidget(self.element_table)
        
        # Obszar wykresu
        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        content_layout.addWidget(self.canvas)
        
        main_layout.addLayout(content_layout)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
        # Dane symulacji
        self.simulation_time_points = []
        self.simulation_element_concentrations = []
        self.simulation_element_names = []
        
    def load_element_data(self):
        """Ładowanie danych o pierwiastkach"""
        # Przykładowe dane o pierwiastkach (w rzeczywistej aplikacji byłyby pobierane z bazy danych)
        self.elements = {
            "U": {"name": "Uran", "half_life": 4.5e9, "state": "Stały", "activation_energy": 0.52, "melting_point": 1405, "boiling_point": 4404},
            "Pu": {"name": "Pluton", "half_life": 2.4e4, "state": "Stały", "activation_energy": 0.57, "melting_point": 912, "boiling_point": 3505},
            "Th": {"name": "Tor", "half_life": 1.4e10, "state": "Stały", "activation_energy": 0.58, "melting_point": 2023, "boiling_point": 5061},
            "Ra": {"name": "Rad", "half_life": 1.6e3, "state": "Stały", "activation_energy": 0.48, "melting_point": 973, "boiling_point": 2010},
            "Rn": {"name": "Radon", "half_life": 3.8, "state": "Gazowy", "activation_energy": 0.36, "melting_point": 202, "boiling_point": 211},
            "Po": {"name": "Polon", "half_life": 138, "state": "Stały", "activation_energy": 0.41, "melting_point": 527, "boiling_point": 1235},
            "Bi": {"name": "Bizmut", "half_life": 2.0e19, "state": "Stały", "activation_energy": 0.43, "melting_point": 544, "boiling_point": 1837},
            "Pb": {"name": "Ołów", "half_life": float('inf'), "state": "Stały", "activation_energy": 0.37, "melting_point": 600, "boiling_point": 2022},
            "Tl": {"name": "Tal", "half_life": float('inf'), "state": "Stały", "activation_energy": 0.33, "melting_point": 577, "boiling_point": 1746},
            "Hg": {"name": "Rtęć", "half_life": float('inf'), "state": "Ciekły", "activation_energy": 0.29, "melting_point": 234, "boiling_point": 630},
        }
        
        # Wypełnienie tabeli
        self.element_table.setRowCount(len(self.elements))
        row = 0
        for symbol, data in self.elements.items():
            self.element_table.setItem(row, 0, QTableWidgetItem(symbol))
            self.element_table.setItem(row, 1, QTableWidgetItem(data["name"]))
            
            half_life = data["half_life"]
            half_life_str = f"{half_life:.2e}" if half_life != float('inf') else "Stabilny"
            self.element_table.setItem(row, 2, QTableWidgetItem(half_life_str))
            
            self.element_table.setItem(row, 3, QTableWidgetItem(data["state"]))
            self.element_table.setItem(row, 4, QTableWidgetItem(f"{data['activation_energy']:.2f} eV"))
            row += 1
            
        # Wypełnienie combobox
        self.element_combo.addItems(self.elements.keys())
        
        # Wyświetlenie początkowego wykresu
        self.plot_half_lives()
        
    def plot_half_lives(self):
        """Rysowanie wykresu okresów połowicznego rozpadu"""
        elements = []
        half_lives = []
        
        for symbol, data in self.elements.items():
            if data["half_life"] != float('inf'):  # Pomijamy stabilne pierwiastki
                elements.append(symbol)
                half_lives.append(data["half_life"])
                
        self.canvas.plot_decay(elements, half_lives)
        
    def analyze_element(self):
        """Analiza wybranego pierwiastka"""
        element = self.element_combo.currentText()
        property_name = self.property_combo.currentText()
        
        if property_name == "Okres połowicznego rozpadu":
            self.plot_half_lives()
        else:
            # Symulacja zmian właściwości w zależności od temperatury
            self.simulate_property_changes()
            
    def simulate_property_changes(self):
        """Symulacja zmian właściwości w zależności od temperatury"""
        element = self.element_combo.currentText()
        property_name = self.property_combo.currentText()
        
        # Generowanie danych dla symulacji
        temperatures = np.linspace(100, 3000, 100)
        
        if property_name == "Energia aktywacji":
            # Symulacja zmiany energii aktywacji z temperaturą (przykład)
            base_value = self.elements[element]["activation_energy"]
            property_values = base_value * (1 + 0.0001 * (temperatures - 300))
            y_label = "Energia aktywacji (eV)"
        elif property_name == "Temperatura topnienia":
            # Symulacja wpływu ciśnienia na temperaturę topnienia (przykład)
            base_value = self.elements[element]["melting_point"]
            pressure = self.pressure_spin.value()
            property_values = base_value * np.ones_like(temperatures) * (1 + 0.01 * np.log(pressure + 1))
            y_label = "Temperatura topnienia (K)"
        elif property_name == "Temperatura wrzenia":
            # Symulacja wpływu ciśnienia na temperaturę wrzenia (przykład)
            base_value = self.elements[element]["boiling_point"]
            pressure = self.pressure_spin.value()
            property_values = base_value * np.ones_like(temperatures) * (1 + 0.02 * np.log(pressure + 1))
            y_label = "Temperatura wrzenia (K)"
        else:
            # Okres połowicznego rozpadu (przykład)
            if self.elements[element]["half_life"] == float('inf'):
                property_values = np.ones_like(temperatures) * 1e20  # Stabilny pierwiastek
            else:
                base_value = self.elements[element]["half_life"]
                # Symulacja wpływu temperatury na okres połowicznego rozpadu (przykład)
                property_values = base_value * np.exp(-0.0001 * (temperatures - 300))
            y_label = "Okres połowicznego rozpadu (lata)"
            
        # Aktualizacja wykresu
        self.canvas.plot_property_change(temperatures, property_values, 
                                         self.elements[element]["name"], y_label)
                                         
    def show_simulation_results(self):
        """Wyświetlenie wyników symulacji dla pierwiastków"""
        if len(self.simulation_time_points) > 0 and len(self.simulation_element_concentrations) > 0:
            self.canvas.plot_simulation_elements(
                self.simulation_time_points,
                self.simulation_element_concentrations,
                self.simulation_element_names
            )
        else:
            # Jeśli nie ma danych symulacji, wygeneruj przykładowe
            time_points = np.linspace(0, 100, 50)
            element_names = ["O", "N", "C", "H", "Fe"]
            element_concentrations = []
            
            # Generowanie przykładowych danych dla każdego pierwiastka
            for i in range(len(element_names)):
                # Różne wzorce zmian dla różnych pierwiastków
                if i == 0:  # Tlen - wzrost, potem stabilizacja
                    conc = 0.2 + 0.6 * (1 - np.exp(-0.05 * time_points))
                elif i == 1:  # Azot - powolny spadek
                    conc = 0.8 - 0.3 * (1 - np.exp(-0.02 * time_points))
                elif i == 2:  # Węgiel - oscylacje
                    conc = 0.1 + 0.05 * np.sin(0.2 * time_points)
                elif i == 3:  # Wodór - gwałtowny spadek
                    conc = 0.5 * np.exp(-0.03 * time_points)
                else:  # Żelazo - powolny wzrost
                    conc = 0.05 + 0.02 * (1 - np.exp(-0.01 * time_points))
                    
                # Dodanie szumu
                conc += np.random.normal(0, 0.01, time_points.shape)
                element_concentrations.append(conc)
                
            self.canvas.plot_simulation_elements(
                time_points,
                element_concentrations,
                element_names
            )
            
    def update_simulation_data(self, time_point, element_data):
        """Aktualizacja danych symulacji dla pierwiastków"""
        if not self.simulation_element_names:
            # Inicjalizacja list elementów przy pierwszym wywołaniu
            self.simulation_element_names = list(element_data.keys())
            self.simulation_element_concentrations = [[] for _ in range(len(self.simulation_element_names))]
            
        self.simulation_time_points.append(time_point)
        
        # Aktualizacja stężeń pierwiastków
        for i, element in enumerate(self.simulation_element_names):
            if element in element_data:
                self.simulation_element_concentrations[i].append(element_data[element])
            else:
                # Jeśli brak danych dla danego pierwiastka, użyj ostatniej wartości lub 0
                last_value = self.simulation_element_concentrations[i][-1] if self.simulation_element_concentrations[i] else 0
                self.simulation_element_concentrations[i].append(last_value)
