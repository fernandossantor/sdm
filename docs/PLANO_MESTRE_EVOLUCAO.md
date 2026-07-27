# Plano mestre de evolução do PlanOS

Última revisão: 27 de julho de 2026 (UTC).

## Objetivo

Este documento consolida a evolução metodológica, funcional, arquitetural e
multiusuário do PlanOS. Ele integra as pendências encontradas na `main`, nas
branches de continuidade e refatoração, nos materiais de mídia e no
`PLANO_MULTIUSUARIO.md`.

As regras de cálculo que orientam este plano estão fixadas em
`DECISOES_METODOLOGICAS_ENGINES.md`.

## Estado de partida

### Base saudável

- fluxo cross-media configurável implementado;
- 60 testes offline aprovados e 3 integrações opcionais;
- migrações locais e remotas sincronizadas até `20260722110000`;
- acesso público bloqueado e backend atual operando com `service_role`;
- GRP, cronograma, alcance estimado, custos e retorno já representados;
- persistência de projetos, briefings, planejamentos e artefatos.

### Lacunas críticas

- todos os repositories normais usam cliente administrativo;
- não há autenticação, propriedade, compartilhamento ou RLS por usuário;
- conceitos de audiência, consumo, entrega e afinidade ainda se sobrepõem;
- GRP cross-media é agregado sem validar comparabilidade;
- alcance líquido usa fallback probabilístico implícito;
- saturação é apenas excesso médio;
- forecast usa defaults silenciosos e pode divergir do plano;
- restrições não são aplicadas uniformemente;
- alocação proporcional é apresentada como otimização;
- custos programáticos e qualidade de mídia estão incompletos;
- atribuição, realizado e incrementalidade não têm modelo próprio;
- documentação de continuidade não funciona como backlog executável.

## Resultado esperado

Ao final, o PlanOS deverá:

- gerar planos metodologicamente auditáveis;
- distinguir medição, premissa, decisão e estimativa;
- produzir soluções viáveis sob restrições;
- preservar histórico e versões;
- comparar planejado, forecast e realizado;
- operar com múltiplos usuários e isolamento no banco;
- compartilhar projetos com papéis explícitos;
- administrar inventários globais e privados;
- explicar cada recomendação, limitação e cálculo;
- executar backup e restauração testados.

## Diretrizes de execução

1. Segurança e metodologia são requisitos de domínio, não acabamentos de UI.
2. Alterações de banco serão aditivas e precedidas por backup.
3. `service_role` ficará restrito a administração e manutenção.
4. Migrações terão caminho de preenchimento para dados legados.
5. Nenhuma fase publicará números que não reconciliem entre telas e exportações.
6. Branches antigas serão fontes de ideias, não bases para merge indiscriminado.
7. Cada fase deverá terminar utilizável, testada e reversível.

## Trilha A — Governança metodológica e dados

### A1. Catálogo de métricas e unidades

Entregas:

- entidades para métrica, unidade, fórmula e compatibilidade;
- distinção entre impactos, impressões, OTS, audiência, circulação, fluxo,
  visualização e contatos estimados;
- regras de quantidade e arredondamento por unidade de compra;
- compatibilidade entre universo, target, praça, período e metodologia.

Aceite:

- nenhuma métrica é agregada sem denominador;
- conversões de unidade são explícitas e testadas;
- métrica nativa permanece visível.

### A2. Proveniência, confiança e versões

Entregas:

- metadados de fonte, período, metodologia, natureza e confiança;
- versão dos engines e fórmulas no plano;
- snapshot das entradas;
- trilha de alterações manuais.

Aceite:

- todo número material do plano pode ser rastreado;
- recalcular cria versão sem alterar o plano histórico.

### A3. Custos e modelos de compra

Entregas:

- preço de tabela, desconto, líquido e custo total;
- fees de tecnologia, dados, verificação e operação;
- open auction, PMP, preferred deal, garantido e direto;
- disponibilidade, capacidade e mínimos comerciais.

Aceite:

- CPM, CPP, ROI e ROAS identificam numerador e denominador;
- totais reconciliam por item, período e plano.

## Trilha B — Reengenharia dos engines

### B1. Pipeline canônico

Ordem:

1. validar briefing e objetivos;
2. montar universo elegível;
3. aplicar restrições duras;
4. calcular componentes de qualidade e aderência;
5. gerar ranking explicável;
6. resolver alocação ou otimização;
7. calcular entrega;
8. consolidar alcance e frequência;
9. gerar forecast por cenários;
10. produzir diagnóstico e recomendações.

Responsabilidades:

