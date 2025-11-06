from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


app = FastAPI(title="Assistente de Viagem API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GuideRequest(BaseModel):
    country: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    start_date: str = Field(..., example="2026-04-15")  
    days: int = Field(..., gt=0)
    preferences: Optional[str] = None

    @validator("start_date")
    def valid_date_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except Exception:
            raise ValueError("start_date deve estar no formato YYYY-MM-DD")


@app.post("/generate-guide")
def generate_guide(req: GuideRequest):
    try:
        
        start = datetime.strptime(req.start_date, "%Y-%m-%d").date()
        end = start + timedelta(days=req.days - 1)

        
        prompt = (
            f"Você é um assistente de viagem que cria guias turísticos personalizados.\n"
            f"Usuário vai para {req.city}, {req.country} de {start.isoformat()} até {end.isoformat()} "
            f"({req.days} dias).\n"
            f"Preferências: {req.preferences or 'Nenhuma específica'}.\n\n"
            f"Produza um guia prático em português com:\n"
            f"- Resumo rápido do destino (1 parágrafo)\n"
            f"- Itinerário dia-a-dia com atividades e horários sugeridos\n"
            f"- Sugestões de restaurantes/bares por categoria\n"
            f"- Dicas de transporte e custo aproximado (baixo/médio/alto)\n"
            f"- Lista curta de frases úteis no idioma local\n"
            f"- Recomendações de segurança e etiqueta local\n"
            f"Seja objetivo e claro."
        )

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        return {"guide": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar guia: {str(e)}")