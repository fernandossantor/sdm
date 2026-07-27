# Revisão de referências — Fase 7

Revisão inicial: 27 de julho de 2026 (UTC).

## Fontes

- [Guia de segurança da informação para agentes de pequeno porte —
  ANPD](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte)
- [Comunicação de incidente de segurança —
  ANPD](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis)
- [OWASP Application Security Verification Standard
  5.0](https://owasp.org/www-project-application-security-verification-standard/)
- decisões, auditorias e ensaios locais registrados em
  `DECISOES_METODOLOGICAS_ENGINES.md`, `AUDITORIA_MULTIUSUARIO_FASE_4.md`,
  `REVISAO_REFERENCIAS_FASE_5.md`, `REVISAO_REFERENCIAS_FASE_6.md` e
  `BACKUP_RESTAURACAO.md`.

## Consequências para homologação

- produção deve falhar fechada quando autenticação ou segredos obrigatórios
  estiverem ausentes;
- chave pública e chave administrativa devem ser distintas;
- autenticação, autorização e auditoria são controles complementares;
- acesso comum deve usar JWT e RLS; `service_role` fica restrita ao backend;
- participantes, finalidade, categorias de dados, retenção e canal de suporte
  devem ser documentados;
- incidentes precisam de registro, avaliação e resposta operacional;
- backup só é aceito depois de restauração e conferência;
- piloto depende de CI, regressão, isolamento multiusuário e gates manuais
  aprovados.

## Estado inicial

| Controle | Estado | Ação |
|---|---|---|
| CI | corrigido e aprovado | manter obrigatório |
| Navegação Fase 6 | corrigida | incluir na homologação |
| Autenticação/RLS | implementada, desligada por padrão | ativar somente no piloto |
| Configuração de produção | fail-closed implementado | validar segredos |
| Segredo administrativo | rotação necessária | bloquear piloto |
| Backup/restauração | ensaios completos anteriores | executar ensaio pré-piloto |
| Observabilidade | auditoria administrativa parcial | criar runbook e sinais |
| Usuários-piloto | não formalizados | definir participantes e aceite |
