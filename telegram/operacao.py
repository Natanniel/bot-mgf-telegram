
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dados import atualizar


def hallOperacao(dados, update: Update):
    
    if(update.message.text == 'Editar'):
        atualizar('usuarios', {'chatid': update.message.chat_id}, {
                  'subacao': 'Editar'})

        message = '*Deseja operar em conta real ou demo ?*\n___Use o menu para selecionar uma opcao___'
        mainbutton = [
            ['Real', 'Demo']
        ]

        keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
        message_reply_text = message
        update.message.reply_text(
            message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

    else:

        if(dados['subacao'] == ''):
            message = '*Operacao*\n\n'
            message += '*Conta* : ' + dados['conta'] + '\n'
            message += '*Operar* : ' + dados['operar'] + '\n'
            message += '*Payout minimo* : ' + \
                str(dados['payout-minimo']) + '\n'
            message += '*Valor entrada* : ' + str(dados['entrada']) + '\n'
            message += '*Stop-Win* : ' + str(dados['stopwin']) + '\n'
            message += '*Stop-Loss* : ' + str(dados['stoploss']) + '\n'
            message += '*Delay* : ' + str(dados['delay']) + '\n'

            mainbutton = [
                ['Editar', 'Voltar']
            ]

            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = message
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

        if(dados['subacao'] == 'Editar'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'conta': update.message.text, 'subacao': 'opcao'})
            message = '*Deseja operar na digital, binaria ou com Maior Payout ?*\n___Use o menu para selecionar uma opcao___'
            mainbutton = [
                ['Digital'],
                ['Binaria'],
                ['Maior Payout']
            ]
            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = message
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')

        if(dados['subacao'] == 'opcao'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                'operar': update.message.text, 'subacao': 'payout-minimo'})
            message = '*Digite o payout minimo para operar (apenas numeros) :*'

            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'payout-minimo'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'payout-minimo': update.message.text, 'subacao': 'entrada'})
            message = '*Qual o valor que voce deseja usar para entradas (apenas numeros) :*'
            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'entrada'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'entrada': update.message.text, 'subacao': 'stopwin'})
            message = '*Qual o valor de stop-win voce deseja usar (apenas numeros) :*'
            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'stopwin'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'stopwin': update.message.text, 'subacao': 'stoploss'})
            message = '*Qual o valor de stop-loss voce deseja usar (apenas numeros) :*'
            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'stoploss'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'stoploss': update.message.text, 'subacao': 'delay'})
            message = '*Qual o valor de delay voce deseja usar (apenas numeros) :*'
            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

        if(dados['subacao'] == 'delay'):
            atualizar('usuarios', {'chatid': update.message.chat_id}, {
                      'delay': update.message.text, 'subacao': ''})
            message = '*Dados alterados com sucesso !*'
            message_reply_text = message
            update.message.reply_text(
                message_reply_text,  parse_mode='Markdown')

            message = '*Operacao*\n\n'
            message += '*Conta* : ' + dados['conta'] + '\n'
            message += '*Operar* : ' + dados['operar'] + '\n'
            message += '*Payout minimo* : ' + str(dados['payout-minimo']) + '\n'
            message += '*Valor entrada* : ' + str(dados['entrada']) + '\n'
            message += '*Stop-Win* : ' + str(dados['stopwin']) + '\n'
            message += '*Stop-Loss* : ' + str(dados['stoploss']) + '\n'
            message += '*Delay* : ' + str(update.message.text) + '\n'

            mainbutton = [
                ['Editar', 'Voltar']
            ]

            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = message
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1, parse_mode='Markdown')
