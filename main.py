import csv


# ==========================================
# 1. CLASSES DE MODELO (HERANÇA E POLIMORFISMO)
# ==========================================
class Imovel:
    def __init__(self, valor_base):
        self.valor_base = valor_base

    def calcular_aluguel_mensal(self):
        return self.valor_base


class Apartamento(Imovel):
    def __init__(self, dois_quartos=False, garagem=False, tem_criancas=True):
        super().__init__(valor_base=700.00)
        self.dois_quartos = dois_quartos
        self.garagem = garagem
        self.tem_criancas = tem_criancas

    def calcular_aluguel_mensal(self):
        valor = self.valor_base
        if self.dois_quartos:
            valor += 200.00
        if self.garagem:
            valor += 300.00
        if not self.tem_criancas:
            valor *= 0.95  # 5% de desconto após adicionais
        return valor


class Casa(Imovel):
    def __init__(self, dois_quartos=False, garagem=False):
        super().__init__(valor_base=900.00)
        self.dois_quartos = dois_quartos
        self.garagem = garagem

    def calcular_aluguel_mensal(self):
        valor = self.valor_base
        if self.dois_quartos:
            valor += 250.00
        if self.garagem:
            valor += 300.00
        return valor


class Estudio(Imovel):
    def __init__(self, pacotes_vagas=0, vagas_extras=0):
        super().__init__(valor_base=1200.00)
        self.pacotes_vagas = pacotes_vagas
        self.vagas_extras = vagas_extras

    def calcular_aluguel_mensal(self):
        valor = self.valor_base
        if self.pacotes_vagas > 0:
            valor += 250.00
            valor += self.vagas_extras * 60.00
        return valor


# ==========================================
# 2. CLASSE DE ORÇAMENTO E EXPORTAÇÃO CSV
# ==========================================
class Orcamento:
    TAXA_CONTRATUAL = 2000.00

    def __init__(self, imovel, parcelas_taxa):
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_parcela_taxa(self):
        return self.TAXA_CONTRATUAL / self.parcelas_taxa

    def exibir_resumo(self):
        aluguel = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_parcela_taxa()

        print("\n" + "=" * 48)
        print("RESUMO DO ORÇAMENTO - R.M IMÓVEIS")
        print("=" * 48)
        print(f"Categoria do Imóvel: {self.imovel.__class__.__name__}")
        print(f"Aluguel Mensal Final: R$ {aluguel:.2f}")
        print("-" * 48)
        print(f"Taxa Contratual Total: R$ {self.TAXA_CONTRATUAL:.2f}")
        print(f"Parcelamento da Taxa: {self.parcelas_taxa}x de R$ {valor_parcela_taxa:.2f}")
        print(f"Total Mensal (Meses 1 a {self.parcelas_taxa}): R$ {aluguel + valor_parcela_taxa:.2f}")
        if self.parcelas_taxa < 12:
            print(f"Total Mensal (Mês {self.parcelas_taxa + 1} ao 12): R$ {aluguel:.2f}")
        print("=" * 48)

    def gerar_csv_projecao(self, nome_arquivo="projecao_12_meses.csv"):
        aluguel = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_parcela_taxa()

        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel Mensal (R$)", "Parcela Taxa Contratual (R$)", "Total Previsto (R$)"])

            for mes in range(1, 13):
                taxa_mes = valor_parcela_taxa if mes <= self.parcelas_taxa else 0.00
                total_mes = aluguel + taxa_mes
                escritor.writerow([
                    f"Mês {mes}",
                    f"{aluguel:.2f}",
                    f"{taxa_mes:.2f}",
                    f"{total_mes:.2f}"
                ])
        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")


# ==========================================
# 3. FUNÇÕES DE VALIDAÇÃO E EXECUÇÃO PRINCIPAL
# ==========================================
def ler_opcao_sn(mensagem):
    while True:
        resp = input(mensagem).strip().upper()
        if resp in ("S", "N"):
            return resp == "S"
        print("Entrada inválida! Digite apenas S ou N.")


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Por favor, digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def main():
    print("=== RENTSMART - SISTEMA DE ORÇAMENTO R.M IMÓVEIS ===")
    print("1 - Apartamento (Base: R$ 700,00)")
    print("2 - Casa (Base: R$ 900,00)")
    print("3 - Estúdio (Base: R$ 1.200,00)")

    tipo = ler_inteiro("Escolha o tipo de imóvel (1 a 3): ", 1, 3)

    if tipo == 1:
        dois_quartos = ler_opcao_sn("Deseja 2 quartos (+R$ 200,00)? [S/N]: ")
        garagem = ler_opcao_sn("Deseja vaga de garagem (+R$ 300,00)? [S/N]: ")
        tem_criancas = ler_opcao_sn("Possui crianças morando no imóvel? [S/N]: ")
        imovel = Apartamento(dois_quartos, garagem, tem_criancas)

    elif tipo == 2:
        dois_quartos = ler_opcao_sn("Deseja 2 quartos (+R$ 250,00)? [S/N]: ")
        garagem = ler_opcao_sn("Deseja vaga de garagem (+R$ 300,00)? [S/N]: ")
        imovel = Casa(dois_quartos, garagem)

    else:
        quer_vagas = ler_opcao_sn("Deseja pacote de 2 vagas (+R$ 250,00)? [S/N]: ")
        pacotes = 1 if quer_vagas else 0
        extras = ler_inteiro("Quantas vagas extras (+R$ 60,00 cada)? [0 a 10]: ", 0, 10) if quer_vagas else 0
        imovel = Estudio(pacotes, extras)

    parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ", 1, 5)

    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()
    orcamento.gerar_csv_projecao()


if __name__ == "__main__":
    main()

