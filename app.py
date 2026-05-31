import streamlit as st

st.set_page_config(page_title="OptiVida", layout="wide")

# Navegación en el sidebar
st.sidebar.title("OptiVida")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Módulos",
    ["Inicio", "M1 - Presupuesto", "M2 - Comidas", "M3 - Estudios", "M4 - Bienestar", "Resumen"]
)

# Mostrar página según selección
if pagina == "Inicio":
    st.title("Sistema de Optimización de Vida Estudiantil")
    st.write("Selecciona un módulo en el menú lateral para comenzar.")

elif pagina == "M1 - Presupuesto":
    st.title("M1 - Presupuesto Mensual")
    st.write("Módulo en construcción")

elif pagina == "M2 - Comidas":
    st.title("M2 - Planificación de Comidas")
    st.write("Módulo en construcción")

elif pagina == "M3 - Estudios":
    st.title("M3 - Calendario de Estudios")
    st.write("Módulo en construcción")

elif pagina == "M4 - Bienestar":
    st.title("M4 - Bienestar Estudiantil")
    st.write("Módulo en construcción")

elif pagina == "Resumen":
    st.title("Resumen del Sistema")
    st.write("Módulo en construcción")