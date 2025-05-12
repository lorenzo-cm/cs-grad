import json
import sys
sys.path.append('../../')
from modules.utils.baseGPT import BaseGPT
from modules.utils.forms import *
from dotenv import load_dotenv
try: 
    from modules.error.responser import *
except:
    from error.responser import *
import os
load_dotenv()


name = os.getenv('NAME')

offer_settings = {"role": "system", "content": '''
            Você é parte de um serviço automatizado de demonstração.
            Sua função é responder coerentemente de acordo com um contexto,
            Quando o cliente chegou até você, significa que ele está interessado no produto
            Você deve, de acordo com o contexto fornecido, formular uma resposta pedindo para ele confirmar o contato.
            Não peça nenhuma informação, apenas para confirmar o contato.
            Não escreva resposta: ou prompt: antes da mensagem.
            Você deve sempre perguntar se o cliente deseja confirmar o contato.
        '''}

offer_examples = {'role': 'assistant', 'content': '''
        Prompt: 
        Oi aqui é o X, eu fiquei interessado no produto de vocês
        Resposta: 
        Olá X, fico feliz que tenha se interessado pela {name}! Gostaria que nossa equipe entrasse em contato com você para mais informações?
        Prompt: 
        Oi queria comprar a {name}!
        Resposta: 
        É a melhor escolha que você pode fazer pro seu negócio! Gostaria que nossa equipe entrasse em contato com você para mais informações?                             
'''}
                            

confirmation_settings = {"role": "system", "content": '''
            Você é parte de um serviço automatizado de demonstração.
            Sua função é responder coerentemente de acordo com um contexto e as mensagens anteriores.
            Você deve agradecer a intenção do cliente em confirmar o contato e perguntar se ele deseja mais alguma coisa.   
        '''}

confirmation_examples = {'role': 'assistant', 'content': '''
        Prompt: 
        Sim, gostaria!
        Reposta: 
        Perfeito! Segue o link para preencher o formulário de contato! Já já nossa equipe entrará em contato com você!
'''}


first_offer_settings = {"role": "system", "content": '''
            Você é parte de um serviço automatizado de demonstração.
            Sua função é responder coerentemente de acordo com um contexto,
            Quando o cliente chegou até você, significa que ele está interessado no produto
            Você deve, de acordo com o contexto fornecido, formular uma resposta pedindo para ele confirmar o contato.
            Não peça nenhuma informação, apenas para confirmar o contato.
            Não escreva resposta: ou prompt: antes da mensagem.
            Você deve sempre perguntar se o cliente deseja confirmar o contato.
        '''}

first_offer_examples = {'role': 'assistant', 'content': '''
        Prompt: 
        Oi aqui é o X, eu fiquei interessado no produto de vocês
        Resposta: 
        Olá X, fico feliz que tenha se interessado pela {name}! Gostaria que nossa equipe entrasse em contato com você para mais informações?
        Prompt: 
        Oi queria comprar a {name}!
        Resposta: 
        É a melhor escolha que você pode fazer pro seu negócio! Gostaria que nossa equipe entrasse em contato com você para mais informações?                             
'''}