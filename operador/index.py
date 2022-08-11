from pathlib import Path
from sre_constants import SRE_FLAG_MULTILINE
from time import sleep
from unicodedata import name

from pywinauto import Application, clipboard, findwindows
from pywinauto.keyboard import send_keys


from dados import seleciona,atualizar
from ttelegram import enviarMensagemOperacao, enviarMensagemInterromper,enviarMensagemParidade,enviarMensagemAndamento
import pyperclip
import psutil 

operando = []
while True:

    # Verificar operacoes que precisam ser interrompidas
    # ==================================================

    dados = seleciona('usuarios', {'operando': 'interromper'})
    for dado in dados:
        enviarMensagemInterromper(dado)
        try:
            app = Application(backend="win32")
            app.connect(process=dado['nomejanela'])
            app.top_window().set_focus()  
            sleep(5)
            send_keys("%{F4}")
        except:
            print('Falhao ao fechar janela ' +  str(dado['nomejanela']))
    sleep(1)


    # Verificar operacoes que precisam ser iniciar
    # ==================================================

    dados = seleciona('usuarios', {'operando': '1'})
    for dado in dados:
        rodandoAntes = []        
        process_name = "p.exe"
        for proc in psutil.process_iter():
            if process_name in proc.name():
                rodandoAntes.append(proc.pid)

        app = Application(backend="uia").start(
            'cmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" p.exe"', create_new_console=True, wait_for_idle=False)

        sleep(15)

        
        # CONTA DEMO OU REAL ============
        
        match dado['conta']:
            case 'Demo':
                send_keys(keys='1{ENTER}')
            case _:
                send_keys(keys='2{ENTER}')

        # CONTA DEMO OU REAL ============

        #match dado['operar']:
          #  case 'Digital':
        send_keys(keys='D{ENTER}')
           # case 'Binaria':
            #    send_keys(keys='B{ENTER}')
           # case _:
            #    send_keys(keys='A{ENTER}')

        # PAYOUT MINIMO ============
        send_keys(keys=str(dado['payout-minimo']) + '{ENTER}')

        # VALOR ENTRADAS ============
        send_keys(keys=str(dado['entrada']) + '{ENTER}')

        # STOPS ============
        send_keys(keys=str(dado['stoploss']) + '{ENTER}')
        send_keys(keys=str(dado['stopwin']) + '{ENTER}')

        # MARTINGALE ============
        send_keys(keys=str(dado['martingale']) + '{ENTER}')
        if(dado['martingale']== 'S'):
            send_keys(keys=str(dado['niveis-martingale']) + '{ENTER}')
            sleep(1)
            send_keys(keys='{ENTER}')  
            sleep(1)
            
            
        # DELAY ============
        send_keys(keys=str(dado['delay']) + '{ENTER}')

        # BACKTEST ============
        send_keys(keys=dado['back-tests-periodicos']+'{ENTER}')

        # SOROS ============
        send_keys(keys=str(dado['soros']) + '{ENTER}')

        # SOROS ============
        send_keys(keys=str(dado['email']) +'{ENTER}')
        send_keys(keys=str(dado['senhaiq']) +'{ENTER}')
        send_keys(keys='S{ENTER}')
        sleep(30
        )

        send_keys("^a^c")
        dadosConsole = pyperclip.paste()

        sleep(1)
        dadosConsole = dadosConsole.split('[+] Quais pares deseja operar?')[1]
        dadosConsole = dadosConsole.replace("[x]::", "")
        dadosConsole = dadosConsole.replace("\r\n", "")
        dadosConsole = dadosConsole.split("+")

        mensagem = ''
        for dadoConsole in dadosConsole:
            if len(dado) > 10:
                mensagem += dadoConsole.strip() + '\n'
        
        pid = None
        for proc in psutil.process_iter():
            if process_name in proc.name():
                encontrou = False
                for antigo in rodandoAntes:
                    if antigo == proc.pid:
                        encontrou = True

                if(encontrou == False):
                    pid = proc.pid
     
        enviarMensagemParidade(dado,mensagem,pid)

    # Iniciar uma paridade
    # ==================================================

    dados = seleciona('usuarios', {'subacao': 'paridadeenviada'})
    for dado in dados:
         
        try:
            app = Application(backend="uia")
            app.connect(process=dado['nomejanela'])
            app.top_window().set_focus()
        except:
            try:
                app.top_window().set_focus()
            except:
                sleep(2)

        sleep(2)
        send_keys(dado['operando'] + "{ENTER}")
        enviarMensagemAndamento(dado)
        
        sleep(5)
       

    # Acompanhando operacao 
    # ==================================================

    dados = seleciona('usuarios', {'subacao': 'operacaoandamento'})
    for dado in dados:
              
        try:
            app = Application(backend="win32")
            app.connect(process=dado['nomejanela'])
            app.top_window().set_focus()            
           
            sleep(5)
            send_keys("^a")
            sleep(1)
            send_keys("^c")
            sleep(1)
            dadosConsole = pyperclip.paste()


        except Exception as e:
            print('Erro :' + str(e))
            sleep(10)
            send_keys("^a")
            sleep(1)
            send_keys("^c")
            sleep(1)
            dadosConsole = pyperclip.paste()
          
        try:
            dadosConsole = dadosConsole.split('----------+------------+---------+------------+----+-----------+----------')[2]
                
            dadosConsole = dadosConsole.replace('    |',' |')
            dadosConsole = dadosConsole.replace('        |',' |')
            dadosConsole = dadosConsole.replace('      |',' |')
        
            enviarMensagemOperacao(dado,dadosConsole)
        except:
            print('Falha ao enviar feedback')
    
    sleep(10)
   
