"""
Módulo de diagnóstico diferencial usando IA
Utiliza OpenAI GPT-5 para analisar sintomas e sugerir diagnósticos diferenciais
"""
import os
import json
from openai import OpenAI

# Referenciando blueprint:python_openai
# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)


def analyze_symptoms(age, sex, symptoms, duration, intensity, additional_info=""):
    """
    Analisa sintomas e retorna diagnósticos diferenciais prováveis
    
    Args:
        age: Idade do paciente
        sex: Sexo do paciente
        symptoms: Descrição dos sintomas
        duration: Duração dos sintomas
        intensity: Intensidade dos sintomas
        additional_info: Informações adicionais (condições pré-existentes, etc)
    
    Returns:
        dict com diagnósticos diferenciais e recomendações
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

    # Construct additional info text separately to avoid f-string issues
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
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Erro ao analisar sintomas: {e}")
        return {
            "diagnoses": [
                {
                    "name": "Erro na Análise",
                    "probability": "desconhecida",
                    "description": "Não foi possível processar sua solicitação no momento. Por favor, tente novamente.",
                    "severity": "desconhecida"
                }
            ],
            "recommendations": [
                "Por favor, tente novamente mais tarde",
                "Se os sintomas persistirem, procure atendimento médico presencial"
            ],
            "warning_signs": [],
            "seek_immediate_care": False,
            "general_advice": "Em caso de dúvida, sempre procure atendimento médico."
        }
