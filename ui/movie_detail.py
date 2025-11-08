from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import pyqtSignal
from models.movie_model import get_movie_by_id
from ui.add_review import AddReviewWindow
from ui.add_movie import AddMovieWindow

class MovieDetailWindow(QWidget):
    movie_updated = pyqtSignal()

    def __init__(self, movie_id, parent=None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.setWindowTitle("Detalle de Película")
        self.setGeometry(300, 150, 500, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.load_movie()

    def load_movie(self):
        self.layout.setSpacing(10)
        self.movie = get_movie_by_id(self.movie_id)
        self.layout.addWidget(QLabel(f"🎬 {self.movie['titulo']} ({self.movie['anio']})"))
        self.layout.addWidget(QLabel(f"Género: {', '.join(self.movie['genero'])}"))
        self.layout.addWidget(QLabel(f"Director: {self.movie['director']}"))
        self.layout.addWidget(QLabel(f"Promedio: {self.movie['estadisticas']['calificacion_promedio']}"))

        self.reviews_label = QLabel("Reseñas:")
        self.layout.addWidget(self.reviews_label)

        self.reviews_list = QListWidget()
        self.layout.addWidget(self.reviews_list)
        self.reload_reviews()

        self.btn_add_review = QPushButton("Agregar Reseña")
        self.layout.addWidget(self.btn_add_review)
        self.btn_add_review.clicked.connect(self.open_add_review)

        self.btn_edit = QPushButton("Editar Película")
        self.layout.addWidget(self.btn_edit)
        self.btn_edit.clicked.connect(self.open_edit_movie)

    def reload_reviews(self):
        """Recarga la lista de reseñas desde la base de datos"""
        self.reviews_list.clear()
        self.movie = get_movie_by_id(self.movie_id)
        for r in self.movie.get("reseñas", []):
            item = QListWidgetItem(f"{r['usuario']} ({r['puntuacion']}/5): {r['comentario']}")
            self.reviews_list.addItem(item)

        # Actualiza el promedio visible
        promedio = self.movie['estadisticas']['calificacion_promedio']
        self.layout.itemAt(3).widget().setText(f"Promedio: {promedio}")

    def open_add_review(self):
        self.add_review = AddReviewWindow(self.movie_id)
        self.add_review.review_added.connect(self.handle_review_added)
        self.add_review.show()

    def handle_review_added(self):
        """Se ejecuta después de agregar una reseña"""
        self.reload_reviews()
        self.movie_updated.emit()

    def open_edit_movie(self):
        self.edit_window = AddMovieWindow(self, edit_mode=True, movie=self.movie)
        result = self.edit_window.exec()
        if result:
            self.reload_reviews()
            self.movie_updated.emit()
