from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))


### A Classe BaseGPT é a classe mãe que segura todos os métodos e atributos comuns entre os modelos de GPT-3
class BaseGPT():
    def __init__(self, # Padrão de python
                 function_call='auto', # Qual função ele vai chamar | auto significa que ele vai escolher
                 model='gpt-3.5-turbo', # Qual modelo ele vai usar
                 temperature=0.2, # Quão aleatório ele vai ser | Se for usar o top_p, deixe em 0.5
                 max_tokens=4096, # Quantos tokens ele vai usar
                 top_p=0.5) -> None: # Quão aleatório ele vai ser | Se for usar o temperature, deixe em 0.5
    
        self.key = None # Chave de acesso à API
        self.prompt = None # Prompt que vai ser usado para gerar a resposta
        self.context = None # Contexto que vai ser usado para gerar a resposta
        self.last_message = None # Última mensagem que foi enviada do usuário e da AI

        self.messages:list = list() # Lista de mensagens que vão ser usadas para instruir a AI
        self.functions:list[dict] = list() # Lista de funções que vão ser usadas para instruir a AI

        self.function_call = function_call # Função que vai ser chamada
        self.model = model # Modelo que vai ser usado
        self.temperature = temperature # Quão aleatório ele vai ser | Se for usar o top_p, deixe em 0.5
        self.max_tokens = max_tokens # Quantos tokens ele vai usar
        self.top_p = top_p # Quão aleatório ele vai ser | Se for usar o temperature, deixe em 0.5

        self.response = {} # save response to log prices
        self.total_price = 0 


    def calc_price(self, prompt_tokens, completion_tokens):
        price_input = 0.0015/1000
        price_output = 0.002/1000

        return prompt_tokens * price_input + completion_tokens * price_output
    

    def log_prices(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            prompt_tokens = self.response['usage']['prompt_tokens']
            completion_tokens = self.response['usage']['completion_tokens']
            price = self.calc_price(prompt_tokens, completion_tokens)
            self.total_price += price
            print(f'Price: ${price}')
            return result
        return wrapper
    

    def log_prices_in(self):
        if self.response.get('usage') == None:
            return 0
        prompt_tokens = self.response['usage']['prompt_tokens']
        completion_tokens = self.response['usage']['completion_tokens']
        price = self.calc_price(prompt_tokens, completion_tokens)
        self.total_price += price
        # print(f'Price: ${price}')
        return price

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, new_total_price):
        self._total_price = new_total_price

    def create(self, func=1): # Cria uma instância de ChatCompletion, caso não queira usar uma função coloque o parâmetro func para 0
        if func: 
            return client.chat.completions.create(model=self.model,
            messages=self.messages,
            functions=self.functions,
            function_call=self.function_call,
            temperature=self.temperature,
            # max_tokens=self.max_tokens, # it is kinda bugged
            top_p=self.top_p)
        else:
            return client.chat.completions.create(model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            # max_tokens=self.max_tokens, # it is kinda bugged
            top_p=self.top_p)
        

    def run(self): # Modulo de execução
        pass

    def forward(self): # Modulo de transferência
        pass

    def clear_messages(self): # Limpar menssagens da lista
        self.messages.clear()