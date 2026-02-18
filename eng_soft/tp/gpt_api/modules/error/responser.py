class ErrorResponser:
    def __init__(self, error = None):
        self.error = error
    

    def handleError(self, error):
        if error == 'database':
            return "Desculpe ocorreu um erro de comunicação com o nosso banco de dados! Tente novamente mais tarde."
        if error == 'not implemented':
            return "Desculpe, essa funcionalidade ainda não foi implementada! Peça para conversar com um humano para resolver esse problema!"
        if error == "identifier":
            return "Desculpe, ocorreu um erro inesperado com minhas capacidades cognitivas! Tente novamente mais tarde."
        if error == "contact flag not found":
            return "Desculpe, ocorreu um erro inesperado com o meu interpretador! Tente novamente mais tarde."