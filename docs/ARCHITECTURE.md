# Arquitetura

## Camadas

Interface

↓

Application Services

↓

Domain

↓

Decision Engines

↓

Repositories

↓

Database

---

## Responsabilidades

### Interface

Renderização.

Nunca implementa regra de negócio.

---

### Application

Orquestra casos de uso.

---

### Domain

Representa entidades do negócio.

---

### Engines

Implementam inteligência.

---

### Repositories

Persistência.

---

### Database

Supabase/PostgreSQL.

---

## Organização

```
components/
pages/
application/
domain/
engine/
infrastructure/
```

---

## Regras

- Services não conhecem SQL.
- Repositories não conhecem regras de negócio.
- Components apenas renderizam.
- Pages apenas orquestram componentes.