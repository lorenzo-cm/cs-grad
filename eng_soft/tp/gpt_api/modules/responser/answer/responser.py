try:
    from .settings import *
except:
    from modules.responser.answer.settings import *

class ResponserAnswer(BaseGPT):
    def __init__(self, key='amenities'):
        super().__init__()

        self.temperature = 0.5
        self.messages.append(awnser_settings)
        self.messages.append(awnser_examples)

    def run(self, prompt:str, last_messages:str='', context:str=''):
        self.messages.append({"role": "user", "content": last_messages + '\n' + context + '\n' + prompt})

        self.response = self.create(func=0)

        if hasattr(self.response, 'choices') and self.response.choices:
            choice = self.response.choices[0]
            if hasattr(choice, 'message'):
                response_message = choice.message

        if hasattr(response_message, 'content') and response_message.content:
            response_message = response_message.content

        return response_message

if __name__ == '__main__':
    responser = ResponserAnswer()
    last_messages = \
    '''
    '''
    prompt = input("$$: ")
    response = responser.run(prompt)
    print(response)