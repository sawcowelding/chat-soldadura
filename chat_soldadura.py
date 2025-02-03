import streamlit as st

class WeldingChatBot:
    def __init__(self, catalog):
        self.catalog = catalog
        self.customer_requirements = {}

    def ask_questions(self):
        st.title("Asistente de Selección de Soldadoras")
        
        mode = st.radio("Seleccione el modo de búsqueda:", ["Filtro Paso a Paso", "Búsqueda Directa"])
        
        if mode == "Búsqueda Directa":
            self.direct_search()
        else:
            self.step_by_step_filter()

    def direct_search(self):
        self.customer_requirements['process'] = st.selectbox("¿Qué tipo de soldadura necesita?", ["MIG", "TIG", "SMAW", "Plasma", "Multiproceso"])
        self.customer_requirements['material'] = st.selectbox("¿Qué tipo de material va a soldar?", ["Acero inoxidable", "Aluminio", "Acero al carbono"])
        self.customer_requirements['amperage'] = st.number_input("¿Cuál es el amperaje máximo que necesita?", min_value=1, step=1)
        self.customer_requirements['cycle'] = st.number_input("¿Qué ciclo de trabajo necesita (%)?", min_value=1, max_value=100, step=1)
        self.customer_requirements['portability'] = st.radio("¿Requiere una máquina portátil?", ["Sí", "No"])
        self.customer_requirements['voltage'] = st.selectbox("¿Qué tipo de conexión eléctrica tiene disponible?", ["Monofásica", "Trifásica", "220V", "380V"])
        self.customer_requirements['pulsed_wave'] = st.radio("¿Requiere onda pulsada?", ["Sí", "No"])
        self.customer_requirements['motosoldadora'] = st.radio("¿Está interesado en motosoldadoras?", ["Sí", "No"])
        
        if st.button("Buscar modelos recomendados"):
            self.recommend_models()

    def step_by_step_filter(self):
        st.subheader("Filtro Paso a Paso")
        filtered_catalog = self.catalog.copy()
        
        process_filter = st.selectbox("Filtrar por tipo de soldadura", ["Todos"] + list(set(model['process'] for model in self.catalog)))
        if process_filter != "Todos":
            filtered_catalog = [model for model in filtered_catalog if model['process'] == process_filter]
        
        material_filter = st.selectbox("Filtrar por material", ["Todos"] + list(set(model['material'] for model in filtered_catalog)))
        if material_filter != "Todos":
            filtered_catalog = [model for model in filtered_catalog if model['material'] == material_filter]
        
        max_amperage = st.slider("Filtrar por amperaje máximo", 1, max(model['amperage'] for model in filtered_catalog), step=10)
        filtered_catalog = [model for model in filtered_catalog if model['amperage'] <= max_amperage]
        
        max_cycle = st.slider("Filtrar por ciclo de trabajo (%)", 1, 100, step=5)
        filtered_catalog = [model for model in filtered_catalog if model['cycle'] <= max_cycle]
        
        voltage_filter = st.selectbox("Filtrar por voltaje", ["Todos"] + list(set(vol for model in filtered_catalog for vol in model['voltage'])))
        if voltage_filter != "Todos":
            filtered_catalog = [model for model in filtered_catalog if voltage_filter in model['voltage']]
        
        pulsed_wave_filter = st.radio("Filtrar por onda pulsada", ["Todos", "Sí", "No"])
        if pulsed_wave_filter != "Todos":
            filtered_catalog = [model for model in filtered_catalog if model['pulsed_wave'] == (pulsed_wave_filter == "Sí")]
        
        motosoldadora_filter = st.radio("Filtrar por motosoldadora", ["Todos", "Sí", "No"])
        if motosoldadora_filter != "Todos":
            filtered_catalog = [model for model in filtered_catalog if model['motosoldadora'] == (motosoldadora_filter == "Sí")]
        
        st.write(f"Opciones disponibles: {len(filtered_catalog)}")
        for model in filtered_catalog:
            st.write(f"- **{model['name']}** | Amperaje: {model['amperage']}A | Ciclo de Trabajo: {model['cycle']}%")

    def recommend_models(self):
        recommendations = [model for model in self.catalog if 
            self.customer_requirements['process'].lower() in model['process'].lower() and
            self.customer_requirements['material'].lower() in model['material'].lower() and
            self.customer_requirements['amperage'] <= model['amperage'] and
            self.customer_requirements['cycle'] <= model['cycle'] and
            self.customer_requirements['voltage'] in model['voltage'] and
            (self.customer_requirements['pulsed_wave'] == "No" or model.get('pulsed_wave', False)) and
            (self.customer_requirements['motosoldadora'] == "No" or model.get('motosoldadora', False))]

        st.subheader("Modelos recomendados:")
        if recommendations:
            for rec in recommendations:
                st.write(f"- **{rec['name']}** | Amperaje: {rec['amperage']}A | Ciclo de Trabajo: {rec['cycle']}%")
        else:
            st.warning("No se encontraron modelos exactos.")

# Carga de datos desde los catálogos oficiales
catalog = [
    {'name': 'Esab Renegade 300', 'process': 'SMAW', 'material': 'Todos', 'amperage': 300, 'cycle': 60, 'voltage': ['220V', '380V'], 'pulsed_wave': False, 'motosoldadora': False},
    {'name': 'Lincoln Idealarc DC600', 'process': 'Multiproceso', 'material': 'Acero al carbono', 'amperage': 600, 'cycle': 100, 'voltage': ['230V', '460V'], 'pulsed_wave': False, 'motosoldadora': False},
    {'name': 'Miller Millermatic 252', 'process': 'MIG', 'material': 'Aluminio', 'amperage': 250, 'cycle': 60, 'voltage': ['230V'], 'pulsed_wave': True, 'motosoldadora': False},
    {'name': 'Sumig Falcon 505', 'process': 'SMAW', 'material': 'Acero inoxidable', 'amperage': 500, 'cycle': 100, 'voltage': ['220V', '440V'], 'pulsed_wave': True, 'motosoldadora': False}
]

st.sidebar.title("Asistente de Selección de Soldadoras")
bot = WeldingChatBot(catalog)
bot.ask_questions()
