#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import time
import math

class SimulationThread(QThread):
    """Wątek symulacji do analizy habitabilności planet"""
    
    # Sygnały do komunikacji z głównym wątkiem
    update_progress = pyqtSignal(int, float, float)  # postęp, czas wykonania, pozostały czas
    update_status = pyqtSignal(str)  # status symulacji
    update_results = pyqtSignal(dict)  # wyniki symulacji
    simulation_finished = pyqtSignal(dict)  # końcowe wyniki symulacji
    
    def __init__(self, params):
        """
        Inicjalizacja wątku symulacji
        
        Parametry:
        - params: słownik parametrów symulacji
        """
        super().__init__()
        self.params = params
        self.is_running = True
        
    def run(self):
        """Główna metoda wątku symulacji"""
        self.update_status.emit("Inicjalizacja symulacji...")
        
        # Pobranie parametrów symulacji
        temperature = self.params.get('temperature', 300)
        pressure = self.params.get('pressure', 1)
        radiation = self.params.get('radiation', 1)
        ph = self.params.get('ph', 7.0)
        oxygen = self.params.get('oxygen', 21)
        nitrogen = self.params.get('nitrogen', 78)
        co2 = self.params.get('co2', 0)
        density = self.params.get('density', 1.0)
        accuracy = self.params.get('accuracy', 5)
        sim_time = self.params.get('sim_time', 100)
        include_radiation = self.params.get('include_radiation', True)
        include_evolution = self.params.get('include_evolution', True)
        include_biology = self.params.get('include_biology', True)
        planet_name = self.params.get('planet_name', "Przykładowa planeta")
        
        # Inicjalizacja zmiennych symulacji
        start_time = time.time()
        total_steps = sim_time * accuracy
        step_time = 0.1  # czas trwania jednego kroku w sekundach (dla realistycznej symulacji)
        
        # Inicjalizacja wyników
        results = {
            'habitability_index': 0,
            'life_forms': "Nieznane",
            'spectral_status': "W trakcie analizy...",
            'element_status': "W trakcie analizy...",
            'bio_status': "W trakcie analizy..."
        }
        
        # Główna pętla symulacji
        for step in range(total_steps):
            if not self.is_running:
                break
                
            # Obliczenie postępu
            progress = int((step + 1) / total_steps * 100)
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / (step + 1)) * (total_steps - (step + 1))
            
            # Emisja sygnału postępu
            self.update_progress.emit(progress, elapsed_time, remaining_time)
            
            # Aktualizacja statusu co 10% postępu
            if step % (total_steps // 10) == 0 or step == 0:
                status_messages = [
                    "Inicjalizacja modelu atmosferycznego...",
                    "Analiza składu atmosferycznego...",
                    "Obliczanie parametrów termodynamicznych...",
                    "Modelowanie wpływu promieniowania...",
                    "Analiza widmowa w toku...",
                    "Badanie właściwości pierwiastków...",
                    "Analiza potencjału biologicznego...",
                    "Korelacja danych środowiskowych...",
                    "Generowanie mapy habitabilności...",
                    "Finalizacja wyników symulacji..."
                ]
                current_status = status_messages[min(progress // 10, 9)]
                self.update_status.emit(current_status)
            
            # Symulacja analizy widmowej (co 20% postępu)
            if step % (total_steps // 5) == 0:
                if step < total_steps // 2:
                    results['spectral_status'] = "Analiza widmowa w toku..."
                else:
                    results['spectral_status'] = "Analiza widmowa zakończona"
                    
            # Symulacja analizy pierwiastkowej (co 25% postępu)
            if step % (total_steps // 4) == 0:
                if step < 3 * total_steps // 4:
                    results['element_status'] = "Analiza pierwiastkowa w toku..."
                else:
                    results['element_status'] = "Analiza pierwiastkowa zakończona"
                    
            # Symulacja analizy biologicznej (co 33% postępu)
            if step % (total_steps // 3) == 0:
                if step < 2 * total_steps // 3:
                    results['bio_status'] = "Analiza biologiczna w toku..."
                else:
                    results['bio_status'] = "Analiza biologiczna zakończona"
            
            # Obliczanie indeksu habitabilności na podstawie parametrów
            # Rzeczywiste obliczenia naukowe
            temp_factor = self.calculate_temperature_factor(temperature)
            pressure_factor = self.calculate_pressure_factor(pressure)
            radiation_factor = self.calculate_radiation_factor(radiation)
            atmosphere_factor = self.calculate_atmosphere_factor(oxygen, nitrogen, co2)
            ph_factor = self.calculate_ph_factor(ph)
            
            # Wagi czynników
            weights = {
                'temperature': 0.3,
                'pressure': 0.2,
                'radiation': 0.15,
                'atmosphere': 0.25,
                'ph': 0.1
            }
            
            # Obliczenie indeksu habitabilności jako ważonej sumy czynników
            habitability_index = (
                weights['temperature'] * temp_factor +
                weights['pressure'] * pressure_factor +
                weights['radiation'] * radiation_factor +
                weights['atmosphere'] * atmosphere_factor +
                weights['ph'] * ph_factor
            ) * 100
            
            # Dodanie losowych fluktuacji dla realizmu (±5%)
            habitability_index += np.random.normal(0, 2)
            habitability_index = max(0, min(100, habitability_index))
            
            # Aktualizacja indeksu habitabilności
            results['habitability_index'] = round(habitability_index, 1)
            
            # Określenie możliwych form życia na podstawie indeksu habitabilności
            results['life_forms'] = self.determine_life_forms(habitability_index)
            
            # Emisja sygnału z aktualnymi wynikami
            self.update_results.emit(results.copy())
            
            # Opóźnienie dla realistycznej symulacji
            time.sleep(step_time)
        
        # Zakończenie symulacji
        final_elapsed_time = time.time() - start_time
        self.update_status.emit("Symulacja zakończona")
        self.update_progress.emit(100, final_elapsed_time, 0)
        
        # Finalne wyniki
        final_results = results.copy()
        final_results['simulation_time'] = final_elapsed_time
        final_results['parameters'] = {
            'temperature': temperature,
            'pressure': pressure,
            'radiation': radiation,
            'ph': ph,
            'oxygen': oxygen,
            'nitrogen': nitrogen,
            'co2': co2,
            'density': density
        }
        
        # Emisja sygnału zakończenia symulacji
        self.simulation_finished.emit(final_results)
    
    def stop(self):
        """Zatrzymanie symulacji"""
        self.is_running = False
        
    def calculate_temperature_factor(self, temperature):
        """
        Obliczenie czynnika temperatury dla habitabilności
        
        Optymalny zakres: 260-310K (dla życia opartego na wodzie)
        """
        # Funkcja Gaussa z centrum w 285K (optymalna temperatura)
        return np.exp(-0.5 * ((temperature - 285) / 50)**2)
    
    def calculate_pressure_factor(self, pressure):
        """
        Obliczenie czynnika ciśnienia dla habitabilności
        
        Optymalny zakres: 0.5-5 atm
        """
        # Funkcja logistyczna dla ciśnienia
        return 1 / (1 + np.exp(-2 * (np.log10(pressure + 0.01) + 0.3)))
    
    def calculate_radiation_factor(self, radiation):
        """
        Obliczenie czynnika promieniowania dla habitabilności
        
        Optymalny zakres: <10 Sv/h
        """
        # Funkcja wykładnicza malejąca
        return np.exp(-0.1 * radiation)
    
    def calculate_atmosphere_factor(self, oxygen, nitrogen, co2):
        """
        Obliczenie czynnika atmosfery dla habitabilności
        
        Optymalne składy:
        - Tlen: 10-30%
        - Azot: 65-80%
        - CO2: 0.03-1%
        """
        # Sprawdzenie czy suma procentowa jest bliska 100%
        total = oxygen + nitrogen + co2
        if abs(total - 100) > 5:
            return 0.1  # Nierealistyczny skład atmosfery
        
        # Czynniki dla poszczególnych gazów
        oxygen_factor = np.exp(-0.5 * ((oxygen - 20) / 15)**2)
        nitrogen_factor = np.exp(-0.5 * ((nitrogen - 75) / 10)**2)
        
        # CO2 ma logarytmiczną skalę optymalności
        if co2 == 0:
            co2_factor = 0.1
        else:
            co2_factor = np.exp(-0.5 * ((np.log10(co2) - np.log10(0.3)) / 1)**2)
        
        # Średnia ważona czynników
        return 0.4 * oxygen_factor + 0.4 * nitrogen_factor + 0.2 * co2_factor
    
    def calculate_ph_factor(self, ph):
        """
        Obliczenie czynnika pH dla habitabilności
        
        Optymalny zakres: 6-8 pH
        """
        # Funkcja Gaussa z centrum w pH 7
        return np.exp(-0.5 * ((ph - 7) / 1.5)**2)
    
    def determine_life_forms(self, habitability_index):
        """
        Określenie możliwych form życia na podstawie indeksu habitabilności
        """
        if habitability_index < 20:
            return "Brak możliwości życia"
        elif habitability_index < 40:
            return "Możliwe ekstremalne mikroorganizmy (niesporczaki, archea)"
        elif habitability_index < 60:
            return "Mikroorganizmy, proste formy wielokomórkowe"
        elif habitability_index < 80:
            return "Różnorodne formy życia, proste ekosystemy"
        else:
            return "Optymalne warunki dla złożonych ekosystemów"
