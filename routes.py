"""
Rotas da aplica\u00e7\u00e3o TeleAcolhe
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from models import Consultation
from ai_diagnosis import analyze_symptoms
import json


@app.route('/')
def index():
    """P\u00e1gina inicial"""
    return render_template('index.html')


@app.route('/sintomas')
def symptoms_form():
    """Formul\u00e1rio de sintomas"""
    return render_template('symptoms.html')


@app.route('/processar', methods=['POST'])
def process_symptoms():
    """Processa os sintomas e gera diagn\u00f3stico"""
    try:
        # Coletando dados do formul\u00e1rio
        age = int(request.form.get('age', 0))
        sex = request.form.get('sex', '')
        symptoms = request.form.get('symptoms', '')
        duration = request.form.get('duration', '')
        intensity = request.form.get('intensity', '')
        additional_info = request.form.get('additional_info', '')
        
        # Validando dados
        if not all([age, sex, symptoms, duration, intensity]):
            return redirect(url_for('symptoms_form'))
        
        # Analisando sintomas com IA
        diagnosis_result = analyze_symptoms(
            age=age,
            sex=sex,
            symptoms=symptoms,
            duration=duration,
            intensity=intensity,
            additional_info=additional_info
        )
        
        # Salvando consulta no banco de dados
        consultation = Consultation(
            age=age,
            sex=sex,
            symptoms=symptoms,
            duration=duration,
            intensity=intensity,
            additional_info=additional_info,
            diagnosis_result=json.dumps(diagnosis_result, ensure_ascii=False)
        )
        db.session.add(consultation)
        db.session.commit()
        
        # Armazenando resultado na sess\u00e3o para exibi\u00e7\u00e3o
        session['last_diagnosis'] = diagnosis_result
        session['consultation_id'] = consultation.id
        
        return redirect(url_for('results'))
        
    except Exception as e:
        print(f"Erro ao processar sintomas: {e}")
        # Store error message in session to display to user
        session['error_message'] = "Não foi possível processar sua solicitação. Por favor, tente novamente mais tarde."
        return redirect(url_for('symptoms_form'))


@app.route('/resultados')
def results():
    """P\u00e1gina de resultados"""
    diagnosis = session.get('last_diagnosis')
    consultation_id = session.get('consultation_id')
    
    if not diagnosis:
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                         diagnosis=diagnosis, 
                         consultation_id=consultation_id)


@app.route('/sobre')
def about():
    """P\u00e1gina sobre o TeleAcolhe"""
    return render_template('about.html')


@app.route('/como-funciona')
def how_it_works():
    """P\u00e1gina explicando como funciona"""
    return render_template('how_it_works.html')
