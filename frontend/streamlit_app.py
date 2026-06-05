import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title = 'Predicción de Riesgo de Crédito',
    page_icon = '💳',
    layout = 'wide'
)

st.title('Predicción de Riesgo de Crédito')
st.caption('Predicción de la probabilidad de default (PD) en los siguientes 6 meses')

left, right = st.columns([1, 2])

with left:
    st.subheader("Información de Cliente")

    with st.form("client_form"):
        age = st.number_input("Edad", min_value=18, max_value=100, value=34)
        gender = st.selectbox("Género (M: Hombre, F: Mujer)", ["M", "F"])
        credit_score = st.number_input("Score Crediticio", min_value=300, max_value=850, value=620)
        net_yearly_income = st.number_input("Ingresos Netos Anuales", min_value=0.0, value=45000.0)
        credit_limit = st.number_input("Límite de Crédito", min_value=0.0, value=10000.0)
        credit_limit_used = st.slider("Límite de Crédito utilizado (%)", 0, 100, 72)
        no_of_days_employed = st.number_input("Permanencia en días de tu Trabajo", value=730.0)
        occupation_type = st.selectbox( 
            "Ocupacion",
            [
                "Unknown",
                "Laborers",
                "Sales staff",
                "Core staff",
                "Managers",
                "Drivers",
                "High skill tech staff",
                "Accountants",
                "Medicine staff",
                "Security staff",
                "Cooking staff",
                "Cleaning staff",
                "Private service staff",
                "Low-skill Laborers",
                "Waiters/barmen staff",
                "Secretaries",
                "Realty agents",
                "HR staff",
                "IT staff"
            ]
        )
        prev_defaults = st.selectbox("¿Cuántos incumplimientos de pago haz tenido?", [0, 1, 2, 3])
        owns_car = st.selectbox("¿Posees un vehículo?", ["Y", "N"])
        owns_house = st.selectbox("¿Posees una casa propia?", ["Y", "N"])
        no_of_children = st.number_input("Número de hijos", min_value=0, value=0)
        total_family_members = st.number_input("Totales miembros de Familia", min_value=1, value=2)
        migrant_worker = st.selectbox("¿Eres un trabajador migrante? (0: No, 1: Sí)", [0, 1])
        yearly_debt_payments = st.number_input("Pagos de Deuda Anuales", min_value=0.0, value=10000.0)

        submitted = st.form_submit_button("Predecir Riesgo")

# cliente_1 ejemplo = {
#     "credit_limit_used": 32.0, #-------------#
#     "no_of_days_employed": 1882, #-------------#
#     "credit_score": 690.0, #-------------#
#     "credit_limit": 25054.25, #-------------#
#     "total_family_members": 3, #-------------#
#     "yearly_debt_payments": 47863.75, #--------#
#     "net_yearly_income": 215555.19, #-------------#
#     "no_of_children": 1, #-------------#
#     "migrant_worker": 0, #-------------#
#     "age": 35, #-------------#
#     "prev_defaults": 0,#-------------#
#     "gender": "F", #-------------#
#     "owns_car": "Y", #-------------#
#     "owns_house": "Y", #-------------#
#     "occupation_type": "Managers" #-------------#
# }

payload = {
    "age": age, 
    "gender": gender,
    "credit_score": credit_score,
    "net_yearly_income": net_yearly_income,
    "credit_limit": credit_limit,
    "credit_limit_used": credit_limit_used,
    "no_of_days_employed": no_of_days_employed,
    "occupation_type": occupation_type,
    "prev_defaults": prev_defaults,
    "owns_car": owns_car,
    "owns_house": owns_house,
    "no_of_children": no_of_children,
    "total_family_members": total_family_members,
    "migrant_worker": migrant_worker,
    "yearly_debt_payments": yearly_debt_payments
}

with right:
    st.subheader("Resultado de Predicción")

    if submitted:
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

            if response.status_code == 201:
                result = response.json()

                probabilidad_default = result["probabilidad_default"]
                categoria_riesgo = result["categoria_riesgo"]
                decision_negocio = result["decision_negocio"]
                decision_f1_score = result["decision_f1_score"]
                shap_waterfall = result["shap_waterfall"]

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Probabilidad de Default",
                    f"{probabilidad_default * 100:.2f}%"
                )

                col2.metric(
                    "Categoría de Riesgo",
                    categoria_riesgo
                )

                col3.metric(
                    "Decisión de Negocio",
                    decision_negocio
                )

                col4.metric(
                    "Decisión según mejor Threshold (F1 Óptimo)",
                    decision_f1_score
                )

                st.progress(min(probabilidad_default, 1.0))

                st.divider()

                st.subheader("Interpretación de Negocio")

                if probabilidad_default < 0.10:
                    st.success("Este cliente muestra bajo riesgo de default.")
                elif probabilidad_default < 0.25:
                    st.warning("Este cliente debería revisarse manualmente.")
                else:
                    st.error("Este cliente muestra alto riesgo de default.")

                st.divider()

                st.subheader("Explicabilidad del Cliente - SHAP Waterfall")

                if "shap_waterfall" in result:
                    st.image(
                        f"data:image/png;base64,{result['shap_waterfall']}",
                        caption="SHAP Waterfall para esta observación"
                    )
                else:
                    st.warning("La API no devolvió el gráfico SHAP.")


                st.write("Información enviada a la API:")
                st.json(payload)

            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Podría no estar conectado a la API. Asegúrese que la API este ejecutándose.")
        except Exception as e:
            st.error(f"Error Inesperado: {e}")

    else:
        st.info("Rellene los datos del cliente y haga clic en «Predecir riesgo».")







