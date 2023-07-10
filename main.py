import sys

import yaml
from loguru import logger
from playwright.sync_api import sync_playwright

from src.browser import ProvemUsuarios
from src.arquivo_clientes import Arquivo
from time import sleep


def main():
    try:
        DIRETORIO_PADRAO = 'C:\\ROBO BAIXAR BOLETO\\'
        ARQUIVO_CONFIGURACAO = DIRETORIO_PADRAO + 'info_configs.yaml'

        with open(ARQUIVO_CONFIGURACAO, 'r') as arquivo_config:
            ARQUIVO_CONFIGURACAO = yaml.safe_load(arquivo_config)

        ARQUIVO_CLIENTES = DIRETORIO_PADRAO + ARQUIVO_CONFIGURACAO['nome_arquivo']
        LOGIN_TRUSOLL = ARQUIVO_CONFIGURACAO['site_provem_usuarios']['login']
        SENHA_TRUSOLL = ARQUIVO_CONFIGURACAO['site_provem_usuarios']['senha']

        #-----OBTEM DADOS DO ARQUIVO EXCEL-----
        arquivo_clientes = Arquivo(ARQUIVO_CLIENTES)
        df = arquivo_clientes.df

        with sync_playwright() as playwright:

            site_provem_usuarios = ProvemUsuarios(playwright=playwright)

            #-----LOOP EM CADA LINHA/CLIENTE-----
            for indice, linha in df.iterrows():
                try:

                    #-----OBTEM DADOS CLIENTE DO ARQUIVO EXCEL-----
                    nome, cpf, hotel = arquivo_clientes.dados_cliente(linha_arquivo=linha)

                    # df.at[indice, 'Boleto Baixado'] = 'teste'
                    # print(df)
                    # sleep(5)
                    # continue

                    #-----EFETUA LOGIN NO SITE PROVEM USUARIOS/TRUSOLL-----
                    site_provem_usuarios.login_trusoll(login=LOGIN_TRUSOLL, senha=SENHA_TRUSOLL)

                    #-----OBTEM DADOS DO CLIENTE DO SITE TRUSOLL-----
                    cpf_cliente, senha_cliente = site_provem_usuarios.obter_dados_cliente(cpf=cpf)
                    print(cpf_cliente, senha_cliente)
                    sleep(1000)

                except Exception as error:
                    linha_erro = sys.exc_info()[-1].tb_lineno
                    logger.critical(f'-Erro- || Mensagem erro: {error} || Linha: {linha_erro}')

    except Exception as error:
        linha_erro = sys.exc_info()[-1].tb_lineno
        logger.critical(f'-Erro- || Mensagem erro: {error} || Linha: {linha_erro}')

if __name__ == '__main__':
    main()