import streamlit as st
import pandas as pd
import sqlite3

# Conexión a la base de datos SQLite
DB_FILE = "mvp_data.db"

def init_db():
    """Inicializar la base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS mvp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador TEXT,
            jornada INTEGER,
            club TEXT
        )
    """)
    conn.commit()
    return conn

# Guardar un registro en la base de datos
def save_to_db(conn, jugador, jornada, club):
    c = conn.cursor()
    c.execute("INSERT INTO mvp (jugador, jornada, club) VALUES (?, ?, ?)", (jugador, jornada, club))
    conn.commit()

# Cargar datos de la base de datos
def load_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT jugador, jornada, club FROM mvp")
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Jugador", "Jornada", "Club"])

# Limpiar la base de datos
def clear_db(conn):
    c = conn.cursor()
    c.execute("DELETE FROM mvp")
    conn.commit()

# Inicializar base de datos
conn = init_db()
data = load_from_db(conn)

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

# Botón para limpiar la base de datos
if st.button("Limpiar todos los MVPs"):
    clear_db(conn)
    data = load_from_db(conn)  # Recargar datos después de limpiar
    st.warning("¡Todos los datos han sido eliminados!")

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
            save_to_db(conn, jugador, int(jornada), club)
            data = load_from_db(conn)  # Recargar los datos desde la base de datos
            st.success(f"¡MVP registrado para {jugador} de {club} en la jornada {jornada}!")

# Mostrar tabla con los registros
st.header("Historial de MVPs")
if not data.empty:
    st.dataframe(data, use_container_width=True)
else:
    st.info("No hay registros de MVPs aún.")

# Análisis de MVPs por jugador
st.header("Total de MVPs por Jugador")
if not data.empty:
    conteo_jugadores = (
        data.groupby(["Jugador", "Club"])
        .size()
        .reset_index(name="MVPs Totales")
        .sort_values(by="MVPs Totales", ascending=False)
    )
    st.table(conteo_jugadores)
else:
    st.info("No hay datos para mostrar estadísticas por jugadores.")

# Análisis de MVPs por club
st.header("Estadísticas de MVPs por Club")
if not data.empty:
    conteo_clubes = data["Club"].value_counts().reset_index()
    conteo_clubes.columns = ["Club", "MVPs Totales"]
    st.bar_chart(conteo_clubes.set_index("Club"))
    st.dataframe(conteo_clubes, use_container_width=True)
else:
    st.info("No hay datos para mostrar estadísticas por clubes.")
