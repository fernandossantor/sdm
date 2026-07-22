# Continuidade do desenvolvimento

Última revisão: 22 de julho de 2026 (UTC).

## Ponto de retomada

- Branch: `main`.
- Última entrega funcional antes deste registro: `f92c0ac` (`Evolui PlanOS com GRP e cronograma semanal`).
- O repositório local e `origin/main` estavam sincronizados nessa revisão.
- O aplicativo publicado usa o nome **PlanOS** e o subtítulo **Plataforma Inteligente de Planejamento Híbrido de Mídia**.
- A última rodada implementou o triângulo Alcance/Frequência/GRP, a exibição de GRP no plano, o cronograma semanal configurável, o guia de uso, a revisão das colunas de planejamento e as descrições fornecidas para o catálogo.
- As migrações remotas do Supabase estavam sincronizadas até `20260722090000`.

## Estado verificado

- Supabase: projeto `SDM` (`moqyzfdgiajglhuqiymw`) vinculado e `ACTIVE_HEALTHY`.
- CLI Supabase: instalada localmente pelo `package-lock.json`; em uma reconstrução do Codespace, `npm ci` é executado automaticamente.
- Credencial do Git: leitura de `origin` confirmada em 22/07/2026.
- GitHub CLI (`gh`): o token próprio reportou expiração, mas isso não afetou a credencial Git usada para sincronizar o repositório. Operações exclusivas da API do `gh` poderão exigir autenticação renovada; commits e pushes usam a credencial Git já configurada.
- Configuração local: `.env` presente e ignorado pelo Git. Segredos não são copiados para arquivos versionados.
- Produção: os segredos permanecem no mecanismo seguro do Streamlit Cloud/Supabase.

## Validação da última entrega

- 51 testes automatizados aprovados; 3 testes de integração opcionais ignorados nessa execução.
- 3 testes de integração aprovados em execução autenticada.
- Health check do runtime aprovado.
- Geração real validada com alcance de 80%, frequência 7 e GRP 560, incluindo três itens e cronograma de 11 semanas.

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

Retomar a partir das próximas observações de uso do PlanOS. O histórico funcional e arquitetural permanece nos commits anteriores e nos demais documentos desta pasta; não é necessário reconstruir as decisões já aplicadas.
