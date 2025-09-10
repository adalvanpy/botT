<<<<<<< HEAD
=======
<<<<<<< HEAD

=======
>>>>>>> bdf2095 (att segurança)
>>>>>>> 151fed0 (alterações feitas)
import requests
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import json
from datetime import datetime

idempotency_key = str(uuid.uuid4())

<<<<<<< HEAD
# 🔐 Suas credenciais
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ACCESS_TOKEN_MP = os.getenv("ACCESS_TOKEN_MP")
=======
<<<<<<< HEAD
TELEGRAM_TOKEN = "8090506199:AAFtcLML6n18k_GuLgjI_W1i9Cx241-Lvj4"
ACCESS_TOKEN_MP = "APP_USR-8447337980819064-090921-cb0b31ffe7d3f74fb1c9f82d2fc08392-388306825"
=======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ACCESS_TOKEN_MP = os.getenv("ACCESS_TOKEN_MP")
>>>>>>> bdf2095 (att segurança)
>>>>>>> 151fed0 (alterações feitas)

GRUPO_VIP_LINK = 'https://t.me/+yy-y1Y9lc54wZGMx'

pagamentos_pendentes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Olá {user.first_name}! 👋\n\n"
        "Para acessar o grupo VIP, você precisa fazer o pagamento via Pix.\n"
        "Valor: R$15,00\n"
        "Após o pagamento, digite ou click em /verificar para obter o link de acesso vip!"
    )

    payload = {
        "transaction_amount": 15.00,
        "description": "Acesso ao grupo VIP",
        "payment_method_id": "pix",
        "payer": {
            "email": "cliente@email.com"
        }
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN_MP}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())
    }

    try:
        response = requests.post("https://api.mercadopago.com/v1/payments", json=payload, headers=headers)
        data = response.json()

        if 'point_of_interaction' in data:
            qr_code = data['point_of_interaction']['transaction_data']['qr_code']
            await update.message.reply_text(f"Use este código Pix:\n{qr_code}")

            payment_id = data['id']
            user_id = update.effective_user.id
            pagamentos_pendentes[user_id] = {
            "payment_id": payment_id,
            "liberado": False,
            "data_inicio": None
            }

        else:
            await update.message.reply_text("⚠️ Houve um erro ao gerar o código Pix. Tente novamente mais tarde.")
            print("Erro na resposta da API:", data)

    except Exception as e:
        await update.message.reply_text("⚠️ Erro inesperado ao tentar gerar o Pix.")
        print("Exceção:", e)


async def verificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in pagamentos_pendentes:
        await update.message.reply_text("❌ Nenhum pagamento pendente encontrado para você.")
        return

    payment_id = pagamentos_pendentes[user_id]["payment_id"]
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN_MP}"
    }

    response = requests.get(f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers)
    data = response.json()

    if data.get("status") == "approved":
        pagamentos_pendentes[user_id]["liberado"] = True
        pagamentos_pendentes[user_id]["data_inicio"] = datetime.now()
        salvar_dados()

        await update.message.reply_text(
            f"✅ Pagamento aprovado!\n\nAqui está seu acesso ao grupo VIP por 30 dias:\n{GRUPO_VIP_LINK}"
        )
    else:
        await update.message.reply_text("⏳ Pagamento ainda não aprovado. Tente novamente em alguns minutos.")


ARQUIVO_DADOS = "pagamentos.json"

def salvar_dados():
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(pagamentos_pendentes, f, default=str)

def carregar_dados():
    global pagamentos_pendentes
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f:
            pagamentos_pendentes = json.load(f)

async def validade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in pagamentos_pendentes or not pagamentos_pendentes[user_id]["liberado"]:
        await update.message.reply_text("❌ Você ainda não tem acesso VIP ativo.")
        return

    data_inicio = datetime.fromisoformat(pagamentos_pendentes[user_id]["data_inicio"])
    dias_restantes = 30 - (datetime.now() - data_inicio).days

    if dias_restantes > 0:
        await update.message.reply_text(f"🗓️ Seu acesso VIP expira em {dias_restantes} dias.")
    else:
        await update.message.reply_text("⚠️ Seu acesso VIP expirou. Faça um novo pagamento para continuar.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("verificar", verificar))
app.add_handler(CommandHandler("validade", validade))
HEAD
app.run_polling()
HEAD
app.run_polling()
app.run_polling()
bdf2095 (att segurança)
151fed0 (alterações feitas)
