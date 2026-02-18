from modules.utils.baseGPT import *
from embeddings.embeddings import *

load_dotenv()

class ResponserEmbeddings(BaseGPT):
    def __init__(self, site_name) -> None:
        super().__init__()
        os.environ["OPENAI_API_KEY"] = os.getenv('KEY') if os.getenv('KEY') !=  None else os.getenv('OPENAI_API_KEY')
        self.site_name = site_name


    def run(self, id, prompt:str, last_messages:str='', context:str='', force_saving=False):
        """Runs the responser

        Args:
            prompt (str): user prompt for site info
            last_messages (str, optional): the previous messages of the user and the bot. Defaults to ''.
            context (str, optional): aditional context if it is necessary. Defaults to ''.

        Returns: 
            response (str): response of the bot
            docs (list): list of documents that the bot used to generate the response
        """
        additional_context = {}
        
        if last_messages:
            additional_context['last_messages'] = last_messages
            
        if context:
            additional_context['context'] = context
        try:
            if force_saving:
                return run_embeddings(id, prompt, additional_context, force_saving=True)
            
            else:
                return run_embeddings(id, prompt, additional_context, force_saving=False)
        except:
            return "Garanta que você possui um pdf funcional para fazer perguntas sobre ele! Você pode inserir um pdf na área do usuário", []