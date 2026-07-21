# SDM — Sistema de Diagnóstico de Mídia

## Sobre

O SDM é um Sistema Especialista destinado ao planejamento estratégico e tático de mídia.

Seu objetivo é apoiar profissionais de mídia na transformação de uma campanha em um plano de mídia consistente, utilizando uma base de conhecimento estruturada e motores de decisão especializados.

O SDM não substitui o planejador.

Ele amplia sua capacidade analítica, oferecendo recomendações, simulações, projeções e diagnósticos fundamentados em regras explícitas.

---

## Principais funcionalidades

- Gestão de Campanhas
- Planejamento Estratégico
- Diagnóstico
- Forecast
- Simulações
- Otimizador
- Painel Executivo
- Relatórios

---

## Arquitetura

O SDM utiliza arquitetura em camadas.

```
Interface
    ↓
Application
    ↓
Domain
    ↓
Engines
    ↓
Repositories
    ↓
Supabase
```

---

## Tecnologias

- Python
- Streamlit
- Supabase
- PostgreSQL

---

## Estrutura

```
application/
components/
domain/
engine/
infrastructure/
pages/
docs/
```

---

## Status

Versão atual:

SDM 1.0 RC — homologação

Validado atualmente:

- fluxo completo offline de Briefing até exportação Excel/CSV;
- renderização de todas as páginas registradas;
- integração de leitura com o Supabase;
- RLS com acesso público bloqueado e `service_role` funcional;
- testes automatizados e CI sem dependência de segredos.

Fora do escopo do 1.0: histórico persistente, usuários, PDF e PowerPoint.
