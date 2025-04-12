from bson.objectid import ObjectId
from database import Database 
from models import Motorista, Corrida, Passageiro 

class MotoristaDAO:
    def __init__(self, database: Database): 
        self.db = database 
        self.collection = self.db.get_collection() 

    def criar_motorista(self, motorista: Motorista):
        motorista_dict = motorista.converter_para_dicionario()
        res = self.collection.insert_one(motorista_dict)
        print(f"Motorista '{motorista.nome}' criado com id: {res.inserted_id}")
        return str(res.inserted_id)

    def ler_motorista_por_id(self, id: str):
        obj_id = ObjectId(id)
        resposta_dicionario = self.collection.find_one({"_id": obj_id})
        if resposta_dicionario:
            print(f"Motorista encontrado.")
            return Motorista.buscar_do_dicionario(resposta_dicionario)
        else:
            print(f"Motorista com id {id} não encontrado.")
            return None

    def buscar_todos_os_motoristas(self):
        motoristas = []
        for doc in self.collection.find():
            motoristas.append(Motorista.buscar_do_dicionario(doc))
        print(f"Encontrado(s) {len(motoristas)} motorista(s).")
        return motoristas

    # Aki no update eu fiz um esquema de mostrar se os dados atualizados eram os mesmos
    def atualizar_motorista(self, id: str, motorista_update: Motorista):
        obj_id = ObjectId(id)
        update_data_dict = motorista_update.converter_para_dicionario()
        res = self.collection.update_one(
            {"_id": obj_id},
            {"$set": update_data_dict} 
        )

        if res.matched_count == 0:
            print(f"Motorista com id {id} não encontrado para atualização.")
        elif res.modified_count == 0:
             print(f"Motorista {id} encontrado, mas os dados eram os mesmos (nenhuma modificação necessária).")
        else:
             print(f"Motorista {id} atualizado com sucesso.")

        return res.modified_count

    def apagar_motorista(self, id: str):
        obj_id = ObjectId(id)
        res = self.collection.delete_one({"_id": obj_id})
        if res.deleted_count > 0:
            print(f"Motorista {id} excluído com sucesso.")
        else:
             print(f"Motorista com id {id} não encontrado para exclusão.")
        return res.deleted_count