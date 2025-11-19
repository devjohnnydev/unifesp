from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância global do SQLAlchemy
db = SQLAlchemy()


class Consultation(db.Model):
    """Modelo para armazenar consultas realizadas pelos usuários"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados demográficos
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    
    # Dados dos sintomas
    symptoms = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    intensity = db.Column(db.String(20), nullable=False)
    additional_info = db.Column(db.Text)
    
    # Diagnóstico gerado pela IA
    diagnosis_result = db.Column(db.Text)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consultation {self.id} - {self.created_at}>'
