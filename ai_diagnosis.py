import os
import json
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError(
        "A variável GROQ_API_KEY não foi encontrada.\n"
        "Defina no .env ou nas variáveis do Render."
    )

groq_client = Groq(api_key=GROQ_API_KEY)

# Prompt rígido para forçar JSON válido
SYSTEM_PROMPT = """
Você é um assistente médico de triagem. Sua resposta DEVE ser exclusivamente JSON válido.

FORMATO OBRIGATÓRIO DA RESPOSTA:

{
  "diagnoses": [
    {
      "name": "...",
      "probability": "alta|média|baixa",
      "description": "...",
      "severity": "leve|moderada|grave"
    }
  ],
  "recommendations": [
    "texto"
  ],
  "warning_signs": [
    "texto"
  ],
  "seek_immediate_care": true,
  "general_advice": "texto"
}

NÃO ESCREVA NADA FORA DO JSON.
NÃO USE COMENTÁRIOS.
NÃO USE TEXTO LIVRE ANTES OU DEPOIS DO JSON.
SOMENTE JSON PURO.
"""


def extract_json(text):
    """Extrai JSON mesmo se o modelo enviar texto fora do JSON."""
    try:
        return json.loads(text)
    except:
        # tenta capturar o JSON entre { ... }
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except Exception:
            raise ValueError("Não foi possível extrair JSON da resposta do modelo.")


def analyze_symptoms(age, sex, symptoms, duration, intensity, additional_info=""):

    additional_info_line = (
        f"- Informações adicionais: {additional_info}" if additional_info else ""
    )

    user_prompt = f"""
Paciente:
- Idade: {age}
- Sexo: {sex}
- Sintomas: {symptoms}
- Duração: {duration}
- Intensidade: {intensity}
{additional_info_line}

Gere o JSON conforme as regras.
"""

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1200,
        )

        content = response.choices[0].message.content

        print("\n===== RESPOSTA BRUTA DO GROQ =====")
        print(content)
        print("==================================\n")

        result = extract_json(content)
        return result

    except Exception as e:
        print("\n" + "=" * 60)
        print("Erro ao analisar sintomas:")
        print(e)
        print("=" * 60 + "\n")

        return {
            "diagnoses": [
                {
                    "name": "Erro na Análise",
                    "probability": "desconhecida",
                    "description": (
                        "Não foi possível processar sua solicitação no momento. "
                        "Pode ser falha na API ou resposta inválida."
                    ),
                    "severity": "desconhecida",
                }
            ],
            "recommendations": [
                "Tente novamente em alguns instantes.",
                "Se houver preocupação, procure atendimento presencial.",
            ],
            "warning_signs": [],
            "seek_immediate_care": False,
            "general_advice": "Em caso de dúvida, procure atendimento médico.",
        }