- `InventoryEngine`: universo candidato e elegibilidade técnica;
- `ScoreEngine`: componentes, normalização e ranking;
- `AllocationEngine`: heurística explicitamente identificada;
- `BudgetOptimizer`: solução sob restrições;
- `MediaPlanEngine`: compra e entrega planejada;
- `ForecastEngine`: cenários condicionados;
- `RecommendationEngine`: explicações baseadas na auditoria;
- `ScenarioEngine`: variações controladas;
- `InsightsEngine`: leitura estratégica sem modificar resultados.

O trabalho da branch `refactor/sdm-finalizacao` será revisado conceito a
conceito, com destaque para desacoplamento, ranking e teste offline. Nenhum
commit será portado sem adaptação ao modelo atual.

### B2. Restrições e viabilidade

Entregas:

- tipos de restrição definidos em domínio;
- aplicação uniforme para objetos e dicionários;
- diagnóstico de inviabilidade;
- simulação de relaxamento com aprovação.

Aceite:

- proibidos nunca entram;
- obrigatórios entram ou a geração falha;
- pisos e tetos permanecem válidos após arredondamento;
- orçamento nunca é excedido silenciosamente.

### B3. Alcance, frequência e GRP

Entregas:

- verificador de comparabilidade;
- alcance líquido por níveis de evidência;
- superposição e incremental auditados;
- distribuição de frequência;
- GRP/TRP por universo;
- confiança do agregado cross-media.

Aceite:

- ordem só afeta resultado quando o método declarar dependência;
- alcance fica entre 0 e 100%;
- GRP incompatível não é somado;
- identidades matemáticas reconciliam dentro da tolerância definida.

### B4. Saturação e resposta

Entregas:

- frequência efetiva e faixas;
- sinalização separada de subexposição e sobre-exposição;
- curvas opcionais, calibradas e versionadas;
- impacto marginal usado pelo otimizador apenas quando defensável.

Aceite:

- ausência de curva não produz falsa estimativa de saturação;
- o usuário vê a origem e confiança do modelo.

### B5. Otimização

Entregas:

- função objetivo selecionável;
- solução com quantidades discretas e restrições;
- multiobjetivo com pesos explícitos;
- relatório de viabilidade e restrições ativas;
- benchmark contra alocação heurística.

Aceite:

- solução respeita todas as restrições duras;
- sobra e déficit são explicados;
- repetição com mesmas entradas é determinística;
- “ótimo” só é usado quando suportado pelo método.

### B6. Forecast, cenários e realizado

Entregas:

- remoção de CPM, CTR, conversão e frequência silenciosos;
- cenário conservador, base e otimista;
- análise de sensibilidade;
- ingestão de realizado;
- comparação planejado × forecast × realizado.

Aceite:

- meios não clicáveis não recebem cliques genéricos;
- ausência de premissa bloqueia somente o resultado dependente;
- plano, dashboard e exportação usam a mesma fonte calculada.

### B7. Atribuição

Entregas:

- modelos baseados em regras;
- janela, eventos e crédito fracionado;
- conversões diretas e assistidas;
- separação de atribuição e incrementalidade;
- suporte futuro a experimento e modelos causais.

Aceite:

- soma do crédito fecha em 100% por conversão elegível;
- limitações de identidade e canais são mostradas;
- receita atribuída não é rotulada como incremental.

## Trilha C — Produto e fluxo do planejamento

### C1. Briefing ampliado

Adicionar:

- mercado e concorrência;
- situação de marca e categoria;
- objetivos encadeados;
- jornada e ciclo de compra;
- sazonalidade;
- praça e capacidade de distribuição;
- critérios criativos;
- riscos e condições regulatórias.

### C2. Estratégia e tática

Entregas:

- separação clara entre estratégia, tática e operação;
- papéis básico/principal, complementar e apoio;
- racional por meio;
- mapa de cobertura da jornada;
- alternativas rejeitadas e respectivos motivos.

### C3. Cronograma e mapas

Entregas:

- flights linear, ondas, concentrado e personalizado;
- resumo semanal e mensal;
- mapas por tipo de mídia;
- inserções, horários, custos, audiência e indicadores;
- reconciliação de cronograma, quantidade e verba.

### C4. Qualidade e transparência

Entregas:

- viewability, fraude, tráfego inválido, brand safety e suitability;
- listas de permissão e bloqueio;
- atualidade e qualidade das fontes;
- riscos de privacidade e uso de dados.

### C5. Relatórios

Entregas:

- plano completo, não apenas tabela;
- anexos de premissas e auditoria;
- exportação consistente em Excel/CSV;
- PDF e PowerPoint em fase posterior;
- comparação de versões.

## Trilha D — Arquitetura multiusuário

Esta trilha incorpora e detalha `PLANO_MULTIUSUARIO.md`.

### D1. Modelo de identidade e espaços

Tabelas propostas:

- `perfis`, vinculado a `auth.users`;
- `espacos_trabalho`;
- `espacos_membros`;
- `projetos_membros`;
- `logs_auditoria`.

Papéis:

