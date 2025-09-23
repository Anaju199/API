# import os
# import django
# import json
# from django.core.mail import send_mail
# from django.conf import settings

# # Configura Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings.dev")
# django.setup()

# def teste_envio_email():
#     # Dados de teste
#     data = {
#         "nome": "Ana Julia",
#         "email": "ana@email.com",
#         "mensagem": "Teste envio direto pelo backend"
#     }

#     try:
#         print("Tentando enviar e-mail...")
#         send_mail(
#             subject="Teste Fale Conosco",
#             message=f"Nome: {data['nome']}\nEmail: {data['email']}\nMensagem:\n{data['mensagem']}",
#             from_email=settings.EMAIL_HOST_USER,  # deve ser igual ao do SMTP
#             recipient_list=[settings.EMAIL_HOST_USER],
#         )
#         print("✅ E-mail enviado com sucesso!")
#     except Exception as e:
#         print(f"❌ Erro ao enviar e-mail: {str(e)}")

# if __name__ == "__main__":
#     teste_envio_email()

import smtplib
from email.message import EmailMessage

host = "smtp.titan.email"
port = 465
email_remetente = "contato@casarohr.com.br"
email_destinatario = "contato@casarohr.com.br"
senha = "Expresso514#"


msg = EmailMessage()
msg['Subject'] = 'Teste Titan'
msg['From'] = email_remetente
msg['To'] = email_destinatario
msg.set_content('Olá! Este é um teste de envio via Titan.')

try:
    # Conectar via SSL na porta 465
    with smtplib.SMTP_SSL("smtp.titan.email", 465) as server:
        server.login(email_remetente, senha)
        server.send_message(msg)
    print("✅ E-mail enviado com sucesso!")
except smtplib.SMTPException as e:
    print("❌ Erro SMTP:", e)