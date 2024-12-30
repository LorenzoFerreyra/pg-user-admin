import streamlit as st
import pandas as pd 
from db_funcs import *
from PIL import Image
import plotly.express as px 

def color_df(val):
	if val == "Done":
		color = "green"
	elif val == "Doing":
		color = "orange"
	else:
		color = "red"

	return f'background-color: {color}'

st.set_page_config(
    page_title="User Admin App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

top_image = Image.open('static/7049.png')
bottom_image = Image.open('static/103-1036487_laptop-png.png')
main_image = Image.open('static/main_banner.png')

st.image(main_image,use_container_width='always')

st.sidebar.image(top_image,use_container_width='auto')
st.title("📄 User Management App 🗣")
menu = ["Crear Usuario ✅", "Actualizar Usuario 👨‍💻", "Eliminar Usuario ❌", "Ver Usuarios 🧾"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Crear Usuario ✅":
    st.subheader("Añadir Usuario")
    user_code = st.text_input("Código de Usuario")
    fullname = st.text_input("Nombre Completo")
    email = st.text_input("Correo Electrónico")
    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Agregar Usuario"):
        add_user(user_code, fullname, email, username, password)

elif choice == "Actualizar Usuario 👨‍💻":
    st.subheader("Actualizar Usuario")
    users = get_users()
    if not users.empty:
        user_code = st.selectbox("Seleccionar Usuario para Actualizar", users["user_code"])
        selected_user = users[users["user_code"] == user_code].iloc[0]

        fullname = st.text_input("Nombre Completo", selected_user["user_fullname"])
        email = st.text_input("Correo Electrónico", selected_user["user_email"])
        username = st.text_input("Nombre de Usuario", selected_user["user_username"])
        password = st.text_input("Nueva Contraseña", type="password")

        if st.button("Actualizar Usuario"):
            update_user(user_code, fullname, email, username, password)
    else:
        st.warning("No hay usuarios registrados.")

elif choice == "Eliminar Usuario ❌":
    st.subheader("Eliminar Usuario")
    users = get_users()
    if not users.empty:
        user_code = st.selectbox("Seleccionar Usuario para Eliminar", users["user_code"])

        if st.button("Eliminar Usuario"):
            delete_user(user_code)
    else:
        st.warning("No hay usuarios registrados.")

elif choice == "Ver Usuarios 🧾":
    st.subheader("Lista de Usuarios")
    users = get_users()
    if not users.empty:
        st.dataframe(users)
    else:
        st.warning("No hay usuarios registrados.")

st.markdown("<br><hr><center>Gestión de usuarios. Soporte del desarrollador: <a href='mailto:ferreyralorenzo2@gmail.com?subject=User Admin Panel WebApp!&body=Please specify the issue you are facing with the app.'><strong>Lorenzo</strong></a></center><hr>", unsafe_allow_html=True)
