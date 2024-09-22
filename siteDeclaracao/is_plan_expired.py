import logging
import os
from dateutil.relativedelta import relativedelta
from django.utils import timezone

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log para DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato personalizado
    filename=os.path.join(LOGS_DIR, "log_file.log"),  # Redireciona para um arquivo 
)
# Adiciona um handler para exibir no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)


def is_plan_expired(user, dataNow=None):
    if dataNow is None:
        dataNow = timezone.now()  # Usa a data atual se não for fornecida
    
    # Log para verificar se a função está sendo chamada
    logging.info(f'Verificando se o plano do usuário {user.DataUserPayment.name}...')

    # Obtendo a data de criação do plano e o tempo de ativação
    created_at = user.DataUserPayment.created_at
    active_time_months = user.DataUserPayment.active_time_month

    # Log para debug
    logging.debug(f'Plano do usuário {user.DataUserPayment.name} criado em {created_at} e ativo por {active_time_months} meses')

    # Calculando a data de expiração do plano
    expiration_date = created_at + relativedelta(days=active_time_months)

    if dataNow >= expiration_date:
        # Calculando o tempo desde a expiração
        time_since_expiration = dataNow - expiration_date
        months_since_expiration = relativedelta(dataNow, expiration_date).months
        days_since_expiration = time_since_expiration.days
        message = f"O plano do usuário {user.DataUserPayment.name} expirou há {months_since_expiration} meses e {days_since_expiration} dias."
        logging.info(message)
        return True, message
    else:
        # Calculando o tempo restante para a expiração
        months_to_expiration = relativedelta(expiration_date, dataNow).months
        days_to_expiration = (expiration_date - dataNow).days
        message = f"O plano do usuário {user.DataUserPayment.name} expira em {months_to_expiration} meses e {days_to_expiration} dias."
        logging.info(message)
        return False, message