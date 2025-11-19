"""
Rotas da aplicação TeleAcolhe
"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Consultation
from ai_diagnosis import analyze_symptoms
import json

# Blueprint principal da aplicação
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Página inicial"""
    return render_template("index.html")


@bp.route("/sintomas")
def symptoms_form():
    """Formulário de sintomas"""
    return render_template("symptoms.html")


@bp.route("/processar", methods=["POST"])
def process_symptoms():
    """Processa os sintomas e gera diagnóstico"""
    try:
        # Coletando dados do formulário
        age = int(request.form.get("age", 0))
        sex = request.form.get("sex", "")
        symptoms = request.form.get("symptoms", "")
        duration = request.form.get("duration", "")
        intensity = request.form.get("intensity", "")
        additional_info = request.form.get("additional_info", "")
        
        # Validando dados
        if not all([age, sex, symptoms, duration, intensity]):
            return redirect(url_for("main.symptoms_form"))
        
        # Analisando sintomas com IA
        diagnosis_result = analyze_symptoms(
            age=age,
            sex=sex,
            symptoms=symptoms,
            duration=duration,
            intensity=intensity,
            additional_info=additional_info,
        )
        
        # Salvando consulta no banco de dados
        consultation = Consultation(
            age=age,
            sex=sex,
            symptoms=symptoms,
            duration=duration,
            intensity=intensity,
            additional_info=additional_info,
            diagnosis_result=json.dumps(diagnosis_result, ensure_ascii=False),
        )
        db.session.add(consultation)
        db.session.commit()
        
        # Armazenando resultado na sessão para exibição
        session["last_diagnosis"] = diagnosis_result
        session["consultation_id"] = consultation.id
        
        return redirect(url_for("main.results"))
    
    except Exception as e:
        print(f"Erro ao processar sintomas: {e}")
        session["error_message"] = (
            "Não foi possível processar sua solicitação. "
            "Por favor, tente novamente mais tarde."
        )
        return redirect(url_for("main.symptoms_form"))


@bp.route("/resultados")
def results():
    """Página de resultados"""
    diagnosis = session.get("last_diagnosis")
    consultation_id = session.get("consultation_id")
    
    if not diagnosis:
        return redirect(url_for("main.index"))
    
    return render_template(
        "results.html",
        diagnosis=diagnosis,
        consultation_id=consultation_id,
    )


@bp.route("/sobre")
def about():
    """Página sobre o TeleAcolhe"""
    return render_template("about.html")


@bp.route("/como-funciona")
def how_it_works():
    """Página explicando como funciona"""
    return render_template("how_it_works.html")
