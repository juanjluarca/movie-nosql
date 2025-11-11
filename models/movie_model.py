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

def get_movies_sorted_by_rating(order="desc"):
    sort_order = -1 if order == "desc" else 1
    pipeline = [
        {"$sort": {"estadisticas.calificacion_promedio": sort_order}}
    ]
    return list(peliculas.aggregate(pipeline))

def search_movies_by_name(name):
    try:
        import re
        regex = re.compile(f'.*{re.escape(name)}.*', re.IGNORECASE)
        movies = list(peliculas.find({"titulo": regex}))
        return movies
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return []

def search_movies_advanced(search_term):
    try:
        import re
        regex = re.compile(f'.*{re.escape(search_term)}.*', re.IGNORECASE)
        movies = list(peliculas.find({
            "$or": [
                {"titulo": regex},
                {"director": regex},
                {"genero": regex},
                {"reparto": regex}
            ]
        }))
        return movies
    except Exception as e:
        print(f"Error en búsqueda avanzada: {e}")
        return []