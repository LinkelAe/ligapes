import streamlit as st
import pandas as pd
import os

# Ruta del archivo CSV
CSV_FILE = "mvp_data.csv"

# Función para cargar datos desde el archivo CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Jugador", "Jornada", "Club"])

# Guardar datos en el archivo CSV
def save_data(data):
    data.to_csv(CSV_FILE, index=False)

# Cargar datos al iniciar
data = load_data()

# Lista de clubes
clubes = [
    "Boca Juniors",
    "Estudiantes de La Plata",
    "Vélez Sarsfield",
    "River Plate",
    "Banfield",
    "Racing Club",
    "Sacachispas",
    "Godoy Cruz",
    "Quilmes",
    "Arsenal de Sarandí",
]

# Título de la página
st.title("Registro de Jugadores MVP")

# Formulario para agregar MVPs
st.header("Añadir un MVP")
with st.form("mvp_form", clear_on_submit=True):
    jugador = st.text_input("Nombre del jugador", placeholder="Ejemplo: Lionel Messi")
    jornada = st.number_input("Número de la jornada", min_value=1, step=1)
    club = st.selectbox("Selecciona el club del jugador", clubes)
    submit = st.form_submit_button("Registrar MVP")

    if submit:
        if not jugador:
            st.warning("Por favor, ingresa el nombre del jugador.")
        else:
            nuevo_registro = {"Jugador": jugador, "Jornada": int(jornada), "Club": club}
            data = pd.concat([data, pd.DataFrame([nuevo_registro])], ignore_index=True)
            save_data(data)  # Guardar datos en el CSV
            st.success(f"¡MVP registrado para {jugador} de {club} en la jornada {jornada}!")

# Mostrar tabla con los registros
st.header("Historial de MVPs")
if not data.empty:
    st.dataframe(data, use_container_width=True)
else:
    st.info("No hay registros de MVPs aún.")
