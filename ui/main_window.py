from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem
)
from ui.add_movie import AddMovieWindow
from ui.movie_detail import MovieDetailWindow
from models.movie_model import get_all_movies

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Películas Review")
        self.setGeometry(200, 100, 600, 500)
        self.layout = QVBoxLayout()

        self.title = QLabel("Lista de Películas")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        self.movie_list = QListWidget()
        self.layout.addWidget(self.movie_list)

        self.btn_add = QPushButton("Agregar Película")
        self.layout.addWidget(self.btn_add)

        self.btn_add.clicked.connect(self.open_add_movie)
        self.movie_list.itemDoubleClicked.connect(self.open_movie_detail)

        self.setLayout(self.layout)
        self.load_movies()

    def load_movies(self):
        self.movie_list.clear()
        for movie in get_all_movies():
            stats = movie.get("estadisticas", {})
            promedio = stats.get("calificacion_promedio", "N/A")
            item = QListWidgetItem(f"{movie['titulo']} ({movie['anio']}) ⭐ {promedio}")
            item.setData(1000, str(movie["_id"]))
            self.movie_list.addItem(item)

    def open_add_movie(self):
        dialog = AddMovieWindow(self)
        result = dialog.exec()
        if result:
            self.load_movies()

    def open_movie_detail(self, item):
        movie_id = item.data(1000)
        self.detail_window = MovieDetailWindow(movie_id)
        self.detail_window.movie_updated.connect(self.load_movies)
        self.detail_window.show()