- global: `ADMINISTRADOR`, `USUARIO`;
- no espaço: `PROPRIETARIO`, `GESTOR`, `MEMBRO`;
- no projeto: `PROPRIETARIO`, `EDITOR`, `LEITOR`.

Decisão:

- dados de produção pertencem a um espaço de trabalho;
- projetos têm proprietário e podem ser compartilhados sem duplicação;
- papel global não substitui permissão contextual.

### D2. Propriedade dos dados

Adicionar conforme a natureza:

- `espaco_id`;
- `criado_por`;
- `atualizado_por`;
- `arquivado_em`;
- `arquivado_por`.

Projetos, briefings, planejamentos, artefatos, públicos privados, cenários,
medições privadas e inventários privados seguirão o espaço.

Catálogos de referência poderão ser globais e somente leitura para usuários
comuns.

### D3. Inventários globais e privados

Inventários terão:

- escopo `GLOBAL` ou `PRIVADO`;
- espaço proprietário quando privado;
- estado ativo/arquivado;
- autor e datas;
- regras de uso e edição.

Inventário global será mantido pelo administrador. Inventário privado será
visível apenas no espaço autorizado.

### D4. Compartilhamento

Entregas:

- compartilhamento com usuário cadastrado;
- leitor, editor e proprietário;
- revogação;
- gestão restrita ao proprietário e administrador;
- auditoria de concessão e remoção.

### D5. Autenticação e sessão

Entregas:

- Supabase Auth;
- cadastro apenas administrativo;
- senha temporária sem persistência legível;
- troca obrigatória no primeiro acesso;
- logout e expiração;
- bloqueio, reativação e redefinição;
- MFA para administrador.

Decisão:

- operações normais usarão o JWT do usuário;
- o cliente administrativo não será injetado em repositories comuns;
- `service_role` será usado apenas em casos administrativos explícitos.

### D6. RLS

Entregas:

- políticas por tabela e operação;
- funções auxiliares seguras para membresia e papel;
- acesso a globais versus privados;
- compartilhamento de projeto;
- revogação imediata.

Aceite:

- usuário A não lê nem altera dados privados de B;
- leitor não escreve;
- editor não gerencia participantes;
- proprietário gerencia o projeto;
- administrador atua somente pelas capacidades previstas;
- URL direta ou chamada de API não contorna a política.

### D7. Área administrativa

Entregas:

- criar e consultar usuários;
- bloquear, reativar e redefinir acesso;
- administrar permissões;
- compartilhar projetos;
- administrar inventários globais;
- consultar logs administrativos.

### D8. Migração dos dados existentes

Estratégia:

1. criar administrador inicial;
2. criar espaço legado;
3. associar registros existentes ao espaço;
4. preencher autores técnicos quando o autor real não existir;
5. validar contagens e referências;
6. somente então tornar colunas obrigatórias.

Não haverá exclusão de dados para simplificar a migração.

## Trilha E — Inventários, histórico e exclusão

### E1. Arquivamento

Arquivamento será a operação padrão para inventários usados. Deve registrar
autor, data e motivo. Inventário arquivado permanece em planos históricos e não
aparece para novas seleções.

### E2. Exclusão física

Permitida somente quando:

- usuário tem permissão;
- inventário nunca foi usado;
- não há medição, preço, papel, planejamento ou artefato dependente;
- operação ocorre em função transacional;
- confirmação explícita foi fornecida;
- auditoria foi registrada.

Relacionamentos históricos não usarão cascata destrutiva indiscriminada.

## Trilha F — Segurança, continuidade e operação

### F1. Segredos

- revisar `.env`, Streamlit Secrets e Supabase;
- impedir exposição de chave administrativa;
- rotacionar qualquer segredo suspeito;
- verificar logs e exportações.

### F2. Backup e restauração

- backup semanal;
- backup antes de cada migration estrutural;
- esquema e dados armazenados privadamente fora do projeto;
- procedimento de restauração documentado;
- teste periódico de restauração.

### F3. Auditoria

Registrar:

- criação e bloqueio de usuário;
- alterações de papel;
- compartilhamento e revogação;
- arquivamento e exclusão;
- mudanças metodológicas relevantes;
- publicação e restauração de versões.

Senhas, tokens e dados sensíveis não serão registrados.

### F4. Privacidade

- classificar dados pessoais;
- minimizar coleta;
- definir retenção;
- registrar finalidade para localização e identificadores;
- estabelecer processo de desativação e remoção;
- revisar requisitos acadêmicos e institucionais antes da abertura.

## Trilha G — Testes e validação

### G1. Testes matemáticos

- exemplos das aulas para GRP, alcance, frequência, CPP e CPM;
- invariantes e limites;
- unidades discretas;
- arredondamento e reconciliação;
- agregações compatíveis e incompatíveis.

### G2. Testes dos engines

