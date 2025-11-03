from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from mock_data import MOCK_MOVIES
from ui.add_review import AddReviewWindow
from ui.add_movie import AddMovieWindow

class MovieDetailWindow(QWidget):
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
        
        self.movie = None
        for m in MOCK_MOVIES:
            if m["_id"] == self.movie_id:
                self.movie = m
                break
        
        if not self.movie:
            self.layout.addWidget(QLabel("Película no encontrada"))
            return
        
        self.layout.addWidget(QLabel(f"{self.movie['titulo']} ({self.movie['anio']})"))
        self.layout.addWidget(QLabel(f"Género: {', '.join(self.movie['genero'])}"))
        self.layout.addWidget(QLabel(f"Director: {self.movie['director']}"))
        self.layout.addWidget(QLabel(f"Promedio: {self.movie['estadisticas']['calificacion_promedio']}"))
        
        sinopsis_label = QLabel(f"Sinopsis: {self.movie['sinopsis']}")
        sinopsis_label.setWordWrap(True)
        self.layout.addWidget(sinopsis_label)

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
        """Recarga la lista de reseñas desde los datos mock"""
        self.reviews_list.clear()
        for r in self.movie.get("reseñas", []):
            item = QListWidgetItem(
                f"Usuario: {r['usuario']} - País: ({r['pais']}) - Calificación: {r['puntuacion']}/5\n"
                f"Comentario: {r['comentario']}\n"
                f"Fecha: {r['fecha']}"
            )
            self.reviews_list.addItem(item)

    def open_add_review(self):
        self.add_review = AddReviewWindow(self.movie_id)
        self.add_review.show()

    def open_edit_movie(self):
        self.edit_window = AddMovieWindow(self, edit_mode=True, movie=self.movie)
        self.edit_window.exec()