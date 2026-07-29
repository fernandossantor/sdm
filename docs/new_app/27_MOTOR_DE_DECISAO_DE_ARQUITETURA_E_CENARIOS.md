# Motor de Decisão de Arquitetura e Cenários

**Documento:** `27_MOTOR_DE_DECISAO_DE_ARQUITETURA_E_CENARIOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado para implementação da versão 1.0  
**Natureza:** Especificação normativa de motor especialista  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

O Motor de Decisão de Arquitetura e Cenários transforma o contrato estratégico do planejamento em configurações de mídia coerentes, simuláveis, comparáveis e ajustáveis.

Sua pergunta central é:

```text
quais configurações de mídia são coerentes e preferíveis
para as prioridades, restrições e condições desta campanha?
```

Ele reúne em uma única fronteira decisória as responsabilidades de:

- gerar arquiteturas candidatas;
- qualificar e selecionar alternativas;
- atribuir papéis estratégicos;
- avaliar cenários simulados;
- comparar alternativas;
- sugerir ajustes;
- buscar configurações melhores dentro de limites explícitos.

Essas funções operam sobre o mesmo objeto decisório e, por isso, não constituem motores separados.

---

## 2. Resultado principal

O resultado principal depende do modo de execução, mas todos pertencem ao mesmo contrato de domínio:

```text
decisao_de_arquitetura_e_cenarios
```

Esse contrato pode conter:

- arquiteturas candidatas;
- cenários qualificados;
- comparação entre cenários;
- recomendação condicionada;
- proposta de ajuste;
- configuração candidata aperfeiçoada;
- alternativas rejeitadas e respectivas razões;
- restrições atendidas ou violadas;
- trade-offs;
- confiança;
- rastreabilidade;
- dependências de simulação e reexecução.

O motor não aprova o plano. A decisão final permanece humana.

---

## 3. Modos de execução

### 3.1 `GERAR_ARQUITETURAS`

Converte o contrato estratégico em poucas arquiteturas candidatas coerentes e aptas à simulação.

### 3.2 `AVALIAR_CENARIOS`

Avalia um ou mais cenários já simulados quanto a validade, aderência estratégica, entrega, eficiência, risco e confiança.

### 3.3 `COMPARAR_CENARIOS`

Compara cenários válidos ou válidos com ressalvas, identifica dominâncias, empates técnicos, incomparabilidades e compensações.

### 3.4 `SUGERIR_AJUSTES`

Propõe alterações localizadas em uma arquitetura ou cenário para corrigir restrições, melhorar aderência ou reduzir perdas.

### 3.5 `BUSCAR_MELHOR_CONFIGURACAO`

Executa busca controlada dentro de um espaço explicitamente delimitado de alternativas, sem prometer solução universal e sem ocultar trade-offs.

### 3.6 `RECALCULAR_DEPENDENCIAS_DECISORIAS`

Reavalia somente arquiteturas, comparações ou recomendações afetadas por alterações localizadas.

---

## 4. Limites da responsabilidade

O motor deve:

- interpretar o contrato estratégico produzido pelo Motor de Tradução;
- relacionar objetivos, resultados e KPIs a jornadas, necessidades, funções e pontos de contato;
- consultar inventários e condições disponíveis;
- filtrar alternativas incompatíveis, indisponíveis ou proibidas;
- qualificar alternativas por aderência contextual;
- atribuir papéis principal, complementar e apoio;
- construir poucas arquiteturas candidatas;
- solicitar simulações ao Motor de Simulação Técnica e Econômica;
- avaliar validade e comparabilidade dos resultados;
- comparar cenários por critérios explícitos;
- sugerir ajustes e configurações alternativas;
- preservar intervenção humana, valores originais e justificativas.

O motor não deve:

- redefinir objetivos estratégicos ou públicos prioritários;
- criar pesos ocultos;
- cadastrar inventários;
- inventar preços, descontos ou disponibilidades;
- implementar fórmulas próprias de alcance, frequência, GRP, CPM, CPA, ROAS ou outros indicadores;
- alterar coeficientes técnicos apenas para melhorar resultados;
- aprovar ou consolidar o plano;
- executar busca combinatória irrestrita;
- substituir a decisão do planejador.

---

## 5. Documentos e bibliotecas consumidos

### 5.1 Documentos funcionais

| Documento | Uso |
|---|---|
| 01 — Campanha | identidade, vigência, contexto e snapshot |
| 02 — Briefing | restrições, verba, período, praça e condições herdadas |
| 03 — Tradução Estratégica | contrato estratégico, pesos, prioridades, mínimos e tensões |
| 04 — Arquitetura de Mídia | estrutura principal de geração e qualificação |
| 05 — Simulações | cenários e resultados projetados recebidos do Motor de Simulação |
| 06 — Comparação de Cenários | critérios, comparabilidade, dominância e trade-offs |
| 07 — Otimização de Cenários | variáveis ajustáveis, protegidas, limites e objetivos de ajuste |
| 08 — Plano Consolidado | recebe a decisão aprovada, sem ser produzido pelo motor |
| 09 — Validação e aprovação | bloqueios de governança e estados humanos |
| 10 — Mapa de Veiculação | recebe linhas aprovadas, sem orientar o mérito decisório |
| 11 — Perfis e Permissões | autoriza executar, alterar, fixar ou aprovar |

### 5.2 Bibliotecas

| Biblioteca | Uso |
|---|---|
| 12 e 12A | contratos, versionamento, snapshots e localização das estruturas |
| 13 — Inventários | tipologias, produtos, ofertas, unidades, disponibilidade e condições |
| 14 — Públicos e Segmentos | aderência, cobertura, seletividade e território |
| 15 — Objetivos, Resultados e KPIs | critérios estratégicos e capacidades requeridas |
| 16 — Jornadas, Necessidades, Funções e Pontos de Contato | progressão da estratégia até categorias de mídia |
| 17 — Conhecimento Técnico | regras de elegibilidade, qualificação, comparação e otimização |
| 17F — Contrato Mínimo de Mensuração | comparabilidade e confiança dos resultados utilizados |
| 18 — Problemas Técnicos | problemas decisórios, gatilhos e procedimentos aplicáveis |
| 18A e 18B | validação de comparabilidade, mensuração e casos de teste |

O consumo é seletivo. Nenhum modo carrega todas essas fontes integralmente.

---

## 6. Entradas por modo

### 6.1 Entradas comuns

```text
id_campanha
id_snapshot_campanha
contrato_estrategico_do_planejamento
modo_execucao
nivel_execucao
perfil_de_acesso
parametros_locais_autorizados
limites_de_execucao
```

### 6.2 `GERAR_ARQUITETURAS`

Obrigatórias:

- objetivos de mídia priorizados;
- resultados pretendidos;
- públicos e praças prioritários;
- restrições rígidas;
- período;
- inventários ou tipologias consultáveis.

Condicionais:

- jornada e etapas;
- necessidades e funções;
- verba;
- capacidades analíticas;
- disponibilidade comercial;
- componentes obrigatórios ou proibidos.

Opcionais:

- benchmarks;
- afinidades observadas;
- histórico de campanha;
- preferências do planejador.

### 6.3 `AVALIAR_CENARIOS` e `COMPARAR_CENARIOS`

Obrigatórias:

- cenários simulados e versionados;
- contrato estratégico ou critérios explícitos de avaliação;
- metadados mínimos de mensuração;
- restrições aplicáveis.

Condicionais:

- métodos de normalização;
- benchmark;
- cenário-base;
- tolerância de empate;
- critérios de risco e robustez.

### 6.4 `SUGERIR_AJUSTES`

Obrigatórias:

- cenário de origem;
- diagnóstico ou problema a corrigir;
- variáveis ajustáveis;
- elementos protegidos;
- limites de alteração.

### 6.5 `BUSCAR_MELHOR_CONFIGURACAO`

Obrigatórias:

- espaço de alternativas delimitado;
- função ou conjunto de objetivos explícitos;
- restrições rígidas e flexíveis;
- limites de candidatos, iterações, tempo e ganho marginal;
- variáveis livres, ajustáveis, condicionadas, protegidas e obrigatórias.

---

## 7. Problemas técnicos acionáveis

O motor pode identificar, entre outros:

- ausência de arquitetura coerente com as prioridades;
- alternativa incompatível com ponto de contato, função ou público;
- inventário indisponível ou não simulável;
- arquitetura excessivamente dependente de um canal;
- público ou praça obrigatória sem atendimento;
- papel estratégico incoerente;
- redundância sem ganho justificável;
- cobertura insuficiente da jornada;
- excesso de alternativas equivalentes;
- cenário inválido por restrição;
- cenários incomparáveis;
- dominância de uma alternativa;
- empate técnico;
- conflito entre desempenho bruto e aderência estratégica;
- excesso de orçamento;
- saturação ou concentração evitável;
- baixa robustez;
- busca sem espaço decisório suficientemente delimitado.

Os códigos, gatilhos e relações devem permanecer na Biblioteca 18.

---

## 8. Processo de geração de arquiteturas

```text
contrato estratégico
→ objetivos e resultados prioritários
→ jornadas, etapas e necessidades aplicáveis
→ funções comunicacionais requeridas
→ pontos de contato candidatos
→ tipologias compatíveis
→ inventários consultáveis
→ filtros de elegibilidade
→ qualificação contextual
→ atribuição de papéis
→ composição controlada
→ arquiteturas candidatas
→ solicitação de simulação prévia
→ eliminação de inviáveis
→ apresentação de poucas alternativas
```

A seleção não deve começar diretamente pelo inventário.

---

## 9. Elegibilidade

Antes de pontuar, o motor deve eliminar ou separar alternativas que violem condições rígidas.

Critérios de elegibilidade podem incluir:

- compatibilidade tipológica;
- aderência à função comunicacional;
- atendimento da etapa e necessidade;
- cobertura territorial;
- disponibilidade temporal;
- público compatível;
- modelo de compra permitido;
- formato permitido;
- dados suficientes para simulação;
- capacidade de mensuração;
- orçamento e lote comercial;
- restrições legais, institucionais ou contratuais.

Estados:

```text
SUGERIDO
ELEGIVEL
SELECIONADO_PARA_SIMULACAO
REJEITADO
INDISPONIVEL
SUBSTITUIDO
```

Uma alternativa excludente não deve permanecer apenas com peso negativo.

---

## 10. Qualificação contextual

Cada alternativa elegível poderá ser qualificada por dimensões como:

- aderência ao objetivo e resultado;
- compatibilidade com o KPI prioritário;
- aderência à jornada, etapa, necessidade e função;
- adequação ao público e território;
- cobertura e seletividade potenciais;
- adequação editorial e contextual;
- capacidade analítica e mensurabilidade;
- flexibilidade operacional e comercial;
- custo e disponibilidade;
- risco de saturação;
- confiança das evidências.

A fórmula, normalização e coeficientes pertencem à Biblioteca 17.

O motor deve preservar:

```text
valor calculado
valor ajustado pelo planejador
valor efetivo
contribuições por dimensão
penalizações
restrições
versão metodológica
justificativa
```

Afinidade observada e aderência estimada não podem ser tratadas como sinônimos.

---

## 11. Papéis estratégicos

Papéis admitidos:

```text
PRINCIPAL
COMPLEMENTAR
APOIO
```

O papel é contextual e pode variar por:

- objetivo;
- público;
- praça;
- etapa;
- necessidade;
- função;
- período;
- cenário.

O motor não deve gravar o papel como propriedade permanente do meio.

A atribuição deve considerar:

- centralidade estratégica;
- contribuição específica;
- capacidade de sustentação;
- complementaridade;
- dependência;
- custo;
- mensurabilidade;
- risco.

---

## 12. Composição controlada das arquiteturas

O motor deve evitar tanto uma única solução precoce quanto proliferação de combinações.

Cada arquitetura candidata deverá declarar:

- componentes obrigatórios;
- componentes selecionados;
- componentes alternativos;
- componentes rejeitados;
- papéis;
- pontos de contato atendidos;
- funções atendidas;
- públicos e praças atendidos;
- hipóteses de cronologia, overlap e saturação;
- variáveis fixas e ajustáveis;
- critérios de diferenciação em relação às demais candidatas.

As candidatas devem representar diferenças decisórias reais, não variações cosméticas.

---

## 13. Relação com o Motor de Simulação

O Motor de Decisão não calcula internamente os resultados técnicos.

Fluxo:

```text
Motor de Decisão
→ envia configuração e resultados requeridos
→ Motor de Simulação calcula
→ devolve resultado versionado
→ Motor de Decisão avalia
```

A solicitação de simulação deve informar somente o necessário:

- cenário ou componentes;
- indicadores requeridos;
- nível de execução;
- hipóteses autorizadas;
- parâmetros locais;
- limites de processamento.

O Motor de Decisão não deve pedir análise detalhada para todos os candidatos. A sequência preferencial é:

```text
filtragem sem simulação
→ simulação PREVIA
→ eliminação de inviáveis ou dominados
→ simulação PADRAO dos finalistas
→ simulação DETALHADA somente quando solicitada
```

---

## 14. Avaliação dos cenários

A avaliação opera em três camadas.

### 14.1 Validade

Verifica se o cenário pode ser considerado:

- orçamento;
- disponibilidade;
- públicos e praças obrigatórios;
- mínimos e máximos;
- consistência da mensuração;
- restrições legais ou institucionais;
- dados essenciais.

Estados:

```text
VALIDO
VALIDO_COM_RESSALVAS
INVALIDO
```

### 14.2 Desempenho

Consome resultados do Motor de Simulação, preservando métricas nativas, equivalentes, unidades, universos e confiança.

### 14.3 Aderência estratégica

Avalia se o cenário entrega aquilo que o contrato estratégico considera prioritário.

Um cenário pode apresentar desempenho bruto alto e aderência estratégica baixa.

---

## 15. Comparabilidade

Cenários não devem ser classificados apenas porque possuem números.

O motor deve verificar, conforme o caso:

- universo;
- público;
- praça;
- período;
- moeda;
- base financeira;
- definição de conversão;
- fórmula de ROAS;
- unidade de referência;
- deduplicação;
- equivalência;
- modelo de atribuição;
- versão metodológica;
- confiança.

Estados de comparabilidade:

```text
COMPARAVEL
COMPARAVEL_COM_NORMALIZACAO
COMPARAVEL_PARCIALMENTE
INCOMPARAVEL
```

Diante de incompatibilidade, o motor deve normalizar, segmentar ou declarar incomparabilidade. Não deve produzir ranking artificial.

---

## 16. Critérios, normalização e pesos

Os critérios podem ser organizados em famílias:

- aderência estratégica;
- entrega de mídia;
- eficiência;
- performance;
- qualidade arquitetônica;
- risco e confiança.

Cada critério deve declarar:

```text
valor original
unidade
direcao desejada
meta ou faixa ideal
metodo de normalizacao
valor normalizado
peso
confiança
```

Direções admitidas:

```text
MAIOR_MELHOR
MENOR_MELHOR
FAIXA_IDEAL
CONDICAO_BINARIA
```

Os pesos devem vir prioritariamente do contrato estratégico. Ajustes locais exigem autorização e registro.

---

## 17. Dominância, empate e trade-offs

### 17.1 Dominância

Uma alternativa domina outra quando é igual ou superior nos critérios relevantes e superior em pelo menos um, sem violar restrições adicionais.

### 17.2 Empate técnico

Diferenças dentro da tolerância configurada não devem ser apresentadas como superioridade substantiva.

### 17.3 Trade-offs

Toda recomendação deve declarar ganhos e perdas, por exemplo:

```text
maior alcance
↔ menor frequência

