import openai 
import os
import json # falta esse
from dotenv import load_dotenv
from datetime import datetime
import pytz
import sys
import threading
import asyncio
sys.path.append('../')

from modules.identifier.identifier import *
from modules.responser.miss.responser import *
from modules.responser.answer.responser import *
from modules.responser.info.responserEmbeddings import *
# from whatsApp.whatsappServer import *
# from whatsApp.chatwootUtils import *
from modules.utils.dates2 import *
from database.dbHandler import *
from modules.utils.forms import *


company_name = "Alia"

def dispatcher(prompt, id):

    print("\n---------------------PROMPT---------------------\n")
    print(prompt)

    #! ---------------------- Initialize Database -----------------------------
  # Database
    db = DatabaseHandler()

    # Initialize user in database
    if not db.check_user_exists(id):
        db.initialize_user(id)

    #! ---------------------- Initialize Variables -----------------------------
    extra = None
    last_messages = db.get_last_message(id)
    if last_messages == None:
        last_messages = ""
    context = ""
    docs = []

    print("\n---------------------LAST MESSAGES---------------------\n")


    # For testing purposes
    print(f"Last messages: {last_messages}")


    # Datetime module
    time_difference, hours, minutes, seconds = get_dt(db, id)
    
    # Flags kwargs
    test_flags = {'test': 1}

    #! ---------------------- Initialize Modules -----------------------------
    identifier = Identifier()
    resp_answer = ResponserAnswer()
    miss = ResponserMiss()
    info = ResponserEmbeddings(company_name)

    #! ---------------------- Remove context -----------------------------
    
    if time_difference is not None:
        if hours is not None:
            if hours >= 3 or time_difference.days >= 1:
                print("\n---------------------CONTEXTO---------------------\n")
                last_messages = ""
                print("Contexto apagado")
    else:
        if hours is not None:
            if hours >= 3:
                last_messages = ""
                print("\n---------------------CONTEXTO---------------------\n")
                print("Contexto apagado")

    test = False

    #! ---------------------- Identifier Run -----------------------------
    # RUN
    intention = identifier.run(prompt=prompt)
    # intention = {'Reserva': 1, 'Informação': None, 'Resposta': None, 'Humano': None, 'Profile': None, 'Miss': None}
    intention_key = find_key_identifier(intention)


    #! ---------------------- MODULES RUN -----------------------------


    if(intention_key == None or intention_key == "miss" or intention_key == "resp" or intention_key == "human"):
        pass
    else:
        # User
        user:User = db.select_user(id)
        if not user:
            user = User(id = id)


    # binary order
    # res, info, resp, human, profile, miss
    print("\n---------------------IDENTIFIER---------------------\n")
    print(intention)
    print(intention_key)
    #! ---------------------- Foward or Run -----------------------------


    # Info
    if intention_key == "info":
        print("\n---------------------INFORMATION---------------------\n")
        try:
            response, docs = info.run(id, prompt, last_messages, context, force_saving=False) # force saving True para quando mudar o pdf ele atualizar
        except:
            response = "Desculpe, algo deu errado. Por favor, tente novamente mais tarde."
            docs = []
    # Resp
    elif intention_key == "resp":
        print("\n--------------------RESPOSTA---------------------\n")
        response = resp_answer.run(prompt, last_messages, context)

    # Human
    elif intention_key == "human":
        print("\n-------------------HUMAN HANDOFF---------------------\n")
        response = 'Para falar com um humano você pode entrar em contato com o número (31) 995302070'

    # Miss
    elif intention_key == "miss":
        print("\n--------------------MISS---------------------\n")
        response = miss.run(prompt, last_messages)


    #! ---------------------- Update Database with new info -----------------------------
    # Update last message    
    db.update_last_message(id, ailm=response, lm=prompt, update_time=True)

    #! ---------------------- Return -----------------------------
    if extra:
        response = response + extra
    


    response_data = {
        "response": response,
        "docs": docs,
    }

    return response_data





if __name__ == '__main__':
    prompt = input("$$ ")
    id = "lulu"
    response = dispatcher(prompt, id)
    print ("-------------------------------------------\n--------- RESPOSTA FINAL DA ALIA ----------\n-------------------------------------------\n")
    print(response)
    print ("-------------------------------------------\n-------------------------------------------\n-------------------------------------------\n")