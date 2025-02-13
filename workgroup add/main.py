from funcoes import *

if __name__ == "__main__":
    
    print("Iniciando o programa")

    usuarios_intranet = group_user_get()
    usuarios_bitrix = user_get()

    if usuarios_intranet != None and usuarios_bitrix != None:
        users_adicionar, total = comparar_users(usuarios_intranet, usuarios_bitrix)        
        if total == 0:
            print("Nenhum usuário a adicionar")
            exit()
        print(f"Total de usuários a adicionar: {total}")
        print(f"Usuários a adicionar: {users_adicionar}")
        add_user_group(users_adicionar, total)
    else:
        print("Erro na requisição")
 