- ranking determinístico;
- restrições duras e flexíveis;
- problemas viáveis e inviáveis;
- comparação heurística × otimização;
- cenários e sensibilidade;
- ausência de dados;
- versões históricas.

### G3. Testes multiusuário

Matriz mínima com:

- duas contas comuns;
- uma administradora;
- dois espaços;
- projeto próprio e compartilhado;
- leitor, editor e proprietário;
- inventário global e privado;
- concessão e revogação.

Testar leitura, inserção, alteração e exclusão diretamente na API, não apenas
pela interface.

### G4. Regressão ponta a ponta

Validar:

- briefing;
- seleção e ranking;
- plano;
- forecast;
- diagnóstico;
- dashboard;
- cenários;
- comparação;
- exportação;
- restauração de plano antigo.

## Sequência de implementação

### Fase 0 — Preparação

1. atualizar `main` e criar branch dedicada;
2. fazer backup e ensaio de restauração;
3. inventariar esquema remoto, dados e usos de `service_role`;
4. converter este plano em issues ou entregas rastreáveis.

Saída: ambiente recuperável e backlog aprovado.

### Fase 1 — Fundação metodológica

1. implementar proveniência, confiança e versões;
2. criar catálogo de métricas e unidades;
3. modelar comparabilidade, custos e tipos de compra;
4. migrar dados atuais sem alterar resultados.

Saída: base capaz de sustentar cálculos auditáveis.

### Fase 2 — Correções críticas dos engines

1. unificar restrições;
2. separar elegibilidade e score;
3. corrigir GRP agregado e alcance;
4. remover defaults silenciosos do forecast;
5. reconciliar plano, forecast e exportação;
6. portar seletivamente ideias da branch de refatoração.

Saída: pipeline consistente, ainda com alocação heurística identificada.

### Fase 3 — Otimização e incerteza

1. implementar solver de restrições;
2. funções objetivo;
3. frequência efetiva e saturação;
4. cenários e sensibilidade;
5. realizado e diagnóstico.

Saída: planejamento defensável e comparável.

### Fase 4 — Fundação multiusuário

1. perfis, espaços, membros e propriedade;
2. migração para espaço legado;
3. clientes autenticados;
4. RLS e testes cruzados;
5. login e sessão.

Saída: isolamento efetivo no servidor e no banco.

Status: concluída em 27 de julho de 2026.

### Fase 5 — Administração e colaboração

1. área administrativa;
2. ciclo de vida de contas;
3. compartilhamento e revogação;
4. inventários globais e privados;
5. logs administrativos.

Saída: operação acadêmica controlada.

### Fase 6 — Produto completo

1. briefing ampliado;
2. estratégia e racional;
3. mapas e cronogramas;
4. atribuição;
5. qualidade programática e localização;
6. relatórios e comparação de versões.

Saída: plano completo, não apenas cálculo tático.

### Fase 7 — Homologação e publicação

1. segurança e privacidade;
2. backup/restauração;
3. regressão matemática e funcional;
4. homologação com usuários-piloto;
5. publicação gradual;
6. monitoramento de erros, uso, armazenamento e disponibilidade.

## Dependências entre trilhas

- A precede B porque engines auditáveis exigem dados qualificados.
- B2 e B3 precedem otimização.
- D1–D3 precedem RLS.
- RLS precede abertura a usuários.
- Versionamento precede colaboração para evitar sobrescrita histórica.
- Arquivamento precede exclusão física.
- Backup testado precede qualquer migration estrutural em produção.

## Fora do escopo inicial

- cadastro público;
- envio automático de convites;
- modelo causal automático sem dados adequados;
- machine learning sem dataset validado;
- API pública;
- cobrança e multiempresa comercial;
- disponibilidade ou SLA de nível empresarial.

## Critérios de conclusão

O plano será considerado concluído quando:

- cálculos obedecerem às decisões metodológicas;
- resultados forem reproduzíveis e explicáveis;
- métricas incompatíveis não forem agregadas;
- restrições e orçamento forem respeitados;
- forecast não inventar premissas;
- planos históricos preservarem método e versão;
- usuários comuns estiverem isolados por RLS;
- compartilhamento e revogação funcionarem;
- inventários globais e privados obedecerem ao escopo;
- arquivamento preservar histórico;
- backup e restauração forem testados;
- suíte matemática, multiusuário e ponta a ponta estiver aprovada;
- publicação piloto funcionar nas limitações acadêmicas aceitas.

## Primeira entrega recomendada

A primeira entrega de implementação será a Fase 0 seguida da Fase 1. Não se
deve iniciar pela tela de login nem pelo novo otimizador: ambos dependem de uma
base de dados versionada, recuperável e metodologicamente consistente.

## Progresso de implementação

### 26 de julho de 2026 — Fase 1, contrato de domínio inicial

