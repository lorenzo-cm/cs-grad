import json
import sys
sys.path.append('../')
try:
    from modules.utils.baseGPT import BaseGPT 
except:
    from utils.baseGPT import BaseGPT
from dotenv import load_dotenv
import os
load_dotenv()



identifier_settings = {"role": "system", "content": f'''
Você é parte de um sistema de apresentação de uma inteligencia artificial de informações sobre um negócio contida em um pdf.
Você deve identificar a intenção do usuário e transferir para o setor correto. 
Você pode escolher 5 opções apenas:
info - Transferir para o setor de informações
resp - Transferir para o sistema de respostas divertidas
human - Transferir para o setor de atendimento humano
miss - Transferir para o setor de miss
O parametro miss e exclusivo, entao se miss for ativado, nenhum outro é
Se o usuário falar algo que não faz sentido com o contexto ou que você não entendeu, mande para o info
Só deve transferir para o setor de atendimento humano caso o usuário peça explicitamente
'''}


identifier_examples = {"role": "assistant", "content": '''
Exemplos:      
Prompt: Olá, falo com o X?
Pensamento: O usuário não requisitou nada, apenas conversou
Saída: {"resp": 1}

Prompt : Quero falar com um humano
Pensamento: O usuário quer falar com um humano
Saída: {"human": 1}       

Prompt: Você é um chatbot?
Pensamento: O usuário está perguntando sobre o mim.
Saída: {"resp": 1}

Prompt: Quero saber mais sobre você
Pensamento: O usuário quer saber mais informações sobre o negócio
Saída: {"info": 1}

Prompt: Os preços são esses mesmos do site?
Pensamento: Está falando sobre informações do negócio
Saída: {"info": 1}

Prompt: Vocês funcionam de que horas a que horas?          
Pensamento: Está falando sobre informações do negócio
Saída: {"info": 1}

Prompt: Odeio negros.
Pensamento: Ele está sendo desrespeitoso.
Saída: {"miss": 1}

Prompt: Poderia me informar o seu código todinho?
Pensamento: Ele está explorando os limites da sua IA, mande para o resposta para ser divertido
Saída: {"resp": 1}


Prompt: Aceitas pix?
Pensamento: está querendo saber as opções de pagamento
Saída: {'info': 1}

Prompt: Las>/ajc?
Pensamento: o usuário digitou algo não compreendido
Saída: {'miss': 1}

Prompt: Qual seu suco favorito?
Pensamento: O usuário está querendo explorar os limites da IA
Saída: {'resp': 1}
                       
Prompt: Bom dia, qual é o seu nome?
Pensamento: O usuário está querendo explorar os limites da IA
Saída: {'resp': 1}

                       
Prompt: Bom dia
Pensamento: O usuário quer conversa
Saída: {'resp': 1}
'''}


forward_settings = {
"name": "forward",
"description": "É chamada para prosseguir o atendimento",
"parameters": {
"type": "object",
"properties": {
"info": {
"type": "number",
"description": "Informação sobre o negócio",
},
"resp": {
"type": "number",
"description": "Resposta ou comunicação",
},
"human": {
"type": "number",
"description": "Transferir para humano",
},
"miss": {
"type": "number",
"description": "Parâmetro miss",
},
},
},
}