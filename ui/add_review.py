from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QSpinBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
from models.movie_model import add_review

class AddReviewWindow(QWidget):
    review_added = pyqtSignal()

    def __init__(self, movie_id):
        super().__init__()
        self.movie_id = movie_id
        self.setWindowTitle("Agregar Reseña")
        self.setGeometry(300, 200, 450, 380)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
            QLineEdit, QTextEdit, QSpinBox {
                padding: 8px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QLabel {
                font-size: 13px;
                color: #b0b0b0;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        form = QFormLayout()
        form.setSpacing(10)
        
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Tu nombre")
        
        self.pais = QLineEdit()
        self.pais.setPlaceholderText("Tu país")
        
        self.puntuacion = QSpinBox()
        self.puntuacion.setRange(1, 5)
        self.puntuacion.setValue(5)
        
        self.comentario = QTextEdit()
        self.comentario.setPlaceholderText("Escribe tu opinión sobre la película...")
        self.comentario.setMaximumHeight(120)

        form.addRow("Usuario:", self.usuario)
        form.addRow("País:", self.pais)
        form.addRow("Puntuación (1—5):", self.puntuacion)
        form.addRow("Comentario:", self.comentario)

        layout.addLayout(form)
        self.btn_save = QPushButton("Guardar Reseña")
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.save_review)
        self.setLayout(layout)

    def save_review(self):
        if not self.usuario.text() or not self.comentario.toPlainText():
            QMessageBox.warning(self, "Campos requeridos", "Por favor completa todos los campos.")
            return
        
        review = {
            "usuario": self.usuario.text(),
            "pais": self.pais.text() or "N/A",
            "puntuacion": self.puntuacion.value(),
            "comentario": self.comentario.toPlainText(),
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }
        add_review(self.movie_id, review)
        QMessageBox.information(self, "Éxito", "Reseña agregada correctamente.")
        self.review_added.emit()
        self.close()