try:
    from .settings import *
except:
    from modules.responser.contact.settings import *

class ResponserContact(BaseGPT):
    def __init__(self):
        super().__init__()

    def run(self, prompt:str, context:str, last_messages:str='', flag=None):
        print(f"\n\n\nprompt: {prompt}, context: {context}, last_messages: {last_messages}, flag: {flag}\n\n\n")
        if flag:
            if flag == 'confirmation':
                self.messages.append(confirmation_settings)
                self.messages.append(confirmation_examples)
                self.messages.append({"role": "user", "content": "contexto " + str(context) + '\n' + last_messages + '\n' + prompt})
                pass
            elif flag == 'offer':
                self.messages.append(offer_settings)
                self.messages.append(offer_examples)
                self.messages.append({"role": "user", "content": 'contexto: ' + str(context) + '\n' + 'last_message: '+ last_messages + '\n' +  'prompt: ' + prompt})
                pass
            elif flag == 'first_offer':
                self.messages.append(first_offer_settings)
                self.messages.append(first_offer_examples)
                self.messages.append({"role": "user", "content": 'contexto: ' + str(context) + '\n' + 'last_message: '+ last_messages + '\n' +  'prompt: ' + prompt})
                pass
            else:
                return ErrorResponser().handleError('contact flag not found')
        else:
            return ErrorResponser().handleError('contact flag not found')
        
        self.response = self.create(func=0)

        if hasattr(self.response, 'choices') and self.response.choices:
            choice = self.response.choices[0]
            if hasattr(choice, 'message'):
                response_message = choice.message

        if hasattr(response_message, 'content') and response_message.content:
            response_message = response_message.content

        return response_message

if __name__ == '__main__':
    responser = ResponserContact()
    last_messages = \
    '''
    olá, boa tarde
    Boa tarde, Carlos! Como posso ajudar você hoje?
    '''
    context = '{"name": "Carlos Augusto", "phone": "000000000""}'
    old_context = '{"name": "Carlos Augusto", "phone": "11999999999""}'
    prompt = input('Prompt: ')
    response = responser.run(prompt, context, last_messages, flag = "consulta")
    print(response)