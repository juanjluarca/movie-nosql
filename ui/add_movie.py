from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
)

class AddMovieWindow(QDialog):
    def __init__(self, parent=None, edit_mode=False, movie=None):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.movie = movie

        self.setWindowTitle("Editar Película" if edit_mode else "Agregar Película")
        self.setGeometry(350, 200, 400, 320)
        layout = QVBoxLayout()

        form = QFormLayout()
        self.titulo = QLineEdit()
        self.anio = QLineEdit()
        self.genero = QLineEdit()
        self.director = QLineEdit()
        self.sinopsis = QTextEdit()

        form.addRow("Título:", self.titulo)
        form.addRow("Año:", self.anio)
        form.addRow("Género:", self.genero)
        form.addRow("Director:", self.director)
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
        self.sinopsis.setText(movie["sinopsis"])

    def save_movie(self):
        if not self.titulo.text() or not self.anio.text():
            QMessageBox.warning(
                self,
                "Incompleto",
                "Complete título y año"
            )
            return
        
        accion = "actualizada" if self.edit_mode else "agregada"
        QMessageBox.information(
            self,
            "demo",
            f"Película {accion} correctamente."
        )
        self.accept()