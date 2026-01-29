import streamlit as st
from sys import exit
import pandas as pd
from stripr import strip_margin # Opcional, para limpiar textos largos
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Autopartes Díaz", layout="wide")

# 1. Conexión con Google Sheets
# Nota: La URL debe ser la que me pasaste
url = "https://docs.google.com/spreadsheets/d/12HqsHiLVVdwtOrX_Qb0HozHWdpyIok6syoUYpbPYJ-Q/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos():
    return conn.read(spreadsheet=url)

st.title("⚙️ Buscador Técnico - Autopartes Díaz")
st.markdown("---")

menu = st.sidebar.selectbox("Seleccione una opción", ["🔍 Buscador", "➕ Registrar Datos"])

if menu == "🔍 Buscador":
    busqueda = st.text_input("Ingrese VIN, OEM o Descripción:")
    if busqueda:
        df = cargar_datos()
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
    st.subheader("Carga de Información a Google Sheets")
    with st.form("registro"):
        c1, c2 = st.columns(2)
        with c1:
            sku = st.text_input("SKU Interno")
            desc = st.text_input("Descripción del Repuesto")
            oem = st.text_input("Códigos OEM")
            prov = st.text_input("Proveedores / Otras Marcas")
        with c2:
            vin = st.text_input("VIN (Dígitos de búsqueda)")
            comp = st.text_area("Compatibilidad (Modelos/Años/Motor)")
            specs = st.text_input("Dientes / Medidas / Notas")
        
        if st.form_submit_button("Guardar en Google Sheets"):
            # Leer datos actuales
            df_actual = cargar_datos()
            # Crear nueva fila
            nuevo_dato = pd.DataFrame([{
                "SKU": sku, "Descripcion_Producto": desc, "Codigos_OEM": oem, 
                "Otros_Proveedores_Marcas": prov, "VIN_Prefijo": vin, 
                "Compatibilidad_Vehiculos": comp, "Especificaciones_Tecnicas": specs
            }])
            # Combinar y actualizar
            df_final = pd.concat([df_actual, nuevo_dato], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            st.success("✅ ¡Dato guardado permanentemente en la nube!")
            st.balloons()