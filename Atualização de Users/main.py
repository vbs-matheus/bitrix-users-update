from functions import *

#Ativar DF
if __name__ == '__main__':
    df = pd.read_excel("Ajustes_Bitrix.xlsx")
    df_usuarios_atualizar = achar_usuarios(df)
    if df_usuarios_atualizar is not None:
        atualizar_usuarios(df_usuarios_atualizar)
    else:
        print("Não foi possível atualizar os usuários")