- criado o contrato canônico de proveniência para natureza, origem e confiança;
- criado o contexto mínimo de comparabilidade definido pela DM-002;
- bloqueada a agregação direta quando há divergência ou metadado ausente;
- conversões permanecem dependentes de autorização explícita;
- resultados calculados passam a exigir versão do método e entradas;
- cobertura adicionada sem alterar cálculos ou persistência existentes.

Próximo bloqueio: concluir o backup e o ensaio de restauração da Fase 0 antes
de criar ou aplicar a migration aditiva do catálogo de métricas.

### 26 de julho de 2026 — Fase 0, backup e restauração

- backup de esquema, dados, dados públicos e papéis gerado fora do repositório;
- checksums SHA-256 calculados;
- esquema restaurado em PostgreSQL 17 isolado;
- 83 tabelas públicas e 93 chaves estrangeiras verificadas;
- dados da aplicação restaurados e contagens materiais conferidas;
- identificada a necessidade de restauração administrativa separada para
  tabelas internas do Storage;
- identificada a ausência do esquema-base nas migrations versionadas.

O procedimento e as pendências estão em `BACKUP_RESTAURACAO.md`. A migration
aditiva da Fase 1 pode ser preparada localmente, mas sua aplicação remota ainda
depende da cópia durável do backup em armazenamento privado.

### 27 de julho de 2026 — Fase 1, persistência metodológica

- migration aditiva criada para unidades, métricas, fórmulas, conversões e
  valores com proveniência;
- catálogo inicial inclui alcance, audiência, impressões, impactos, contatos
  estimados, GRP, frequência e investimento;
- fatos medidos exigem fonte e resultados exigem fórmula, versão e entradas;
- conversões são registros explícitos e exigem aprovação por padrão;
- RLS foi habilitada nas cinco tabelas, sem acesso para `anon` e
  `authenticated`;
- migration aplicada duas vezes com sucesso na restauração isolada, confirmando
  compatibilidade e idempotência;
- backup durável verificado no Google Drive sem compartilhamento;
- migration `20260727000000` aplicada e confirmada no projeto remoto;
- seeds remotos conferidos: 8 unidades e 8 métricas;
- health check, auditoria de segurança, regressão e 3 integrações autenticadas
  aprovados;
- geração legada por nome corrigida para preservar a frequência e sua faixa
  salvas no briefing;
- suíte offline ampliada para 68 testes aprovados.

### 27 de julho de 2026 — Fase 1, versões e snapshots

- criada estrutura imutável de versões de planejamento;
- planos legados recebem versão inicial sem alteração dos resultados;
- inserção, edição, recálculo e arquivamento geram snapshots transacionais;
- entradas, resultados, versões de engines e fórmulas ficam separados;
- cada versão recebe hash de conteúdo e número monotônico por plano;
- atualização e exclusão de versões são bloqueadas no banco;
- exclusão funcional passa a arquivamento para preservar o histórico;
- migration validada na restauração isolada e aplicada no projeto remoto após
  novo backup privado;
- backfill remoto conferido: 1 planejamento, 1 versão inicial e hash válido;
- acesso público à nova tabela permanece bloqueado, enquanto o papel de serviço
  consegue validar o schema;
- health check, auditoria de segurança, regressão e integrações autenticadas
  aprovados;
- suíte offline ampliada para 69 testes aprovados.

### 27 de julho de 2026 — Fase 1, custos auditáveis

- criado contrato monetário com arredondamento decimal determinístico;
- preço de tabela, desconto e preço líquido ficam separados no item;
- custo de mídia e fees de tecnologia, dados, verificação e operação são
  calculados e reconciliados com o custo total;
- preço unitário legado permanece compatível como preço líquido quando não há
  detalhamento comercial;
- consolidação, snapshot do plano e exportação preservam a decomposição;
- descontos e fees inválidos são rejeitados explicitamente;
- suíte offline ampliada para 71 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 1, condições comerciais

- preços passam a registrar moeda e modelo de negociação: open auction, PMP,
  preferred deal, garantido ou direto;
- fees percentuais e fixos, mínimos comerciais, disponibilidade e capacidade
  ficam associados ao preço e à sua vigência;
- o cadastro de inventários permite manter as novas condições;
- o planejamento herda mínimos e limites cadastrados e valida o orçamento pelo
  custo total com fees;
- registros legados recebem `BRL` e `DIRETO` sem alteração de valores;
- migration `20260727020000` validada duas vezes na restauração isolada;
- backup privado pré-migration verificado no Google Drive;
- migration aplicada e confirmada no projeto remoto;
- cinco preços legados conferidos com moeda, modelo e defaults íntegros;
- acesso público ao cadastro de preços permanece bloqueado;
- suíte offline ampliada para 73 testes; health check, auditoria, regressão e
  integrações autenticadas aprovados.

