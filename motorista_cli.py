from motorista_dao import MotoristaDAO
from models import Motorista, Corrida, Passageiro

class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            print("\n--- CLI de Gerenciamento de Motorista ---")
            print("Comandos disponíveis:", ", ".join(self.commands.keys()), ", help, quit")
            command = input("Digite o comando: ").strip().lower()

            if command == "quit":
                print("Saindo da CLI do Motorista... Até breve XD")
                break
            elif command == "help":
                self._display_help()
            elif command in self.commands:
                self.commands[command]()
            else:
                print(f"Comando inválido '{command}'. Digite 'help' para opções.")

    def _display_help(self):
        print("\n--- Ajuda ---")
        print("create : Adicionar um novo Motorista com suas Corridas.")
        print("read   : Encontrar e exibir um Motorista pelo seu ID.")
        print("readall: Exibir todos os Motoristas.")
        print("update : Atualizar os detalhes de um Motorista existente (substitui todos os dados).")
        print("delete : Remover um Motorista pelo seu ID.")
        print("help   : Mostrar esta mensagem de ajuda.")
        print("quit   : Sair da aplicação.")
        print("------------")


class MotoristaCLI(SimpleCLI):
    def __init__(self, motorista_dao: MotoristaDAO):
        super().__init__()
        self.motorista_dao = motorista_dao
        self.add_command("create", self._criar_motorista_cli)
        self.add_command("read", self._ler_motorista_cli)
        self.add_command("readall", self._buscar_todos_os_fluxo_motoristas)
        self.add_command("update", self._atualizar_motorista_cli)
        self.add_command("delete", self._apagar_motorista_cli)


    def _prompt_de_passageiro(self):
        print("-- Insira os Detalhes do Passageiro --")
        while True:
            nome = input("   Nome do Passageiro: ").strip()
            if nome: break
            print("   O nome do Passageiro não pode estar vazio.")
        while True:
            documento = input("   Documento do Passageiro: ").strip()
            if documento: break
            print("   O documento do Passageiro não pode estar vazio.")
        return Passageiro(nome=nome, documento=documento)

    def _prompt_de_corrida(self):
        # Tive que colocar alguns ValueError pra poder validar entrada de dados
        print("\n-- Insira os Detalhes da Corrida --")
        while True:
            try:
                nota = int(input("   Nota da Corrida (ex., 1-5): "))
                if 1 <= nota <= 5: 
                    break
                else: print("   A nota deve estar entre 1 e 5.")
            except ValueError:
                print("   Entrada inválida. Por favor, insira um número inteiro para a nota.")
        while True:
            try:
                distancia = float(input("   Distância da Corrida (km): "))
                if distancia >= 0: break
                else: print("   A distância não pode ser negativa.")
            except ValueError:
                print("   Entrada inválida. Por favor, insira um número para a distância.")
        while True:
            try:
                valor = float(input("   Valor da Corrida (R$): "))
                if valor >= 0: break
                else: print("   O valor não pode ser negativo.")
            except ValueError:
                print("   Entrada inválida. Por favor, insira um número para o valor.")

        passageiro = self._prompt_de_passageiro() 
        return Corrida(nota=nota, distancia=distancia, valor=valor, passageiro=passageiro)

    def _buscar_dados_do_motorista(self, existing_motorista: Motorista = None):
        print("\n--- Insira os Detalhes do Motorista ---")
        default_name = existing_motorista.nome if existing_motorista else ""
        while True:
            nome = input(f"Nome do Motorista [{default_name}]: ").strip() or default_name
            if nome: break
            print("O nome do Motorista não pode estar vazio.")

        corridas = []
        if existing_motorista:
            print(f"Número atual de corridas: {len(existing_motorista.corridas)}")
            replace_corridas = input("Substituir corridas existentes? (sim/não) [não]: ").lower().strip() == 'sim'
            if not replace_corridas:
                corridas = existing_motorista.corridas 
            else:
                print("Coletando novas corridas...")
        else:
            replace_corridas = True 

        if replace_corridas:
            while True:
                add_more = input("Adicionar uma Corrida? (sim/não) [sim]: ").lower().strip()
                if add_more == 'não':
                    break
                corrida = self._prompt_de_corrida()
                corridas.append(corrida)
                print("Corrida adicionada.")
                
                if add_more not in ('', 'sim'):
                    break
        
        if corridas:
             nota = sum(c.nota for c in corridas) / len(corridas)
        else:
             nota = 0.0 
        print(f"Nota média calculada: {nota:.2f}")
        motorista_obj = Motorista(
            nome=nome,
            corridas=corridas,
            nota=nota,
            _id=existing_motorista._id if existing_motorista else None
        )
        return motorista_obj

    def _criar_motorista_cli(self):
        print("\n======= Criar Novo Motorista =======")
        motorista_obj = self._buscar_dados_do_motorista() 
        if motorista_obj:
             self.motorista_dao.criar_motorista(motorista_obj)

    def _ler_motorista_cli(self):
        print("\n======= Ler Motorista por ID =======")
        motorista_id = input("Digite o ID do Motorista para ler: ").strip()
        if not motorista_id:
             print("O ID não pode estar vazio.")
             return
        motorista = self.motorista_dao.ler_motorista_por_id(motorista_id)
        if motorista:
            print("\n--- Detalhes do Motorista ---")
            print(f"ID        : {motorista._id}")
            print(f"Nome      : {motorista.nome}")
            print(f"Nota Média: {motorista.nota:.2f}")
            print("--- Corridas ---")
            if motorista.corridas:
                for i, corrida in enumerate(motorista.corridas, 1):
                    print(f"  Corrida {i}:")
                    print(f"    Nota      : {corrida.nota}")
                    print(f"    Distância : {corrida.distancia} km")
                    print(f"    Valor     : R$ {corrida.valor:.2f}")
                    print(f"    Passageiro:")
                    print(f"      Nome    : {corrida.passageiro.nome}")
                    print(f"      Documento: {corrida.passageiro.documento}")
            else:
                print("  Nenhuma corrida registrada.")
            print("-----------------------")
        
    def _buscar_todos_os_fluxo_motoristas(self):
         print("\n======= Ler Todos os Motoristas =======")
         motoristas = self.motorista_dao.buscar_todos_os_motoristas()
         print(motoristas)
         if motoristas:
             print(f"\n--- Listando {len(motoristas)} Motoristas ---")
             for m in motoristas:
                 print(f"ID: {m._id}, Nome: {m.nome}, Nota Média: {m.nota:.2f}, Corridas: {len(m.corridas)}")
             print("----------------------------")
         else:
             print("Nenhum motorista encontrado no banco de dados.")

    def _atualizar_motorista_cli(self):
        print("\n======= Atualizar Motorista =======")
        motorista_id = input("Digite o ID do Motorista para atualizar: ").strip()
        if not motorista_id:
             print("O ID não pode estar vazio.")
             return
        existing_motorista = self.motorista_dao.ler_motorista_por_id(motorista_id)
        if not existing_motorista:
             return
        print(f"Atualizando Motorista: {existing_motorista.nome} (ID: {motorista_id})")
        updated_motorista_obj = self._buscar_dados_do_motorista(existing_motorista)
        if updated_motorista_obj:
             self.motorista_dao.atualizar_motorista(motorista_id, updated_motorista_obj)

    def _apagar_motorista_cli(self):
        print("\n======= Excluir Motorista =======")
        motorista_id = input("Digite o ID do Motorista para excluir: ").strip()
        if not motorista_id:
             print("O ID não pode estar vazio.")
             return
        motorista = self.motorista_dao.ler_motorista_por_id(motorista_id) 
        if motorista:
            confirm = input(f"Tem certeza que deseja excluir {motorista.nome} (ID: {motorista_id})? (sim/não): ").lower()
            if confirm == 'sim':
                self.motorista_dao.apagar_motorista(motorista_id)
            else:
                print("Exclusão cancelada.")