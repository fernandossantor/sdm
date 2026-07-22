# Plano de evolução multiusuário

Última revisão: 22 de julho de 2026 (UTC).

## Finalidade deste documento

Este documento é o ponto de retomada para a futura evolução do PlanOS para um
ambiente acadêmico multiusuário. Ele sistematiza as decisões tomadas na
conversa de planejamento e deve ser consultado antes de iniciar a
implementação.

Nenhuma das funcionalidades descritas abaixo estava autorizada para
implementação no momento desta revisão. Este registro não altera código,
banco de dados, configuração ou publicação.

## Contexto e premissas

- Uso acadêmico, com no máximo aproximadamente 200 pessoas por ano.
- Manter inicialmente Supabase, GitHub, Codespaces e Streamlit em seus planos
  gratuitos.
- O ChatGPT Plus/Codex será usado apenas no desenvolvimento e manutenção; ele
  não hospeda o aplicativo nem fornece capacidade de execução aos usuários.
- O cadastro inicial será controlado pelo administrador, sem cadastro público.
- Convites e credenciais poderão ser comunicados manualmente, sem dependência
  inicial de SMTP externo.
- O aplicativo poderá usar uma única implantação e um único banco, desde que a
  separação entre administração e produção seja garantida por autorização no
  servidor e por políticas no banco.

## Decisões funcionais

### 1. Exclusão de inventários

- Adicionar opção de excluir inventários, preferencialmente na página de
  cadastro e, se for útil à navegação, também no catálogo.
- Exigir confirmação explícita antes da operação.
- Verificar referências do inventário em planos e demais entidades.
- Impedir exclusões que deixem dados inconsistentes.
- Quando houver histórico ou dependências, avaliar arquivamento ou desativação
  em vez de exclusão física.
- Registrar autor e data da operação.

### 2. Autenticação e contas

- Implementar autenticação com Supabase Auth.
- Permitir que somente o administrador crie contas na primeira fase.
- Criar a conta já confirmada quando o fluxo administrativo assim exigir.
- Usar senha inicial temporária e exigir sua alteração no primeiro acesso.
- Nunca armazenar ou registrar senhas em texto legível.
- Permitir bloqueio, reativação e redefinição administrativa de acesso.
- Não abrir cadastro público enquanto não houver decisão específica para isso.

### 3. Papéis e áreas do aplicativo

Implementar pelo menos os papéis `administrador` e `usuário`.

A área administrativa, acessível somente ao administrador, deverá permitir:

- criar e consultar usuários;
- bloquear e reativar contas;
- redefinir o acesso;
- conceder e remover permissões;
- compartilhar projetos;
- administrar inventários globais;
- consultar registros básicos de operações administrativas.

A área de produção deverá permitir aos usuários comuns:

- acessar somente os dados da própria conta ou espaço de trabalho;
- usar os inventários autorizados;
- criar e editar planos;
- acessar projetos próprios ou compartilhados;
- executar somente operações permitidas pelo seu papel.

Ocultar elementos da interface não será considerado proteção suficiente. O
servidor e o banco deverão negar acessos não autorizados mesmo quando alguém
tentar abrir diretamente uma URL ou chamar uma operação fora da interface.

### 4. Isolamento dos dados

- Associar planos, inventários privados e demais registros ao proprietário ou
  espaço de trabalho correspondente.
- Criar modelo de espaços de trabalho e associação de membros se esse modelo
  for confirmado durante o desenho técnico.
- Implementar Row Level Security (RLS) em todas as tabelas multiusuário.
- Usar a sessão e o JWT do usuário nas operações normais.
- Eliminar o uso indiscriminado de `service_role` no fluxo comum.
- Manter credenciais administrativas somente no servidor e apenas para
  operações estritamente administrativas.
- Testar explicitamente tentativas de leitura e alteração entre contas.

### 5. Inventários globais e privados

- Inventários globais serão mantidos pelo administrador e disponibilizados aos
  usuários autorizados.
- Inventários privados pertencerão a um usuário ou espaço de trabalho e não
  serão visíveis a outras contas sem autorização explícita.
- Edição, exclusão, arquivamento e utilização deverão respeitar propriedade,
  papel e dependências existentes.

### 6. Compartilhamento de projetos

- Permitir compartilhar um projeto com outro usuário já cadastrado.
- Não duplicar os dados do projeto para realizar o compartilhamento.
- Prever permissões de proprietário, editor e leitor.
- Permitir a revogação posterior do acesso.
- Restringir a gestão dos participantes ao proprietário e ao administrador.
- Fazer o compartilhamento inicialmente pela interface interna, sem envio de
  convite por e-mail.

### 7. Comunicação manual de credenciais

Na primeira fase, o administrador poderá:

1. criar a conta;
2. gerar ou definir uma senha temporária;
3. comunicar as credenciais por um canal externo;
4. exigir a alteração da senha no primeiro acesso;
5. conceder acesso a projetos diretamente a usuários já cadastrados.

