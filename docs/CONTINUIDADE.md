# Continuidade do desenvolvimento

Última revisão: 27 de julho de 2026 (UTC).

## Ponto de retomada

- Branch: `agent/corrige-restricoes-e-moeda`.
- Fases 4, 5 e 6 concluídas; Fase 7 em homologação controlada.
- Último checkpoint funcional: `9dfc8d2`
  (`Prepara migracao para chaves Supabase atuais`).
- A branch de continuidade permanece disponível para retomada no Codespace.
- O aplicativo publicado usa o nome **MediAd Planner** e o subtítulo **Plataforma Inteligente de Planejamento Híbrido de Mídia**.
- A última rodada restaurou o logo na barra lateral, preservou o logo reduzido
  na página Início, manteve favicon e título completo no navegador, introduziu
  entradas monetárias em pt-BR e unificou pisos, tetos e quantidade automática
  entre a interface e o motor do Plano de Mídia.
- As migrações remotas do Supabase estão sincronizadas até `20260727080000`.

## Estado verificado

- Supabase: projeto `SDM` (`moqyzfdgiajglhuqiymw`) vinculado e `ACTIVE_HEALTHY`.
- CLI Supabase: instalada localmente pelo `package-lock.json`; em uma reconstrução do Codespace, `npm ci` é executado automaticamente.
- Credencial do Git: leitura de `origin` confirmada em 22/07/2026.
- GitHub CLI (`gh`): autenticado como `fernandossantor`; operações Git e da API estavam disponíveis nesta revisão.
- GitHub Actions: checks de push e PR aprovados nos checkpoints recentes.
- Configuração local: `.env` presente e ignorado pelo Git. Segredos não são copiados para arquivos versionados.
- Produção: os segredos permanecem no mecanismo seguro do Streamlit Cloud/Supabase.

## Validação da última entrega

- `git diff --check` aprovado.
- Compilação de todos os módulos Python aprovada.
- 159 testes automatizados aprovados; 3 testes de integração opcionais
  ignorados na suíte offline.
- 3 testes de integração autenticados aprovados.
- Health check autenticado aprovado para 20 tabelas críticas.
- Auditoria confirmou as tabelas críticas bloqueadas ao acesso público.
- Gate unificado de homologação conectado aprovado.
- Regressão funcional autenticada aprovada. A antiga asserção do forecast foi
  alinhada à regra do motor, que projeta apenas inventários com métricas.
- Renderização da página inicial aprovada com duas imagens e sem texto MediAd Planner
  duplicado. Entrada `1.000.000,00` convertida corretamente para cálculo.

## Retomada rápida

O ambiente atual já contém as dependências. Se o Codespace for recriado, as dependências Python e a CLI do Supabase serão restauradas automaticamente pela configuração do contêiner.

Para confirmar o estado sem alterar dados:

```bash
git status -sb
npx --yes supabase@latest projects list
python -m scripts.health_check
```

Antes de uma nova alteração de banco, comparar as migrações locais e remotas. Antes de publicar, executar a suíte proporcional à mudança e revisar `git diff` para impedir a inclusão de credenciais.

## Próximo trabalho

Retomar pela Fase 7 em `docs/PLANO_MESTRE_EVOLUCAO.md`. A migração local,
a homologação conectada e o backup restaurável posterior à troca das chaves
foram concluídos. A próxima ação é:

1. instalar `sb_publishable_...` e `sb_secret_...` no mecanismo seguro da
   hospedagem, sem enviar ou versionar os valores;
2. manter o piloto desativado durante a validação da versão candidata;
3. repetir os gates de saúde, segurança e integração na hospedagem;
4. conferir no painel do Supabase que as chaves legadas deixaram de ser usadas;
5. somente então desativar `anon` e `service_role`.

Não rotacionar a JWT Signing Key e não ativar o piloto antes desses gates.

As decisões obrigatórias para
fórmulas, dados, restrições, forecast, otimização, atribuição e auditoria estão
em `docs/DECISOES_METODOLOGICAS_ENGINES.md`.

O plano mestre também incorpora a evolução multiusuário, os inventários globais
e privados, o compartilhamento, a segurança, o backup e os testes de isolamento.
O histórico funcional e arquitetural permanece nos commits anteriores e nos
demais documentos desta pasta; não é necessário reconstruir decisões já
registradas.

A Fase 6 entregou briefing ampliado, estratégia e racional, mapas e
cronogramas reconciliados, atribuição auditável, qualidade programática e
localização, relatórios completos e comparação histórica de versões.

## Evolução cross-media em andamento

Em 22 de julho de 2026 foi implementada a base da versão 2.0: identificadores
legíveis e versionados, duplicação das entidades, contexto ativo, indicadores
reais na página inicial, medições com fonte e metodologia, planejamento
configurável por inventário, alcance incremental, saturação, custos e retorno,
cronograma visual e comparação ponderada de estratégias. A migração remota
`20260722110000` foi aplicada. O modelo está documentado em
`docs/MODELO_PLANEJAMENTO_CROSS_MEDIA.md`.
