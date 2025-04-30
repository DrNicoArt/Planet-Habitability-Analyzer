#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QSpinBox
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QDoubleSpinBox, QCheckBox
from PyQt5.QtCore import Qt

class SimulationPanel(QWidget):
    """Panel parametrów symulacji"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika panelu parametrów symulacji"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Grupa parametrów środowiskowych
        env_group = QGroupBox("Parametry środowiskowe")
        env_layout = QFormLayout()
        
        # Temperatura
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 5000)
        self.temp_slider.setValue(300)
        self.temp_spin = QSpinBox()
        self.temp_spin.setRange(0, 5000)
        self.temp_spin.setValue(300)
        self.temp_slider.valueChanged.connect(self.temp_spin.setValue)
        self.temp_spin.valueChanged.connect(self.temp_slider.setValue)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_spin)
        env_layout.addRow("Temperatura (K):", temp_layout)
        
        # Ciśnienie
        pressure_layout = QHBoxLayout()
        self.pressure_slider = QSlider(Qt.Horizontal)
        self.pressure_slider.setRange(0, 1000)
        self.pressure_slider.setValue(1)
        self.pressure_spin = QSpinBox()
        self.pressure_spin.setRange(0, 1000)
        self.pressure_spin.setValue(1)
        self.pressure_slider.valueChanged.connect(self.pressure_spin.setValue)
        self.pressure_spin.valueChanged.connect(self.pressure_slider.setValue)
        pressure_layout.addWidget(self.pressure_slider)
        pressure_layout.addWidget(self.pressure_spin)
        env_layout.addRow("Ciśnienie (atm):", pressure_layout)
        
        # Promieniowanie
        radiation_layout = QHBoxLayout()
        self.radiation_slider = QSlider(Qt.Horizontal)
        self.radiation_slider.setRange(0, 10000)
        self.radiation_slider.setValue(1)
        self.radiation_spin = QSpinBox()
        self.radiation_spin.setRange(0, 10000)
        self.radiation_spin.setValue(1)
        self.radiation_slider.valueChanged.connect(self.radiation_spin.setValue)
        self.radiation_spin.valueChanged.connect(self.radiation_slider.setValue)
        radiation_layout.addWidget(self.radiation_slider)
        radiation_layout.addWidget(self.radiation_spin)
        env_layout.addRow("Promieniowanie (Sv/h):", radiation_layout)
        
        # pH
        ph_layout = QHBoxLayout()
        self.ph_slider = QSlider(Qt.Horizontal)
        self.ph_slider.setRange(0, 140)
        self.ph_slider.setValue(70)
        self.ph_spin = QDoubleSpinBox()
        self.ph_spin.setRange(0, 14)
        self.ph_spin.setValue(7.0)
        self.ph_spin.setSingleStep(0.1)
        
        # Połączenie sliderów i spinboxów z konwersją wartości
        self.ph_slider.valueChanged.connect(lambda val: self.ph_spin.setValue(val / 10))
        self.ph_spin.valueChanged.connect(lambda val: self.ph_slider.setValue(int(val * 10)))
        
        ph_layout.addWidget(self.ph_slider)
        ph_layout.addWidget(self.ph_spin)
        env_layout.addRow("pH:", ph_layout)
        
        env_group.setLayout(env_layout)
        main_layout.addWidget(env_group)
        
        # Grupa parametrów atmosferycznych
        atm_group = QGroupBox("Parametry atmosferyczne")
        atm_layout = QFormLayout()
        
        # Skład atmosfery - tlen
        oxygen_layout = QHBoxLayout()
        self.oxygen_slider = QSlider(Qt.Horizontal)
        self.oxygen_slider.setRange(0, 100)
        self.oxygen_slider.setValue(21)
        self.oxygen_spin = QSpinBox()
        self.oxygen_spin.setRange(0, 100)
        self.oxygen_spin.setValue(21)
        self.oxygen_spin.setSuffix("%")
        self.oxygen_slider.valueChanged.connect(self.oxygen_spin.setValue)
        self.oxygen_spin.valueChanged.connect(self.oxygen_slider.setValue)
        oxygen_layout.addWidget(self.oxygen_slider)
        oxygen_layout.addWidget(self.oxygen_spin)
        atm_layout.addRow("Tlen:", oxygen_layout)
        
        # Skład atmosfery - azot
        nitrogen_layout = QHBoxLayout()
        self.nitrogen_slider = QSlider(Qt.Horizontal)
        self.nitrogen_slider.setRange(0, 100)
        self.nitrogen_slider.setValue(78)
        self.nitrogen_spin = QSpinBox()
        self.nitrogen_spin.setRange(0, 100)
        self.nitrogen_spin.setValue(78)
        self.nitrogen_spin.setSuffix("%")
        self.nitrogen_slider.valueChanged.connect(self.nitrogen_spin.setValue)
        self.nitrogen_spin.valueChanged.connect(self.nitrogen_slider.setValue)
        nitrogen_layout.addWidget(self.nitrogen_slider)
        nitrogen_layout.addWidget(self.nitrogen_spin)
        atm_layout.addRow("Azot:", nitrogen_layout)
        
        # Skład atmosfery - CO2
        co2_layout = QHBoxLayout()
        self.co2_slider = QSlider(Qt.Horizontal)
        self.co2_slider.setRange(0, 100)
        self.co2_slider.setValue(0)
        self.co2_spin = QSpinBox()
        self.co2_spin.setRange(0, 100)
        self.co2_spin.setValue(0)
        self.co2_spin.setSuffix("%")
        self.co2_slider.valueChanged.connect(self.co2_spin.setValue)
        self.co2_spin.valueChanged.connect(self.co2_slider.setValue)
        co2_layout.addWidget(self.co2_slider)
        co2_layout.addWidget(self.co2_spin)
        atm_layout.addRow("CO2:", co2_layout)
        
        # Gęstość atmosfery
        density_layout = QHBoxLayout()
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(0, 500)
        self.density_slider.setValue(100)
        self.density_spin = QDoubleSpinBox()
        self.density_spin.setRange(0, 5)
        self.density_spin.setValue(1)
        self.density_spin.setSingleStep(0.01)
        self.density_spin.setSuffix("x Ziemia")
        
        # Połączenie sliderów i spinboxów z konwersją wartości
        self.density_slider.valueChanged.connect(lambda val: self.density_spin.setValue(val / 100))
        self.density_spin.valueChanged.connect(lambda val: self.density_slider.setValue(int(val * 100)))
        
        density_layout.addWidget(self.density_slider)
        density_layout.addWidget(self.density_spin)
        atm_layout.addRow("Gęstość atmosfery:", density_layout)
        
        atm_group.setLayout(atm_layout)
        main_layout.addWidget(atm_group)
        
        # Grupa parametrów symulacji
        sim_group = QGroupBox("Parametry symulacji")
        sim_layout = QFormLayout()
        
        # Dokładność symulacji
        accuracy_layout = QHBoxLayout()
        self.accuracy_slider = QSlider(Qt.Horizontal)
        self.accuracy_slider.setRange(1, 10)
        self.accuracy_slider.setValue(5)
        self.accuracy_spin = QSpinBox()
        self.accuracy_spin.setRange(1, 10)
        self.accuracy_spin.setValue(5)
        self.accuracy_slider.valueChanged.connect(self.accuracy_spin.setValue)
        self.accuracy_spin.valueChanged.connect(self.accuracy_slider.setValue)
        accuracy_layout.addWidget(self.accuracy_slider)
        accuracy_layout.addWidget(self.accuracy_spin)
        sim_layout.addRow("Dokładność symulacji:", accuracy_layout)
        
        # Czas symulacji
        time_layout = QHBoxLayout()
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(1, 1000)
        self.time_slider.setValue(100)
        self.time_spin = QSpinBox()
        self.time_spin.setRange(1, 1000)
        self.time_spin.setValue(100)
        self.time_spin.setSuffix(" jednostek")
        self.time_slider.valueChanged.connect(self.time_spin.setValue)
        self.time_spin.valueChanged.connect(self.time_slider.setValue)
        time_layout.addWidget(self.time_slider)
        time_layout.addWidget(self.time_spin)
        sim_layout.addRow("Czas symulacji:", time_layout)
        
        # Opcje symulacji
        self.include_radiation = QCheckBox("Uwzględnij efekty promieniowania")
        self.include_radiation.setChecked(True)
        sim_layout.addRow("", self.include_radiation)
        
        self.include_evolution = QCheckBox("Uwzględnij ewolucję atmosfery")
        self.include_evolution.setChecked(True)
        sim_layout.addRow("", self.include_evolution)
        
        self.include_biology = QCheckBox("Uwzględnij wpływ na formy życia")
        self.include_biology.setChecked(True)
        sim_layout.addRow("", self.include_biology)
        
        sim_group.setLayout(sim_layout)
        main_layout.addWidget(sim_group)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
