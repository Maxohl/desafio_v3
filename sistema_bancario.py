import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

#Classes 
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero_da_conta = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_da_conta(self):
        return self._numero_da_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n=== Saldo Insuficiente. ===")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n=== Valor inválido. ===")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n=== Valor inválido. ===")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"Limite para saques: R$ {self._limite:.2f}")
            print("\n=== Limite do valor execido. ===")

        elif excedeu_saques:
            print("\n=== Número máximo de saques excedido. ===")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero_da_conta}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

#Menus
def menu_inicial():
    menu = """\n
    ================ Bem Vindo ================
    [1] Entrar
    [2] Novo Usuário
    [3] Nova Conta Corrente
    [4] Sair
    ===========================================
    
    => """
    return input(textwrap.dedent(menu))


def menu_principal():
    menu = """\n
    ================== Menu ==================
    [1] Saldo
    [2] Saque
    [3] Depósito
    [4] Extrato
    [5] Sair
    ==========================================
    
    => """
    return input(textwrap.dedent(menu))

#Funções

def fazer_login(cpf, nome, clientes):
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return False
    elif cliente.nome == nome:
        return True
    
    else:
        print("Usuário ou CPF inválidos.")
        return False
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n=== Cliente não possui conta corrente. ===")
        return

    return cliente.contas[0]

def depositar(usuario_cpf, clientes):
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    cliente = filtrar_cliente(usuario_cpf, clientes)
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(usuario_cpf,  clientes):
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)

    cliente = filtrar_cliente(usuario_cpf, clientes)
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_saldo(usuario_cpf, clientes):
    cliente = filtrar_cliente(usuario_cpf, clientes)
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ SALDO ================")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("\n=======================================")


def exibir_extrato(usuario_cpf, clientes):
    cliente = filtrar_cliente(usuario_cpf, clientes)
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================== EXTRATO ==================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f} \t{transacao["data"]}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=============================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    nome = input("Informe o nome completo: ")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente and cliente.cpf == cpf:
        print("\n=== Já existe cliente com esse CPF. ===")
        return
    
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n=== Cliente não encontrado. ===")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

#Montando o programa.
def main():
    clientes = []
    contas = []
    usuario_nome = None
    usuario_cpf = None

    while True:
        #mostra o menu inicial onde cadastros e login são feitos
        opcao = menu_inicial()

        if opcao == "1": #Entra no menu principal, onde operações bancarias são realizadas

            #Salva o usuario e o cpf em variaveis para usuario não ter que ficar entrando com cpf toda vez que quizer fazer uma operação.
            usuario_cpf = input("Informe o CPF: ")
            usuario_nome = input("Informe o nome: ")
            
            # Autentifica o usuario aqui, verifica se o nome e cpf existem na lista de contas.
            login = fazer_login(usuario_cpf, usuario_nome, clientes)
            if login: 
                print("\n=== Bem-vindo,", usuario_nome, "! ===")
                while True:
                    opcao = menu_principal()
                    if opcao == "1":                                #Mostrar Saldo
                        exibir_saldo(usuario_cpf, clientes)
                        input("\nPressione enter para continuar.")
                    elif opcao == "2":                              #Saque
                        sacar(usuario_cpf, clientes)
                        input("\nPressione enter para continuar.")
                    elif opcao == "3":                              #Depósito
                        depositar(usuario_cpf, clientes)
                        input("\nPressione enter para continuar.")
                    elif opcao == "4":                              #Extrato
                        exibir_extrato(usuario_cpf, clientes)
                        input("\nPressione enter para continuar.")
                    elif opcao == "5":                              #Sair e voltar ao menu Inicial
                        break
                    else:
                        print("\n=== Operação inválida, por favor selecione novamente a operação desejada. ===")
                        input("\nPressione enter para continuar.")
        elif opcao == "2":          #Novo Usuário
            criar_cliente(clientes)
        elif opcao == "3":          #Nova Conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "4":          #Sair e fechar o programa
            break
        else:
            print("\n=== Operação inválida, por favor selecione novamente a operação desejada. ===")
            input("\nPressione enter para continuar.")
            

main()
