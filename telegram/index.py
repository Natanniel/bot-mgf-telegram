from dados import cadastrar, seleciona, atualizar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import re
# Conter a chave da api vinda do botfather
from telegram.ext.updater import Updater
# Isso será invocado toda vez que um bot receber uma atualização
from telegram.update import Update
# Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.callbackcontext import CallbackContext
# Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.commandhandler import CommandHandler
# Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.messagehandler import MessageHandler
# Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from telegram.ext.filters import Filters
from time import sleep

from operacao import hallOperacao
from martingale import hallMartingale
from operando import hallOperando


updater = Updater(
    "5410422526:AAEdRSlwYPFNKSvaZD8m_Cy3utpoPdp1F_U", use_context=True)


def validarEmail(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+",  email)


# inicializar o processo do BOT
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Informe abaixo o seu e-mail exatamente como você colocou quando foi realizar a sua inscrição em nosso produto :")


def verificarUsuarioTemChatLogado(chatid):
    dados = seleciona('usuarios', {'chatid': chatid})
    if(len(list(dados)) > 0):
        return True
    else:
        return False


def hall(update: Update, dados):

    martingale = '🔴'
    backtestes = '🔴'

    if(dados['martingale'] == 'S'):
        martingale = '🟢'

    if(dados['back-tests-periodicos'] == 'S'):
        backtestes = '🟢'

    mainbutton = [
        ['🧠 Operacao', '⚙️ Martin-Gale ' + martingale],
        ['💹 Back-testes ' + backtestes, '🚨 Suporte'],
        ['🤖 Operar']
    ]

    keyBoard1 = ReplyKeyboardMarkup(
        mainbutton, resize_keyboard=True)
    message_reply_text = '*Bem-vindo(a) !*\n\nVoce esta no menu principal.\nClique no icone de menu proximo ao botao do microfone para acessar o menu.'
    update.message.reply_text(
        message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')


def recepcionar(update: Update, context: CallbackContext):

    if verificarUsuarioTemChatLogado(update.message.chat_id):

        dados = seleciona('usuarios', {'chatid': update.message.chat_id})
        dados = list(dados)[0]

        if(update.message.text == 'Voltar'):
            atualizar(
                'usuarios', {'chatid': update.message.chat_id}, {'acao': ''})
            hall(update, dados)
        else:
            if(update.message.text == '🧠 Operacao' or dados['acao'] == '🧠 Operacao'):
                atualizar('usuarios', {'chatid': update.message.chat_id}, {
                          'acao': '🧠 Operacao'})
                hallOperacao(dados, update)

            else:
                # martingale
                if('⚙️ Martin-Gale' in update.message.text or '⚙️ Martin-Gale' == dados['acao']):
                    atualizar('usuarios', {'chatid': update.message.chat_id}, {
                              'acao': '⚙️ Martin-Gale'})
                    hallMartingale(dados, update)

                else:
                    if('Soros' in update.message.text):
                        print('Soros') 
                    else:
                        if('Back-testes' in update.message.text):
                            if(dados['back-tests-periodicos'] == 'S'):
                                atualizar('usuarios', {'chatid': update.message.chat_id}, { 'back-tests-periodicos': 'N'})
                                update.message.reply_text("___Backtest desativado !___",  parse_mode='Markdown')
                                dados = seleciona('usuarios', {'chatid': update.message.chat_id})
                                dados = list(dados)[0]
                                hall(update,dados)
                            else:
                                atualizar('usuarios', {'chatid': update.message.chat_id}, { 'back-tests-periodicos': 'S'})
                                update.message.reply_text("___Backtest ativado !___",  parse_mode='Markdown')
                                dados = seleciona('usuarios', {'chatid': update.message.chat_id})
                                dados = list(dados)[0]
                                hall(update,dados)
                           
                            
                        else:                            
                            if('🤖 Operar' in update.message.text or dados['acao'] in '🤖 Operar'):
                                hallOperando(dados,update)
                     

    else:

        # AREA AINDA NAO LOGADO
        dados = seleciona(
            'usuarios', {'chatid-tentando': update.message.chat_id})
        if(len(list(dados)) > 0):

            # Ja tendo validado o email ele procura validar a senha
            dados = seleciona('usuarios', {'senha': update.message.text})

            if(len(list(dados)) > 0):
                # Tendo confirmado email e senha ele altera o chatid temporario para o chat id autenticado
                atualizar('usuarios', {
                          'chatid-tentando': update.message.chat_id}, {'chatid': update.message.chat_id})
                dados = list(dados)[0]
                hall(update,dados)
            else:
                # Nao confirmando email e senha ele limpa o chat id temporario
                atualizar('usuarios', {
                          'chatid-tentando': update.message.chat_id}, {'chatid-tentando': ''})
                update.message.reply_text(
                    "Usuario ou senha invalido \nPor favor, informe o seu email :")
        else:
            # Valida se o email digitado e valido
            if(validarEmail(update.message.text)):

                dados = seleciona('usuarios', {'email': update.message.text})

                if(len(list(dados)) > 0):
                    # Atualiza o chat-id temporario para o do chat do usuario e solicita a snha
                    atualizar('usuarios', {'email': update.message.text}, {
                        'chatid-tentando': update.message.chat_id})
                    update.message.reply_text("Por favor, informe sua senha :")
                else:
                    update.message.reply_text(
                        "Email nao cadastrado !\nPor favor, informe o seu email :")
            else:
                update.message.reply_text(
                    "Formato de email invalido !\nPor favor, informe o seu email :")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, recepcionar))


updater.start_polling()
print('bot iniciado')
