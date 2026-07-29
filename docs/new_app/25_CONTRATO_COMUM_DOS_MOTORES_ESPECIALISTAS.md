# Contrato Comum dos Motores Especialistas

**Documento:** `25_CONTRATO_COMUM_DOS_MOTORES_ESPECIALISTAS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado para especificação da versão 1.0  
**Natureza:** Contrato normativo compartilhado  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

Este documento estabelece o contrato comum dos três motores especialistas do MediAd Planner antes da especificação individual de cada responsabilidade:

1. Motor de Tradução Estratégica;
2. Motor de Decisão de Arquitetura e Cenários;
3. Motor de Simulação Técnica e Econômica.

O contrato define como os motores recebem comandos, consomem configurações e bibliotecas, selecionam problemas e procedimentos, produzem resultados, registram confiança e explicações e declaram dependências de reexecução.

Ele não cria novos campos de negócio nem substitui os documentos 01 a 18B. Os motores utilizam os campos configuráveis, objetos e relações já definidos, por referência ou snapshot versionado.

---

## 2. Princípios comuns

Todos os motores devem obedecer aos seguintes princípios:

1. consumir somente dados pertinentes ao comando e ao modo de execução;
2. não recadastrar campos já definidos nos documentos funcionais ou bibliotecas;
3. não manter cópias próprias de fórmulas, regras, problemas ou taxonomias;
4. consultar conhecimentos da Biblioteca 17 e problemas da Biblioteca 18 por versão;
5. distinguir dados informados, herdados, calculados, estimados e inferidos;
6. permitir resultado parcial quando a ausência de dados não impedir a decisão solicitada;
7. nunca transformar ausência em zero;
8. preservar intervenções humanas, valores originais e justificativas;
9. produzir saída explicável, reproduzível e rastreável;
10. declarar o que deve ser invalidado quando houver alteração das entradas.

---

## 3. Estrutura geral da execução

Toda execução seguirá, conceitualmente, a cadeia:

```text
comando
→ resolução do contexto
→ identificação do problema
→ seleção das entradas necessárias
→ validação local
→ seleção dos conhecimentos e procedimentos
→ execução
→ composição da saída
→ registro de confiança e rastreabilidade
→ declaração de dependências
```

A cadeia não obriga uma implementação monolítica. Cada etapa poderá ser atendida por procedimentos pequenos, serviços compartilhados e repositórios especializados.

---

## 4. Envelope comum de comando

Todo motor receberá um comando estruturado com, no mínimo:

```text
id_comando
motor_destino
modo_execucao
nivel_execucao
id_campanha
id_snapshot_campanha
id_usuario
perfil_de_acesso
solicitado_em
origem_do_comando
objetivo_da_execucao
referencias_de_entrada
parametros_locais
limites_de_execucao
```

### 4.1 Identidade e contexto

- `id_comando`: identificador único da solicitação;
- `motor_destino`: motor responsável pela execução;
- `modo_execucao`: operação específica admitida pelo motor;
- `nivel_execucao`: `PREVIA`, `PADRAO` ou `DETALHADA`;
- `id_campanha`: unidade de trabalho;
- `id_snapshot_campanha`: fotografia versionada das configurações utilizadas;
- `id_usuario`: autor da solicitação;
- `perfil_de_acesso`: permissões aplicáveis à operação.

### 4.2 Intenção da solicitação

- `origem_do_comando`: interface, serviço de aplicação, reexecução, cálculo isolado ou chamada de outro motor;
- `objetivo_da_execucao`: resultado que precisa ser produzido;
- `referencias_de_entrada`: contratos, cenários, componentes, resultados ou objetos reutilizados;
- `parametros_locais`: ajustes autorizados somente para a execução atual;
- `limites_de_execucao`: tempo, número de candidatos, iterações ou profundidade permitidos.

O comando não deve transportar indiscriminadamente todo o snapshot. Ele referencia o contexto e permite que o motor resolva apenas as entradas necessárias.

---

## 5. Resolução seletiva do contexto

Antes da execução, o motor deverá construir um contexto resolvido contendo somente os dados aplicáveis.

```text
contexto_resolvido
├── dados_obrigatorios
├── dados_condicionais_acionados
├── dados_opcionais_disponiveis
├── valores_herdados
├── padroes_configuraveis_aplicados
├── dados_ausentes
└── dados_nao_pertinentes
```

Cada entrada deverá ser classificada como:

```text
OBRIGATORIA
CONDICIONAL
OPCIONAL
HERDADA
PADRAO_CONFIGURAVEL
NAO_PERTINENTE
```

A classificação depende do motor, do modo e do problema em execução. Um campo pode ser obrigatório em um modo e não pertinente em outro.

---

## 6. Precedência dos valores

Quando houver mais de uma fonte possível para o mesmo parâmetro, será aplicada a seguinte ordem de precedência:

```text
ajuste local autorizado da execução
→ configuração específica do cenário ou componente
→ snapshot da campanha
→ configuração institucional ou da biblioteca
→ padrão versionado do objeto de conhecimento
```

A aplicação de um valor posterior na ordem não pode apagar os anteriores. A execução deve registrar:

- valor efetivamente utilizado;
- origem do valor;
- valor anterior, quando substituído;
- autorização da substituição;
- escopo da substituição;
- justificativa, quando exigida.

---

## 7. Identificação dos problemas técnicos

Cada motor identifica somente problemas pertencentes à sua responsabilidade.

O vínculo mínimo será:

```text
comando
→ problema_tecnico
→ gatilhos_confirmados
→ entradas_requeridas
→ procedimentos_elegiveis
```

O registro do problema deve conter:

```text
codigo_do_problema
versao
estado_de_identificacao
gatilhos_observados
evidencias
restricoes
subproblemas_acionados
```

Estados iniciais:

```text
IDENTIFICADO
IDENTIFICADO_COM_RESSALVA
NAO_IDENTIFICADO
INDETERMINADO
```

Os motores não criarão catálogos paralelos. Códigos, gatilhos, restrições e relações permanecem na Biblioteca 18.

---

## 8. Seleção dos conhecimentos e procedimentos

Após identificar o problema, o motor consultará objetos da Biblioteca 17 e procedimentos compatíveis.

A seleção deve considerar:

- domínio técnico;
- tipologia de mídia;
- universo e público;
- praça e período;
- dados disponíveis;
- unidade de observação;
- estado de deduplicação;
- estado de equivalência;
- condições de validade;
- confiança metodológica;
- versão.

Cada procedimento selecionado deverá registrar:

```text
codigo_do_procedimento
objeto_de_conhecimento
versao_do_objeto
motivo_da_selecao
entradas_consumidas
pre_condicoes
restricoes
alternativas_rejeitadas
```

O motor coordena a seleção e execução, mas fórmulas e regras permanecem fora de sua estrutura decisória fixa.

---

## 9. Validação local

Cada motor valida somente o que precisa consumir ou produzir. Não haverá Motor de Validação autônomo.

O resultado de cada validação será:

```text
VALIDO
VALIDO_COM_ALERTA
INVALIDO
INDETERMINADO
```

Uma validação deve registrar:

```text
codigo
objeto_validado
resultado
severidade
mensagem
impacto_na_execucao
acao_recomendada
```

Severidades iniciais:

```text
INFORMATIVA
ATENCAO
RESTRITIVA
BLOQUEANTE
```

Uma inconsistência somente será bloqueante quando impedir a saída solicitada. Dados insuficientes para uma análise avançada não devem bloquear uma resposta preliminar possível.

---

## 10. Níveis comuns de execução

### 10.1 PREVIA

Utiliza o conjunto mínimo de dados e procedimentos para:

- verificar viabilidade;
- filtrar alternativas;
- estimar ordem de grandeza;
- identificar lacunas relevantes;
- evitar cálculos caros desnecessários.

Resultados prévios devem ser claramente classificados como estimados ou provisórios.

### 10.2 PADRAO

Executa os procedimentos necessários para sustentar a decisão corrente com qualidade adequada à jornada principal.

É o nível padrão da interface.

### 10.3 DETALHADA

Executa análises adicionais solicitadas pelo usuário ou exigidas por condição específica, podendo incluir:

- variantes metodológicas;
- distribuição ampliada de frequência;
- cenários adicionais;
- análises de sensibilidade;
- memória técnica completa;
- comparações secundárias.

O nível detalhado não deve ser acionado automaticamente apenas porque os dados estão disponíveis.

---

## 11. Estados comuns da execução

```text
RECEBIDA
EM_RESOLUCAO_DE_CONTEXTO
AGUARDANDO_DADO_ESSENCIAL
EM_EXECUCAO
CONCLUIDA
CONCLUIDA_COM_RESSALVAS
PARCIAL
NAO_EXECUTAVEL
CANCELADA
FALHA_TECNICA
```

### 11.1 Resultado parcial

`PARCIAL` significa que o motor produziu uma resposta utilizável, mas não executou todas as análises desejadas por falta de dados, restrição metodológica ou limite de execução.

### 11.2 Não executável

`NAO_EXECUTAVEL` será utilizado quando não for possível produzir a saída principal sem violar regras de validade ou fabricar informação.

### 11.3 Falha técnica

`FALHA_TECNICA` será reservada a erro de infraestrutura, integração ou implementação. Não deve ser usada para representar briefing incompleto ou ausência legítima de dados.

---

## 12. Envelope comum de saída

Todo motor retornará uma saída com estrutura comum:

```text
id_execucao
id_comando
motor
modo_execucao
nivel_execucao
estado_execucao
resultado_principal
resultados_secundarios
validacoes
alertas
restricoes
confianca
explicacao
rastreabilidade
dependencias
reexecucao
produzido_em
versao_do_contrato
```

### 12.1 Resultado principal

Cada motor terá exatamente um tipo de resultado principal por modo. Resultados auxiliares deverão permanecer subordinados ao contrato dessa saída.

### 12.2 Resultados secundários

Podem conter métricas, alternativas, diagnósticos ou decomposições necessárias à interpretação, sem transformar cada resultado em novo motor ou novo fluxo.

---

## 13. Contrato mínimo de mensuração

Toda saída que contenha valor mensurável deverá declarar, conforme o documento 17F:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Esses metadados deverão ser herdados, calculados ou resolvidos automaticamente sempre que possível. Não constituem formulário obrigatório para o usuário.

Um resultado numérico sem esses metadados não poderá ser promovido a valor comparável ou consolidado quando eles forem necessários à interpretação.

---

## 14. Natureza dos valores

Valores consumidos ou produzidos devem possuir natureza explícita:

```text
INFORMADO
HERDADO
CALCULADO
ESTIMADO
INFERIDO
AJUSTADO_PELO_USUARIO
PADRAO_APLICADO
NAO_DISPONIVEL
NAO_APLICAVEL
INVALIDO
```

O sistema deverá preservar o valor bruto e o valor apresentado após arredondamento ou formatação.

---

## 15. Confiança

A saída deve separar, quando aplicável:

```text
confianca_metodologica
confianca_dos_dados
confianca_da_aplicacao
confianca_do_resultado
```

A confiança do resultado não será uma média automática obrigatória. Ela poderá ser uma classificação composta, desde que o método esteja versionado e explicado.

Estados iniciais:

```text
ALTA
MEDIA
BAIXA
INDETERMINADA
```

A baixa confiança não invalida automaticamente um resultado. Ela altera a forma de apresentação, comparação e recomendação.

---

## 16. Alertas e restrições

Alertas deverão ser deduplicados e priorizados por impacto.

Cada alerta conterá:

```text
codigo
severidade
titulo
mensagem
objeto_afetado
impacto
acao_possivel
origem
```

A interface deverá apresentar primeiro os alertas que alteram a decisão. Alertas meramente técnicos permanecerão na memória detalhada.

---

## 17. Explicabilidade

A explicação é parte obrigatória da saída de cada motor e não será reconstruída posteriormente por um motor separado.

A estrutura mínima será:

```text
conclusao_pratica
principais_razoes
restricoes_relevantes
alternativas_rejeitadas
trade_offs
conhecimentos_aplicados
memoria_tecnica
```

A apresentação será progressiva:

```text
resultado principal
→ justificativa resumida
→ alertas e trade-offs
→ memória técnica detalhada
```

Cada motor explica somente sua própria decisão ou cálculo.

---

## 18. Rastreabilidade

Toda execução deverá registrar:

- comando e usuário solicitante;
- snapshot e versões consumidas;
- entradas efetivamente utilizadas;
- valores padrão e ajustes locais;
- problemas identificados;
- conhecimentos e procedimentos selecionados;
- validações executadas;
- alternativas rejeitadas;
- resultados brutos e apresentados;
- confiança e alertas;
- duração e limites da execução;
- intervenções humanas.

A reprodução exige o mesmo conjunto de entradas, versões, parâmetros e limites. Resultados dependentes de fonte externa mutável devem preservar snapshot ou identificação da consulta.

---

## 19. Dependências e invalidação

Cada saída deverá publicar suas dependências de forma explícita:

```text
depende_de
produz_para
invalida_quando
recalcula_quando
preserva_quando
```

Tipos iniciais de dependência:

```text
ESTRATEGICA
DECISORIA
TECNICA
ECONOMICA
TEMPORAL
TERRITORIAL
MENSURACAO
INVENTARIO
GOVERNANCA
```

A camada de aplicação utilizará essas dependências para reexecução incremental. O motor declara a dependência; o orquestrador controla a sequência.

---

## 20. Contrato de reexecução

Toda saída deve informar uma política de reexecução:

```text
NENHUMA
RECALCULAR_PARCIALMENTE
REEXECUTAR_MODO
REEXECUTAR_MOTOR
INVALIDAR_DEPENDENTES
REQUERER_NOVA_DECISAO_HUMANA
```

Exemplos:

```text
mudança de preço
→ Motor de Simulação: RECALCULAR_PARCIALMENTE
→ Motor de Decisão: INVALIDAR_DEPENDENTES
→ Motor de Tradução: NENHUMA
```

```text
mudança de objetivo prioritário
→ Motor de Tradução: REEXECUTAR_MOTOR
→ demais resultados: INVALIDAR_DEPENDENTES
```

```text
mudança apenas de texto do plano
→ três motores: NENHUMA
```

---

## 21. Intervenção humana

O usuário poderá, conforme permissão:

- aceitar ou rejeitar uma recomendação;
- fixar ou bloquear componentes;
- escolher variante metodológica permitida;
- alterar parâmetro configurável;
- informar dado externo;
- substituir valor padrão;
- aprovar resultado com ressalva.

A intervenção deverá registrar:

```text
usuario
acao
objeto_afetado
valor_anterior
valor_novo
justificativa
escopo
executada_em
```

Nenhuma intervenção poderá apagar o resultado original ou ocultar alertas e restrições previamente emitidos.

---

## 22. Limites de processamento

Todo motor deverá respeitar limites definidos no comando ou em padrão configurável:

- tempo máximo;
- quantidade máxima de objetos carregados;
- número de alternativas ou cenários;
- número de iterações;
- profundidade de combinações;
- tolerância de ganho marginal;
- volume de memória técnica retornada.

Ao alcançar um limite, o motor deverá preferir saída parcial explicada a expansão silenciosa da execução.

---

## 23. Cache e reutilização

Resultados poderão ser reutilizados quando forem idênticos:

- comando funcional;
- entradas efetivamente consumidas;
- versões dos objetos;
- parâmetros aplicados;
- nível de execução;
- limites relevantes.

O cache não pode ser usado quando houver alteração em dependência declarada ou quando a fonte externa não possuir snapshot válido.

A reutilização deve ser transparente na rastreabilidade.

---

## 24. Erros de domínio e erros técnicos

### 24.1 Erros de domínio

Exemplos:

- dado obrigatório ausente;
- universo incompatível;
- cenário não comparável;
- fórmula não aplicável;
- inventário indisponível;
- limite orçamentário violado.

Devem produzir estados, alertas ou resultados insuficientes estruturados.

### 24.2 Erros técnicos

Exemplos:

- falha de banco;
- timeout inesperado;
- erro de integração;
- objeto versionado inacessível;
- exceção de implementação.

Devem produzir `FALHA_TECNICA`, preservar logs e não ser apresentados como conclusão metodológica.

---

## 25. Relação entre os três motores

```text
Motor de Tradução Estratégica
→ produz contrato_estrategico

