try:
    from .settings import *
except:
    from modules.responser.miss.settings import *

class ResponserMiss(BaseGPT):
    def __init__(self):
        super().__init__()
        self.temperature = 0.8
        self.messages.append(responser_settings)
        self.messages.append(responser_examples)

    def run(self, prompt:str, last_messages:str=''):

        self.messages.append({"role": "user", "content": last_messages + '\n' + prompt})

        self.response = self.create(func=0)

        if hasattr(self.response, 'choices') and self.response.choices:
            choice = self.response.choices[0]
            if hasattr(choice, 'message'):
                response_message = choice.message

        if hasattr(response_message, 'content') and response_message.content:
            response_message = response_message.content

        return response_message


if __name__ == '__main__':
    responser = ResponserMiss()
    last_messages = \
    '''
    '''
    prompt = input('Prompt: ')
    response = responser.run(prompt, last_messages)
    print(response)