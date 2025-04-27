# Golden Raspberry Awards

## Descrição
API RESTful que lê um dataset CSV de filmes de indicados e vencedores da Golden Raspberry Awards. O dataset esperado tem as colunas ["year", "title", "studios", "producers", "winner"] nessa sequência.

## Setup da API
Para rodar a API localmente é preciso primeiro instalar os pacotes,
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

e configurar as variáveis de ambiente no arquivo index.py.
```python
environ["DATABASE_URL"] = "sqlite:///:memory:"  # URL de conexão com o banco de dados
environ["INITIAL_DATASET_PATH"] = "Movielist.csv" # Path do dataset, dê preferência por utilizar o path absoluto
environ["CSV_DELIMITER"] = ";" # Delimitador do dataset csv
```

## Rode localmente
Para rodar o servidor utilize o comando
```shell
$ python3 index.py
```

## Testes
Para rodar os testes utilize o comando
```shell
$ pytest
```

## Endpoints
Para testar os endpoints da API basta fazer uma requisição HTTP para a URL
```http
GET http://127.0.0.1:5000/awards/longest-fastest-consecutive-awards
```
ou utilizar a interface do Swagger http://127.0.0.1:5000/
