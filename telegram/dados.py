import pymongo

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:dKR3DEgE21PMUz6J@principal.t7ghz.mongodb.net/?retryWrites=true&w=majority")


def seleciona(collection, query):
    mydb = myclient["telegrambot"]
    mycol = mydb[collection]
    return mycol.find(query)


def atualizar(collection, query, dados):
    mydb = myclient["telegrambot"]
    mycol = mydb[collection]
    mycol.update_one(query, {"$set": dados})


def cadastrar():
    db = myclient["telegrambot"]
    collection = db["usuarios"]
    dados = {
        "status": True,
        "email": "teste@teste.com.br",
        "senha": "123456",
        "conta": "Demo",
        "operar": "Binaria",
        "payout-minimo": 80,
        "entrada": 2,
        "stoploss": 50,
        "stopwin": 50,
        "delay": 1,
        "martingale": "S",
        "niveis-martingale": 2,
        "back-tests-periodicos": "S",
        "soros": "N",
        "niveis-soros": 2,
        "percentual-soros": 50,
        "acao": "",
        "subacao":"",
        "chatid": "",
        "chatid-tentando": "",
        "operando" : '0',
        "nomejanela" : '',
        'idmensagem':0,
        "senhaiq": ''
    }

    x = collection.insert_one(dados)
