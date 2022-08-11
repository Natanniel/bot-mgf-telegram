
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dados import atualizar


def hallOperando(dados, update: Update):

    if(dados['subacao'] == 'senha'):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {
                  'subacao': 'operando', 'operando': '1', 'acao': '🤖 Operar', 'senhaiq': update.message.text})

        message = '*Iniciando operacao*\n\n'
        message += '___Aguarde instrucoes do robo___'

        mainbutton = [
            ['Interromper']
        ]

        keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
        message_reply_text = message
        update.message.reply_text(
            message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

    if(dados['subacao'] == ''):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {
                  'subacao': 'senha',  'acao': '🤖 Operar'})
        
        message = '*Iniciando operacao*\n\n'
        message += 'Por favor informe sua senha iqoption:'     

        message_reply_text = message
        update.message.reply_text(
            message_reply_text,  parse_mode='Markdown')


    
    if(update.message.text == 'Interromper'):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {
            'subacao': '', 'operando': 'interromper'})

        message = '*Interrompendo operacao*\n\n'
        message += '___Por favor, aguarde___'

        message_reply_text = message
        update.message.reply_text(
            message_reply_text,  parse_mode='Markdown')


    if(dados['subacao'] == 'operando' and dados['operando'] == 'paridade' and update.message.text != 'Interromper'):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {'operando':  update.message.text, 'subacao' : 'paridadeenviada'})

        message = '*Comando enviado*\n\n'
        message += '*Par selecionado* : '  +update.message.text +'\n'
        message += '___Por favor, aguarde___'

        message_reply_text = message
        update.message.reply_text(            message_reply_text,  parse_mode='Markdown')

   