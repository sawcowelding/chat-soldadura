{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import streamlit as st\
\
class WeldingChatBot:\
    def __init__(self, catalog):\
        self.catalog = catalog\
        self.customer_requirements = \{\}\
\
    def ask_questions(self):\
        st.title("Asistente de Selecci\'f3n de Soldadoras")\
        \
        self.customer_requirements['process'] = st.selectbox("\'bfQu\'e9 tipo de soldadura necesita?", ["MIG", "TIG", "SMAW", "Plasma", "Multiproceso"])\
        self.customer_requirements['material'] = st.selectbox("\'bfQu\'e9 tipo de material va a soldar?", ["Acero inoxidable", "Aluminio", "Acero al carbono"])\
        self.customer_requirements['amperage'] = st.number_input("\'bfCu\'e1l es el amperaje m\'e1ximo que necesita?", min_value=1, step=1)\
        self.customer_requirements['cycle'] = st.number_input("\'bfQu\'e9 ciclo de trabajo necesita (%)?", min_value=1, max_value=100, step=1)\
        self.customer_requirements['portability'] = st.radio("\'bfRequiere una m\'e1quina port\'e1til?", ["S\'ed", "No"])\
        self.customer_requirements['voltage'] = st.selectbox("\'bfQu\'e9 tipo de conexi\'f3n el\'e9ctrica tiene disponible?", ["Monof\'e1sica", "Trif\'e1sica", "220V", "380V"])\
        self.customer_requirements['budget'] = st.number_input("\'bfCu\'e1l es el presupuesto m\'e1ximo?", min_value=1, step=1)\
        \
        if st.button("Buscar modelos recomendados"):\
            self.recommend_models()\
\
    def recommend_models(self):\
        recommendations = []\
        for model in self.catalog:\
            if (\
                self.customer_requirements['process'].lower() in model['process'].lower() and\
                self.customer_requirements['material'].lower() in model['material'].lower() and\
                self.customer_requirements['amperage'] <= model['amperage'] and\
                self.customer_requirements['cycle'] <= model['cycle'] and\
                self.customer_requirements['voltage'] in model['voltage'] and\
                self.customer_requirements['budget'] >= model['price']\
            ):\
                recommendations.append(model)\
\
        if recommendations:\
            st.subheader("Modelos recomendados:")\
            for rec in recommendations:\
                st.write(f"- **\{rec['name']\}** | Amperaje: \{rec['amperage']\}A | Ciclo de Trabajo: \{rec['cycle']\}% | Precio: $\{rec['price']\}")\
        else:\
            st.warning("No se encontraron modelos que coincidan con todos los criterios.")\
\
# Ejemplo de cat\'e1logo con informaci\'f3n de los modelos (extra\'eddo de los PDFs)\
catalog = [\
    \{'name': 'Esab Bantam 2.5', 'process': 'SMAW', 'material': 'Acero al carbono', 'amperage': 120, 'cycle': 40, 'voltage': ['220V'], 'price': 200\},\
    \{'name': 'Lincoln MegaForce 175', 'process': 'SMAW', 'material': 'Acero inoxidable', 'amperage': 175, 'cycle': 60, 'voltage': ['120V', '230V'], 'price': 500\},\
    \{'name': 'Miller Millermatic 142', 'process': 'MIG', 'material': 'Aluminio', 'amperage': 140, 'cycle': 60, 'voltage': ['120V'], 'price': 800\},\
    \{'name': 'Sumig Welbee P402', 'process': 'Multiproceso', 'material': 'Acero al carbono', 'amperage': 400, 'cycle': 100, 'voltage': ['220V', '440V'], 'price': 3000\}\
]\
\
st.sidebar.title("Asistente de Selecci\'f3n de Soldadoras")\
bot = WeldingChatBot(catalog)\
bot.ask_questions()\
}