menor custo
↔ menor confiança

maior conversão estimada
↔ maior dependência de canal
```

Uma pontuação geral nunca deve ocultar essas diferenças.

---

## 18. Sugestão de ajustes

O modo `SUGERIR_AJUSTES` deve partir de um problema explícito.

Fluxo:

```text
cenário de origem
→ diagnóstico
→ variáveis ajustáveis
→ elementos protegidos
→ poucas alterações plausíveis
→ simulação incremental
→ comparação com origem
→ ganhos, perdas e riscos
→ proposta de ajuste
```

Podem ser ajustados, quando autorizados:

- distribuição de verba;
- inventários;
- quantidades;
- papéis;
- praça;
- público;
- cronograma;
- flight;
- continuidade;
- concentração;
- composição de canais.

Não podem ser alterados silenciosamente:

- objetivos estratégicos;
- públicos ou praças obrigatórios;
- restrições legais;
- inventários já contratados;
- fórmulas;
- preços inexistentes;
- definições de conversão;
- parâmetros protegidos.

---

## 19. Busca por melhor configuração

`BUSCAR_MELHOR_CONFIGURACAO` é um modo avançado e não deve ser acionado automaticamente.

A busca deverá operar sobre:

```text
espaco delimitado
+ objetivos explicitos
+ restricoes
+ variaveis autorizadas
+ limites de execucao
```

Controles obrigatórios:

- máximo de candidatos iniciais;
- máximo de candidatos por rodada;
- máximo de simulações simultâneas;
- máximo de iterações;
- profundidade máxima de alteração;
- tempo máximo;
- tolerância de ganho marginal;
- eliminação precoce de inviáveis;
- eliminação de dominados;
- preservação de diversidade entre finalistas.

Critérios de parada:

- limite atingido;
- ausência de ganho relevante;
- convergência;
- falta de novos candidatos válidos;
- restrição de tempo;
- cancelamento humano.

A saída preferencial é um pequeno conjunto de finalistas eficientes, não uma suposta solução universal.

---

## 20. Níveis de execução

### 20.1 `PREVIA`

- aplica filtros rígidos;
- qualifica dimensões essenciais;
- gera poucos candidatos;
- solicita simulações aproximadas;
- elimina inviáveis.

### 20.2 `PADRAO`

- produz arquiteturas justificadas;
- compara cenários finalistas;
- aplica pesos, normalização e trade-offs;
- oferece recomendação condicionada.

### 20.3 `DETALHADA`

- amplia análise de sensibilidade;
- examina robustez;
- explora variantes metodológicas;
- executa busca controlada adicional;
- produz memória decisória completa.

O nível detalhado não é padrão.

---

## 21. Confiança

A confiança deve considerar:

- completude do contrato estratégico;
- qualidade dos inventários;
- atualidade de preços e disponibilidade;
- qualidade dos dados de público;
- validade da mensuração;
- confiança das equivalências;
- dependência de estimativas ou proxies;
- sensibilidade das conclusões;
- estabilidade da recomendação diante de pequenas mudanças.

Estados iniciais:

```text
ALTA
MEDIA
BAIXA
INDETERMINADA
```

Uma recomendação com baixa confiança pode ser apresentada, desde que não seja tratada como conclusão definitiva.

---

## 22. Explicabilidade

Cada decisão deve permitir reconstruir:

```text
contrato estratégico
→ jornada, necessidade e função
→ ponto de contato
→ tipologia e inventário
→ filtros de elegibilidade
→ qualificações
→ papel estratégico
→ arquitetura
→ simulação utilizada
→ avaliação
→ recomendação
```

A explicação deve apresentar, em camadas:

1. diferença prática;
2. razões principais;
3. restrições e trade-offs;
4. alternativas rejeitadas;
5. memória técnica.

---

## 23. Intervenção humana

O planejador pode, conforme permissão:

- fixar componentes;
- proibir alternativas;
- alterar papel;
- ajustar peso local;
- modificar limite;
- aceitar ou rejeitar recomendação;
- selecionar cenário não recomendado;
- interromper busca;
- solicitar nova simulação.

Toda intervenção deve registrar:

- valor original;
- valor alterado;
- autor;
- data;
- justificativa, quando exigida;
- escopo;
- dependências invalidadas.

O motor não deve apagar a recomendação original.

---

## 24. Saída por modo

### 24.1 `GERAR_ARQUITETURAS`

```text
arquiteturas_candidatas
```

### 24.2 `AVALIAR_CENARIOS`

```text
avaliacao_de_cenarios
```

### 24.3 `COMPARAR_CENARIOS`

```text
analise_comparativa_de_cenarios
```

### 24.4 `SUGERIR_AJUSTES`

```text
proposta_de_ajuste
```

### 24.5 `BUSCAR_MELHOR_CONFIGURACAO`

```text
conjunto_de_configuracoes_finalistas
```

Todas as saídas devem obedecer ao envelope comum do documento 25.

---

## 25. Dependências e reexecução

| Alteração | Efeito |
|---|---|
| objetivo, público ou prioridade | invalidar arquiteturas e avaliações dependentes |
| jornada, necessidade ou função | refazer qualificações relacionadas |
| inventário ou disponibilidade | reavaliar elegibilidade e cenários afetados |
| papel estratégico | reavaliar arquitetura e simulação correspondente |
| quantidade, preço ou cronograma | preservar estrutura quando possível; solicitar nova simulação |
| parâmetro de overlap ou saturação | preservar contrato estratégico; reavaliar após simulação |
| critério, peso ou tolerância de comparação | preservar simulações; refazer avaliação |
| componente protegido ou obrigatório | refazer somente espaço decisório afetado |
| texto ou formatação do plano | não executar o motor |

---

## 26. Cache e reutilização

Podem ser reutilizados quando as dependências permanecerem válidas:

- qualificação público–inventário;
- qualificação indicador–inventário;
- elegibilidade;
- aderência de ponto de contato;
- simulações de componentes inalterados;
- normalizações estáveis;
- comparações parciais;
- diagnósticos anteriores.

A chave de reutilização deve considerar versões de:

- snapshot;
- contrato estratégico;
- inventários e ofertas;
- conhecimentos;
- problemas;
- simulações;
- parâmetros locais.

---

## 27. Critérios de aceite

O motor estará especificado corretamente quando:

1. gerar arquiteturas sem começar diretamente por meios;
2. consumir o contrato estratégico sem redefini-lo;
3. consultar inventários e bibliotecas seletivamente;
4. separar elegibilidade de pontuação;
5. atribuir papéis contextuais;
6. solicitar cálculos ao Motor de Simulação, sem duplicá-los;
7. impedir comparação artificial de cenários incompatíveis;
8. preservar métricas originais e normalizadas;
9. declarar dominâncias, empates e trade-offs;
10. limitar busca, candidatos e iterações;
11. permitir intervenção humana rastreável;
12. recalcular apenas dependências afetadas;
13. produzir poucas alternativas relevantes;
14. explicar por que cada alternativa foi aceita, rejeitada ou preferida.

---

## 28. Casos mínimos de teste

### Caso 1 — Geração a partir de contrato completo

Deve gerar poucas arquiteturas distintas, coerentes e simuláveis.

### Caso 2 — Contrato com meio obrigatório

Deve preservar o meio obrigatório sem atribuir automaticamente papel principal.

### Caso 3 — Inventário indisponível

Deve rejeitar ou substituir o inventário sem refazer a tradução estratégica.

### Caso 4 — Dois cenários incomparáveis

Deve segmentar ou declarar incomparabilidade, sem ranking geral.

### Caso 5 — Cenário de maior entrega, mas baixa aderência

Deve explicitar o conflito e não recomendar apenas pelo maior número.

### Caso 6 — Excesso de orçamento

Deve sugerir poucas reduções plausíveis e solicitar simulação incremental.

### Caso 7 — Busca com espaço excessivo

Deve exigir delimitação ou aplicar limites, nunca executar combinação irrestrita.

### Caso 8 — Alteração manual de papel

Deve preservar recomendação original, registrar intervenção e invalidar apenas dependências afetadas.

### Caso 9 — Empate técnico

Deve evitar superioridade artificial dentro da tolerância configurada.

### Caso 10 — Ausência de deduplicação confiável

Deve reduzir confiança e impedir comparação indevida de alcance líquido combinado.

---

## 29. Princípio consolidado

> O Motor de Decisão de Arquitetura e Cenários converte prioridades estratégicas em poucas configurações coerentes, solicita ao Motor de Simulação somente as projeções necessárias e transforma resultados em comparação, ajuste e recomendação explicáveis. Ele reúne geração, avaliação e otimização porque todas operam sobre a mesma decisão, mas permanece leve por meio de filtragem prévia, execução progressiva, limites explícitos, reutilização e intervenção humana.