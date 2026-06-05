import pandas as pd
import numpy as np

class Negocio():
    def __init__(self):
        pass

    def categorias_riesgo(self, probabilidad_cliente) -> str:
        """Clasifica al cliente dependiendo la probabilidad de Default"""
        if probabilidad_cliente < 0.20:
            categoria = 'Muy Bajo Riesgo'
        elif probabilidad_cliente < 0.6:
            categoria = 'Riesgo Medio'
        elif probabilidad_cliente < 0.8:
            categoria = 'Alto Riesgo'
        else:
            categoria = 'Muy Alto Riesgo'
        return categoria

    def decision_negocio(self, probabilidad_cliente) -> str:
        """Decide si Aceptar, Rechazar o Revisar Manualmente"""
        if probabilidad_cliente < 0.10:
            return "Aprobar"
        if probabilidad_cliente < 0.25:
            return "Revisión Manual"
        else:
            return "Rechazar"

