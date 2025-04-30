#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QFont

class LogConsole(QWidget):
    """Konsola logów do monitorowania operacji systemowych"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika konsoli logów"""
        # Główny układ
        main_layout = QVBoxLayout()
        
        # Pole tekstowe dla logów
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        
        # Ustawienie czcionki o stałej szerokości
        font = QFont("Courier New", 9)
        self.log_text.setFont(font)
        
        # Ustawienie kolorów
        self.log_text.setStyleSheet("background-color: #f0f0f0; color: #000000;")
        
        main_layout.addWidget(self.log_text)
        
        # Ustawienie głównego układu
        self.setLayout(main_layout)
        
        # Dodanie początkowego komunikatu
        self.add_log("Aplikacja uruchomiona", "info")
        
    def add_log(self, message, level="info"):
        """
        Dodanie komunikatu do konsoli logów
        
        Parametry:
        - message: treść komunikatu
        - level: poziom komunikatu (info, warning, error, success)
        """
        # Utworzenie formatu tekstu w zależności od poziomu komunikatu
        text_format = QTextCharFormat()
        
        if level == "info":
            text_format.setForeground(QColor("#000000"))  # czarny
        elif level == "warning":
            text_format.setForeground(QColor("#FF8C00"))  # pomarańczowy
        elif level == "error":
            text_format.setForeground(QColor("#FF0000"))  # czerwony
        elif level == "success":
            text_format.setForeground(QColor("#008000"))  # zielony
        
        # Dodanie prefiksu w zależności od poziomu komunikatu
        if level == "info":
            prefix = "[INFO] "
        elif level == "warning":
            prefix = "[OSTRZEŻENIE] "
        elif level == "error":
            prefix = "[BŁĄD] "
        elif level == "success":
            prefix = "[SUKCES] "
        
        # Dodanie znacznika czasu
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Pełny komunikat
        full_message = f"[{timestamp}] {prefix}{message}"
        
        # Dodanie komunikatu do konsoli
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(full_message + "\n")
        
        # Przewinięcie do końca
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()
        
    def clear_logs(self):
        """Wyczyszczenie konsoli logów"""
        self.log_text.clear()
        self.add_log("Konsola wyczyszczona", "info")
