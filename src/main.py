import fastapi
from fastapi import FastAPI, APIRouter
#from fastapi import routing
import sklearn
from pathlib import Path
import sys
from starlette import status
import pandas as pd
import numpy as np
import joblib
import logging
import json
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT))

from src.transformers import MissingIndicatorTransformer
from src.schemas import Cliente, ResponsePrediction
from src.utils.negocio import Negocio

app = FastAPI()

logging.basicConfig(
    level= logging.INFO,
    filename= 'app.log'
)
logger = logging.getLogger(__name__)

@app.get('/health', status_code = status.HTTP_200_OK)
def health():
    return {
        'status': 'ok'
    }

@app.get('/', status_code = status.HTTP_200_OK)
def home():
    return {
        "message": "Predicción de Riesgo de Crédito API está ejecutándose"
    }


@app.post('/predict', status_code= status.HTTP_201_CREATED)
def predict(data: Cliente):
    data_cliente = data.model_dump()
    data_cliente_df = pd.DataFrame([data_cliente])
    data_cliente_df.rename(
    columns= {
        'credit_limit_used': 'credit_limit_used(%)'
    },
    inplace = True
    )

    pipeline_model = joblib.load('./artifacts/model/logistic_model.pkl')
    preprocessor = pipeline_model[:-1]
    final_model = pipeline_model[-1]
    feature_names = joblib.load('./artifacts/metadata/features_names.pkl')
    shap_background = pd.read_parquet(
        './artifacts/interpretabilidad/shap_background.parquet'
    )
    explainer = shap.Explainer(
        final_model,
        shap_background
    )
    logging.info('DataFrame creado correctamente y Pipeline cargado correctamente')
    
    ## Transformación manual de WOEs
    ### Cargar reglas WOE del train - Esto se podría pasar como clase en Sklearn
    reglas_woe = joblib.load('./artifacts/encoders/woe_bins.pkl')

    # 1ra Feature: credit_limit_used(%) -> 0% missings
    data_cliente_df['credit_limit_used(%)_woe'] = pd.cut(
        x= data_cliente_df['credit_limit_used(%)'],
        bins= reglas_woe['credit_limit_used(%)']['bins'],
        labels = reglas_woe['credit_limit_used(%)']['woe_values']
    ).astype(float)

    # 2da Feature: no_of_days_employed -> (1.02% missings)
    data_cliente_df['no_of_days_employed_woe'] = pd.cut(
        x= data_cliente_df['no_of_days_employed'],
        bins= reglas_woe['no_of_days_employed']['bins'],
        labels = reglas_woe['no_of_days_employed']['woe_values']
    ).astype(float)
    data_cliente_df.loc[data_cliente_df['no_of_days_employed'].isna(), 'no_of_days_employed_woe'] = reglas_woe['no_of_days_employed']['missing_woe']

    # 3ra Feature: credit_score -> (0.02% missings)
    data_cliente_df['credit_score_woe'] = pd.cut(
        x= data_cliente_df['credit_score'],
        bins= reglas_woe['credit_score']['bins'],
        labels = reglas_woe['credit_score']['woe_values']
    ).astype(float)
    data_cliente_df.loc[data_cliente_df['credit_score'].isna(), 'credit_score_woe'] = reglas_woe['credit_score']['missing_woe']

    ## Capa de convertir a float mis columnas
    num_cols = [
    'credit_limit_used(%)',
    'no_of_days_employed',
    'credit_score',
    'credit_limit',
    'total_family_members',
    'yearly_debt_payments',
    'net_yearly_income',
    'no_of_children',
    'migrant_worker',
    'age',
    'prev_defaults',
    'credit_limit_used(%)_woe',
    'no_of_days_employed_woe',
    'credit_score_woe'
    ]

    data_cliente_df[num_cols] = data_cliente_df[num_cols].astype(float)

    # =========================
    # SHAP para cliente nuevo
    # =========================

    X_cliente_transformed = preprocessor.transform(data_cliente_df)

    X_cliente_shap = pd.DataFrame(
        X_cliente_transformed,
        columns=feature_names
    )

    shap_values_cliente = explainer(X_cliente_shap)

    fig = plt.figure(figsize=(10, 6))

    shap.plots.waterfall(
        shap_values_cliente[0],
        show=False,
        max_display=12
    )

    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=150
    )

    buffer.seek(0)

    shap_waterfall_base64 = base64.b64encode(
        buffer.read()
    ).decode("utf-8")

    plt.close(fig)

    ## Predicción del Pipeline si es default en 6 meses
    prediccion_cliente = pipeline_model.predict_proba(data_cliente_df)
    prob_default_cliente = prediccion_cliente[:, 1]
    categoria_riesgo_cliente = Negocio().categorias_riesgo(probabilidad_cliente = prob_default_cliente)
    decision_negocio = Negocio().decision_negocio(probabilidad_cliente = prob_default_cliente)
    
    # Decisión según threshold óptimo (maximizado el F1 Score)
    with open('./artifacts/metrics/best_threshold.json', 'r') as f:
        best_threshold = json.load(f)
    decision_f1 = np.where(prob_default_cliente.item() >= best_threshold['threshold'], "Rechazar", "Aprobar").item()

    return {
        'probabilidad_default': round(prob_default_cliente.item(), 3),
        'categoria_riesgo': categoria_riesgo_cliente,
        'decision_negocio': decision_negocio,
        'decision_f1_score': decision_f1,
        'shap_waterfall': shap_waterfall_base64
    }

















