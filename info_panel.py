#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt5.QtWidgets import QFormLayout, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class InfoPanel(QWidget):
    """Panel informacji wyświetlający podsumowanie parametrów symulacji i wyników analizy"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika panelu informacji"""
        # Główny układ
        main_layout = QHBoxLayout()
        
        # Grupa parametrów symulacji
        params_group = QGroupBox("Parametry symulacji")
        params_layout = QFormLayout()
        
        # Etykiety dla parametrów
        self.planet_name_label = QLabel("Przykładowa planeta")
        self.planet_name_label.setFont(QFont("Arial", 10, QFont.Bold))
        params_layout.addRow("Planeta:", self.planet_name_label)
        
        self.temperature_label = QLabel("300 K")
        params_layout.addRow("Temperatura:", self.temperature_label)
        
        self.pressure_label = QLabel("1 atm")
        params_layout.addRow("Ciśnienie:", self.pressure_label)
        
        self.radiation_label = QLabel("1 Sv/h")
        params_layout.addRow("Promieniowanie:", self.radiation_label)
        
        self.atmosphere_label = QLabel("O₂: 21%, N₂: 78%, CO₂: 0%")
        params_layout.addRow("Atmosfera:", self.atmosphere_label)
        
        params_group.setLayout(params_layout)
        main_layout.addWidget(params_group)
        
        # Grupa wyników analizy
        results_group = QGroupBox("Wyniki analizy")
        results_layout = QFormLayout()
        
        # Etykiety dla wyników
        self.habitability_label = QLabel("Nieznany")
        self.habitability_label.setFont(QFont("Arial", 10, QFont.Bold))
        results_layout.addRow("Indeks habitabilności:", self.habitability_label)
        
        # Pasek postępu dla habitabilności
        self.habitability_progress = QProgressBar()
        self.habitability_progress.setRange(0, 100)
        self.habitability_progress.setValue(0)
        self.habitability_progress.setTextVisible(True)
        self.habitability_progress.setFormat("%v%")
        results_layout.addRow("", self.habitability_progress)
        
        self.life_forms_label = QLabel("Nieznane")
        results_layout.addRow("Możliwe formy życia:", self.life_forms_label)
        
        self.spectral_status_label = QLabel("Nie przeprowadzono")
        results_layout.addRow("Status analizy widmowej:", self.spectral_status_label)
        
        self.element_status_label = QLabel("Nie przeprowadzono")
        results_layout.addRow("Status analizy pierwiastkowej:", self.element_status_label)
        
        self.bio_status_label = QLabel("Nie przeprowadzono")
        results_layout.addRow("Status analizy biologicznej:", self.bio_status_label)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        # Grupa statusu symulacji
        status_group = QGroupBox("Status symulacji")
        status_layout = QVBoxLayout()
        
        # Status symulacji
        self.simulation_status = QLabel("Gotowy do rozpoczęcia")
        self.simulation_status.setAlignment(Qt.AlignCenter)
        self.simulation_status.setFont(QFont("Arial", 10, QFont.Bold))
        status_layout.addWidget(self.simulation_status)
        
        # Pasek postępu symulacji
        self.simulation_progress = QProgressBar()
        self.simulation_progress.setRange(0, 100)
        self.simulation_progress.setValue(0)
        status_layout.addWidget(self.simulation_progress)
        
        # Czas symulacji
        self.simulation_time = QLabel("Czas: 0s")
        self.simulation_time.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.simulation_time)
        
        # Pozostały czas
        self.remaining_time = QLabel("Pozostało: --")
        self.remaining_time.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.remaining_time)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
    def update_parameters(self, planet_name, temperature, pressure, radiation, atmosphere):
        """Aktualizacja parametrów symulacji"""
        self.planet_name_label.setText(planet_name)
        self.temperature_label.setText(f"{temperature} K")
        self.pressure_label.setText(f"{pressure} atm")
        self.radiation_label.setText(f"{radiation} Sv/h")
        self.atmosphere_label.setText(atmosphere)
        
    def update_results(self, habitability_index, life_forms, spectral_status, element_status, bio_status):
        """Aktualizacja wyników analizy"""
        self.habitability_label.setText(f"{habitability_index}/100")
        self.habitability_progress.setValue(int(habitability_index))
        
        # Ustawienie koloru paska postępu w zależności od indeksu habitabilności
        if habitability_index < 30:
            self.habitability_progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        elif habitability_index < 70:
            self.habitability_progress.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")
        else:
            self.habitability_progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            
        self.life_forms_label.setText(life_forms)
        self.spectral_status_label.setText(spectral_status)
        self.element_status_label.setText(element_status)
        self.bio_status_label.setText(bio_status)
        
    def update_simulation_status(self, status, progress, elapsed_time, remaining_time):
        """Aktualizacja statusu symulacji"""
        self.simulation_status.setText(status)
        self.simulation_progress.setValue(progress)
        self.simulation_time.setText(f"Czas: {elapsed_time}s")
        self.remaining_time.setText(f"Pozostało: {remaining_time}s")
