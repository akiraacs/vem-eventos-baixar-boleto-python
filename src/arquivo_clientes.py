import pandas as pd


class Arquivo:
    def __init__(self, arquivo):
        self.df = pd.read_excel(arquivo, dtype=str)

    def dados_cliente(self, linha_arquivo):
        nome = linha_arquivo['Nome']
        cpf = linha_arquivo['CPF']
        hotel = linha_arquivo['Hotel']

        return nome, cpf, hotel