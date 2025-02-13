import requests
import json
import time
import math
from env import *

max_retries = 3
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'qmb=0.'
    }

def url_metodo(metodo:str):
    return f"{bitrix_url}/{token}/{metodo}"

def group_user_get():

    url = url_metodo("sonet_group.user.get")
    payload = json.dumps({
    "ID": 679
    })

    retries = 0
    response = None
    while retries < max_retries:
        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
            user_ids = [i["USER_ID"] for i in response["result"]]
            total = len(user_ids)
            print("Total de usuários da Intranet: ", total)
            return user_ids
        except requests.exceptions.RequestException as e: # Caso ocorra um erro na requisição
            print(f"requisição falhou: {e}")
            retries += 1
            if retries == max_retries:
                print("Número máximo de tentativas excedido, tente novamente mais tarde")
                return None
            time.sleep(5) # Espera 5 segundos antes de tentar novamente

def user_get():

    url = url_metodo("user.get")
    payload = json.dumps({
      "USER_TYPE": "employee",
      "ACTIVE": True
    })
    
    #Primeira Requisição Para Pegar os 50 primeiros usuários e o total de usuários
    retries = 0
    response = None
    while retries < max_retries:
        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
            break
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed: {e}")
            retries += 1
            if retries == max_retries:
                print("Número máximo de tentativas excedido, tente novamente mais tarde")
                return None
            time.sleep(5)
    if response and "result" in response:
        user_ids = [i["ID"] for i in response["result"]]
        total = response["total"]
        print("Total de usuários ativos no bitrix: ", total)
    else:
        print("Erro na requisição")
        return None

    if total > 50:
        for i in range(50, total + 1, 50):
            payload = json.dumps({
                "USER_TYPE": "employee",
                "ACTIVE": True,
                "start": i
            })
            retries = 0
            response = None
            while retries < max_retries:
                try:
                    response = requests.request("POST", url, headers=headers, data=payload).json()
                    break
                except requests.exceptions.RequestException as e:
                    print(f"Falha na requisição: {e}")
                    retries += 1
                    if retries == max_retries:
                        print("Número máximo de tentativas excedido, tente novamente mais tarde")
                        return None
                    time.sleep(5)
            if response and "result" in response:
                user_ids.extend([i["ID"] for i in response["result"]])
                progresso = int((i / total) * 100)
                if math.ceil(progresso % 10) == 0:
                    print("Identificando usuários...\n Progresso: ", progresso,"%")
            else:
                print("Erro na requisição")
                return None
                           
    return user_ids

def comparar_users(A:list, B:list):
    A = set(A)
    B = set(B)
    diferenca = list(set(B) - set(A))
    total = len(diferenca)
    return diferenca, total

def add_user_group(users_adicionar:list, total:int):

    tempo_espera = 300

    url = url_metodo("sonet_group.user.add")

    for user, i in zip(users_adicionar, range(total + 1)):
        retries = 0
        while retries < max_retries:
            try:
                payload = json.dumps({
                "GROUP_ID": 679,
                "USER_ID": user
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                resultado = response.raise_for_status()
                if resultado == None:
                    progresso = int((i / total) * 100)
                    if math.ceil(progresso % 10) == 0:
                        print("Adicionando usuários ao grupo...\n Progresso: ", progresso,"%")
                    break
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries == max_retries:
                    print(f"Falha na requisição: {e}\nNúmero máximo de tentativas excedido. Aguardando {tempo_espera} segundos para tentar novamente")
                    time.sleep(tempo_espera)
                time.sleep(5)

    print("Todos os usuários foram adicionados com sucesso")
                    