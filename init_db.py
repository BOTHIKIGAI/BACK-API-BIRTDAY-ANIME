from app.config.database import Base, engine
from app.models.tables.anime import Anime
from app.models.tables.author import Author
from app.models.tables.episode import Episode
from app.models.relationships.anime_author_association import anime_author_association
from app.models.relationships.episode_author_association import episode_author_association

def init_db():
    # Crea todas las tablas en la base de datos
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    init_db()