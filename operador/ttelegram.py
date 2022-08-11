from telegram.ext.updater import Updater
from telegram import ReplyKeyboardMarkup
from dados import atualizar
from pywinauto.keyboard import send_keys

updater = Updater(
    "5410422526:AAEdRSlwYPFNKSvaZD8m_Cy3utpoPdp1F_U", use_context=True)

def enviarMensagemOperacao(dados, mensagem):
    
    message = '*Entradas*\n\n'
    stopDetectado = ''

    x = mensagem.split('\r\n')
    mensagem = ''
    for dado in x:
            if(len(dado) > 5):
                aux = dado.split('|')
                if('STOP' in aux[1]):
                    stopDetectado ='*' + aux[1].strip() + '*'
                else:

                    status = '❌'
                    if aux[5].strip() == 'WIN':
                        status = '✅'

                    mensagem += aux[0].strip() + ' ' + aux[1].strip() + ' ' + status + '\n'
                    mensagem += '*Tipo* : ' + aux[2].strip() + '\n'
                    mensagem += '*Entrada* : ' + aux[3].strip() + '\n'
                    mensagem += '*Gales* : ' + aux[4].strip() + '\n'
                    mensagem += '*LUCRO* : ' + aux[6].strip() + '\n\n'
                

   # mensagem = mensagem.split('\r\n')

    message += mensagem + stopDetectado
    message_reply_text = message
    keyBoard1 = ReplyKeyboardMarkup([['Interromper']], resize_keyboard=True)

    try:
        updater.bot.delete_message( dados['chatid'], dados['idmensagem'])    
    except:
        print('')

    idMensagem = updater.bot.send_message(chat_id=dados['chatid'], text=message_reply_text, reply_markup=keyBoard1,  parse_mode='Markdown')
    atualizar('usuarios', {'chatid': dados['chatid']}, {'idmensagem' : idMensagem.message_id})
    send_keys("{ENTER}")

def enviarMensagemAndamento(dados):

    atualizar('usuarios', {'chatid': dados['chatid']}, {
        'subacao': 'operacaoandamento'})

    message = '*Operacao em andamento !*\n\n'
    keyBoard1 = ReplyKeyboardMarkup([['Interromper']], resize_keyboard=True)

    message_reply_text = message
    updater.bot.send_message(
        chat_id=dados['chatid'], text=message_reply_text, reply_markup=keyBoard1,   parse_mode='Markdown')


def enviarMensagemInterromper(dados):

    atualizar('usuarios', {'chatid': dados['chatid']}, {
        'subacao': '', 'acao': '', 'operando': '0'})

    message = '*Operacao interrompida com sucesso !*\n\n'
    mainbutton = [
        ['Voltar']
    ]
    keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)

    message_reply_text = message
    updater.bot.send_message(
        chat_id=dados['chatid'], text=message_reply_text, reply_markup=keyBoard1,  parse_mode='Markdown')


def enviarMensagemParidade(dados, mensagem, janela):
    atualizar('usuarios', {'chatid': dados['chatid']}, {
        'operando': 'paridade', 'nomejanela': janela})

    mensagem = mensagem.replace('PAYOUT de ', 'Payout ')
    mensagem = mensagem.replace('assertividade', 'acerto')

    opcoesImpar = []
    opcoesPar = []
    auxOpcoes = mensagem.split('+')

    auxOpcoes = auxOpcoes[0].split(" - ")
    impar = True
    for a in auxOpcoes:
        a = a.strip()
        if(len(a) < 7):
            if impar:
                opcoesImpar.append(a)
                impar = False
            else:
                opcoesPar.append(a)
                impar = True
        else:
            try:
                a = a.split("%")[2].strip()
            except:
                a = a.strip()
            if(len(a) > 2):
                if impar:
                    opcoesImpar.append(a)
                    impar = False
                else:
                    opcoesPar.append(a)
                    impar = True

    keyBoard1 = ReplyKeyboardMarkup([opcoesImpar, opcoesPar,['Interromper']], resize_keyboard=True)
    mensagem = '*Selecione o par desejado*\n\n' + mensagem + "\n\n___Use o menu para selecionar uma opcao___"
    message_reply_text = mensagem
    updater.bot.send_message(
        chat_id=dados['chatid'], text=message_reply_text, reply_markup=keyBoard1,  parse_mode='Markdown')
