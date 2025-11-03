from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QSpinBox, QPushButton, QMessageBox
)
from datetime import datetime

class AddReviewWindow(QWidget):
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
        if not self.usuario.text() or not self.pais.text() or not self.comentario.toPlainText():
            QMessageBox.warning(
                self,
                "Campos incompletos",
                "Por favor complete todos los campos."
            )
            return
        
        QMessageBox.information(
            self,
            "testing",
            f"Reseña agregada correctamente."
        )
        self.close()