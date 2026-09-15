<h1 align="center">API de Clientes e Débitos</h1>

Projeto de estudo desenvolvido com Python para praticar construção de APIs, autenticação com JWT, SQLAlchemy e integração com Model Context Protocol (MCP).

## Sobre o projeto

A aplicação permite que usuários (contadores) façam login e gerenciem seus próprios clientes e débitos.

Cada usuário só pode acessar os clientes que cadastrou, garantindo o isolamento dos dados entre usuários.

Além da API REST, o projeto possui um servidor MCP que permite disponibilizar algumas funcionalidades da aplicação como ferramentas que podem ser utilizadas por uma IA.

## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- MySQL
- JWT
- Passlib / bcrypt
- MCP

## Funcionalidades

### Autenticação

- Cadastro de usuário
- Login com email e senha
- Autenticação utilizando JWT
- Consulta do usuário autenticado
- Senhas armazenadas utilizando hash

### Clientes

- Cadastrar cliente
- Listar clientes
- Consultar cliente
- Atualizar cliente
- Excluir cliente

Cada cliente pertence a um usuário.

### Débitos

- Cadastrar débito para um cliente
- Listar débitos
- Filtrar débitos pagos ou pendentes
- Marcar débito como pago

## MCP

Como parte dos estudos sobre Model Context Protocol, foi criado um servidor MCP integrado à API e ao banco de dados.

O MCP funciona como uma ponte entre uma IA e as funcionalidades da aplicação. As funcionalidades são disponibilizadas como ferramentas (`tools`) que a IA pode chamar de acordo com o que o usuário solicita.

Atualmente, o MCP possui ferramentas para:

- Listar clientes
- Cadastrar clientes
- Consultar débitos de um cliente

O servidor utiliza o mesmo JWT da aplicação para identificar o usuário e garantir que os clientes acessados pertençam a ele.

## Como Rodar
```text

Como rodar
1. Criar o ambiente virtual
python -m venv .venv

2. Ativar o ambiente virtual
.venv\Scripts\activate

3. Instalar as dependências
pip install -r requirements.txt

4. Configurar o .env
Crie um arquivo .env na raiz do projeto:
SECRET_KEY="sua-chave-secreta"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="mysql+asyncmy://usuario:senha@localhost:3306/debits"

5. Iniciar a API
uvicorn main:app --reload

A API estará disponível em:
http://localhost:8000/docs

As tabelas do banco são criadas automaticamente quando a API é iniciada.

6. Iniciar o MCP
Abra outro terminal e execute:
mcp dev mcp_server.py

O comando abrirá o MCP Inspector, onde é possível visualizar e testar as ferramentas disponíveis.
