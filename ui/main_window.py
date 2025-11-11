from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QGridLayout, QComboBox, QLineEdit, QMessageBox)
from models.movie_model import get_all_movies, get_movies_sorted_by_rating, search_movies_advanced
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from ui.add_movie import AddMovieWindow
from ui.movie_detail import MovieDetailWindow
import urllib.request

class MovieCard(QFrame):
    def __init__(self, movie, parent=None):
        super().__init__(parent)
        self.movie = movie
        self.parent_window = parent
        self.setFixedSize(220, 380)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
            MovieCard {
                background-color: #2d2d2d;
                border-radius: 8px;
                border: 1px solid #3d3d3d;
            }
            MovieCard:hover {
                border: 2px solid #2196F3;
                background-color: #353535;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.img_label = QLabel()
        self.img_label.setFixedSize(220, 280)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setStyleSheet("background-color: #1e1e1e; border-radius: 8px 8px 0 0;")

        self.load_image(movie.get("imagen_url", ""))
        layout.addWidget(self.img_label)

        info_container = QWidget()
        info_container.setStyleSheet("background-color: #2d2d2d; border-radius: 0 0 8px 8px;")
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(4)

        title = QLabel(movie["titulo"])
        title.setWordWrap(True)
        title.setMaximumHeight(40)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        info_layout.addWidget(title)

        stats = movie.get("estadisticas", {})
        promedio = stats.get("calificacion_promedio", 0)
        year_rating = QLabel(f"{movie['anio']} • {promedio}/5")
        year_rating.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        info_layout.addWidget(year_rating)

        info_container.setLayout(info_layout)
        layout.addWidget(info_container)

        self.setLayout(layout)

    def load_image(self, url):
        if url:
            try:
                data = urllib.request.urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(220, 280, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    self.img_label.setPixmap(scaled)
                    return
            except:
                pass

        self.img_label.setText("Sin imagen")
        self.img_label.setStyleSheet("background-color: #1e1e1e; color: #6d6d6d; font-size: 14px; border-radius: 8px 8px 0 0;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_detail()

    def open_detail(self):
        self.detail_window = MovieDetailWindow(str(self.movie["_id"]))
        self.detail_window.movie_updated.connect(self.parent_window.load_movies)
        self.detail_window.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_search_term = ""
        self.setWindowTitle("CineReview")
        self.setGeometry(100, 50, 1000, 700)
        self.setStyleSheet("background-color: #1e1e1e;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header principal
        header = QHBoxLayout()
        title = QLabel("CineReview")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        header.addWidget(title)
        header.addStretch()

        self.btn_add = QPushButton("Agregar Película")
        self.btn_add.setFixedHeight(40)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_add.clicked.connect(self.open_add_movie)
        header.addWidget(self.btn_add)
        main_layout.addLayout(header)
        #--
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por título, director o género...")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #666;
                color: white;
                border: 1px solid #888;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        self.search_input.returnPressed.connect(self.search_movies)
        search_layout.addWidget(self.search_input)
        
        self.btn_search = QPushButton("Buscar")
        self.btn_search.setFixedSize(80, 35)
        self.btn_search.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_search.clicked.connect(self.search_movies)
        search_layout.addWidget(self.btn_search)
        
        self.btn_clear_search = QPushButton("Limpiar")
        self.btn_clear_search.setFixedSize(80, 35)
        self.btn_clear_search.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.btn_clear_search.clicked.connect(self.clear_search)
        search_layout.addWidget(self.btn_clear_search)
        
        main_layout.addLayout(search_layout)
        #--
        # --- FILTRO DE ORDEN POR CALIFICACIÓN ---
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Ordenar por calificación:")
        filter_label.setStyleSheet("color: #e0e0e0; font-size: 14px;")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Mejor calificadas", "Peor calificadas"])
        self.filter_combo.setFixedWidth(150)
        self.filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #666;
                color: white;
                border: 1px solid #888;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.filter_combo.currentIndexChanged.connect(self.load_movies)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        
        self.results_label = QLabel("Todas las películas")
        self.results_label.setStyleSheet("color: #b0b0b0; font-size: 14px; font-weight: bold;")
        filter_layout.addWidget(self.results_label)
        
        main_layout.addLayout(filter_layout)

        # Área de scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #1e1e1e; }")

        # Contenedor de galería
        self.gallery_container = QWidget()
        self.gallery_layout = QGridLayout()
        self.gallery_layout.setSpacing(20)
        self.gallery_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.gallery_container.setLayout(self.gallery_layout)
        scroll.setWidget(self.gallery_container)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        self.load_movies()


    def search_movies(self):
        search_text = self.search_input.text().strip()
        self.current_search_term = search_text
        
        if not search_text:
            self.clear_search()
            return
        
        try:
            movies = search_movies_advanced(search_text)
            self.display_movies(movies, f"Resultados: '{search_text}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la búsqueda: {str(e)}")

    def clear_search(self):
        self.search_input.clear()
        self.current_search_term = ""
        self.load_movies()


    def display_movies(self, movies, message=""):
        for i in reversed(range(self.gallery_layout.count())):
            widget = self.gallery_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if message:
            self.results_label.setText(message)

        if not movies:
            no_movies = QLabel("No se encontraron películas...")
            no_movies.setStyleSheet("color: #6d6d6d; font-size: 16px; padding: 40px;")
            no_movies.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.gallery_layout.addWidget(no_movies, 0, 0)
            return

        row, col = 0, 0
        for movie in movies:
            card = MovieCard(movie, self)
            self.gallery_layout.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def load_movies(self):
        if self.current_search_term:
            self.search_movies()
            return
            
        try:
            selected = self.filter_combo.currentText()
            order = "desc" if selected == "Mejor calificadas" else "asc"
            movies = get_movies_sorted_by_rating(order)
            self.display_movies(movies, f"Todas las películas ({len(movies)} encontradas)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar películas: {str(e)}")

    def open_add_movie(self):
        dialog = AddMovieWindow(self)
        result = dialog.exec()
        if result:
            self.load_movies()

    filter_layout = None