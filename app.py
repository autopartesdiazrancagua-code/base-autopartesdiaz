import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Autopartes Díaz", layout="wide")

# URL de tu Google Sheet
url = "https://docs.google.com/spreadsheets/d/12HqsHiLVVdwtOrX_Qb0HozHWdpyIok6syoUYpbPYJ-Q/edit?usp=sharing"

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos():
    # ttl=0 para actualizar datos al instante
    return conn.read(spreadsheet=url, ttl=0)

st.title("⚙️ Buscador Técnico - Autopartes Díaz")
st.markdown("---")

menu = st.sidebar.selectbox("Seleccione una opción", ["🔍 Buscador", "➕ Registrar Datos"])

if menu == "🔍 Buscador":
    busqueda = st.text_input("Ingrese VIN, OEM o Descripción:")
    if busqueda:
        df = cargar_datos()
        # Filtro inteligente en todas las columnas
        resultados = df[df.apply(lambda r: r.astype(str).str.contains(busqueda, case=False).any(), axis=1)]
        
        if not resultados.empty:
            for _, fila in resultados.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([1, 1.5])
                    with col1:
                        st.subheader(fila['Descripcion_Producto'])
                        st.write(f"**SKU:** {fila['SKU']}")
                        st.write(f"**OEM:** {fila['Codigos_OEM']}")
                        st.write(f"**Marcas/Proveedores:** {fila['Otros_Proveedores_Marcas']}")
                        st.write(f"**Specs:** {fila['Especificaciones_Tecnicas']}")
                    with col2:
                        st.info(f"**Compatibilidad:**\n\n{fila['Compatibilidad_Vehiculos']}")
                        st.caption(f"VIN asociado: {fila['VIN_Prefijo']}")
        else:
            st.warning("No se encontraron coincidencias.")

elif menu == "➕ Registrar Datos":
    st.subheader("Carga de Información")
    st.write("Agrega los repuestos directamente en tu Google Sheet para que se actualicen en la web.")
    st.link_button("Ir a Google Sheets (Editor)", url)