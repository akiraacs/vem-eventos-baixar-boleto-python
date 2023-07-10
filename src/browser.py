from datetime import datetime
from time import sleep

from playwright.sync_api import sync_playwright


class IniciaBrowser:
    def __init__(self, playwright):
        #-----INICIA NAVEGADOR-----
        browser = playwright.chromium.launch(headless=False)
        self.page = browser.new_page()
        self.page.set_default_timeout(5000)

class ProvemUsuarios(IniciaBrowser):

    def login_trusoll(self, login, senha):
        self.page.goto('https://vem.provem.app/admin/funcionario/login')
        self.page.get_by_label("Login:").fill(login)
        self.page.get_by_label("Senha:").fill(senha)
        self.page.get_by_role("button", name="Confirmar").click()

    def obter_dados_cliente(self, cpf):
        self.page.goto('https://vem.provem.app/admin/usuario/listar')
        self.page.locator("#filter_cpf").fill(cpf)
        self.page.get_by_role("button", name="Aplicar Filtros").click()
        self.page.locator(".alt > td").first.click()
        cpf_cliente = self.page.get_by_label("CPF*:").input_value()
        self.page.get_by_role("link", name="Dados de Acesso").click()
        senha_cliente = self.page.get_by_label("Senha:").input_value()
        self.page.pause()

        return cpf_cliente, senha_cliente

class ProvemCompras(IniciaBrowser):
    def __init__(self, playwright):
        super().__init__(playwright)

    def login_provem(self, cpf_cliente, senha_cliente):
        try:
            self.page.goto('https://web.provem.app/login')
            self.page.get_by_label("CPF:").fill(cpf_cliente)
            self.page.get_by_label("Senha:").fill(senha_cliente)
            self.page.get_by_role("button", name="Login").click()
            self.page.wait_for_url('https://web.provem.app/')

        except Exception:
            raise Exception('Erro ao fazer login')


    def acessar_compra(self):
        try:
            self.page.goto('https://web.provem.app/compras')
            self.page.locator('xpath=//*[@id="root"]/div/div/div[3]/a').click()

        except Exception:
            raise Exception('Não exsistem compras ativas para esse cliente')

    def gerar_boleto(self):
        # try:
        #-----DATA DE ANÁLISE PARA OS BOLETOS-----
        data_atual = datetime.now()
        mes_atual = datetime.now().month
        data_vencimento_analise = datetime(data_atual.year, mes_atual, 9).strftime('%d/%m')

        boleto_encontrado = False
        index = 0
        while index <= 8:
            # try:
            self.page.locator('.m-10 > .bg-white > div > div > div:nth-child(4) > span:nth-child(2)').locator(f'nth={index}').click()
            sleep(8)

            bloco_pagamento = self.page.locator('.m-10').locator(f'nth={index}').inner_text().split('\n')
            data_vencimento_boleto = bloco_pagamento[1]
            status_boleto = bloco_pagamento[4]

            self.page.pause()

            if data_vencimento_analise in data_vencimento_boleto and status_boleto == 'Pendente':

                boleto_encontrado = True
                print('entrou')
                with self.page.expect_popup() as page1_info:
                    self.page.get_by_role("button", name="Confirmar").click()
                page1 = page1_info
                print(page1)
                sleep(1000)

                index += 1
                break
                
            if boleto_encontrado == False:
                raise Exception('Não possui boleto do dia 09 para o mês vigente')

                # except Exception:
                #     pass


        # except Exception as error:
        #     print(error)

        # print('tentando fazer download')
        # with self.page.expect_download() as download_info:
        #     self.page.get_by_role("button", name="Confirmar").click()
        #     download = download_info.value
        #     print(download.path())
        # download.save_as('C:\\ROBO BAIXAR BOLETO\\boleto.pdf')
        # print('fim')

if __name__ == '__main__':
    cpf_cliente = '70136747612'
    senha_cliente = 'lucas001'

    with sync_playwright() as playwright:
        site_provem_compras = ProvemCompras(playwright=playwright)
        site_provem_compras.login_provem(cpf_cliente=cpf_cliente, senha_cliente=senha_cliente)

        site_provem_compras.acessar_compra()

        site_provem_compras.gerar_boleto()