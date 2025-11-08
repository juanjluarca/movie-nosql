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
        self.setGeometry(300, 200, 400, 300)
        layout = QVBoxLayout()

        form = QFormLayout()
        self.usuario = QLineEdit()
        self.pais = QLineEdit()
        self.puntuacion = QSpinBox()
        self.puntuacion.setRange(1, 5)
        self.comentario = QTextEdit()

        form.addRow("Usuario:", self.usuario)
        form.addRow("País:", self.pais)
        form.addRow("Puntuación (1–5):", self.puntuacion)
        form.addRow("Comentario:", self.comentario)

        layout.addLayout(form)
        self.btn_save = QPushButton("Guardar")
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.save_review)
        self.setLayout(layout)

    def save_review(self):
        review = {
            "usuario": self.usuario.text(),
            "pais": self.pais.text(),
            "puntuacion": self.puntuacion.value(),
            "comentario": self.comentario.toPlainText(),
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }
        add_review(self.movie_id, review)
        QMessageBox.information(self, "Éxito", "Reseña agregada correctamente.")
        self.review_added.emit()
        self.close()
