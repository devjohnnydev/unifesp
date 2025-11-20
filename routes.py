"""
Rotas da aplicação TeleAcolhe
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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
    # Se veio alguma mensagem de erro anterior, já fica disponível via flash
    error_message = session.pop("error_message", None)
    return render_template("symptoms.html", error_message=error_message)


@bp.route("/processar", methods=["POST"])
def process_symptoms():
    """Processa os sintomas e gera diagnóstico com IA (Groq)"""
    try:
        # 1. Coleta dados do formulário
        age_raw = request.form.get("age", "").strip()
        sex = request.form.get("sex", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        duration = request.form.get("duration", "").strip()
        intensity = request.form.get("intensity", "").strip()
        additional_info = request.form.get("additional_info", "").strip()

        # 2. Validação básica
        try:
            age = int(age_raw)
        except ValueError:
            age = 0

        if age <= 0 or not (sex and symptoms and duration and intensity):
            session["error_message"] = (
                "Por favor, preencha todos os campos obrigatórios corretamente "
                "(idade, sexo, sintomas, duração e intensidade)."
            )
            return redirect(url_for("main.symptoms_form"))

        # 3. Chama a IA (Groq)
        diagnosis_result = analyze_symptoms(
            age=age,
            sex=sex,
            symptoms=symptoms,
            duration=duration,
            intensity=intensity,
            additional_info=additional_info,
        )

        # LOG no servidor para depuração
        print("\n===== DIAGNÓSTICO GERADO PELA IA =====")
        print(json.dumps(diagnosis_result, ensure_ascii=False, indent=2))
        print("======================================\n")

        # 4. Salva consulta no banco
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

        # 5. Guarda na sessão para exibir na página de resultados
        session["last_diagnosis"] = diagnosis_result
        session["consultation_id"] = consultation.id

        return redirect(url_for("main.results"))

    except Exception as e:
        # Se algo deu ruim fora da IA (db, sessão, etc.)
        import traceback
        print("\n" + "=" * 60)
        print("Erro ao processar sintomas:")
        traceback.print_exc()
        print("=" * 60 + "\n")

        session["error_message"] = (
            "Não foi possível processar sua solicitação no momento. "
            "Por favor, tente novamente em alguns instantes."
        )
        return redirect(url_for("main.symptoms_form"))


@bp.route("/resultados")
def results():
    """Página de resultados"""
    diagnosis = session.get("last_diagnosis")
    consultation_id = session.get("consultation_id")

    if not diagnosis:
        # Se não há diagnóstico na sessão, volta pra home
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
