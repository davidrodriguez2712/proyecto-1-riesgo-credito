from pydantic import BaseModel, Field
from typing import Literal

class Cliente(BaseModel):
    # Numerical
    credit_limit_used: float = Field(description= 'Límite de crédito utilizado por el cliente')
    no_of_days_employed: int = Field(description= 'Tiempo de permanencia en el último trabajo medido en días del cliente')
    credit_score: float = Field(description= 'Score crediticio del cliente')
    credit_limit: float = Field(description= 'Límite de crédito del cliente')
    total_family_members: int = Field(description= 'Total de miembros de familia del cliente')
    yearly_debt_payments: float = Field(description= 'Pagos por deudas anuales del cliente')
    net_yearly_income: float = Field(description= 'Ingresos anuales del cliente')
    no_of_children: int = Field(description= 'Número de hijos')
    migrant_worker: int = Field(description= 'Si es un trabajdor migrante')
    age: int = Field(description= 'Edad del cliente')
    prev_defaults: int = Field(description= 'Si el cliente tuvo previamente un incumplimiento de pago')

    # Categorical
    gender: Literal['F', 'M'] = Field(description= 'Edad del cliente')
    owns_car: Literal['N', 'Y'] = Field(description= '¿El cliente posee un carro?')
    owns_house: Literal['N', 'Y'] = Field(description= '¿El cliente es dueño de una casa?')
    occupation_type: Literal[
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
    ] = Field(description= 'Tipo de trabajo actual o último del cliente')


class ResponsePrediction(BaseModel):
    probability_default: float
    prediction: int
    #risk_label = str


