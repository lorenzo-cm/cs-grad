
try:
    from modules.contact.settings import *
except:
    from .settings import *

import time

class Contact(BaseGPT):
    def __init__(self):
        super().__init__()

        self.responser = ResponserContact()

        self.messages.append(contact_settings)
        self.messages.append(contact_examples)

        self.functions.append(exctract_keys_settings)
        self.function_call = {'name': 'extract_keys'}


    def forward(self, db:DatabaseHandler, user_id:str, prompt:str, last_messages:str='', *args, **kwargs) -> str:   
                
        context, flag = self.run(db, user_id, prompt, last_messages, *args, **kwargs)

        print(f'Context: {context},  Flag: {flag}\n\n\n')

        if flag == 'confirmation':
            return "Fico muito feliz que você se interessou pelas minhas altas capacidades de atendimento. Segue o link para preencher o formulário de confirmação: https://Iara.one/form. Posso te ajudar em algo mais?"
        elif flag == 'offer':
            return self.responser.run(prompt, context, last_messages, flag)   
        elif flag == 'first_offer':
            db.set_bool(user_id, True)
            return self.responser.run(prompt, context, last_messages, flag)
        else:
            ErrorResponser().handleError('contact flag not found')

    def extract_keys(self,
                    id = 1,
                    db:DatabaseHandler = None,
                    name = None,
                    confirmation = None, 
                    *args, **kwargs) -> (dict, str):
        
        # print(f'FLAGS: alter: {alter}, cancel: {cancel}, consult: {consult}, confirmation: {confirmation}')

        # Info from db
        user_from_db:User|None = db.select_user(id, name=True)

        #inciializa o contexto
        context = ""


        print(f'Name: {name}, id: {id}, confirmation: {confirmation}')

        # New info passed rn
        user_new = User(id=id, name=name, confirmation_flag=confirmation)
        print(f'User new: {user_new}')

        print(1)
        # Se não tem nem usuario nem reserva, deve-se criar ambos
        if not user_from_db:
            user_from_db = db.insert_user(user_new)
        else:
            user_from_db = db.update_user(user_new)
        print(2)   
        updated_user = db.select_user(id, name=True, confirmation_flag=True)
        print(3)
        context = updated_user.to_dict()
        print(4)
        user_confirmation = updated_user.confirmation_flag

        print(f'User confirmation: {user_confirmation}')

        if confirmation and user_confirmation:
            return context, 'confirmation'
        
        elif not confirmation and user_confirmation:
            return context, 'offer'
        
        else:
            return context, 'first_offer'


    def run(self, db:DatabaseHandler(), id:str, prompt:str, last_messages:str='', *args, **kwargs):

        self.messages.append({"role": "user", "content":str(last_messages) + '\n' + str(prompt)})

        self.response = self.create()

        if hasattr(self.response, 'choices') and self.response.choices:
            choice = self.response.choices[0]
            if hasattr(choice, 'message'):
                response_message = choice.message


        if hasattr(response_message, 'function_call') and response_message.function_call:
            function_call = response_message.function_call
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)
            
            available_functions = {'extract_keys': self.extract_keys}

            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                function_response = function_to_call(
                    id=id,
                    db=db,
                    name=function_args.get('name'),
                    confirmation=function_args.get('confirmation'),
                    *args,
                    **kwargs
                )

            return function_response
        

if __name__ == '__main__':
    db:DatabaseHandler = DatabaseHandler()
    reservation = Contact()

    prompt = str(input('*** '))
    
    response = reservation.forward('+5531725253', db, '898989', prompt)

    print(response)