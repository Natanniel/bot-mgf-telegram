
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dados import atualizar


def hallMartingale(dados, update: Update):

    if(update.message.text == 'Editar'):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {
                  'subacao': 'Editar'})

        message = '*Deseja ativar/desativar o fator martin-gale ?*\n___Use o menu para selecionar uma opcao___'
        mainbutton = [
            ['🟢 Ativado'],
            ['🔴 Desativado']
        ]
        keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
        message_reply_text = message
        update.message.reply_text(
            message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

    else:

        if(dados['subacao'] == ''):

            martingale = '🔴 Desativado'

            if(dados['martingale'] == 'S'):
                martingale = '🟢 Ativado'

            message = '*Martingale*\n\n'
            message += '*Status* : ' + martingale + '\n'
            message += '*Niveis de Gale* : ' + \
                str(dados['niveis-martingale']) + '\n'

            mainbutton = [
                ['Editar', 'Voltar']
            ]

            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = message
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

        if(dados['subacao'] == 'Editar'):
            martingale = 'S'
            if(update.message.text == '🔴 Desativado'):
                martingale = 'N'

            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'martingale': martingale, 'subacao': 'niveis'})

            message = '*Digite a quantidade de niveis de martin-gale (apenas numeros)*'

            message_reply_text = message
            update.message.reply_text(
            message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'niveis'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'niveis-martingale': update.message.text, 'subacao': ''})

            martingale = '🔴 Desativado'

            if(dados['martingale'] == 'S'):
                martingale = '🟢 Ativado'


            message = '*Martingale*\n\n'
            message += '*Status* : ' + martingale + '\n'
            message += '*Niveis de Gale* : ' + str(update.message.text)

            mainbutton = [
                ['Editar', 'Voltar']
            ]

            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = message
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')
