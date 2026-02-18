from datetime import datetime
import os
import re
try:
    from modules.utils.forms import *
except:
    from modules.utils.forms import *

# UTILS.PY é um arquivo que contém funções que são utilizadas em mais de um arquivo do projeto.

# Essa função retorna a data e a hora atual
def current_date_and_hour():
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')  # e.g., '2023-08-04'
    current_hour_and_minute = now.strftime('%H:%M')  # e.g., '14:30' for 2:30 PM
    return date, current_hour_and_minute


def find_key_identifier(input_dict):
    for key, value in input_dict.items():
        if value is not None:
            return key
    return None 

def convert_date_format(date_str: str) -> str:
    """Convert date from 'day-month-year' to 'year-month-day' format."""
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    return date_obj.strftime('%Y-%m-%d')


def convert_date(date_str):
    """Converts date DD-MM-YYYY or DD/MM/YYYY into DD/MM/YYYY

    Args:
        date_str (str): input date as a string

    Returns:
        str: formatted date string
    """
    if '-' in date_str:
        date_str = date_str.replace('-', '/')

    # Split the date into day, month, and year
    day, month, year = date_str.split('/')

    # Create the new date format
    formatted_date = f"{day}/{month}/{year}"
    return formatted_date


# Forma um dicionário com as colunas informadas
def make_dict(row, columns):
    keys = columns
    return dict(zip(keys, row))


def valida_email(email):
    """
    Verify if the given email has a valid format.
    
    :param email: str, email to be verified
    :return: bool, True if valid format, False otherwise
    """
    # Regular expression to match most common email formats
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    return bool(re.match(email_regex, email))


def valida_cpf(cpf):

    # Retira apenas os dígitos do CPF, ignorando os caracteres especiais
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    print(f"numeros: {numeros}")

    quant_digitos = False
    validacao1 = False
    validacao2 = False

    if len(numeros) == 11:
        quant_digitos = True

        soma_produtos = sum(a*b for a, b in zip(numeros[0:9], range(10, 1, -1)))
        digito_esperado = (soma_produtos * 10 % 11) % 10
        if numeros[9] == digito_esperado:
            validacao1 = True

        soma_produtos1 = sum(a*b for a, b in zip(numeros[0:10], range(11, 1, -1)))
        digito_esperado1 = (soma_produtos1 * 10 % 11) % 10
        if numeros[10] == digito_esperado1:
            validacao2 = True

        if quant_digitos == True and validacao1 == True and validacao2 == True:
            cpf_formatado = ''.join(map(str, numeros))
            print(f"O CPF {cpf_formatado} é válido.")
            return True, cpf_formatado
        else:
            cpf_formatado = ''.join(map(str, numeros))
            print(f"O CPF {cpf_formatado} não é válido... Tente outro CPF...")
            return False, False

    else:
        cpf_formatado = ''.join(map(str, numeros))
        print(f"O CPF {cpf_formatado} não é válido... Tente outro CPF...")
        return False, False


def merge_dicts(dict1, dict2) -> dict:
    """
    Merge two dictionaries into one.

    example:
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    merged_dict = merge_dicts(dict1, dict2) = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    """
    merged_dict = dict1.copy()
    merged_dict.update(dict2)
    return merged_dict


def update_dict(dict_old, dict_new) -> dict:
    """
    Update a dictionary with new values based in the new one.

    example:
    dict_old = {'a': 1, 'b': 2, 'c': 10}
    dict_new = {'a': 3, 'b': None, 'd': 4}
    updated_dict = update_dict(dict_old, dict_new) = {'a': 1, 'b': 2, 'd': 4}
    """
    result = {}
    for key in dict_new:
        if dict_new[key] is not None:
            result[key] = dict_new[key]
        elif dict_old is not None and key in dict_old:
            result[key] = dict_old[key]
        else:
            result[key] = None
    return result


def get_path_to_project():
    # Get the current working directory
    current_directory = os.getcwd()

    # Search for the root directory named "hotelGPT"
    root_directory = None
    for path in os.path.abspath(current_directory).split(os.path.sep):
        if path == "hotelGPT":
            root_directory = os.path.abspath(current_directory)[:os.path.abspath(current_directory).index(path) + len(path)]
            break

    if root_directory:
        return root_directory
    else:
        return 'WrongPath'


def extract_cost(input_string):
    # Define a regular expression pattern to match the cost (USD)
    pattern = r"Total Cost \(USD\): \$([\d.]+)"

    # Search for the pattern in the input string
    match = re.search(pattern, input_string)

    if match:
        cost_usd = match.group(1)
        return float(cost_usd)
    else:
        return None

def getUpdatedInfo(parameters:dict, visitor:User) -> tuple[User, dict]:
    if visitor:
        visitorDict = visitor.to_dict()
        listaDeValidade = []
        for key in parameters.keys():
            #! FOR EACH PARAMETER ADDED YOU HAVE TO MANUALLY SET THE PREFERENCE HERE
            if key == 'name':
                if parameters[key] != None:
                    visitor.name = parameters[key]
                else:
                    visitor.name = visitorDict[key]
            elif key == 'email': 
                if parameters[key] != None:
                    visitor.email = parameters[key]
                else:
                    visitor.email = visitorDict[key]
            elif key == 'cpf': 
                if parameters[key] != None:
                    visitor.cpf = parameters[key]
                    cpfValido, cpfFormatado = valida_cpf(visitor.cpf)
                    # Se o cpf não for válido, pega o antigo
                    if not cpfValido:
                        visitor.cpf = visitorDict[key]
                        listaDeValidade.append("cpf")
                    # Se o cpf for válido pega o novo
                    else:
                        visitor.cpf = cpfFormatado
                else:
                    # Se não tiver cpf novo, pega o antigo
                    visitor.cpf = visitorDict[key]
            #! COLOCAR RETORNO DE ERRO AQUI
            else:
                print(f"key {key} not found")
    else:
        return parameters, None
    
    return visitor, listaDeValidade


if __name__ == '__main__':
    emailList = ["tomastlm2000@gmail.com", "tomas@aila.one", "jpjunho@yahoo.com.br", "olsimone@terra.com.br", "tomaslm00@ufmg.br", "tomas.muniz@dcc.ufmg.br"]
    for email in emailList:
        print(valida_email(email))
    pass