### 27 de julho de 2026 — Fase 2, elegibilidade e restrições duras

- criado contrato único de elegibilidade compatível com objetos e dicionários;
- inventários, plataformas, ambientes e tecnologias proibidos são excluídos
  antes do cálculo de score;
- seleções obrigatórias funcionam como filtro de elegibilidade, não como bônus;
- inventário obrigatório ausente torna a geração inviável com causa explícita;
- score deixa de misturar qualidade e aderência com restrições duras;
- ranking e alocador passam a usar a mesma semântica;
- alocação registra elegíveis, excluídos, motivos e obrigatórios;
- suíte offline ampliada para 79 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 2, limites de compra

- criado resolvedor único para pisos e tetos de quantidade e verba;
- interface e engine usam a mesma fórmula e a mesma ordem de aplicação;
- quantidades discretas são arredondadas antes da validação final;
- piso de verba considera preço líquido, fees percentuais e fees fixos;
- disponibilidade e capacidade permanecem como tetos efetivos;
- metas acima do teto não são mais reduzidas silenciosamente;
- conflitos entre pisos e tetos produzem diagnóstico de inviabilidade;
- restrições ativas ficam preservadas no plano, snapshot e exportação;
- suíte offline ampliada para 82 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 2, GRP e alcance auditáveis

- o contrato de comparabilidade passa a controlar a consolidação real do GRP;
- universo, target, praça, período, métrica, metodologia e granularidade são
  verificados antes da soma;
- componentes incompatíveis ou indeterminados permanecem visíveis por meio,
  mas não produzem `grp_total`;
- o motivo da não agregação integra a auditoria e o snapshot do plano;
- metas originais do briefing não são sobrescritas por agregado inválido;
- ausência de superposição ou incremental deixa o alcance líquido indisponível;
- hipótese de independência exige seleção explícita e recebe confiança baixa;
- suíte offline ampliada para 86 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 2, forecast sem defaults silenciosos

- removidos os defaults implícitos de CPM, conversão e frequência;
- o forecast prioriza entrega e resultados já calculados no plano;
- cada resultado dependente só é produzido quando suas entradas existem;
- zero explicitamente informado permanece diferente de dado ausente;
- inventários sem métricas continuam visíveis com a lista de lacunas;
- dashboard e insights exibem indisponibilidade em vez de converter lacunas em
  zero;
- comparação por conversões incompletas é bloqueada com causa explícita;
- suíte offline ampliada para 87 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 2, alocação heurística identificada

- redistribuição proporcional deixa de ser apresentada como otimização;
- método, versão, função e limitações acompanham cada simulação;
- a interface informa explicitamente que não há solver nem ótimo comprovado;
- resultado declara condição de viabilidade e sobra ou déficit de orçamento;
- obrigatório sem score positivo e conjunto sem peso viável falham com causa;
- mensagens, guia e navegação adotam “Simulação Heurística de Verba”;
- suíte offline ampliada para 88 testes e regressão conectada aprovadas.

### 27 de julho de 2026 — Fase 2, sobre-exposição sem falsa saturação

- frequência acima do limite passa a ser nomeada como sobre-exposição;
- saturação econômica fica explicitamente indisponível sem curva calibrada;
- o comparador deixa de interpretar métrica ausente como zero;
- snapshots antigos com `risco_saturacao` continuam legíveis;
- interface, guia e modelo cross-media adotam a mesma semântica.

### 27 de julho de 2026 — Fase 2, plano, forecast e exportação reconciliados

- totais do forecast passam a priorizar o consolidado auditável do plano;
- alcance líquido deixa de ser substituído pela soma dos alcances dos meios;
- CTR, CPM, CPC e CPA consolidados passam a usar razões sobre os totais;
- forecast legado não soma resultados parciais quando algum item está ausente;
- dashboard usa o mesmo contrato agregado da página de forecast;
- exportação ganha aba estruturada para resultados consolidados.

### 27 de julho de 2026 — Fase 2, portabilidade seletiva concluída

- a branch `refactor/sdm-finalizacao` foi auditada sem merge entre históricos;
- forecast tolerante a coleção nula de métricas foi reimplementado;
- validações, compatibilidade e testes já cobertos foram identificados;
- ranking e planejador antigos foram rejeitados por conflitarem com os
  contratos metodológicos atuais;
- payloads multiusuário e workspace foram encaminhados às fases futuras;
- decisões detalhadas ficam em `AUDITORIA_BRANCH_REFATORACAO.md`;
- Fase 2 encerrada com 92 testes offline aprovados e 3 integrações opcionais
  desabilitadas por padrão.

### 27 de julho de 2026 — Fase 3, solver linear inicial

- criado solver contínuo com HiGHS para maximizar aderência ponderada pela verba;
- orçamento, reserva, elegibilidade, obrigatoriedade, pisos e tetos por item,
  ambiente e plataforma integram o modelo;
