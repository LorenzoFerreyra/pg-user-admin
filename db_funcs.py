import streamlit as st
from sqlalchemy import text, create_engine
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

db_config = st.secrets["connections"]["postgresql"]


# Configuración del motor de base de datos usando secretos
engine = create_engine(
    f"{db_config['dialect']}://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
    connect_args={'options': '-csearch_path=public'}
)

def get_users():
    query = text('SELECT user_code, user_fullname, user_email, user_username FROM public."user"')
    try:
        df = pd.read_sql(query, engine)
        return df
    except SQLAlchemyError as e:
        st.error(f"Error al obtener usuarios: {e}")
        return pd.DataFrame()


def add_user(fullname, email, username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with engine.connect() as conn:
            # Obtener el último user_code y sumarle 1
            result = conn.execute("SELECT MAX(user_code) FROM \"user\"").fetchone()
            last_user_code = result[0]  # Obtener el valor máximo de user_code
            new_user_code = last_user_code + 1 if last_user_code is not None else 1  # Si es el primer usuario, asigna 1

            # Insertar el nuevo usuario
            query = text("""
                INSERT INTO "user" (user_code, user_fullname, user_email, user_username, user_password)
                VALUES (:user_code, :fullname, :email, :username, :password)
            """)
            conn.execute(query, {
                "user_code": new_user_code,
                "fullname": fullname,
                "email": email,
                "username": username,
                "password": hashed_password
            })
        st.success("Usuario agregado exitosamente.")
    except SQLAlchemyError as e:
        st.error(f"Error al agregar usuario: {e}")



# Función para actualizar un usuario
def update_user(user_code, fullname, email, username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = text("""
        UPDATE user
        SET user_fullname = :fullname,
            user_email = :email,
            user_username = :username,
            user_password = :password
        WHERE user_code = :user_code
    """)
    try:
        with engine.connect() as conn:
            conn.execute(query, {
                "user_code": user_code,
                "fullname": fullname,
                "email": email,
                "username": username,
                "password": hashed_password
            })
        st.success("Usuario actualizado exitosamente.")
    except SQLAlchemyError as e:
        st.error(f"Error al actualizar usuario: {e}")

# Función para eliminar un usuario
def delete_user(user_code):
    query = text("DELETE FROM user WHERE user_code = :user_code")
    try:
        with engine.connect() as conn:
            conn.execute(query, {"user_code": user_code})
        st.success("Usuario eliminado exitosamente.")
    except SQLAlchemyError as e:
        st.error(f"Error al eliminar usuario: {e}")
