# Homologação e piloto controlado

Revisão: 27 de julho de 2026 (UTC).

## Estado atual

O gate automatizado conectado foi aprovado em 27 de julho de 2026:

- 157 testes offline;
- regressão funcional;
- health check de 10 tabelas;
- auditoria de bloqueio público;
- 3 testes de integração;
- 23 migrations locais e remotas sincronizadas.

Executar novamente depois da rotação de segredos:

```bash
python -m scripts.homologar --connected --saida /tmp/planos-homologacao.json
```

O arquivo de evidência fica fora do repositório e não deve conter segredos.

## Gates anteriores ao piloto

- [ ] chave administrativa rotacionada;
- [ ] `.env` local atualizado sem versionamento;
- [ ] segredos da hospedagem atualizados;
- [ ] `PLANOS_ENV=production`;
- [ ] `PLANOS_AUTH_ENABLED=true`;
- [ ] gate conectado aprovado após a rotação;
- [ ] backup completo posterior à rotação validado;
- [ ] restauração desse backup ensaiada;
- [ ] CI do commit candidato aprovado;
- [ ] participantes e período do piloto registrados;
- [ ] aviso de privacidade e limitações apresentado aos participantes;
- [ ] responsável operacional e substituto definidos;
- [ ] canal de suporte e registro de incidentes definido.

Qualquer item aberto impede o início do piloto.

## Roteiro funcional

Cada piloto executará em espaço próprio ou compartilhado explicitamente:

1. entrar e trocar a senha temporária;
2. criar ou selecionar projeto;
3. preencher briefing ampliado;
4. selecionar papéis dos meios;
5. gerar e salvar plano;
6. revisar estratégia, premissas, custos, alcance e frequência;
7. conferir cronogramas e reconciliação;
8. gerar forecast e diagnóstico;
9. registrar realizado apenas com fonte e período;
10. comparar versões;
11. testar atribuição com dados não identificáveis;
12. documentar qualidade e localização quando aplicável;
13. exportar o relatório completo;
14. confirmar que outro usuário não acessa o projeto sem compartilhamento;
15. compartilhar como leitor e editor e testar revogação.

## Aceite

O piloto é aprovado somente quando:

- nenhuma falha crítica de isolamento, autenticação ou perda de dados ocorrer;
- cálculos e exportações forem reproduzíveis;
- orçamento, quantidades e cronograma reconciliarem;
- lacunas e limitações forem visíveis;
- leitor não editar e usuário sem vínculo não acessar;
- revogação retirar o acesso;
- erros relevantes tiverem registro e resposta;
- feedback dos participantes estiver classificado e rastreável.

## Interrupção imediata

Suspender o piloto e desabilitar o acesso quando houver:

- exposição de segredo ou dado pessoal;
- acesso cruzado não autorizado;
- perda, alteração indevida ou corrupção de dados;
- backup não recuperável;
- indisponibilidade persistente sem diagnóstico;
- divergência financeira ou metodológica silenciosa.
