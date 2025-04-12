from typing import List

class Passageiro:
    def __init__(self, nome: str, documento: str):
        self.nome = nome
        self.documento = documento

    def converter_para_dicionario(self):
        return self.__dict__
    
    # Metodo pra transformar isso em metodo da classe (que nem os metodos estaticos do java)
    @classmethod
    def buscar_do_dicionario(cls, data: dict):
        return cls(nome=data.get('nome'), documento=data.get('documento'))


class Corrida:
    def __init__(self, nota: int, distancia: float, valor: float, passageiro: Passageiro):
        self.nota = nota
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro 

    def converter_para_dicionario(self):
        return {
            "nota": self.nota,
            "distancia": self.distancia,
            "valor": self.valor,
            "passageiro": self.passageiro.converter_para_dicionario() 
        }

    @classmethod
    def buscar_do_dicionario(cls, data: dict):
        passageiro_data = data.get('passageiro', {})
        passageiro = Passageiro.buscar_do_dicionario(passageiro_data)
        return cls(
            nota=data.get('nota'),
            distancia=data.get('distancia'),
            valor=data.get('valor'),
            passageiro=passageiro
        )

class Motorista:
    def __init__(self, nome: str, corridas: List[Corrida], nota: float, _id=None): 
        self.nome = nome
        self.corridas = corridas 
        self.nota = nota 
        self._id = _id 

    # Da mesma forma, esse aqui eh pra poder mandar pra formato de dicionario
    def converter_para_dicionario(self):
        return {
            "nome": self.nome,
            "nota": self.nota,
            "corridas": [c.converter_para_dicionario() for c in self.corridas] 
        }

    # Esse aqui eh so um metodo auxiliar pra poder traduzar a partir de um dicionario
    @classmethod
    def buscar_do_dicionario(cls, data: dict):
        corridas_data = data.get('corridas', [])
        corridas = [Corrida.buscar_do_dicionario(c_data) for c_data in corridas_data]
        return cls(
            nome=data.get('nome'),
            nota=data.get('nota'),
            corridas=corridas,
            _id=data.get('_id') 
        )