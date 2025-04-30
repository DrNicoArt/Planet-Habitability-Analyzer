#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QDockWidget, QStatusBar
from PyQt5.QtWidgets import QAction, QToolBar, QMenu, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from modules.spectral_module import SpectralModule
from modules.element_module import ElementModule
from modules.biological_module import BiologicalModule
from modules.visualization_3d import Visualization3DModule
from modules.input_panel import InputPanel
from modules.simulation_panel import SimulationPanel
from modules.filter_panel import FilterPanel
from modules.log_console import LogConsole
from modules.info_panel import InfoPanel
from modules.simulation_thread import SimulationThread

class HabitabilityAnalyzer(QMainWindow):
    """
    Główne okno aplikacji do analizy habitabilności planet.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizator Habitabilności Planet")
        self.setMinimumSize(1200, 800)
        
        # Inicjalizacja wątku symulacji
        self.simulation_thread = None
        
        # Inicjalizacja interfejsu użytkownika
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        # Utworzenie menu głównego
        self.create_menu()
        
        # Utworzenie paska narzędzi
        self.create_toolbar()
        
        # Utworzenie centralnego obszaru roboczego z zakładkami
        self.create_central_widget()
        
        # Utworzenie paneli bocznych
        self.create_dock_widgets()
        
        # Utworzenie panelu dolnego
        self.create_bottom_panel()
        
        # Utworzenie paska statusu
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Gotowy")
        
        # Wyświetlenie okna
        self.show()
        
    def create_menu(self):
        """Tworzenie menu głównego aplikacji"""
        # Menu Plik
        file_menu = self.menuBar().addMenu("&Plik")
        
        new_action = QAction("&Nowy projekt", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Otwórz", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Zapisz", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("&Eksportuj wyniki", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Zamknij aplikację", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Edycja
        edit_menu = self.menuBar().addMenu("&Edycja")
        
        settings_action = QAction("&Ustawienia aplikacji", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)
        
        # Menu Widok
        view_menu = self.menuBar().addMenu("&Widok")
        
        fullscreen_action = QAction("&Tryb pełnoekranowy", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Menu Pomoc
        help_menu = self.menuBar().addMenu("&Pomoc")
        
        doc_action = QAction("&Dokumentacja", self)
        doc_action.triggered.connect(self.show_documentation)
        help_menu.addAction(doc_action)
        
        about_action = QAction("&O programie", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Tworzenie paska narzędzi"""
        toolbar = QToolBar("Główny pasek narzędzi")
        self.addToolBar(toolbar)
        
        # Dodanie akcji do paska narzędzi
        import_action = QAction("Importuj dane", self)
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)
        
        self.simulate_action = QAction("Rozpocznij symulację", self)
        self.simulate_action.triggered.connect(self.start_simulation)
        toolbar.addAction(self.simulate_action)
        
        self.stop_simulation_action = QAction("Zatrzymaj symulację", self)
        self.stop_simulation_action.triggered.connect(self.stop_simulation)
        self.stop_simulation_action.setEnabled(False)
        toolbar.addAction(self.stop_simulation_action)
        
        save_session_action = QAction("Zapisz sesję", self)
        save_session_action.triggered.connect(self.save_session)
        toolbar.addAction(save_session_action)
        
        reset_view_action = QAction("Reset widoku", self)
        reset_view_action.triggered.connect(self.reset_view)
        toolbar.addAction(reset_view_action)
        
    def create_central_widget(self):
        """Tworzenie centralnego obszaru roboczego z zakładkami"""
        self.tab_widget = QTabWidget()
        
        # Zakładka Widmowa
        self.spectral_module = SpectralModule()
        self.tab_widget.addTab(self.spectral_module, "Analiza Widmowa")
        
        # Zakładka Pierwiastkowa
        self.element_module = ElementModule()
        self.tab_widget.addTab(self.element_module, "Analiza Pierwiastków")
        
        # Zakładka Biologiczna
        self.biological_module = BiologicalModule()
        self.tab_widget.addTab(self.biological_module, "Analiza Biologiczna")
        
        # Zakładka 3D
        self.visualization_3d = Visualization3DModule()
        self.tab_widget.addTab(self.visualization_3d, "Wizualizacja 3D")
        
        self.setCentralWidget(self.tab_widget)
        
    def create_dock_widgets(self):
        """Tworzenie paneli bocznych (dock widgets)"""
        # Panel danych wejściowych
        self.input_dock = QDockWidget("Dane Wejściowe", self)
        self.input_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.input_panel = InputPanel()
        self.input_dock.setWidget(self.input_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.input_dock)
        
        # Panel parametrów symulacji
        self.simulation_dock = QDockWidget("Parametry Symulacji", self)
        self.simulation_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.simulation_panel = SimulationPanel()
        self.simulation_dock.setWidget(self.simulation_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.simulation_dock)
        
        # Panel filtrów i ustawień
        self.filter_dock = QDockWidget("Filtry i Ustawienia", self)
        self.filter_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.filter_panel = FilterPanel()
        self.filter_dock.setWidget(self.filter_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.filter_dock)
        
        # Ustawienie zakładek dla paneli bocznych
        self.tabifyDockWidget(self.input_dock, self.simulation_dock)
        self.tabifyDockWidget(self.simulation_dock, self.filter_dock)
        self.input_dock.raise_()
        
    def create_bottom_panel(self):
        """Tworzenie panelu dolnego"""
        # Panel dolny z konsolą logów i panelem informacji
        bottom_dock = QDockWidget("Panel Dolny", self)
        bottom_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        # Konsola logów
        self.log_console = LogConsole()
        bottom_layout.addWidget(self.log_console)
        
        # Panel informacji
        self.info_panel = InfoPanel()
        bottom_layout.addWidget(self.info_panel)
        
        bottom_dock.setWidget(bottom_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottom_dock)
        
    # Metody obsługi zdarzeń
    def new_project(self):
        """Tworzenie nowego projektu"""
        self.log_console.add_log("Tworzenie nowego projektu...")
        # Implementacja tworzenia nowego projektu
        
    def open_project(self):
        """Otwieranie istniejącego projektu"""
        self.log_console.add_log("Otwieranie projektu...")
        # Implementacja otwierania projektu
        
    def save_project(self):
        """Zapisywanie projektu"""
        self.log_console.add_log("Zapisywanie projektu...")
        # Implementacja zapisywania projektu
        
    def export_results(self):
        """Eksportowanie wyników"""
        self.log_console.add_log("Eksportowanie wyników...")
        # Implementacja eksportowania wyników
        
    def show_settings(self):
        """Wyświetlanie ustawień aplikacji"""
        self.log_console.add_log("Otwieranie ustawień aplikacji...")
        # Implementacja wyświetlania ustawień
        
    def toggle_fullscreen(self, checked):
        """Przełączanie trybu pełnoekranowego"""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
            
    def show_documentation(self):
        """Wyświetlanie dokumentacji"""
        self.log_console.add_log("Otwieranie dokumentacji...")
        # Implementacja wyświetlania dokumentacji
        
    def show_about(self):
        """Wyświetlanie informacji o programie"""
        QMessageBox.about(self, "O programie", 
                         "Analizator Habitabilności Planet\n\n"
                         "Interdyscyplinarne narzędzie badawcze do analizy warunków habitabilności planet.\n\n"
                         "Wersja: 1.0.0")
        
    def import_data(self):
        """Importowanie danych"""
        self.log_console.add_log("Importowanie danych...")
        # Implementacja importowania danych
        
    def get_simulation_parameters(self):
        """Pobieranie parametrów symulacji z interfejsu użytkownika"""
        params = {
            'temperature': self.simulation_panel.temp_spin.value(),
            'pressure': self.simulation_panel.pressure_spin.value(),
            'radiation': self.simulation_panel.radiation_spin.value(),
            'ph': self.simulation_panel.ph_spin.value(),
            'oxygen': self.simulation_panel.oxygen_spin.value(),
            'nitrogen': self.simulation_panel.nitrogen_spin.value(),
            'co2': self.simulation_panel.co2_spin.value(),
            'density': self.simulation_panel.density_spin.value(),
            'accuracy': self.simulation_panel.accuracy_spin.value(),
            'sim_time': self.simulation_panel.time_spin.value(),
            'include_radiation': self.simulation_panel.include_radiation.isChecked(),
            'include_evolution': self.simulation_panel.include_evolution.isChecked(),
            'include_biology': self.simulation_panel.include_biology.isChecked(),
            'planet_name': self.input_panel.planet_name.text()
        }
        return params
        
    def start_simulation(self):
        """Rozpoczęcie symulacji"""
        # Sprawdzenie czy symulacja już nie jest uruchomiona
        if self.simulation_thread is not None and self.simulation_thread.isRunning():
            self.log_console.add_log("Symulacja już jest uruchomiona", "warning")
            return
            
        self.log_console.add_log("Rozpoczynanie symulacji...", "info")
        self.statusBar.showMessage("Symulacja w toku...")
        
        # Aktualizacja interfejsu
        self.simulate_action.setEnabled(False)
        self.stop_simulation_action.setEnabled(True)
        
        # Pobranie parametrów symulacji
        params = self.get_simulation_parameters()
        
        # Aktualizacja panelu informacji z parametrami
        atmosphere_text = f"O₂: {params['oxygen']}%, N₂: {params['nitrogen']}%, CO₂: {params['co2']}%"
        self.info_panel.update_parameters(
            params['planet_name'],
            params['temperature'],
            params['pressure'],
            params['radiation'],
            atmosphere_text
        )
        
        # Inicjalizacja i uruchomienie wątku symulacji
        self.simulation_thread = SimulationThread(params)
        
        # Połączenie sygnałów
        self.simulation_thread.update_progress.connect(self.update_simulation_progress)
        self.simulation_thread.update_status.connect(self.update_simulation_status)
        self.simulation_thread.update_results.connect(self.update_simulation_results)
        self.simulation_thread.simulation_finished.connect(self.simulation_finished)
        
        # Uruchomienie wątku
        self.simulation_thread.start()
        
    def stop_simulation(self):
        """Zatrzymanie symulacji"""
        if self.simulation_thread is not None and self.simulation_thread.isRunning():
            self.log_console.add_log("Zatrzymywanie symulacji...", "warning")
            self.simulation_thread.stop()
            self.simulation_thread.wait()  # Czekanie na zakończenie wątku
            self.log_console.add_log("Symulacja zatrzymana", "warning")
            self.statusBar.showMessage("Symulacja zatrzymana")
            
            # Aktualizacja interfejsu
            self.simulate_action.setEnabled(True)
            self.stop_simulation_action.setEnabled(False)
        
    def update_simulation_progress(self, progress, elapsed_time, remaining_time):
        """Aktualizacja postępu symulacji"""
        self.info_panel.update_simulation_status(
            self.info_panel.simulation_status.text(),
            progress,
            round(elapsed_time, 1),
            round(remaining_time, 1)
        )
        
    def update_simulation_status(self, status):
        """Aktualizacja statusu symulacji"""
        self.info_panel.simulation_status.setText(status)
        self.log_console.add_log(status, "info")
        self.statusBar.showMessage(status)
        
    def update_simulation_results(self, results):
        """Aktualizacja wyników symulacji"""
        # Aktualizacja panelu informacji
        self.info_panel.update_results(
            results['habitability_index'],
            results['life_forms'],
            results['spectral_status'],
            results['element_status'],
            results['bio_status']
        )
        
        # Pobieranie aktualnych parametrów
        params = self.get_simulation_parameters()
        
        # Aktualizacja modułu widmowego
        elapsed_time = self.info_panel.simulation_time.text().replace("Czas: ", "").replace("s", "")
        try:
            elapsed_time = float(elapsed_time)
        except ValueError:
            elapsed_time = 0
            
        self.spectral_module.update_simulation_data(
            elapsed_time,
            results['habitability_index'],
            params['temperature'],
            params['pressure']
        )
        
        # Aktualizacja modułu pierwiastkowego
        # Przykładowe dane o pierwiastkach
        element_data = {
            'O': 0.2 + 0.6 * (1 - np.exp(-0.05 * elapsed_time)),
            'N': 0.8 - 0.3 * (1 - np.exp(-0.02 * elapsed_time)),
            'C': 0.1 + 0.05 * np.sin(0.2 * elapsed_time),
            'H': 0.5 * np.exp(-0.03 * elapsed_time),
            'Fe': 0.05 + 0.02 * (1 - np.exp(-0.01 * elapsed_time))
        }
        
        self.element_module.update_simulation_data(
            elapsed_time,
            element_data
        )
        
        # Aktualizacja modułu biologicznego
        # Przykładowe dane o organizmach
        organism_data = {}
        for organism in self.biological_module.organisms.keys():
            # Różne wzorce przeżywalności dla różnych organizmów
            if "Niesporczak" in organism:
                viability = 80 + 10 * np.sin(0.05 * elapsed_time)
            elif "Deinococcus" in organism:
                viability = 60 + 20 * np.sin(0.1 * elapsed_time)
            elif "Thermococcus" in organism:
                viability = 40 + 30 * np.sin(0.15 * elapsed_time)
            elif "coli" in organism:
                viability = 30 + 20 * np.sin(0.2 * elapsed_time)
            else:  # Homo sapiens
                viability = 20 + 10 * np.sin(0.25 * elapsed_time)
                
            viability = max(0, min(100, viability))
            organism_data[organism] = viability
            
        self.biological_module.update_simulation_data(
            elapsed_time,
            results['habitability_index'],
            organism_data
        )
        
        # Aktualizacja wizualizacji 3D
        atmosphere_data = {
            'oxygen': params['oxygen'],
            'nitrogen': params['nitrogen'],
            'co2': params['co2']
        }
        
        self.visualization_3d.update_simulation_data(
            int(self.info_panel.simulation_progress.value()),
            results['habitability_index'],
            params['temperature'],
            params['pressure'],
            params['radiation'],
            atmosphere_data
        )
        
    def simulation_finished(self, results):
        """Obsługa zakończenia symulacji"""
        self.log_console.add_log("Symulacja zakończona", "success")
        self.statusBar.showMessage("Symulacja zakończona")
        
        # Aktualizacja interfejsu
        self.simulate_action.setEnabled(True)
        self.stop_simulation_action.setEnabled(False)
        
        # Wyświetlenie komunikatu o zakończeniu
        QMessageBox.information(self, "Symulacja zakończona",
                               f"Symulacja zakończona z indeksem habitabilności: {results['habitability_index']}\n"
                               f"Możliwe formy życia: {results['life_forms']}\n"
                               f"Czas symulacji: {round(results['simulation_time'], 1)} sekund")
        
    def save_session(self):
        """Zapisywanie sesji"""
        self.log_console.add_log("Zapisywanie sesji...")
        # Implementacja zapisywania sesji
        
    def reset_view(self):
        """Reset widoku"""
        self.log_console.add_log("Resetowanie widoku...")
        # Implementacja resetowania widoku
        
    def closeEvent(self, event):
        """Obsługa zdarzenia zamknięcia aplikacji"""
        # Zatrzymanie wątku symulacji, jeśli jest uruchomiony
        if self.simulation_thread is not None and self.simulation_thread.isRunning():
            reply = QMessageBox.question(self, 'Symulacja w toku',
                                        "Symulacja jest w toku. Czy na pewno chcesz zamknąć aplikację?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.simulation_thread.stop()
                self.simulation_thread.wait()
                event.accept()
            else:
                event.ignore()
                return
        
        reply = QMessageBox.question(self, 'Zamknięcie aplikacji',
                                     "Czy na pewno chcesz zamknąć aplikację?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HabitabilityAnalyzer()
    sys.exit(app.exec_())
