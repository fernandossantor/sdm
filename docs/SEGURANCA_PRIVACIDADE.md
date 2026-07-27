# Segurança e privacidade operacional

Revisão: 27 de julho de 2026 (UTC).

## Gate de produção

O PlanOS somente aceita `PLANOS_ENV=production` quando:

- `PLANOS_AUTH_ENABLED=true`;
- URL, chave pública e chave `service_role` estão presentes;
- chave pública e chave administrativa são diferentes.

A chave `service_role` pertence exclusivamente ao backend e às rotinas
administrativas. Ela não pode ser incluída no Git, enviada ao navegador,
copiada para logs ou usada como `SUPABASE_KEY`.

## Dados e acesso

- cadastro de contas é controlado por administrador;
- senha temporária deve ser trocada no primeiro acesso;
- sessões são isoladas por requisição;
- operações comuns usam o JWT do usuário e políticas RLS;
- operações administrativas exigem administrador ativo e geram auditoria;
- projetos compartilhados usam papéis de proprietário, editor e leitor;
- arquivamento preserva o histórico.

## Privacidade do piloto

O piloto deve usar somente dados necessários ao planejamento. Não devem ser
inseridos dados pessoais sensíveis, credenciais, listas identificáveis de
consumidores ou sinais individuais de localização. Dados geográficos devem
registrar finalidade, base legal, fonte, precisão, período e limitações.

Antes do piloto, os participantes devem receber:

- finalidade e escopo acadêmico da plataforma;
- categorias de dados tratadas;
- responsáveis pelo acesso e suporte;
- prazo de retenção;
- canal para correção ou remoção;
- limitações de disponibilidade e ausência de SLA empresarial.

## Gates ainda manuais

- rotacionar qualquer segredo que tenha sido exposto;
- configurar segredos no ambiente seguro de hospedagem;
- confirmar que autenticação está habilitada;
- executar auditoria RLS e teste multiusuário;
- confirmar backup restaurável recente;
- registrar participantes, período e aceite do piloto.
