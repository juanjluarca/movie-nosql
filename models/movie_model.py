from bson import ObjectId
from database import get_db

db = get_db()
peliculas = db["peliculas"]

def get_all_movies():
    return list(peliculas.find())

def add_movie(data):
    peliculas.insert_one(data)

def get_movie_by_id(movie_id):
    return peliculas.find_one({"_id": ObjectId(movie_id)})

def add_review(movie_id, review):
    peliculas.update_one(
        {"_id": ObjectId(movie_id)},
        {"$push": {"reseñas": review}}
    )

    movie = peliculas.find_one({"_id": ObjectId(movie_id)})
    reseñas = movie.get("reseñas", [])
    if reseñas:
        promedio = sum(r["puntuacion"] for r in reseñas) / len(reseñas)
        peliculas.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": {
                "estadisticas.calificacion_promedio": round(promedio, 2),
                "estadisticas.total_reseñas": len(reseñas)
            }}
        )

def delete_review(movie_id, review_index):
    """Elimina una reseña por su índice"""
    movie = peliculas.find_one({"_id": ObjectId(movie_id)})
    reseñas = movie.get("reseñas", [])
    
    if 0 <= review_index < len(reseñas):
        reseñas.pop(review_index)
        peliculas.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": {"reseñas": reseñas}}
        )
        
        if reseñas:
            promedio = sum(r["puntuacion"] for r in reseñas) / len(reseñas)
            peliculas.update_one(
                {"_id": ObjectId(movie_id)},
                {"$set": {
                    "estadisticas.calificacion_promedio": round(promedio, 2),
                    "estadisticas.total_reseñas": len(reseñas)
                }}
            )
        else:
            peliculas.update_one(
                {"_id": ObjectId(movie_id)},
                {"$set": {
                    "estadisticas.calificacion_promedio": 0,
                    "estadisticas.total_reseñas": 0
                }}
            )

def delete_movie(movie_id):
    peliculas.delete_one({"_id": ObjectId(movie_id)})

def update_movie(movie_id, data):
    peliculas.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": data}
    )
    