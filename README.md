# Desafio Técnico - Estagiário Python/Django 2026.1

Sistema de gerenciamento escolar desenvolvido como parte do processo seletivo. A aplicação permite o gerenciamento de alunos, cursos e matrículas, além de fornecer relatórios financeiros e acadêmicos através de um Dashboard e API Rest.

## 🚀 Tecnologias

* **Linguagem:** Python 3
* **Framework Web:** Django & Django Rest Framework (DRF)
* **Banco de Dados:** PostgreSQL
* **Infraestrutura:** Docker & Docker Compose
* **Frontend:** Templates Django + Bootstrap 5

## 📂 Arquivos Obrigatórios

Conforme solicitado, a raiz do projeto contém:
* `Dockerfile`: Configuração da imagem da aplicação.
* `docker-compose.yml`: Orquestração dos serviços (Web + DB).
* `meu_database.sql`: Dump/Modelagem do banco de dados.
* `README.md`: Este arquivo de documentação.

## 🐳 Como Rodar

A aplicação está totalmente containerizada. O `docker-compose` gerencia a instalação de dependências, migrações do banco e execução do servidor.

### Passo a Passo

1.  Clone o repositório.
2.  Na raiz do projeto, execute o comando:

```bash
docker-compose up --build