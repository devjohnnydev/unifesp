"""
Módulo de diagnóstico diferencial usando IA (Groq)
Utiliza modelos da Groq (ex: Llama 3) para analisar sintomas e sugerir diagnósticos diferenciais.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis do .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError(
        "A variável de ambiente GROQ_API_KEY não foi encontrada.\n"
        "Verifique se o arquivo .env está na mesma pasta do app.py "
        "e se contém a linha:\n\nGROQ_API_KEY=SUACHAVEAQUI\n"
    )

# Cliente da Groq
groq_client = Groq(api_key=GROQ_API_KEY)


def analyze_symptoms(age, sex, symptoms, duration, intensity, additional_info=""):
    """
    Analisa sintomas e retorna diagnósticos diferenciais prováveis.

    Args:
        age: Idade do paciente
        sex: Sexo do paciente
        symptoms: Descrição dos sintomas
        duration: Duração dos sintomas
        intensity: Intensidade dos sintomas
        additional_info: Informações adicionais (condições pré-existentes, etc)

    Returns:
        dict com diagnósticos diferenciais e recomendações
        (conforme o formato esperado pela aplicação)
    """

    system_prompt = """Você é um assistente médico especializado em triagem inicial e diagnóstico diferencial.
Sua função é ajudar pessoas em regiões com baixa cobertura médica a entender seus sintomas.

IMPORTANTE: 
- Sempre enfatize que isto NÃO substitui consulta médica presencial
- Foque em orientações gerais de saúde e sinais de alerta
- Use linguagem simples e acessível
- Considere condições comuns e prevalentes no Brasil
- Sempre recomende procurar atendimento médico quando necessário

Responda em JSON com este formato exato:
{
  "diagnoses": [
    {
      "name": "Nome da condição",
      "probability": "alta/média/baixa",
      "description": "Descrição breve e clara",
      "severity": "leve/moderada/grave"
    }
  ],
  "recommendations": [
    "Recomendação 1",
    "Recomendação 2"
  ],
  "warning_signs": [
    "Sinal de alerta 1",
    "Sinal de alerta 2"
  ],
  "seek_immediate_care": true/false,
  "general_advice": "Conselho geral de cuidados"
}"""

    additional_info_line = ""
    if additional_info:
        additional_info_line = f"- Informações adicionais: {additional_info}"

    user_prompt = f"""Paciente com as seguintes características:
- Idade: {age} anos
- Sexo: {sex}
- Sintomas: {symptoms}
- Duração: {duration}
- Intensidade: {intensity}
{additional_info_line}

Por favor, analise estes sintomas e forneça diagnósticos diferenciais prováveis com recomendações."""

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            # Alguns modelos da Groq suportam JSON estruturado nesse formato
            response_format={"type": "json_object"},
            max_output_tokens=2048,
            temperature=0.2,
        )

        content = completion.choices[0].message.content
        if not content:
            raise ValueError("Resposta vazia da API Groq.")

        result = json.loads(content)
        return result

    except Exception as e:
        # LOG detalhado no terminal para debug
        print("\n" + "=" * 60)
        print("Erro ao analisar sintomas com Groq:")
        print(f"Tipo: {type(e)}")
        print(f"Detalhes: {e}")
        print("Modelo usado:", GROQ_MODEL)
        print("=" * 60 + "\n")

        # Fallback: estrutura padrão de erro, para não quebrar o template
        return {
            "diagnoses": [
                {
                    "name": "Erro na Análise",
                    "probability": "desconhecida",
                    "description": (
                        "Não foi possível processar sua solicitação no momento. "
                        "Por favor, tente novamente em alguns minutos."
                    ),
                    "severity": "desconhecida",
                }
            ],
            "recommendations": [
                "Tente novamente mais tarde.",
                "Se os sintomas persistirem, procure atendimento médico presencial."
            ],
            "warning_signs": [],
            "seek_immediate_care": False,
            "general_advice": "Em caso de dúvida, sempre procure atendimento médico."
        }
