# Guia de Desenvolvimento

## Organização

Pages

↓

Components

↓

Services

↓

Engines

↓

Repositories

↓

Database

---

## Convenções

- Componentes reutilizáveis.
- Services sem SQL.
- Repositories sem regras de negócio.
- Pages apenas orquestram.
- Engines independentes da interface.

---

## Estilo

- Funções pequenas.
- Métodos com responsabilidade única.
- Separação entre domínio e apresentação.

---

## Testes

Execute a suíte offline com:

```bash
python -m unittest discover -s tests -v
```

Antes de enviar mudanças, valide também o piso de cobertura usado pelo CI:

```bash
pytest -q --cov=domain --cov=engine --cov=application.services \
  --cov-report=term --cov-fail-under=70 tests
```

O teste de conexão com o Supabase é opcional e exige configuração explícita:

```bash
SDM_RUN_INTEGRATION=1 python -m unittest tests.test_connection -v
```

---

## Objetivo

Todo novo código deve preservar a arquitetura do SDM.
