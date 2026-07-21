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

## Navegação

A interface é organizada em três grupos:

- **Workflow oficial:** Briefing, Planejamento, Diagnóstico, Forecast, Painel
  Executivo e Relatórios.
- **Análises avançadas:** Comparador, Cenários, Otimizador e Insights.
- **Base de conhecimento:** Catálogos, Papéis de mídia, Inventários, Públicos,
  Universos e Segmentos.

`app.py` é a fonte de verdade da navegação. Arquivos em `pages/` não devem ser
tratados automaticamente como etapas do workflow.

## Motores ativos

- `AllocationEngine`
- `BudgetOptimizer`
- `ClassificacaoPapeisEngine`
- `ForecastEngine`
- `InsightsEngine`
- `InventoryEngine`
- `RecommendationEngine`
- `ScenarioEngine`
- `ScoreEngine`

Não são permitidos motores que acessem o banco diretamente. Toda consulta ou
persistência passa por `infrastructure/repositories/` e é orquestrada por um
Application Service.

---

## Regras

- Services não conhecem SQL.
- Repositories não conhecem regras de negócio.
- Components apenas renderizam.
- Pages apenas orquestram componentes.
- Pages não importam `engine` ou `infrastructure` diretamente.
- Modelos de negócio pertencem a `domain/models/`.
