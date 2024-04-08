try:
    from modules.identifier.settings import *
except:
    from settings import *


class Identifier(BaseGPT):    
    def __init__(self):
        super().__init__()

        self.messages.append(identifier_settings)
        self.messages.append(identifier_examples)
        # self.messages.append(identifier_examples_fine_tuning)

        self.functions.append(forward_settings)
        self.function_call = {'name': 'forward'}

        # self.model = 'gpt-3.5-turbo-16k'
        # self.max_tokens=10

    def forward(self,  info, resp, human, miss):
        return {
            'info': info,
            'resp': resp,
            'human': human,
            'miss': miss,
        }


    def run(self, prompt:str, last_message:str=''):
        if last_message:
            self.messages.append({"role": "assistant", "content": "last_messages" + last_message})

        self.messages.append({"role": "user", "content": prompt})

        self.response = self.create()

        if hasattr(self.response, 'choices') and self.response.choices:
            choice = self.response.choices[0]
            if hasattr(choice, 'message'):
                response_message = choice.message


        if hasattr(response_message, 'function_call') and response_message.function_call:
                    function_call = response_message.function_call
                    function_name = function_call.name
                    function_args = json.loads(function_call.arguments)

                    available_functions = {
                        'forward': self.forward,
                        # Add other functions as necessary
                    }

                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(
                            info=function_args.get('info'),
                            resp=function_args.get('resp'),
                            human=function_args.get('human'),
                            miss=function_args.get('miss')
                        )


                    return function_response    





if __name__ == '__main__':
    prompt = input()
    identifier = Identifier()
    print(identifier.run(prompt))