# Documentação Técnica da API - Projeto Cloud

## Visão Geral

Este projeto é uma API RESTful desenvolvida com **FastAPI**, estruturada para realizar:

- Registro e autenticação de usuários com proteção por **JWT**;
- Consulta a dados externos atualizados via **web scraping** (ex: índice Bovespa);
- Armazenamento seguro dos dados e usuários com **PostgreSQL**;
- Implantação via **Docker Compose** e **AWS Lightsail**.

---

## Estrutura dos Arquivos

- `main.py`: ponto de entrada da aplicação.
- `app.py`: definição da API, endpoints e rotas.
- `models.py`: modelos de dados SQLAlchemy.
- `schemas.py`: validação de entrada/saída via Pydantic.
- `auth.py`: lógicas de autenticação, hash e geração/validação de token JWT.
- `database.py`: configuração da conexão com PostgreSQL via variáveis de ambiente.
- `scrapping.py`: script de coleta e inserção de dados do índice Bovespa.
- `.env`: (não incluso no repo) armazena as variáveis sensíveis (como senha e host do banco).

---

## Funcionamento da API

### Endpoints Disponíveis

#### 1. `POST /registrar`

Cria um novo usuário, desde que o email ainda não esteja cadastrado. A senha é armazenada como **hash** com bcrypt, e um **JWT** é gerado no retorno.

**Request**:

```json
{
  "nome": "João",
  "email": "joao@insper.edu.br",
  "senha": "senhaSegura123"
}
