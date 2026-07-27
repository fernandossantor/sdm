# Runbook operacional do MediAd Planner

Revisão: 27 de julho de 2026 (UTC).

## Responsabilidades

Antes do piloto, preencher:

- responsável primário: pendente;
- substituto: pendente;
- canal de suporte: pendente;
- janela do piloto: pendente;
- retenção dos dados e backups: pendente.

## Verificação de rotina

No início e no fim de cada sessão de piloto:

```bash
python -m scripts.health_check
python -m scripts.auditar_seguranca
```

Antes de cada versão candidata:

```bash
python -m scripts.homologar --connected --saida /tmp/planos-homologacao.json
python -m scripts.verificar_backup /caminho/privado/do/backup
```

Também conferir:

- GitHub Actions do commit candidato;
- logs de execução da hospedagem;
- saúde, armazenamento e conexões no painel do Supabase;
- crescimento de projetos, versões e artefatos;
- logs administrativos e tentativas recorrentes de acesso.

O health check cobre as estruturas históricas e as tabelas críticas de perfis,
espaços, membros, projetos, compartilhamentos, planejamentos, versões,
artefatos, preços e auditoria. Uma tabela inacessível encerra o comando com
falha.

## Classificação de incidentes

| Severidade | Exemplo | Resposta |
|---|---|---|
| Crítica | segredo exposto, acesso cruzado, perda de dados | interromper piloto imediatamente |
| Alta | login indisponível, escrita bloqueada para todos | suspender novas sessões e diagnosticar |
| Média | exportação ou análise específica falha | registrar, orientar contorno e corrigir |
| Baixa | texto, layout ou orientação incorreta | registrar para próxima versão |

## Resposta inicial

1. registrar horário, usuário afetado, ação e evidência;
2. não copiar tokens, senhas ou dados pessoais para o chamado;
3. conter o impacto: revogar sessão, bloquear conta ou interromper piloto;
4. preservar logs e identificar a versão;
5. avaliar confidencialidade, integridade e disponibilidade;
6. restaurar somente a partir de conjunto validado;
7. repetir saúde, segurança, integração e fluxo afetado;
8. documentar causa, correção, risco residual e decisão de reabertura.

Incidentes com dados pessoais devem ser avaliados pelo responsável institucional
conforme a regulamentação e os procedimentos aplicáveis. O MediAd Planner não decide
automaticamente se uma comunicação regulatória é necessária.

## Recuperação

- confirmar o diretório exato e o manifesto do backup;
- validar SHA-256 antes de qualquer restauração;
- restaurar em ambiente isolado;
- comparar identidades, tabelas, constraints e contagens materiais;
- executar testes RLS e multiusuário;
- somente então decidir sobre recuperação do ambiente do piloto.

## Retorno ao serviço

Reabrir somente quando:

- causa estiver identificada ou risco contido;
- gate conectado estiver aprovado;
- isolamento e permissões estiverem confirmados;
- backup recuperável estiver disponível;
- participantes receberem orientação sobre o ocorrido quando aplicável.
