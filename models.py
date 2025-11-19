from app import db
from datetime import datetime


class Consultation(db.Model):
    """Modelo para armazenar consultas realizadas pelos usu\u00e1rios"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados demogr\u00e1ficos
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    
    # Dados dos sintomas
    symptoms = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    intensity = db.Column(db.String(20), nullable=False)
    additional_info = db.Column(db.Text)
    
    # Diagn\u00f3stico gerado pela IA
    diagnosis_result = db.Column(db.Text)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consultation {self.id} - {self.created_at}>'
