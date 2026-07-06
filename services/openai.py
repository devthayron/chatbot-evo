from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_INSTRUCTIONS = (
    "Você é um chatbot de WhatsApp da empresa Guara. "
    "Responda de forma natural, direta e sem usar markdown. "
    "Cada mensagem do histórico começa com o horário em que foi enviada, "
    "no formato [dd/mm HH:MM]. Use isso pra entender o tempo entre as mensagens "
    "(ex: se o cliente sumiu e voltou depois), mas não repita o horário na sua resposta."
)


class OpenAIService:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-5.4-nano"

    def generate_response(self, messages) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=messages,
            instructions=SYSTEM_INSTRUCTIONS,
        )

        return response.output_text


openai_service = OpenAIService()