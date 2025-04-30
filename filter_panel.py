#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QSlider, QSpinBox, QCheckBox
from PyQt5.QtCore import Qt

class FilterPanel(QWidget):
    """Panel filtrów i ustawień"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika panelu filtrów i ustawień"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Grupa filtrów widmowych
        spectral_group = QGroupBox("Filtry widmowe")
        spectral_layout = QFormLayout()
        
        # Wybór algorytmu filtrowania
        self.filter_algorithm = QComboBox()
        self.filter_algorithm.addItems(["Filtr Kalmana", "Filtr Gaussa", "Filtr medianowy", "Bez filtrowania"])
        spectral_layout.addRow("Algorytm filtrowania:", self.filter_algorithm)
        
        # Intensywność filtrowania
        intensity_layout = QHBoxLayout()
        self.filter_intensity_slider = QSlider(Qt.Horizontal)
        self.filter_intensity_slider.setRange(1, 10)
        self.filter_intensity_slider.setValue(5)
        self.filter_intensity_spin = QSpinBox()
        self.filter_intensity_spin.setRange(1, 10)
        self.filter_intensity_spin.setValue(5)
        self.filter_intensity_slider.valueChanged.connect(self.filter_intensity_spin.setValue)
        self.filter_intensity_spin.valueChanged.connect(self.filter_intensity_slider.setValue)
        intensity_layout.addWidget(self.filter_intensity_slider)
        intensity_layout.addWidget(self.filter_intensity_spin)
        spectral_layout.addRow("Intensywność filtrowania:", intensity_layout)
        
        # Zakres widmowy
        self.spectral_range_min = QSpinBox()
        self.spectral_range_min.setRange(100, 5000)
        self.spectral_range_min.setValue(300)
        self.spectral_range_min.setSuffix(" nm")
        
        self.spectral_range_max = QSpinBox()
        self.spectral_range_max.setRange(100, 5000)
        self.spectral_range_max.setValue(1000)
        self.spectral_range_max.setSuffix(" nm")
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(self.spectral_range_min)
        range_layout.addWidget(QLabel("-"))
        range_layout.addWidget(self.spectral_range_max)
        
        spectral_layout.addRow("Zakres widmowy:", range_layout)
        
        # Opcje filtrowania
        self.remove_background = QCheckBox("Usuń tło")
        self.remove_background.setChecked(True)
        spectral_layout.addRow("", self.remove_background)
        
        self.normalize_spectra = QCheckBox("Normalizuj widma")
        self.normalize_spectra.setChecked(True)
        spectral_layout.addRow("", self.normalize_spectra)
        
        spectral_group.setLayout(spectral_layout)
        main_layout.addWidget(spectral_group)
        
        # Grupa korekcji zniekształceń
        correction_group = QGroupBox("Korekcja zniekształceń")
        correction_layout = QFormLayout()
        
        # Wybór modelu korekcji
        self.correction_model = QComboBox()
        self.correction_model.addItems(["Model liniowy", "Model kwadratowy", "Model atmosferyczny", "Bez korekcji"])
        correction_layout.addRow("Model korekcji:", self.correction_model)
        
        # Poziom korekcji
        correction_level_layout = QHBoxLayout()
        self.correction_level_slider = QSlider(Qt.Horizontal)
        self.correction_level_slider.setRange(0, 100)
        self.correction_level_slider.setValue(50)
        self.correction_level_spin = QSpinBox()
        self.correction_level_spin.setRange(0, 100)
        self.correction_level_spin.setValue(50)
        self.correction_level_spin.setSuffix("%")
        self.correction_level_slider.valueChanged.connect(self.correction_level_spin.setValue)
        self.correction_level_spin.valueChanged.connect(self.correction_level_slider.setValue)
        correction_level_layout.addWidget(self.correction_level_slider)
        correction_level_layout.addWidget(self.correction_level_spin)
        correction_layout.addRow("Poziom korekcji:", correction_level_layout)
        
        # Opcje korekcji
        self.correct_absorption = QCheckBox("Koryguj absorpcję atmosferyczną")
        self.correct_absorption.setChecked(True)
        correction_layout.addRow("", self.correct_absorption)
        
        self.correct_scattering = QCheckBox("Koryguj rozpraszanie")
        self.correct_scattering.setChecked(True)
        correction_layout.addRow("", self.correct_scattering)
        
        self.correct_interference = QCheckBox("Koryguj interferencję")
        self.correct_interference.setChecked(True)
        correction_layout.addRow("", self.correct_interference)
        
        correction_group.setLayout(correction_layout)
        main_layout.addWidget(correction_group)
        
        # Grupa ustawień wyświetlania
        display_group = QGroupBox("Ustawienia wyświetlania")
        display_layout = QFormLayout()
        
        # Wybór palety kolorów
        self.color_palette = QComboBox()
        self.color_palette.addItems(["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "Tęcza"])
        display_layout.addRow("Paleta kolorów:", self.color_palette)
        
        # Styl wykresu
        self.plot_style = QComboBox()
        self.plot_style.addItems(["Linie", "Punkty", "Linie i punkty", "Słupki", "Obszar"])
        display_layout.addRow("Styl wykresu:", self.plot_style)
        
        # Opcje wyświetlania
        self.show_grid = QCheckBox("Pokaż siatkę")
        self.show_grid.setChecked(True)
        display_layout.addRow("", self.show_grid)
        
        self.show_legend = QCheckBox("Pokaż legendę")
        self.show_legend.setChecked(True)
        display_layout.addRow("", self.show_legend)
        
        self.show_markers = QCheckBox("Pokaż znaczniki")
        self.show_markers.setChecked(False)
        display_layout.addRow("", self.show_markers)
        
        display_group.setLayout(display_layout)
        main_layout.addWidget(display_group)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
