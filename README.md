# 🧠 FaceQA API

API para validação da qualidade de imagens faciais (Face Quality Assessment) via modelo de machine learning.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Poetry](https://python-poetry.org/)

---

## 🛠 Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/OtavMacedo/FaceQA-backend.git
cd FaceQA-backend
```

2. Instale as dependências:

```bash
poetry install
```

3. Configure variáveis de ambiente (ex: `.env`):

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/faceqa
```

4. Rode a API:

```bash
poetry run uvicorn app.main:app --reload
```

---

## ✅ Endpoints principais

| Método | Rota        | Descrição                              |
|--------|-------------|----------------------------------------|
| POST   | `/faceqa/`  | Valida a qualidade de uma face (base64)|

---

## 📌 TODO
- Melhorar a injeção de dependências (estou instanciando a mesma classe mais de 1 vez)
- Notificação por email ao atingir limite de uso
- Exportação de logs de uso

### Funcionalidades

- [ ] 🔐 Autenticação via JWT
- [ ] 💳 Sistema de créditos por requisição
- [ ] 📈 Dashboard de uso por chave de API
- [ ] 🧪 Testes automatizados (Pytest)
- [ ] 📄 Documentação Swagger personalizada
- [ ] 🐳 Dockerfile + docker-compose
- [ ] 📬
- [ ] 📁

---

## 🤝 Contribuição

Sinta-se à vontade para abrir *issues* ou *pull requests*. Toda ajuda é bem-vinda!

---

## 📄 Licença