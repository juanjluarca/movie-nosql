from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from models.movie_model import add_movie, update_movie

class AddMovieWindow(QDialog):
    def __init__(self, parent=None, edit_mode=False, movie=None):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.movie = movie

        self.setWindowTitle("Editar Película" if edit_mode else "Agregar Película")
        self.setGeometry(350, 200, 450, 400)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QLabel {
                font-size: 13px;
                color: #b0b0b0;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)

        form = QFormLayout()
        form.setSpacing(10)
        
        self.titulo = QLineEdit()
        self.anio = QLineEdit()
        self.genero = QLineEdit()
        self.director = QLineEdit()
        self.imagen_url = QLineEdit()
        self.imagen_url.setPlaceholderText("https://ejemplo.com/imagen.jpg")
        self.sinopsis = QTextEdit()
        self.sinopsis.setMaximumHeight(100)

        form.addRow("Título:", self.titulo)
        form.addRow("Año:", self.anio)
        form.addRow("Género:", self.genero)
        form.addRow("Director:", self.director)
        form.addRow("URL Imagen:", self.imagen_url)
        form.addRow("Sinopsis:", self.sinopsis)

        layout.addLayout(form)
        self.btn_save = QPushButton("Actualizar" if edit_mode else "Guardar")
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.save_movie)
        self.setLayout(layout)

        if edit_mode and movie:
            self.load_movie_data(movie)

    def load_movie_data(self, movie):
        self.titulo.setText(movie["titulo"])
        self.anio.setText(str(movie["anio"]))
        self.genero.setText(", ".join(movie["genero"]))
        self.director.setText(movie["director"])
        self.imagen_url.setText(movie.get("imagen_url", ""))
        self.sinopsis.setText(movie["sinopsis"])

    def save_movie(self):
        data = {
            "titulo": self.titulo.text(),
            "anio": int(self.anio.text()),
            "genero": [g.strip() for g in self.genero.text().split(",")],
            "director": self.director.text(),
            "imagen_url": self.imagen_url.text(),
            "sinopsis": self.sinopsis.toPlainText()
        }

        if self.edit_mode:
            update_movie(self.movie["_id"], data)
            QMessageBox.information(self, "Éxito", "Película actualizada correctamente.")
        else:
            data["reseñas"] = []
            data["estadisticas"] = {"calificacion_promedio": 0, "total_reseñas": 0}
            add_movie(data)
            QMessageBox.information(self, "Éxito", "Película agregada correctamente.")

        self.accept()