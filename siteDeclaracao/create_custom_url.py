import unicodedata
import re

def create_custom_url(nome1, nome2, id, domain='https://www.htecfull.com/love/post/', separator='-'):
    """Cria uma URL personalizada a partir dos primeiros nomes de duas pessoas e um ID.

    Args:
        nome1 (str): O primeiro nome da primeira pessoa.
        nome2 (str): O primeiro nome da segunda pessoa.
        id (int): Um identificador único.
        domain (str, optional): O domínio base da URL. Defaults to 'https://www.htecfull.com/'.
        separator (str, optional): O separador entre os componentes da URL. Defaults to '-'.

    Returns:
        str: A URL personalizada.

    **Observações:**
    * A função considera apenas o primeiro nome de cada pessoa.
    * Os nomes são truncados em 15 caracteres.
    * Caracteres especiais são removidos.
    """

    # Obter apenas o primeiro nome de cada pessoa
    nome1 = nome1.split()[0][:15].lower()
    nome2 = nome2.split()[0][:15].lower()

    # Remover caracteres especiais, exceto letras, números e hífens
    nome1 = re.sub(r'[^a-zA-Z0-9-]', '', nome1)
    nome2 = re.sub(r'[^a-zA-Z0-9-]', '', nome2)

    # Remover acentos
    nome1 = unicodedata.normalize('NFKD', nome1).encode('ASCII', 'ignore').decode('ASCII')
    nome2 = unicodedata.normalize('NFKD', nome2).encode('ASCII', 'ignore').decode('ASCII')

    # Construir a URL
    url = domain + str(id) + separator + nome1 + separator+"&"+separator+ nome2
    return url