# Continuidade do desenvolvimento

Última revisão: 22 de julho de 2026 (UTC).

## Ponto de retomada

- Branch: `agent/melhora-validacoes-identidade-planos`.
- Base da branch: `a4c61e0` (`Merge pull request #3 from fernandossantor/agent/planos-cross-media-v2`).
- Última entrega funcional antes deste registro: `3e2c732` (`Melhora validações e identidade do PlanOS`).
- A branch deve ser retomada a partir do PR associado; `origin/main` continua como base da entrega.
- O aplicativo publicado usa o nome **PlanOS** e o subtítulo **Plataforma Inteligente de Planejamento Híbrido de Mídia**.
- A última rodada adicionou a marca gráfica do PlanOS à página inicial e à barra lateral, além de tornar explícitos todos os impedimentos que desabilitam a geração de um plano.
- As migrações remotas do Supabase estavam sincronizadas até `20260722110000`.

## Estado verificado

- Supabase: projeto `SDM` (`moqyzfdgiajglhuqiymw`) vinculado e `ACTIVE_HEALTHY`.
- CLI Supabase: instalada localmente pelo `package-lock.json`; em uma reconstrução do Codespace, `npm ci` é executado automaticamente.
- Credencial do Git: leitura de `origin` confirmada em 22/07/2026.
- GitHub CLI (`gh`): autenticado como `fernandossantor`; operações Git e da API estavam disponíveis nesta revisão.
- Configuração local: `.env` presente e ignorado pelo Git. Segredos não são copiados para arquivos versionados.
- Produção: os segredos permanecem no mecanismo seguro do Streamlit Cloud/Supabase.

## Validação da última entrega

- `git diff --check` aprovado.
- Compilação dos três módulos Python alterados aprovada.
- 55 testes automatizados aprovados; 3 testes de integração opcionais ignorados nessa execução.
- Health check autenticado aprovado para as 10 tabelas verificadas.
- O teste autenticado `python -m scripts.regression_test` permanece com uma falha na asserção `Forecast consistente`: o plano possui inventários e verba, mas a quantidade de previsões diverge da quantidade de itens. A falha está fora dos arquivos de UI alterados nesta entrega e deve ser investigada na próxima rodada.

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

Investigar a divergência do teste de regressão em `Forecast consistente` e, depois, retomar a partir das próximas observações de uso do PlanOS. O histórico funcional e arquitetural permanece nos commits anteriores e nos demais documentos desta pasta; não é necessário reconstruir as decisões já aplicadas.

## Evolução cross-media em andamento

Em 22 de julho de 2026 foi implementada a base da versão 2.0: identificadores
legíveis e versionados, duplicação das entidades, contexto ativo, indicadores
reais na página inicial, medições com fonte e metodologia, planejamento
configurável por inventário, alcance incremental, saturação, custos e retorno,
cronograma visual e comparação ponderada de estratégias. A migração remota
`20260722110000` foi aplicada. O modelo está documentado em
`docs/MODELO_PLANEJAMENTO_CROSS_MEDIA.md`.
