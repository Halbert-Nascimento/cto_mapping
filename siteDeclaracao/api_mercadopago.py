import mercadopago
from .chaveToken import chaveAPI


def gerar_link_pagamento( session_id, attempt_id, item, valor, descricao,  quantidade):
    sdk = mercadopago.SDK(chaveAPI())

    request_options = mercadopago.config.RequestOptions()
    # request_options.custom_headers = {
    #     'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
    # }

    request = {
        "items": [
            { 
                "id": '1', 
                "title": item, 
                "quantity": quantidade,
                "unit_price": valor,
                "description": descricao,
            }
        ],
        "metadata": {
            "attempt_id": attempt_id, 
            "session_id": session_id,
        },
        "back_urls": {
            "success": "https://www.htecfull.com/love/success",
            "failure": "https://www.htecfull.com/love/fail",
            "pending": "https://www.htecfull.com/love/pending",
        },
        "auto_return": "all",
        
    }
    preference_response = sdk.preference().create(request)
    preference = preference_response["response"]
    print(preference)
    print(preference["init_point"])

    return preference["init_point"]


    