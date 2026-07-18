# SDM — Sistema de Diagnóstico de Mídia

> Sistema especialista para apoio ao planejamento estratégico e tático de mídia.

O SDM é uma plataforma de apoio à decisão que transforma informações de uma campanha em recomendações estruturadas para planejamento de mídia, utilizando uma Base de Conhecimento, motores especializados e modelos de diagnóstico.

---

# Objetivo

Apoiar profissionais de mídia durante todas as etapas do planejamento:

- Campanha
- Planejamento
- Diagnóstico
- Plano de Mídia
- Forecast
- Painel Executivo
- Relatórios

O SDM não substitui o planejador.

Ele amplia sua capacidade analítica por meio de conhecimento estruturado, algoritmos transparentes e recomendações explicáveis.

---

# Arquitetura

```
Interface (Streamlit)
        ↓
Components
        ↓
Application Services
        ↓
Domain
        ↓
Decision Engines
        ↓
Repositories
        ↓
Supabase / PostgreSQL
```

---

# Tecnologias

- Python 3
- Streamlit
- Supabase
- PostgreSQL

---

# Estrutura do Projeto

```
application/
components/
data/
database/
docs/
domain/
engine/
infrastructure/
pages/
repositories/
scripts/
```

---

# Documentação

A documentação completa encontra-se em:

```
docs/
```

Principais documentos:

- ARCHITECTURE.md
- DOMAIN.md
- DATABASE.md
- WORKFLOW.md
- PRODUCT.md
- METHODOLOGY.md
- KNOWLEDGE_MODEL.md
- UI_LANGUAGE.md
- DECISIONS.md
- ROADMAP.md

---

# Estado do Projeto

Versão atual:

**v0.4**

Marco alcançado:

- Arquitetura consolidada
- Modelo de domínio definido
- Workflow implementado
- Documentação arquitetural concluída
- Home modularizada

---

# Próximas etapas

- UX da Base de Conhecimento
- Planejamento Assistido
- Forecast
- Painel Executivo
- Inteligência Artificial

---

# Licença

Em definição.