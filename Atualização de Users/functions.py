import pandas as pd
import requests
import json
from env import *
from time import sleep
import os


def requisicao(metodo, chamada, parametro, resposta_parametro, payload=None, tentativas=3):

    url_requisicao = f"{bitrix_url}/{token}/{chamada}?{parametro}={resposta_parametro}"
    headers = {"Content-Type": "application/json", "Cookie": "qmb=0."}

    for tentativa in range (1, tentativas + 1):
        try:
            response = requests.request(metodo, url_requisicao, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:
                response_bitrix = response.json()
                operating = response_bitrix["time"]["operating"]
                return response_bitrix, operating
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None, None
            
        except requests.exceptions.ConnectTimeout:
            print(f"Timeout ao tentar conectar ao Bitrix")
        
        except requests.exceptions.RequestException as e:
            print (f"Erro de requisição: {e}")

        if tentativa <= tentativas:
            sleep(5)



def verificar_operating(operating, limite=350, pausa=300):
    if operating >= limite:
        print('Pausa para zerar o operating')
        sleep(pausa)


def achar_usuarios(dataframe):

    ids_users = []
    siglas = []
    contratantes = []
    grupos = []
    
    for email, sigla, pj_contratante, grupo_economico in zip(dataframe["E-MAIL BNKRIO"], dataframe["SIGLA CORRETA"], dataframe["CONTRATANTE CORRETA"], dataframe["GRUPO ECONÔMICO"]):
        response_bitrix, operating = requisicao("GET", "user.get", "EMAIL", f"{email}")
        if response_bitrix:
            id_usuario = response_bitrix["result"][0]["ID"]
            ids_users.append(id_usuario)
            siglas.append(sigla)
            contratantes.append(pj_contratante)
            grupos.append(grupo_economico)
            print(f"ID:{id_usuario}; operating:{operating}")
            verificar_operating(operating)
        else:
           print(f"Não foi encontrado usuário com o email {email}") 
        
    
    dados = {
        "ID": ids_users,
        "SIGLA": siglas,
        "CONTRATANTE": contratantes,
        "GRUPO": grupos
    }
    
    novo_df = pd.DataFrame(dados)
    novo_df.to_excel("Ajustes_Bitrix_Final.xlsx", index=False)
    if os.path.exists("Ajustes_Bitrix_Final.xlsx"):
        print("Arquivo temporário criado")
        return novo_df
    else:
        print("Não foi possível criar o arquivo temporário")
        return None

def atualizar_usuarios(dataframe):

    for id, sigla, pj_contratante, grupo_economico in zip(dataframe["ID"], dataframe["SIGLA"], dataframe["CONTRATANTE"], dataframe["GRUPO"]): 
        payload_data = {}
        if sigla:
            payload_data["UF_USR_1649342940885"] = sigla
        if pj_contratante:
            payload_data["UF_USR_1731945583942"] = int(pj_contratante)
        if grupo_economico:
            payload_data["UF_USR_1734442439507"] = grupo_economico

        payload = json.dumps(payload_data)

        response_bitrix, operating = requisicao("POST", "user.update", "ID", id, payload=payload)
        if response_bitrix:
            print(f"User {id} atualizado: SIGLA {sigla}; Pj Contratante: {pj_contratante}; Grupo Economico: {grupo_economico} | Operating: {operating}")
            verificar_operating(operating)
        else:
           print(f"Não foi possível atualizar o usuário {id}")
    
    if os.path.exists("Ajustes_Bitrix_Final.xlsx"):
        os.remove("Ajustes_Bitrix_Final.xlsx")
        print("Arquivo temporário removido")
    else:
        print("O arquivo não chegou a ser produzido")

