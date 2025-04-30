#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QGroupBox
from PyQt5.QtCore import Qt

class InputPanel(QWidget):
    """Panel danych wejściowych"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika panelu danych wejściowych"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Grupa parametrów planety
        planet_group = QGroupBox("Parametry planety")
        planet_layout = QFormLayout()
        
        # Nazwa planety
        self.planet_name = QLineEdit("Przykładowa planeta")
        planet_layout.addRow("Nazwa planety:", self.planet_name)
        
        # Masa planety
        self.planet_mass = QLineEdit("1.0")
        planet_layout.addRow("Masa (Ziemia=1):", self.planet_mass)
        
        # Promień planety
        self.planet_radius = QLineEdit("1.0")
        planet_layout.addRow("Promień (Ziemia=1):", self.planet_radius)
        
        # Odległość od gwiazdy
        self.star_distance = QLineEdit("1.0")
        planet_layout.addRow("Odległość od gwiazdy (AU):", self.star_distance)
        
        # Typ gwiazdy
        self.star_type = QComboBox()
        self.star_type.addItems(["Typ G (jak Słońce)", "Typ K (pomarańczowy karzeł)", 
                                "Typ M (czerwony karzeł)", "Typ F (biało-żółta)", "Typ A (biała)"])
        planet_layout.addRow("Typ gwiazdy:", self.star_type)
        
        planet_group.setLayout(planet_layout)
        main_layout.addWidget(planet_group)
        
        # Grupa importu danych
        import_group = QGroupBox("Import danych")
        import_layout = QVBoxLayout()
        
        # Wybór źródła danych
        self.data_source = QComboBox()
        self.data_source.addItems(["Dane lokalne", "Baza danych online", "Symulacja"])
        import_layout.addWidget(QLabel("Źródło danych:"))
        import_layout.addWidget(self.data_source)
        
        # Przyciski importu
        import_buttons_layout = QVBoxLayout()
        
        self.import_spectral_button = QPushButton("Importuj dane widmowe")
        self.import_spectral_button.clicked.connect(self.import_spectral_data)
        import_buttons_layout.addWidget(self.import_spectral_button)
        
        self.import_element_button = QPushButton("Importuj dane pierwiastkowe")
        self.import_element_button.clicked.connect(self.import_element_data)
        import_buttons_layout.addWidget(self.import_element_button)
        
        self.import_bio_button = QPushButton("Importuj dane biologiczne")
        self.import_bio_button.clicked.connect(self.import_bio_data)
        import_buttons_layout.addWidget(self.import_bio_button)
        
        import_layout.addLayout(import_buttons_layout)
        import_group.setLayout(import_layout)
        main_layout.addWidget(import_group)
        
        # Grupa konfiguracji eksperymentu
        experiment_group = QGroupBox("Konfiguracja eksperymentu")
        experiment_layout = QFormLayout()
        
        # Typ eksperymentu
        self.experiment_type = QComboBox()
        self.experiment_type.addItems(["Analiza habitabilności", "Korekta widm", 
                                      "Modelowanie atmosfery", "Symulacja ewolucji"])
        experiment_layout.addRow("Typ eksperymentu:", self.experiment_type)
        
        # Czas symulacji
        self.simulation_time = QLineEdit("1000")
        experiment_layout.addRow("Czas symulacji (lata):", self.simulation_time)
        
        # Przycisk konfiguracji
        self.configure_button = QPushButton("Konfiguruj eksperyment")
        self.configure_button.clicked.connect(self.configure_experiment)
        experiment_layout.addRow("", self.configure_button)
        
        experiment_group.setLayout(experiment_layout)
        main_layout.addWidget(experiment_group)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
    def import_spectral_data(self):
        """Import danych widmowych"""
        if self.data_source.currentText() == "Dane lokalne":
            file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z danymi widmowymi", "", 
                                                     "Pliki danych (*.csv *.fits *.dat);;Wszystkie pliki (*)")
            if file_path:
                # Tutaj byłaby implementacja importu danych z pliku
                pass
        else:
            # Tutaj byłaby implementacja importu danych z innych źródeł
            pass
        
    def import_element_data(self):
        """Import danych o pierwiastkach"""
        if self.data_source.currentText() == "Dane lokalne":
            file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z danymi o pierwiastkach", "", 
                                                     "Pliki danych (*.csv *.json *.dat);;Wszystkie pliki (*)")
            if file_path:
                # Tutaj byłaby implementacja importu danych z pliku
                pass
        else:
            # Tutaj byłaby implementacja importu danych z innych źródeł
            pass
        
    def import_bio_data(self):
        """Import danych biologicznych"""
        if self.data_source.currentText() == "Dane lokalne":
            file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z danymi biologicznymi", "", 
                                                     "Pliki danych (*.csv *.json *.dat);;Wszystkie pliki (*)")
            if file_path:
                # Tutaj byłaby implementacja importu danych z pliku
                pass
        else:
            # Tutaj byłaby implementacja importu danych z innych źródeł
            pass
        
    def configure_experiment(self):
        """Konfiguracja eksperymentu"""
        # Tutaj byłaby implementacja konfiguracji eksperymentu
        pass
