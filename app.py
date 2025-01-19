import streamlit as st
import pandas as pd

# Título de la página
st.title("Registro de Jugadores MVP")

# Inicializar o cargar datos
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Jugador", "Jornada"])

data = st.session_state.get("data", load_data())

# Formulario para agregar MVPs
st.header("Añadir un MVP")
with st.form("mvp_form", clear_on_submit=True):
    jugador = st.text_input("Nombre del jugador", placeholder="Ejemplo: Lionel Messi")
    jornada = st.number_input("Número de la jornada", min_value=1, step=1)
    submit = st.form_submit_button("Registrar MVP")

    if submit:
        if not jugador:
            st.warning("Por favor, ingresa el nombre del jugador.")
        else:
            nuevo_registro = {"Jugador": jugador, "Jornada": int(jornada)}
            data = pd.concat([data, pd.DataFrame([nuevo_registro])], ignore_index=True)
            st.session_state["data"] = data
            st.success(f"¡MVP registrado para {jugador} en la jornada {jornada}!")

# Mostrar tabla con los registros
st.header("Historial de MVPs")
if not data.empty:
    st.dataframe(data)
else:
    st.info("No hay registros de MVPs aún.")

# Análisis de MVPs por jugador
st.header("Estadísticas de MVPs")
if not data.empty:
    conteo = data["Jugador"].value_counts().reset_index()
    conteo.columns = ["Jugador", "MVPs Totales"]
    st.bar_chart(conteo.set_index("Jugador"))
    st.dataframe(conteo)
else:
    st.info("No hay datos para mostrar estadísticas.")
