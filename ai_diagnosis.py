"""
Módulo de diagnóstico diferencial usando IA (Groq)
Utiliza modelos da Groq (ex: Llama 3.3) para analisar sintomas.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis do .env (em desenvolvimento local)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Se não tiver GROQ_MODEL no ambiente, usa Llama 3.3 direto
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError(
        "A variável de ambiente GROQ_API_KEY não foi encontrada.\n"
        "Defina no arquivo .env (para rodar localmente) OU "
        "nas variáveis de ambiente do Render."
    )

# Cliente da Groq
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


def extract_json(text: str) -> dict:
    """Tenta extrair JSON mesmo se vier texto fora do objeto."""
    try:
        return json.loads(text)
    except Exception:
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except Exception:
            raise ValueError("Não foi possível extrair JSON da resposta do modelo.")


def analyze_symptoms(age, sex, symptoms, duration, intensity, additional_info=""):
    """
    Analisa sintomas e retorna diagnósticos diferenciais prováveis.
    """

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
            # ajuda a forçar JSON estruturado em alguns modelos
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        print("\n===== RESPOSTA BRUTA DO GROQ =====")
        print("Modelo:", GROQ_MODEL)
        print(content)
        print("==================================\n")

        result = extract_json(content)
        return result

    except Exception as e:
        import traceback

        print("\n" + "=" * 60)
        print("Erro ao analisar sintomas com Groq:")
        print("Tipo:", type(e))
        print("Detalhes:", e)
        print("Modelo usado:", GROQ_MODEL)
        traceback.print_exc()
        print("=" * 60 + "\n")

        # Fallback para a tela de resultados não quebrar
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
