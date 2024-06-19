from pymongo import MongoClient
from faker import Faker
import random

client = MongoClient('mongodb://localhost:27017')
db = client.foodshare #trocar nome pelo db usado

faker = Faker()

# cada função deve ser adaptada para sua coleção
def generate_empresa():
    return {
        'nome': faker.company(),
        'cnpj': faker.bothify(text='##.###.###/####-##'),
        'ramo': faker.job(),
        'certificacao': faker.word()
    }

def generate_pessoa():
    return {
        'nome': faker.name(),
        'cpf': faker.bothify(text='###.###.###-##'),
        'dtNasc': faker.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        'idade': random.randint(18, 80),
        'endereco': {
            'cep': faker.zipcode(),
            'rua': faker.street_name(),
            'bairro': faker.street_name(),
            'cidade': faker.city()
        }
    }

def generate_produto(doador):
    return {
        'idProduto': random.randint(100000, 999999),
        'dataCadastro': faker.date_this_year().isoformat(),
        'produto': faker.word(),
        'codBarra': faker.bothify(text='##########'),
        'dtProducao': faker.date_this_decade().isoformat(),
        'marca': faker.company(),
        'validade': faker.date_between(start_date='today', end_date='+2y').isoformat(),
        'quantidade': random.randint(1, 100),
        'tipo': faker.word(),
        'doador': doador
    }

def generate_relatorio():
    return {
        'relatorio': [
            {
                'idProduto': random.randint(100000, 999999),
                'dataCadastro': faker.date_this_year().isoformat(),
                'doador': {
                    'tipo': 'empresa',
                    'cnpj': faker.bothify(text='##.###.###/####-##')
                },
                'nomeProduto': faker.word(),
                'validade': faker.date_between(start_date='today', end_date='+2y').isoformat(),
                'idLocalDistribuicao': faker.bothify(text='??????????')
            },
            {
                'idProduto': random.randint(100000, 999999),
                'dataCadastro': faker.date_this_year().isoformat(),
                'doador': {
                    'tipo': 'pessoa',
                    'cpf': faker.bothify(text='###.###.###-##')
                },
                'nomeProduto': faker.word(),
                'validade': faker.date_between(start_date='today', end_date='+2y').isoformat(),
                'idLocalDistribuicao': faker.bothify(text='??????????')
            }
        ]
    }

def generate_local_distribuicao():
    return {
        'nomeLocal': faker.company(),
        'produtosRecebidos': [
            {
                'idProduto': random.randint(100000, 999999),
                'doador': {
                    'tipo': 'empresa',
                    'cnpj': faker.bothify(text='##.###.###/####-##')
                },
                'dataEnvio': faker.date_this_year().isoformat()
            },
            {
                'idProduto': random.randint(100000, 999999),
                'doador': {
                    'tipo': 'pessoa',
                    'cpf': faker.bothify(text='###.###.###-##')
                },
                'dataEnvio': faker.date_this_year().isoformat()
            }
        ]
    }

# aqui sera inseridos os dados, mude o range para quantos dados voce quer
def seed_db():
    empresas = [generate_empresa() for _ in range(10000)]
    pessoas = [generate_pessoa() for _ in range(10000)]
    produtos = [generate_produto({'tipo': 'empresa', 'id': faker.bothify(text='##.###.###/####-##')}) for _ in range(10000)]
    relatorios = [generate_relatorio() for _ in range(10000)]
    locais_distribuicao = [generate_local_distribuicao() for _ in range(10000)]

    db.empresas.insert_many(empresas)
    db.pessoas.insert_many(pessoas)
    db.produtos.insert_many(produtos)
    db.relatorios.insert_many(relatorios)
    db.locaisDistribuicao.insert_many(locais_distribuicao)

if __name__ == '__main__':
    seed_db()
    print('Dados inseridos com sucesso')
