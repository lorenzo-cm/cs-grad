import json
import sys
import openai


from modules.utils.baseGPT import BaseGPT 
from modules.utils.utils import *
from modules.utils.forms import *
from database.dbHandler import *
from modules.responser.contact.responser import * 


try: 
    from modules.error.responser import *
except:
    from error.responser import *


from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv('NAME')

contact_settings = {"role": "system", "content": f'''
            Você faz parte de um sistema de identificação de interesse em nosso produto. 
            Você é o setor responsável por identificar a intenção do usuário de conhecer mais e confirmar que o usuário gostaria de ser contactado.            
            Assim, você deve identificar alguns parâmetros:
            
            name: nome do usuário
            email: email do usuário
            
            Caso o usuário queira confirmar o contato, você deve ativar a flag:
            
            confirm: confirmar o contato
            
            Além disso, caso o usuário não forneça, peça discretamente e gentilmente pelo nome e email. 
                        
            Caso não saiba a intenção deixe todas as flags como None
                                
            Entenda a frase pedaço por pedaço para gerar a conclusão final
        '''}

contact_examples = {'role': 'assistant', 'content': '''
    Prompt: Gostei do seu produto, como faço para colocar no meu negócio?
    Resposta: {"name": "None", "email": "None", "confirm": "None"}
                        
    Prompt: Gostaria de confirmar o contato
    Resposta: {"name": "None", "email": "None", "confirm": "1"}
                        
    Prompt: meu email de contato é X@X.com
    Resposta: {"name": "None", "email": "X@X.com" "confirm": "None"}
'''}
                        
exctract_keys_settings = {
            "name": "extract_keys",
            "description": "Se o usuário quiser fazer uma reserva use esta função para extrair as informações necessárias.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Nome para o contato"
                    },
                    "confirmation": {
                        "type": "integer",
                        "description": "Flag para confirmar o contato"
                    }
                }
            },
        }