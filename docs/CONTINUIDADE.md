# Continuidade do desenvolvimento

Última revisão: 22 de julho de 2026 (UTC).

## Ponto de retomada

- Branch: `agent/corrige-restricoes-e-moeda`.
- Base da branch: `bb4d6d1` (`Padroniza interface e corrige preços do plano (#5)`).
- Última entrega funcional antes deste registro: `aa4fcda` (`Corrige restrições e moeda no planejamento`).
- Publicação concluída pelo PR `#6`; merge em `origin/main`: `320fa5c`
  (`Corrige restrições e moeda no planejamento (#6)`).
- A branch de continuidade permanece disponível para retomada no Codespace.
- O aplicativo publicado usa o nome **PlanOS** e o subtítulo **Plataforma Inteligente de Planejamento Híbrido de Mídia**.
- A última rodada restaurou o logo na barra lateral, preservou o logo reduzido
  na página Início, manteve favicon e título completo no navegador, introduziu
  entradas monetárias em pt-BR e unificou pisos, tetos e quantidade automática
  entre a interface e o motor do Plano de Mídia.
- As migrações remotas do Supabase estavam sincronizadas até `20260722110000`.

## Estado verificado

- Supabase: projeto `SDM` (`moqyzfdgiajglhuqiymw`) vinculado e `ACTIVE_HEALTHY`.
- CLI Supabase: instalada localmente pelo `package-lock.json`; em uma reconstrução do Codespace, `npm ci` é executado automaticamente.
- Credencial do Git: leitura de `origin` confirmada em 22/07/2026.
- GitHub CLI (`gh`): autenticado como `fernandossantor`; operações Git e da API estavam disponíveis nesta revisão.
- GitHub Actions: CI pós-merge `29955148246` concluído com sucesso.
- Configuração local: `.env` presente e ignorado pelo Git. Segredos não são copiados para arquivos versionados.
- Produção: os segredos permanecem no mecanismo seguro do Streamlit Cloud/Supabase.

## Validação da última entrega

- `git diff --check` aprovado.
- Compilação de todos os módulos Python aprovada.
- 60 testes automatizados aprovados; 3 testes de integração opcionais ignorados nessa execução.
- 3 testes de integração autenticados aprovados.
- Health check autenticado aprovado para as 10 tabelas verificadas.
- Regressão funcional autenticada aprovada. A antiga asserção do forecast foi
  alinhada à regra do motor, que projeta apenas inventários com métricas.
- Renderização da página inicial aprovada com duas imagens e sem texto PlanOS
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

Retomar a partir das próximas observações de uso do PlanOS. O histórico
funcional e arquitetural permanece nos commits anteriores e nos demais
documentos desta pasta; não é necessário reconstruir as decisões já aplicadas.

## Evolução cross-media em andamento

Em 22 de julho de 2026 foi implementada a base da versão 2.0: identificadores
legíveis e versionados, duplicação das entidades, contexto ativo, indicadores
reais na página inicial, medições com fonte e metodologia, planejamento
configurável por inventário, alcance incremental, saturação, custos e retorno,
cronograma visual e comparação ponderada de estratégias. A migração remota
`20260722110000` foi aplicada. O modelo está documentado em
`docs/MODELO_PLANEJAMENTO_CROSS_MEDIA.md`.
