import threading
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

from config import DB_URI

# ================= ENGINE =================
engine = create_engine(DB_URI, connect_args={"check_same_thread": False})

BASE = declarative_base()

SESSION = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)

INSERTION_LOCK = threading.RLock()

# ================= TABLE =================
class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(255))

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name


BASE.metadata.create_all(engine)

# ================= ADD USER =================
def add_user(user_id, user_name):
    with INSERTION_LOCK:
        try:
            user = SESSION.query(User).filter(User.id == user_id).first()

            if not user:
                user = User(user_id, user_name)
                SESSION.add(user)
                SESSION.commit()

        except Exception as e:
            SESSION.rollback()
            print(f"Error add_user: {e}")

# ================= DELETE USER =================
def delete_user(user_id):
    with INSERTION_LOCK:
        try:
            SESSION.query(User).filter(User.id == user_id).delete()
            SESSION.commit()

        except Exception as e:
            SESSION.rollback()
            print(f"Error delete_user: {e}")

# ================= GET ALL USERS =================
def full_userbase():
    try:
        return SESSION.query(User).all()

    except Exception as e:
        print(f"Error full_userbase: {e}")
        return []

# ================= GET USER IDS =================
def get_all_user_ids():
    try:
        return [user.id for user in SESSION.query(User.id).all()]

    except Exception as e:
        print(f"Error get_all_user_ids: {e}")
        return []
