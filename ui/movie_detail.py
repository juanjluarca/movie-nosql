from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QMessageBox, QScrollArea, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QFont
from models.movie_model import get_movie_by_id, delete_movie, delete_review
from ui.add_review import AddReviewWindow
from ui.add_movie import AddMovieWindow
import urllib.request

class MovieDetailWindow(QWidget):
    movie_updated = pyqtSignal()

    def __init__(self, movie_id, parent=None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.setWindowTitle("Detalle de Película")
        self.setGeometry(200, 100, 800, 650)
        self.setStyleSheet("background-color: #1e1e1e;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        content.setLayout(self.layout)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        self.load_movie()
    
    def clear_layout(self, layout):
        """Limpia un layout recursivamente"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())
    
    def load_movie(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())
        
        self.movie = get_movie_by_id(self.movie_id)
        
        if not self.movie:
            self.layout.addWidget(QLabel("Película no encontrada"))
            return
        
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        card_layout = QHBoxLayout()
        
        img_label = QLabel()
        img_label.setFixedSize(250, 370)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("background-color: #1e1e1e; border-radius: 8px;")
        
        img_url = self.movie.get("imagen_url", "")
        if img_url:
            try:
                data = urllib.request.urlopen(img_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(250, 370, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    img_label.setPixmap(scaled)
                else:
                    img_label.setText("Sin imagen")
                    img_label.setStyleSheet("background-color: #1e1e1e; color: #6d6d6d; border-radius: 8px; font-size: 14px;")
            except:
                img_label.setText("Sin imagen")
                img_label.setStyleSheet("background-color: #1e1e1e; color: #6d6d6d; border-radius: 8px; font-size: 14px;")
        else:
            img_label.setText("Sin imagen")
            img_label.setStyleSheet("background-color: #1e1e1e; color: #6d6d6d; border-radius: 8px; font-size: 14px;")
        
        card_layout.addWidget(img_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        
        title = QLabel(self.movie['titulo'])
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        title.setWordWrap(True)
        info_layout.addWidget(title)
        
        year = QLabel(f"Año: {self.movie['anio']}")
        year.setStyleSheet("color: #b0b0b0; font-size: 15px;")
        info_layout.addWidget(year)
        
        genre = QLabel(f"Género: {', '.join(self.movie['genero'])}")
        genre.setStyleSheet("color: #b0b0b0; font-size: 15px;")
        info_layout.addWidget(genre)
        
        director = QLabel(f"Director: {self.movie['director']}")
        director.setStyleSheet("color: #b0b0b0; font-size: 15px;")
        info_layout.addWidget(director)
        
        stats = self.movie.get('estadisticas', {})
        self.rating_label = QLabel(f"Calificación: {stats.get('calificacion_promedio', 0)}/5 ({stats.get('total_reseñas', 0)} reseñas)")
        rating_font = QFont()
        rating_font.setPointSize(14)
        rating_font.setBold(True)
        self.rating_label.setFont(rating_font)
        self.rating_label.setStyleSheet("color: #FF9800; margin-top: 10px;")
        info_layout.addWidget(self.rating_label)
        
        sinopsis_title = QLabel("Sinopsis:")
        sinopsis_title.setStyleSheet("color: #e0e0e0; font-size: 14px; font-weight: bold; margin-top: 10px;")
        info_layout.addWidget(sinopsis_title)
        
        sinopsis = QLabel(self.movie.get('sinopsis', 'Sin sinopsis'))
        sinopsis.setWordWrap(True)
        sinopsis.setStyleSheet("color: #b0b0b0; font-size: 13px; line-height: 1.5;")
        info_layout.addWidget(sinopsis)
        
        info_layout.addStretch()
        
        btn_layout = QHBoxLayout()
        
        self.btn_edit = QPushButton("Editar")
        self.btn_edit.setFixedHeight(40)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_edit.clicked.connect(self.open_edit_movie)
        btn_layout.addWidget(self.btn_edit)
        
        self.btn_delete = QPushButton("Eliminar Película")
        self.btn_delete.setFixedHeight(40)
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.btn_delete.clicked.connect(self.delete_movie_confirm)
        btn_layout.addWidget(self.btn_delete)
        
        info_layout.addLayout(btn_layout)
        
        card_layout.addLayout(info_layout)
        card.setLayout(card_layout)
        self.layout.addWidget(card)
        
        reviews_header = QHBoxLayout()
        reviews_title = QLabel("Reseñas")
        reviews_font = QFont()
        reviews_font.setPointSize(18)
        reviews_font.setBold(True)
        reviews_title.setFont(reviews_font)
        reviews_title.setStyleSheet("color: #e0e0e0;")
        reviews_header.addWidget(reviews_title)
        
        reviews_header.addStretch()
        
        self.btn_add_review = QPushButton("Agregar Reseña")
        self.btn_add_review.setFixedHeight(38)
        self.btn_add_review.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.btn_add_review.clicked.connect(self.open_add_review)
        reviews_header.addWidget(self.btn_add_review)
        
        self.layout.addLayout(reviews_header)
        
        self.reviews_container = QVBoxLayout()
        self.reviews_container.setSpacing(12)
        self.layout.addLayout(self.reviews_container)
        self.reload_reviews()
    
    def reload_reviews(self):
        """Recarga la lista de reseñas desde la base de datos"""
        for i in reversed(range(self.reviews_container.count())):
            item = self.reviews_container.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())
        
        self.movie = get_movie_by_id(self.movie_id)
        reviews = self.movie.get("reseñas", [])
        
        if not reviews:
            no_reviews = QLabel("No hay reseñas aún. ¡Sé el primero en agregar una!")
            no_reviews.setStyleSheet("color: #6d6d6d; font-size: 14px; padding: 20px; background-color: #2d2d2d; border-radius: 8px;")
            no_reviews.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reviews_container.addWidget(no_reviews)
        else:
            for idx, r in enumerate(reviews):
                review_card = QFrame()
                review_card.setStyleSheet("""
                    QFrame {
                        background-color: #2d2d2d;
                        border-radius: 8px;
                        padding: 15px;
                    }
                """)
                review_layout = QVBoxLayout()
                
                header = QHBoxLayout()
                
                user_info = QLabel(f"{r['usuario']} • {r['pais']}")
                user_font = QFont()
                user_font.setBold(True)
                user_info.setFont(user_font)
                user_info.setStyleSheet("color: #e0e0e0; font-size: 14px;")
                header.addWidget(user_info)
                
                header.addStretch()
                
                rating = QLabel(f"{r['puntuacion']}/5")
                rating.setStyleSheet("color: #FF9800; font-size: 13px; font-weight: bold;")
                header.addWidget(rating)
                
                date = QLabel(r.get('fecha', ''))
                date.setStyleSheet("color: #6d6d6d; font-size: 12px;")
                header.addWidget(date)
                
                btn_delete_review = QPushButton("×")
                btn_delete_review.setFixedSize(30, 30)
                btn_delete_review.setStyleSheet("""
                    QPushButton {
                        background-color: #3d3d3d;
                        color: #f44336;
                        border: none;
                        border-radius: 4px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #f44336;
                        color: white;
                    }
                """)
                btn_delete_review.clicked.connect(lambda checked, i=idx: self.delete_review_confirm(i))
                header.addWidget(btn_delete_review)
                
                review_layout.addLayout(header)
                
                comment = QLabel(r['comentario'])
                comment.setWordWrap(True)
                comment.setStyleSheet("color: #b0b0b0; font-size: 13px; margin-top: 8px;")
                review_layout.addWidget(comment)
                
                review_card.setLayout(review_layout)
                self.reviews_container.addWidget(review_card)
        
        stats = self.movie.get('estadisticas', {})
        self.rating_label.setText(f"Calificación: {stats.get('calificacion_promedio', 0)}/5 ({stats.get('total_reseñas', 0)} reseñas)")
    
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
            self.load_movie()
            self.movie_updated.emit()
    
    def delete_review_confirm(self, review_index):
        """Confirma y elimina una reseña"""
        reply = QMessageBox.question(
            self, 
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar esta reseña?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_review(self.movie_id, review_index)
            self.reload_reviews()
            self.movie_updated.emit()
            QMessageBox.information(self, "Éxito", "Reseña eliminada correctamente.")
    
    def delete_movie_confirm(self):
        """Confirma y elimina la película"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar '{self.movie['titulo']}'?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_movie(self.movie_id)
            self.movie_updated.emit()
            QMessageBox.information(self, "Éxito", "Película eliminada correctamente.")
            self.close()