A senha temporária não deverá permanecer visível nem ser gravada em texto
legível. SMTP externo poderá ser incluído posteriormente para confirmação,
recuperação de senha e convites automáticos.

## Infraestrutura gratuita e limitações aceitas

### Supabase Free

Para o volume acadêmico previsto, as cotas atuais são amplamente superiores à
quantidade esperada de usuários. Ainda assim, deverão ser considerados:

- limite de dois projetos gratuitos ativos;
- banco de 500 MB por projeto;
- 1 GB de armazenamento de arquivos;
- 5 GB de egress;
- possibilidade de pausa após um período de baixa atividade geral;
- ausência de SLA, suporte dedicado e backups automáticos recuperáveis no
  plano gratuito.

O pausamento é avaliado para o projeto inteiro, e não para cada usuário. A
atividade de qualquer usuário conta como atividade do banco. O uso diário do
projeto reduz substancialmente o risco de pausa, embora não constitua garantia
formal de disponibilidade.

### E-mail do Supabase

O provedor SMTP padrão é destinado a testes, tem restrições de destinatários e
limite reduzido de mensagens. Ele não deve ser usado como sistema de entrega
para produção. A administração manual evita essa dependência na primeira fase.

### Streamlit Community Cloud

- O aplicativo pode hibernar depois de inatividade.
- A hibernação é geral para a aplicação, não individual por usuário.
- Um novo acesso pode reativar a aplicação.
- Limites de memória, CPU e ausência de SLA são aceitos durante a fase
  acadêmica inicial.

### GitHub, Codespaces e Codex

- GitHub Free será usado para versionamento e CI dentro das cotas disponíveis.
- Codespaces será usado somente para desenvolvimento, respeitando a franquia
  mensal de processamento e armazenamento.
- Codex no ChatGPT Plus possui limites variáveis conforme a complexidade e a
  duração das tarefas; esses limites não interferem no uso do aplicativo pelos
  alunos.
- Se o aplicativo não chamar a API da OpenAI em tempo de execução, seus
  usuários não gerarão consumo de API da OpenAI.

## Backup e continuidade

- Criar procedimento periódico de backup do Supabase.
- Adotar inicialmente frequência semanal e executar backup adicional antes de
  alterações estruturais relevantes.
- Exportar esquema e dados pelas ferramentas oficiais do Supabase/PostgreSQL.
- Armazenar as cópias fora do banco principal e em local privado.
- Nunca versionar dados reais de usuários em repositório público.
- Documentar e testar o procedimento de restauração.
- Tratar a prevenção de perda de dados separadamente do risco de pausa: uso
  frequente evita inatividade, mas não protege contra exclusões ou erros.

## Segurança mínima antes da abertura aos usuários

- Revisar segredos e variáveis de ambiente.
- Confirmar que chaves administrativas nunca chegam ao navegador.
- Aplicar e testar RLS em todas as tabelas multiusuário.
- Testar acesso cruzado com pelo menos duas contas comuns e uma administradora.
- Registrar operações administrativas relevantes.
- Proteger a conta administradora com senha forte e MFA.
- Definir regras de desativação, retenção e eventual remoção de usuários.
- Rever o tratamento de dados pessoais no contexto acadêmico.

## Sequência recomendada de implementação

1. Confirmar o estado do repositório, da produção e das migrações.
2. Fazer backup completo antes de alterar o modelo de dados.
3. Mapear tabelas, relações e todos os usos atuais de `service_role`.
4. Definir o modelo de usuários, espaços, papéis e compartilhamentos.
5. Criar e revisar as migrações do banco.
6. Implementar e testar as políticas RLS.
7. Adaptar a camada de acesso ao Supabase para usar a identidade do usuário.
8. Implementar login, sessão e troca obrigatória da senha inicial.
9. Criar a área administrativa.
10. Isolar planos e inventários por proprietário ou espaço.
11. Implementar compartilhamento e suas permissões.
12. Implementar exclusão ou arquivamento seguro de inventários.
13. Criar e testar a rotina de backup e restauração.
14. Executar testes de segurança, regressão e múltiplos usuários.
15. Publicar gradualmente e acompanhar uso, armazenamento e disponibilidade.

## Critérios para considerar a evolução concluída

- Usuários comuns não acessam a área administrativa.
- Nenhuma conta lê ou altera dados privados de outra conta sem
  compartilhamento.
- Inventários globais e privados obedecem às regras definidas.
- Projetos podem ser compartilhados e o acesso pode ser revogado.
- Exclusão ou arquivamento de inventários preserva a integridade histórica.
- Credenciais administrativas permanecem restritas ao servidor.
- Backup e restauração foram testados.
- O fluxo completo funciona na implantação do Streamlit dentro das limitações
  aceitas para o uso acadêmico.

## Orientação para a retomada

Ao retomar este trabalho, não começar diretamente pela interface. Primeiro
auditar o modelo existente, o acesso com `service_role`, as migrações e as
relações dos inventários. Apresentar o desenho técnico e o impacto esperado
antes de aplicar alterações estruturais ou publicar uma nova versão.
