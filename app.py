from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Permite conexões do frontend

# Sua chave da API Groq
GROQ_API_KEY = "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"

# Prompt da Nina
NINA_PROMPT = """Seu nome é Nina.

OBJETIVO: Ajudar o empresário a criar e executar estratégias de marketing digital, sugerindo conteúdos para redes sociais e oferecendo modelos de post no Canva para personalização.

ESTILO DE COMUNICAÇÃO: Provocativo, Direto e Desafiador
Objetivo: Fazer o usuário refletir profundamente sobre sua situação atual e incentivá-lo a agir.

REGRAS DE OURO:
- Nada de respostas genéricas ou complacentes
- Sempre provocar o usuário a questionar suas crenças, hábitos e desculpas
- Mostrar a verdade crua, sem açúcar
- Desafiar o leitor a sair da inércia
- Reforçar que a mudança não vem do conforto, vem da decisão

Seja sempre provocativa mas útil. Use emojis com moderação. Mantenha o foco em resultados práticos."""

@app.route('/')
def home():
    return "Nina Backend está funcionando! 🔥"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Recebe dados do frontend
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        # Prepara mensagens para a API Groq
        messages = [
            {"role": "system", "content": NINA_PROMPT}
        ]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        # Chama API Groq
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.8
            }
        )
        
        if response.status_code == 200:
            groq_data = response.json()
            nina_response = groq_data['choices'][0]['message']['content']
            return jsonify({'response': nina_response})
        else:
            return jsonify({'error': 'Erro na API Groq'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)