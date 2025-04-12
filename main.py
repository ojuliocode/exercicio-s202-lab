
import sys
from database import Database
from motorista_dao import MotoristaDAO
from motorista_cli import MotoristaCLI

from models import Passageiro, Corrida, Motorista

def main():
    db_instance = Database(database_name="laboratorio_avaliativo_03", collection_name="Motoristas")
    motorista_dao = MotoristaDAO(database=db_instance)
    cli = MotoristaCLI(motorista_dao=motorista_dao)
    cli.run()
    
if __name__ == "__main__":
    main()