- inviabilidade não produz distribuição fabricada;
- resultado informa método, versão, função objetivo, status, iterações e
  restrições ativas;
- ótimo só é declarado quando o solver retorna solução ótima;
- heurística proporcional permanece disponível como benchmark explícito;
- quantidades discretas e curvas de resposta permanecem limitações declaradas.

### 27 de julho de 2026 — Fase 3, funções objetivo iniciais

- solver permite selecionar aderência estratégica ou conversões projetadas;
- aderência usa o score estratégico versionado do plano;
- conversões usam a razão entre conversões e investimento de referência;
- coeficiente ausente, investimento não positivo ou objetivo sem ganho positivo
  bloqueiam a solução;
- cada item preserva coeficiente e origem usados na função;
- conversões são identificadas como extrapolação linear, sem alegar resposta
  marginal ou saturação calibrada.

### 27 de julho de 2026 — Fase 3, frequência efetiva por faixas

- planejamento aceita alcances `1+`, `2+`, `3+` e `4+` opcionais por meio;
- faixas N+ devem ser monotônicas e o alcance `1+` reconcilia com o alcance;
- subexposição, faixa eficiente e sobre-exposição são calculadas no universo e
  entre as pessoas alcançadas;
- ausência dos limiares necessários mantém o resultado indisponível;
- distribuição integra item, snapshot, consolidado auditável e exportação;
- saturação econômica continua indisponível sem curva de resposta calibrada.

### 27 de julho de 2026 — Fase 3, cenários e sensibilidade

- cenários antigos baseados em multiplicadores de papel deixam de orientar a
  interface principal;
- plano e investimento ficam fixos durante a análise;
- conservador, base e otimista variam impressões, CTR e taxa de conversão por
  premissas explícitas e editáveis;
- a cadeia de dependência recalcula cliques e conversões sem defaults;
- lacunas bloqueiam somente os resultados dependentes;
- resultados são identificados como condicionais, não intervalos estatísticos;
- revisão acadêmica e mercadológica fica registrada em
  `REVISAO_REFERENCIAS_FASE_3.md`.

### 27 de julho de 2026 — Fase 3, realizado e diagnóstico de desempenho

- realizado passa a ser estado próprio, sem sobrescrever plano ou forecast;
- fonte, período, universo, público e praça acompanham os valores observados;
- datas do planejamento passam a integrar o objeto e o snapshot restaurável;
- comparação cobre investimento, impressões, cliques e conversões por meio;
- desvios só são calculados quando período e contexto são comparáveis;
- período parcial ou contexto divergente permanece sem percentual de desvio;
- comparação pode ser salva como artefato auditável do projeto;
- diferenças são descritivas e não alegam causalidade, incrementalidade ou
  atribuição.

### 27 de julho de 2026 — Encerramento da Fase 3

- solver, funções objetivo, frequência efetiva, sensibilidade e realizado
  integram um pipeline auditável;
- revisão acadêmica e mercadológica foi incorporada às decisões e limitações;
- suíte offline encerrada com 104 testes aprovados e 3 integrações opcionais
  desabilitadas por padrão;
- próxima etapa condicionada ao plano de migração multiusuário, backup e testes
  de isolamento por RLS.

### 27 de julho de 2026 — Fase 4, fundação de propriedade e RLS

- modelo adota perfis, espaços e membros com proprietário, editor e leitor;
- cadeia projeto → briefing → planejamento → artefato recebe `espaco_id`;
- dados atuais são encaminhados para um espaço legado sem exposição automática;
- versões herdam autorização pela relação com o planejamento;
- políticas separam leitura de membro e escrita de proprietário/editor;
- autopromoção de papel global e vínculos cruzados entre espaços são bloqueados;
- migration idempotente e isolamento entre três identidades validados localmente;
- repositories e serviços comuns passam a resolver um cliente por requisição,
  usando JWT quando a sessão o fornecer;
- o `service_role` permanece como fallback transitório, sem ser injetado
  diretamente no fluxo comum;
- a RPC legada de cópia fica reservada ao `service_role` até ganhar validação
  contextual de espaço;
- login, renovação, logout e troca obrigatória da senha temporária foram
  preparados sob `PLANOS_AUTH_ENABLED`, desligado por padrão;
- cada login usa cliente isolado, em conformidade com Supabase Auth e gestão
  de sessões recomendada pela OWASP;
- o espaço ativo passa a ser revalidado contra a membresia, propagado nas
  inclusões centrais e aplicado como filtro adicional às leituras;
- troca de espaço, logout e expiração removem contextos privados anteriores;
- cópias centrais usam RPC contextual que valida origem, espaço e permissão;
- cópias de entidades ainda sem escopo permanecem bloqueadas;
- aplicação remota permanece bloqueada até novo backup e teste controlado de
  autenticação.

