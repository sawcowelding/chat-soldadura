import streamlit as st

class WeldingChatBot:
    def __init__(self, catalog):
        self.catalog = catalog
        self.customer_requirements = {}

    def ask_questions(self):
        st.title("Asistente de Selección de Soldadoras")
        
        self.customer_requirements['process'] = st.selectbox("¿Qué tipo de soldadura necesita?", ["MIG", "TIG", "SMAW", "Plasma", "Multiproceso"])
        self.customer_requirements['material'] = st.selectbox("¿Qué tipo de material va a soldar?", ["Acero inoxidable", "Aluminio", "Acero al carbono"])
        self.customer_requirements['amperage'] = st.number_input("¿Cuál es el amperaje máximo que necesita?", min_value=1, step=1)
        self.customer_requirements['cycle'] = st.number_input("¿Qué ciclo de trabajo necesita (%)?", min_value=1, max_value=100, step=1)
        self.customer_requirements['portability'] = st.radio("¿Requiere una máquina portátil?", ["Sí", "No"])
        self.customer_requirements['voltage'] = st.selectbox("¿Qué tipo de conexión eléctrica tiene disponible?", ["Monofásica", "Trifásica", "220V", "380V"])
        self.customer_requirements['budget'] = st.number_input("¿Cuál es el presupuesto máximo?", min_value=1, step=1)
        
        if st.button("Buscar modelos recomendados"):
            self.recommend_models()

    def recommend_models(self):
        recommendations = []
        similar_matches = []

        for model in self.catalog:
            match_criteria = (
                self.customer_requirements['process'].lower() in model['process'].lower() and
                self.customer_requirements['material'].lower() in model['material'].lower() and
                self.customer_requirements['amperage'] <= model['amperage'] and
                self.customer_requirements['cycle'] <= model['cycle'] and
                self.customer_requirements['voltage'] in model['voltage'] and
                self.customer_requirements['budget'] >= model['price']
            )
            
            if match_criteria:
                recommendations.append(model)
            else:
                similarity_score = sum([
                    self.customer_requirements['process'].lower() in model['process'].lower(),
                    self.customer_requirements['material'].lower() in model['material'].lower(),
                    self.customer_requirements['amperage'] <= model['amperage'],
                    self.customer_requirements['cycle'] <= model['cycle'],
                    self.customer_requirements['voltage'] in model['voltage'],
                    self.customer_requirements['budget'] >= model['price']
                ])
                if similarity_score >= 3:  # Mostrar modelos con al menos 3 coincidencias
                    similar_matches.append(model)

        if recommendations:
            st.subheader("Modelos recomendados:")
            for rec in recommendations:
                st.write(f"- **{rec['name']}** | Amperaje: {rec['amperage']}A | Ciclo de Trabajo: {rec['cycle']}% | Precio: ${rec['price']}")
        else:
            st.warning("No se encontraron modelos exactos. Aquí tienes algunas opciones similares:")
            for rec in similar_matches:
                st.write(f"- **{rec['name']}** | Amperaje: {rec['amperage']}A | Ciclo de Trabajo: {rec['cycle']}% | Precio: ${rec['price']}")

# Ejemplo de catálogo con información de los modelos (extraído de los PDFs)
catalog = [
    {'name': 'Esab Bantam 2.5', 'process': 'SMAW', 'material': 'Acero al carbono', 'amperage': 120, 'cycle': 40, 'voltage': ['220V'], 'price': 200},
    {'name': 'Lincoln MegaForce 175', 'process': 'SMAW', 'material': 'Acero inoxidable', 'amperage': 175, 'cycle': 60, 'voltage': ['120V', '230V'], 'price': 500},
    {'name': 'Miller Millermatic 142', 'process': 'MIG', 'material': 'Aluminio', 'amperage': 140, 'cycle': 60, 'voltage': ['120V'], 'price': 800},
    {'name': 'Sumig Welbee P402', 'process': 'Multiproceso', 'material': 'Acero al carbono', 'amperage': 400, 'cycle': 100, 'voltage': ['220V', '440V'], 'price': 3000}
]

st.sidebar.title("Asistente de Selección de Soldadoras")
bot = WeldingChatBot(catalog)
bot.ask_questions()
