#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMatrix4x4, QVector3D
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class Visualization3DModule(QWidget):
    """Moduł wizualizacji 3D planet i ich atmosfer"""
    
    def __init__(self):
        super().__init__()
        # Inicjalizacja zmiennych do przechowywania elementów sceny
        self.planet_mesh = None
        self.atmosphere_mesh = None
        self.critical_zones = []
        
        # Inicjalizacja interfejsu
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika modułu wizualizacji 3D"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Panel kontrolny
        control_layout = QHBoxLayout()
        
        # Etykieta informacyjna
        info_label = QLabel("Wizualizacja 3D planety i jej atmosfery")
        info_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(info_label)
        
        # Etykieta statusu symulacji
        self.simulation_status_label = QLabel("Status symulacji: Brak aktywnej symulacji")
        self.simulation_status_label.setAlignment(Qt.AlignRight)
        control_layout.addWidget(self.simulation_status_label)
        
        main_layout.addLayout(control_layout)
        
        # Widżet OpenGL do renderowania 3D
        self.view_3d = gl.GLViewWidget()
        main_layout.addWidget(self.view_3d)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
        # Inicjalizacja sceny 3D
        self.init_3d_scene()
        
    def init_3d_scene(self):
        """Inicjalizacja sceny 3D z planetą i atmosferą"""
        # Ustawienie kamery
        self.view_3d.setCameraPosition(distance=40)
        
        # Dodanie siatki
        grid = gl.GLGridItem()
        grid.setSize(200, 200)
        grid.setSpacing(10, 10)
        self.view_3d.addItem(grid)
        
        # Tworzenie planety (sfera)
        planet_radius = 10
        self.planet_mesh = self.create_sphere(radius=planet_radius, rows=20, cols=20, color=(0.5, 0.5, 1.0, 1.0))
        self.view_3d.addItem(self.planet_mesh)
        
        # Tworzenie atmosfery (półprzezroczysta sfera)
        atmosphere_radius = 12
        self.atmosphere_mesh = self.create_sphere(radius=atmosphere_radius, rows=20, cols=20, color=(0.6, 0.8, 1.0, 0.3))
        self.view_3d.addItem(self.atmosphere_mesh)
        
        # Dodanie osi
        axis_x = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [20, 0, 0]]), color=(1, 0, 0, 1), width=2)
        axis_y = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 20, 0]]), color=(0, 1, 0, 1), width=2)
        axis_z = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, 20]]), color=(0, 0, 1, 1), width=2)
        self.view_3d.addItem(axis_x)
        self.view_3d.addItem(axis_y)
        self.view_3d.addItem(axis_z)
        
        # Dodanie etykiet osi
        self.add_text_label("X", pos=(21, 0, 0), color=(255, 0, 0, 255))
        self.add_text_label("Y", pos=(0, 21, 0), color=(0, 255, 0, 255))
        self.add_text_label("Z", pos=(0, 0, 21), color=(0, 0, 255, 255))
        
        # Dodanie przykładowych stref krytycznych
        self.add_critical_zone(pos=(5, 5, 8), radius=2, color=(1, 0, 0, 0.7), label="Strefa A")
        self.add_critical_zone(pos=(-7, 3, 5), radius=1.5, color=(1, 0.5, 0, 0.7), label="Strefa B")
        
    def create_sphere(self, radius=10, rows=10, cols=20, color=(1.0, 1.0, 1.0, 1.0)):
        """Tworzenie siatki sferycznej dla planety lub atmosfery"""
        # Generowanie wierzchołków i kolorów
        vertices = []
        colors = []
        
        for i in range(rows+1):
            phi = np.pi * i / rows
            for j in range(cols):
                theta = 2 * np.pi * j / cols
                
                x = radius * np.sin(phi) * np.cos(theta)
                y = radius * np.sin(phi) * np.sin(theta)
                z = radius * np.cos(phi)
                
                vertices.append([x, y, z])
                colors.append(color)
        
        # Generowanie indeksów dla trójkątów
        indices = []
        for i in range(rows):
            for j in range(cols):
                p1 = i * cols + j
                p2 = i * cols + (j + 1) % cols
                p3 = (i + 1) * cols + j
                p4 = (i + 1) * cols + (j + 1) % cols
                
                # Dwa trójkąty tworzące czworokąt
                indices.append([p1, p2, p3])
                indices.append([p2, p4, p3])
        
        # Tworzenie siatki
        mesh = gl.GLMeshItem(
            vertexes=np.array(vertices),
            faces=np.array(indices),
            faceColors=np.array([color for _ in range(len(indices))]),
            smooth=True,
            drawEdges=False,
            shader='shaded'
        )
        
        return mesh
    
    def add_text_label(self, text, pos, color=(255, 255, 255, 255)):
        """Dodanie etykiety tekstowej do sceny 3D"""
        text_item = gl.GLTextItem(pos=pos, text=text, color=color)
        self.view_3d.addItem(text_item)
        
    def add_critical_zone(self, pos, radius=1.0, color=(1.0, 0.0, 0.0, 0.7), label=None):
        """Dodanie strefy krytycznej do sceny 3D"""
        # Dodanie sfery reprezentującej strefę krytyczną
        sphere = self.create_sphere(radius=radius, rows=10, cols=10, color=color)
        sphere.translate(pos[0], pos[1], pos[2])
        self.view_3d.addItem(sphere)
        
        # Dodanie etykiety dla strefy
        if label:
            self.add_text_label(label, (pos[0], pos[1], pos[2] + radius + 0.5))
            
        # Zapisanie strefy do listy
        self.critical_zones.append({
            'mesh': sphere,
            'pos': pos,
            'radius': radius,
            'color': color,
            'label': label
        })
        
        return sphere
            
    def update_planet_model(self, planet_data):
        """Aktualizacja modelu planety na podstawie danych"""
        # Ta metoda byłaby używana do aktualizacji modelu 3D na podstawie danych z symulacji
        # W rzeczywistej aplikacji byłaby bardziej rozbudowana
        pass
        
    def update_simulation_data(self, progress, habitability_index, temperature, pressure, radiation, atmosphere_data):
        """Aktualizacja wizualizacji 3D na podstawie danych symulacji"""
        # Aktualizacja etykiety statusu
        self.simulation_status_label.setText(f"Status symulacji: {progress}% - Indeks habitabilności: {habitability_index}")
        
        # Aktualizacja koloru planety na podstawie temperatury
        if temperature < 200:
            planet_color = (0.2, 0.2, 0.8, 1.0)  # Zimna (niebieska)
        elif temperature < 300:
            planet_color = (0.5, 0.5, 1.0, 1.0)  # Umiarkowana (jasnoniebieska)
        elif temperature < 400:
            planet_color = (0.8, 0.8, 0.2, 1.0)  # Ciepła (żółta)
        else:
            planet_color = (0.8, 0.2, 0.2, 1.0)  # Gorąca (czerwona)
            
        # Aktualizacja koloru atmosfery na podstawie składu
        oxygen = atmosphere_data.get('oxygen', 21)
        nitrogen = atmosphere_data.get('nitrogen', 78)
        co2 = atmosphere_data.get('co2', 0)
        
        # Kolor atmosfery zależny od składu
        r = 0.6 + 0.4 * (co2 / 100)  # Więcej CO2 = bardziej czerwona
        g = 0.6 + 0.4 * (oxygen / 100)  # Więcej tlenu = bardziej zielona
        b = 0.6 + 0.4 * (nitrogen / 100)  # Więcej azotu = bardziej niebieska
        
        atmosphere_color = (r, g, b, 0.3)
        
        # Aktualizacja rozmiaru atmosfery na podstawie ciśnienia
        atmosphere_radius = 12 + pressure / 50  # Większe ciśnienie = większa atmosfera
        
        # Usunięcie starych modeli
        if self.planet_mesh is not None:
            self.view_3d.removeItem(self.planet_mesh)
        if self.atmosphere_mesh is not None:
            self.view_3d.removeItem(self.atmosphere_mesh)
            
        # Utworzenie nowych modeli
        self.planet_mesh = self.create_sphere(radius=10, rows=20, cols=20, color=planet_color)
        self.atmosphere_mesh = self.create_sphere(radius=atmosphere_radius, rows=20, cols=20, color=atmosphere_color)
        
        # Dodanie nowych modeli do sceny
        self.view_3d.addItem(self.planet_mesh)
        self.view_3d.addItem(self.atmosphere_mesh)
        
        # Aktualizacja stref krytycznych na podstawie habitabilności
        # Usunięcie starych stref
        for zone in self.critical_zones:
            self.view_3d.removeItem(zone['mesh'])
        self.critical_zones = []
        
        # Dodanie nowych stref w zależności od habitabilności
        if habitability_index < 30:
            # Niski indeks habitabilności - dodaj strefy niebezpieczne
            self.add_critical_zone(pos=(5, 5, 8), radius=3, color=(0.8, 0.0, 0.0, 0.7), label="Strefa niebezpieczna")
            self.add_critical_zone(pos=(-7, 3, 5), radius=2.5, color=(0.8, 0.0, 0.0, 0.7), label="Strefa niebezpieczna")
            self.add_critical_zone(pos=(0, -6, 7), radius=2, color=(0.8, 0.0, 0.0, 0.7), label="Strefa niebezpieczna")
        elif habitability_index < 70:
            # Średni indeks habitabilności - dodaj strefy umiarkowane
            self.add_critical_zone(pos=(5, 5, 8), radius=2, color=(0.8, 0.8, 0.0, 0.7), label="Strefa umiarkowana")
            self.add_critical_zone(pos=(-7, 3, 5), radius=1.5, color=(0.8, 0.8, 0.0, 0.7), label="Strefa umiarkowana")
        else:
            # Wysoki indeks habitabilności - dodaj strefy bezpieczne
            self.add_critical_zone(pos=(5, 5, 8), radius=2, color=(0.0, 0.8, 0.0, 0.7), label="Strefa bezpieczna")
            self.add_critical_zone(pos=(-7, 3, 5), radius=1.5, color=(0.0, 0.8, 0.0, 0.7), label="Strefa bezpieczna")
            self.add_critical_zone(pos=(0, -6, 7), radius=2, color=(0.0, 0.8, 0.0, 0.7), label="Strefa bezpieczna")
