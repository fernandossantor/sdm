# Incremento — Briefing estruturado e versionado

Data: 1º de agosto de 2026 (UTC).

## Entregue

- conteúdo metodológico independente do contexto administrativo da Campanha;
- estados canônicos do Briefing;
- edição de rascunho com motivo, autoria, instante e valores auditáveis;
- criação de nova versão sem sobrescrever a anterior;
- histórico de versões e ações visíveis de Editar e Criar nova versão;
- persistência por RPCs transacionais, RLS e rollback;
- interface progressiva para situação, objetivos, território, públicos,
  jornada, período, verba, restrições e pretensões.

Não foram introduzidos objetivo de mídia, KPI, alcance, frequência, flight,
arquitetura ou cálculos no Briefing.

## Verificações

- suíte completa: 207 testes aprovados e 3 integrações opcionais ignoradas;
- `git diff --check`: aprovado;
- migração `20260801210000`: aplicada e sincronizada no Supabase;
- gate de migrações conectado: aprovado;
- demais gates conectados: inconclusivos por resets HTTP/2 do endpoint REST,
  após confirmação das chaves novas vigentes.

## Próxima homologação

Validar na aplicação hospedada, com usuário autenticado:

1. edição do Briefing v1 em rascunho;
2. motivo e autoria registrados;
3. criação do Briefing v2;
4. v1 preservado como Substituído;
5. histórico visível e conteúdo herdado da Campanha não editável.

## Itens preservados fora do incremento

- `docs/PLANO_EVOLUCAO_INTEGRADO.md`;
- `docs/materials/`;
- alterações locais do usuário em `assets/`.