Motor de Decisão de Arquitetura e Cenários
→ consome contrato_estrategico
→ produz arquitetura ou avaliacao_decisoria

Motor de Simulação Técnica e Econômica
→ consome arquitetura, cenário ou componente
→ produz resultado_de_simulacao

Motor de Decisão
↔ utiliza resultados de simulação para comparar e aperfeiçoar
```

As chamadas iterativas entre Decisão e Simulação são coordenadas pela camada de aplicação. Um motor não acessa estruturas internas do outro; utiliza contratos versionados.

---

## 26. Proibição de dependências indevidas

Não será permitido:

- Motor de Tradução consultar preços para classificar objetivos;
- Motor de Decisão implementar fórmulas próprias de alcance, GRP, CPM ou custos;
- Motor de Simulação redefinir objetivos, prioridades ou papéis estratégicos;
- qualquer motor modificar cadastro mestre sem ação explícita de serviço autorizado;
- qualquer motor aprovar plano em nome do usuário;
- qualquer motor gerar diretamente documentos finais como responsabilidade decisória.

---

## 27. Estrutura lógica mínima de implementação

O contrato conceitual poderá ser implementado com estruturas equivalentes a:

```text
comandos_motor
execucoes_motor
execucoes_contextos
execucoes_entradas
execucoes_problemas
execucoes_procedimentos
execucoes_validacoes
execucoes_resultados
execucoes_alertas
execucoes_explicacoes
execucoes_dependencias
execucoes_intervencoes
```

Essa lista não determina a modelagem definitiva do banco. Estruturas poderão ser agregadas quando não houver diferença relevante de ciclo de vida, consulta, versionamento ou integridade.

---

## 28. Critérios de aceite de um motor

Um motor somente será considerado especificado quando declarar:

1. responsabilidade decisória exclusiva;
2. modos de execução;
3. comandos aceitos;
4. entradas obrigatórias, condicionais, opcionais e herdadas;
5. documentos e bibliotecas consultados;
6. problemas técnicos acionáveis;
7. procedimentos selecionáveis;
8. saída principal de cada modo;
9. validações locais;
10. estados de confiança e alertas;
11. explicação e rastreabilidade;
12. dependências e política de reexecução;
13. limites de processamento;
14. casos de teste positivos, parciais, inválidos e de falha.

---

## 29. Próxima etapa

Com o contrato comum consolidado, os três motores deverão ser especificados separadamente, nesta ordem:

1. Motor de Tradução Estratégica;
2. Motor de Decisão de Arquitetura e Cenários;
3. Motor de Simulação Técnica e Econômica.

A ordem é documental. Na implementação, o Motor de Simulação poderá fornecer procedimentos técnicos necessários aos testes do Motor de Decisão, sem alterar as fronteiras definidas.

---

## 30. Princípio consolidado

> Os motores do MediAd Planner não são depósitos de campos, fórmulas ou regras. São fronteiras especializadas que recebem comandos, resolvem seletivamente o contexto, identificam problemas, aplicam conhecimentos versionados e produzem respostas explicáveis. O contrato comum garante interoperabilidade sem duplicação, execução progressiva sem peso desnecessário e reexecução incremental sem reconstruir o planejamento inteiro.
