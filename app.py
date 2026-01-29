import streamlit as st
import pandas as pd
import os

# Configuración de la aplicación
st.set_page_config(page_title="Consulta Técnica de Repuestos", layout="wide")

# Nombre del archivo Excel
ARCHIVO_EXCEL = "inventario_repuestos.xlsx"

def inicializar_base_de_datos():
    if not os.path.exists(ARCHIVO_EXCEL):
        # Parámetros técnicos para cargar (sin precio)
        columnas = [
            "SKU", 
            "Descripcion_Producto", 
            "Codigos_OEM", 
            "Otros_Proveedores_Marcas", 
            "VIN_Prefijo", 
            "Compatibilidad_Vehiculos", 
            "Especificaciones_Tecnicas"
        ]
        df = pd.DataFrame(columns=columnas)
        df.to_excel(ARCHIVO_EXCEL, index=False)
        return True
    return False

def cargar_datos():
    return pd.read_excel(ARCHIVO_EXCEL)

# Crear archivo si no existe
inicializar_base_de_datos()

st.title("⚙️ Buscador Técnico - Autopartes Díaz")
st.markdown("---")

menu = st.sidebar.selectbox("Seleccione una opción", ["🔍 Buscador", "➕ Registrar Datos"])

if menu == "🔍 Buscador":
    busqueda = st.text_input("Ingrese VIN, OEM o Descripción:")
    if busqueda:
        df = cargar_datos()
        # Búsqueda inteligente en todas las celdas del Excel
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
    st.subheader("Carga Manual de Información")
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
        
        if st.form_submit_button("Guardar en Excel"):
            df = cargar_datos()
            nuevo = {
                "SKU": sku, "Descripcion_Producto": desc, "Codigos_OEM": oem, 
                "Otros_Proveedores_Marcas": prov, "VIN_Prefijo": vin, 
                "Compatibilidad_Vehiculos": comp, "Especificaciones_Tecnicas": specs
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_excel(ARCHIVO_EXCEL, index=False)
            st.success("Dato guardado localmente.")