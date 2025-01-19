import streamlit as st
import pandas as pd

# Título de la página
st.title("Registro de Jugadores MVP")

# Inicializar o cargar datos
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Jugador", "Jornada", "Club"])

data = st.session_state.get("data", load_data())

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
            st.session_state["data"] = data
            st.success(f"¡MVP registrado para {jugador} de {club} en la jornada {jornada}!")




# Funcionalidad de edición
st.header("Editar MVP")
if not data.empty:
    seleccion = st.selectbox("Selecciona el jugador a editar:", data["Jugador"].unique())
    jugador_editar = data[data["Jugador"] == seleccion].iloc[0]

    with st.form("edit_form"):
        nuevo_jugador = st.text_input("Nombre del jugador", value=jugador_editar["Jugador"])
        nueva_jornada = st.number_input("Número de la jornada", min_value=1, step=1, value=jugador_editar["Jornada"])
        nuevo_club = st.selectbox("Selecciona el club del jugador", clubes, index=clubes.index(jugador_editar["Club"]))
        editar = st.form_submit_button("Guardar cambios")

        if editar:
            # Actualizar el DataFrame
            index = data[data["Jugador"] == seleccion].index[0]
            data.at[index, "Jugador"] = nuevo_jugador
            data.at[index, "Jornada"] = nueva_jornada
            data.at[index, "Club"] = nuevo_club
            st.session_state["data"] = data
            st.success(f"Se actualizaron los datos de {seleccion} a {nuevo_jugador}.")

# Análisis de MVPs por club
st.header("Estadísticas de MVPs por Club")
if not data.empty:
    conteo_clubes = data["Club"].value_counts().reset_index()
    conteo_clubes.columns = ["Club", "MVPs Totales"]
    st.bar_chart(conteo_clubes.set_index("Club"))
    st.dataframe(conteo_clubes.style.set_properties(**{'text-align': 'center'}), use_container_width=True)
else:
    st.info("No hay datos para mostrar estadísticas por clubes.")


# Mostrar tabla con los registros
st.header("Historial de MVPs")
if not data.empty:
    st.dataframe(data, use_container_width=True)
else:
    st.info("No hay registros de MVPs aún.")