### 27 de julho de 2026 — Backup pré-migration multiusuário

- esquema, dados completos, dados públicos e papéis foram exportados;
- checksums SHA-256 foram registrados em manifesto próprio;
- esquema e dados públicos foram restaurados em PostgreSQL isolado;
- 89 tabelas públicas, 106 chaves estrangeiras e seis contagens materiais
  foram conferidas;
- conjunto durável foi verificado no Google Drive como não compartilhado;
- a migration remota não foi aplicada durante o procedimento.

### 27 de julho de 2026 — Aplicação da fundação multiusuário

- migration `20260727030000` aplicada após backup restaurável;
- histórico local e remoto ficou sincronizado;
- regressão e integrações conectadas foram aprovadas;
- todos os registros centrais receberam espaço, sem valores nulos;
- espaço legado permanece sem membros e autenticação permanece desativada;
- próximo gate: criar contas controladas, atribuir membresias e repetir os
  testes de isolamento usando sessões Auth reais.

### 27 de julho de 2026 — Encerramento da Fase 4

- duas contas confirmadas foram criadas sem persistência de senha legível;
- papéis de administrador e usuário comum foram atribuídos;
- dois espaços e suas membresias foram validados com JWTs reais;
- isolamento cruzado de leitura e escrita foi confirmado;
- escrita legítima no espaço próprio foi confirmada;
- dados temporários do teste foram removidos;
- autenticação de produção permanece desligada até a área administrativa
  fornecer redefinição segura e ativação gradual;
- próxima etapa: Fase 5, administração e colaboração.

### 27 de julho de 2026 — Fase 5, fundação administrativa

- referências oficiais do Supabase e recomendações OWASP foram revistas;
- administração exige JWT válido e perfil global de administrador ativo antes
  de acessar o cliente `service_role`;
- criação de conta gera senha temporária forte, confirmada e exibida somente
  como retorno imediato;
- bloqueio, reativação e redefinição de senha foram encapsulados;
- autobloqueio administrativo foi impedido;
- senha redefinida nunca integra os detalhes de auditoria;
- migration de logs administrativos foi preparada com leitura por
  administrador e escrita exclusiva por `service_role`;
- migration validada duas vezes localmente e políticas confirmadas com
  administrador e usuário comum;
- área administrativa preparada para listar e criar contas, bloquear,
  reativar e redefinir senha temporária;
- acesso direto à página revalida o JWT e o papel no servidor;
- ações sensíveis exigem confirmação e senhas são exibidas uma única vez;
- próxima etapa: novo backup, aplicação remota da auditoria e teste controlado
  da área administrativa antes de ativar o login.

### 27 de julho de 2026 — Backup pré-auditoria administrativa

- esquema, dados completos, dados públicos, papéis e manifesto SHA-256 foram
  exportados antes da migration `20260727040000`;
- os cinco artefatos foram copiados ao Google Drive privado e conferidos como
  não compartilhados;
- a restauração incluiu as identidades reais do Supabase Auth, além dos dados
  públicos;
- a migration multiusuário idempotente recompôs o gatilho entre `auth` e
  `public`, que não pertence ao dump do schema público;
- origem e restauração coincidiram nas contagens materiais, incluindo usuários,
  perfis, espaços, projetos, planejamentos, versões e métricas;
- a migration de auditoria e seu teste de RLS passaram no banco restaurado;
- próximo gate: aplicar a migration remota, executar regressão conectada e
  testar a área administrativa sem habilitar ainda o login geral.

### 27 de julho de 2026 — Aplicação da auditoria administrativa

- migration `20260727040000` aplicada após o backup restaurável;
- histórico local e remoto ficou sincronizado;
- tabela `logs_auditoria` confirmada pela API administrativa, inicialmente sem
  registros;
- regressão funcional e três integrações conectadas foram aprovadas;
- acesso público ao banco permanece bloqueado;
- autenticação geral permanece desativada até o teste controlado da área
  administrativa com uma sessão Auth real.

### 27 de julho de 2026 — Validação controlada da administração

- a conta administradora foi autenticada com JWT real e listou as duas contas;
- tentativa de autobloqueio foi rejeitada antes de qualquer alteração;
- a conta comum foi bloqueada e reativada, retornando ao estado ativo;
- redefinição produziu senha temporária somente em memória e preservou a
  exigência de troca no primeiro acesso;
- a mesma conta comum foi recusada ao tentar construir o serviço
  administrativo;
- bloqueio, reativação e redefinição foram registrados na auditoria sem
  senhas nos detalhes;
- as senhas aleatórias do ensaio não foram exibidas nem persistidas; o primeiro
  acesso deverá começar por nova redefinição administrativa controlada;
- login geral permanece desligado; próxima entrega da Fase 5 é o
  compartilhamento de projetos com proprietário, editor e leitor.
