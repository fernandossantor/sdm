# Núcleo 3 — GRP e Equivalências Multimídia

**Documento:** `17E_NUCLEO_3_GRP_E_EQUIVALENCIAS_MULTIMIDIA.md`  
**Documento principal:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Protocolo:** `17B_PROTOCOLO_DE_FORMALIZACAO_DOS_OBJETOS_DE_CONHECIMENTO_TECNICO.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em validação  
**Natureza:** Conjunto coeso de Objetos de Conhecimento Técnico

---

## 1. Finalidade

Este núcleo formaliza o GRP como medida de pressão bruta e estabelece alternativas condicionadas de equivalência entre diferentes mídias.

O objetivo não é declarar que todas as mídias possuem GRP idêntico, mas permitir que o MediAd Planner:

- reconheça quando uma métrica já é diretamente expressa em pontos sobre um universo;
- converta exposições brutas em pontos percentuais quando houver universo compatível;
- mantenha diferenças entre impressão servida, oportunidade de exposição e exposição qualificada;
- classifique a equivalência como direta, convertida, condicionada ou inválida;
- preserve ressalvas metodológicas na comparação multimídia.

Princípio central:

```text
mesma forma algébrica
não implica
mesmo significado de exposição
```

---

## 2. Objetos principais

Este núcleo mantém apenas quatro objetos principais:

```text
KT_CONCEITO_GRP
KT_CALCULO_GRP
KT_CONVERSAO_GRP_IMPACTOS
KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
```

As variantes por meio permanecem como regras internas do objeto de equivalência, e não como novos objetos ou novas bibliotecas.

---

# 3. KT_CONCEITO_GRP

## 3.1 Identificação

```text
codigo: KT_CONCEITO_GRP
nome: Conceito técnico de GRP
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.0.0
```

## 3.2 Definição

GRP — Gross Rating Points — representa a soma bruta de pontos percentuais de exposição ou audiência de uma programação em relação a um universo declarado.

Admite repetição da mesma pessoa ou unidade ao longo das exposições. Por isso, não representa alcance líquido.

## 3.3 Finalidade

Expressar a pressão bruta produzida por uma programação sobre uma base populacional comum.

## 3.4 Unidade

```text
pontos percentuais brutos
```

Um GRP corresponde, matematicamente, a exposições brutas equivalentes a 1% do universo declarado.

## 3.5 Condições de validade

- universo identificado;
- unidade populacional identificada;
- praça e período declarados;
- exposição ou audiência definida;
- valores componentes compatíveis;
- ausência de mistura direta entre pessoas, domicílios, dispositivos ou fluxos;
- regra de contagem conhecida.

## 3.6 Restrições

- GRP não informa alcance líquido isoladamente;
- GRP não informa distribuição de frequência;
- GRP não comprova atenção, lembrança, resposta ou resultado;
- GRP de pessoas não é diretamente equivalente a GRP domiciliar;
- pontos produzidos com definições distintas de exposição não são automaticamente comparáveis;
- a extensão do termo GRP para outras mídias exige explicitação da métrica de origem.

## 3.7 Interpretação

Um valor de 250 GRP significa que o total bruto de exposições equivale a 250% do universo declarado. Isso pode decorrer, por exemplo, de 50% de alcance médio submetido a frequência média 5, mas outras distribuições também podem produzir o mesmo total.

---

# 4. KT_CALCULO_GRP

## 4.1 Identificação

```text
codigo: KT_CALCULO_GRP
nome: Cálculo de GRP
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA, FORMULA_DERIVADA]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.0.0
```

## 4.2 Finalidade

Calcular a pressão bruta por diferentes formas matematicamente equivalentes, desde que as bases sejam compatíveis.

## 4.3 Formas de cálculo

### Por audiência e inserções

```text
grp_programa = audiencia_percentual × numero_de_insercoes
```

### Pela soma da programação

```text
grp_total = soma(grp_de_cada_programa_ou_unidade)
```

### Por alcance e frequência

```text
grp = alcance_percentual × frequencia_media
```

### Por exposições brutas e universo

```text
grp = exposicoes_brutas / universo_correspondente × 100
```

## 4.4 Regras internas

As quatro formas pertencem ao mesmo objeto porque representam a mesma relação de pressão bruta. A forma utilizada deve ser registrada na execução.

## 4.5 Validações

- audiência percentual e inserções devem se referir à mesma unidade de programação;
- os componentes somados devem utilizar universo, praça, período e unidade compatíveis;
- alcance e frequência devem derivar da mesma base deduplicada;
- exposições brutas e universo devem usar unidade populacional compatível;
- denominadores devem ser maiores que zero;
- valores ausentes não devem ser substituídos por zero.

## 4.6 Saída

```text
grp
forma_de_calculo
universo
unidade_populacional
periodo
praca
definicao_de_exposicao
status_de_validacao
alertas
```

## 4.7 Tratamento de zero e ausência

- zero de audiência ou zero de exposições produz zero GRP, quando observado validamente;
- universo zero torna o cálculo inválido;
- ausência de alcance, frequência, audiência ou exposições impede apenas a forma correspondente;
- se outra forma válida estiver disponível, o cálculo pode prosseguir com rastreabilidade.

---

# 5. KT_CONVERSAO_GRP_IMPACTOS

## 5.1 Identificação

```text
codigo: KT_CONVERSAO_GRP_IMPACTOS
nome: Conversão entre GRP e impactos
classe_do_objeto: TRANSFORMACAO
subtipos: [CONVERSAO, FORMULA_INVERSA]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.0.0
```

## 5.2 Fórmulas

```text
impactos = grp × universo / 100
```

```text
grp = impactos / universo × 100
```

## 5.3 Condições

- GRP e universo devem usar a mesma unidade populacional;
- o universo deve corresponder ao rating que originou o GRP;
- praça e período devem ser compatíveis;
- impactos significam exposições brutas, não pessoas únicas;
- a definição de exposição deve permanecer registrada.

## 5.4 Interpretação

A conversão traduz pontos percentuais brutos em quantidade absoluta de exposições dentro de uma base. Ela não melhora a qualidade da medição nem resolve diferenças entre definições de exposição.

---

# 6. KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA

## 6.1 Identificação

```text
codigo: KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
nome: Equivalência condicionada de pressão entre mídias
classe_do_objeto: REGRA_TECNICA
subtipos: [COMPARABILIDADE, CONVERSAO, CLASSIFICACAO]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: COMPARABILIDADE_MULTIMIDIA
status: EM_VALIDACAO
versao: 1.0.0
```

## 6.2 Definição

Regra que verifica se uma métrica de determinada mídia pode ser expressa em pontos percentuais brutos sobre um universo comum e comparada, com ou sem ressalvas, a métricas de outras mídias.

A equivalência é de escala e pressão, não necessariamente de qualidade de contato, atenção, duração, visibilidade, contexto ou efeito.

## 6.3 Estados de equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

### EQUIVALENCIA_DIRETA

A métrica já representa pontos percentuais brutos sobre universo, target, praça e período compatíveis.

### EQUIVALENCIA_APOS_CONVERSAO

Há exposições brutas e universo compatível, permitindo:

```text
pontos_de_pressao = exposicoes_brutas / universo × 100
```

### EQUIVALENCIA_CONDICIONADA

A conversão é matematicamente possível, mas a exposição de origem possui natureza diferente ou depende de hipótese relevante.

### NAO_EQUIVALENTE

Não existe unidade de exposição compatível, universo identificável ou procedimento metodológico defensável.

### DADOS_INSUFICIENTES

Faltam metadados para classificar a relação.

---

## 6.4 Matriz de alternativas por mídia

### Televisão linear

Métrica de origem preferencial:

```text
rating percentual por insercao
```

Alternativas:

```text
soma de ratings → GRP
impactos / universo → GRP
alcance percentual × frequência média → GRP
```

Classificação esperada:

```text
EQUIVALENCIA_DIRETA
```

Ressalvas:

- distinguir audiência domiciliar e individual;
- distinguir universo total, universo com TV e target;
- preservar praça, programa, faixa e período.

### Rádio

Métrica de origem preferencial:

```text
audiencia percentual ou impactos estimados
```

Alternativas:

```text
soma de ratings → pontos de pressão
impactos / universo → pontos de pressão
alcance × frequência → pontos de pressão
```

Classificação esperada:

```text
EQUIVALENCIA_DIRETA
ou
EQUIVALENCIA_APOS_CONVERSAO
```

Ressalvas:

- definição de audiência e janela temporal;
- base de ouvintes e praça;
- exposição potencial versus escuta aferida.

### Digital display, social e vídeo online

Métrica de origem possível:

```text
impressoes servidas
impressoes validas
impressoes visiveis
alcance unico
frequencia
```

Alternativas:

```text
impressoes / universo do target × 100
alcance percentual × frequência média
```

Classificação esperada:

```text
EQUIVALENCIA_APOS_CONVERSAO
ou
EQUIVALENCIA_CONDICIONADA
```

Ressalvas obrigatórias:

- impressão servida não equivale necessariamente a impressão visível;
- pessoa, conta, cookie e dispositivo não são unidades idênticas;
- tráfego inválido deve ser filtrado quando aplicável;
- alcance entre plataformas exige deduplicação;
- frequência de plataforma pode não ser frequência de pessoa.

O sistema deve registrar o qualificador da exposição:

```text
SERVIDA
VALIDA
VISIVEL
COMPLETA
AUDIVEL
QUALIFICADA
```

### CTV, OTT e streaming

Métrica de origem possível:

```text
impressoes de video
alcance estimado
frequencia
exposicoes em dispositivo ou domicilio
```

Alternativa:

```text
impressoes qualificadas / universo compatível × 100
```

Classificação esperada:

```text
EQUIVALENCIA_APOS_CONVERSAO
ou
EQUIVALENCIA_CONDICIONADA
```

Ressalvas:

- distinguir dispositivo, domicílio e pessoa;
- registrar início de reprodução, duração e conclusão quando disponíveis;
- tratar server-side ad insertion e duplicidades;
- explicitar medição de co-viewing quando utilizada.

### OOH e DOOH

Métrica de origem possível:

```text
oportunidades de ver
impressoes estimadas
contatos potenciais
alcance e frequência modelados
```

Alternativas:

```text
impressoes estimadas / universo da praça × 100
alcance percentual × frequência média
```

Classificação esperada:

```text
EQUIVALENCIA_CONDICIONADA
```

Ressalvas:

- fluxo não equivale automaticamente a contato publicitário;
- passagem não equivale automaticamente a visualização;
- exposição pode ser modelada por visibilidade, direção, distância, velocidade e tempo;
- pessoas, veículos e viagens não podem ser misturados;
- DOOH deve separar plays, oportunidades e audiência estimada.

### Cinema

Métrica de origem possível:

```text
publico pagante ou espectadores estimados por sessao
```

Alternativa:

```text
exposicoes totais / universo da praça ou target × 100
```

Classificação esperada:

```text
EQUIVALENCIA_APOS_CONVERSAO
ou
EQUIVALENCIA_CONDICIONADA
```

Ressalvas:

- público por sessão pode ser uma contagem de entradas, não pessoas deduplicadas;
- repetição entre sessões exige tratamento;
- universo deve ser definido de forma defensável.

### Jornal e revista

Métrica de origem possível:

```text
leitores por edicao
circulacao
exemplares
contatos estimados
```

Alternativas:

```text
leitores estimados × insercoes / universo × 100
```

Classificação esperada:

```text
EQUIVALENCIA_CONDICIONADA
```

Ressalvas:

- circulação não equivale a leitores;
- leitores por exemplar podem ser estimados;
- edições e períodos precisam ser compatíveis;
- exposição à publicação não comprova exposição ao anúncio.

### Mídia própria, e-mail e CRM

Métrica de origem possível:

```text
mensagens entregues
contatos entregues
aberturas validas
alcance unico
```

Alternativas:

```text
entregas ou aberturas / universo elegível × 100
```

Classificação esperada:

```text
EQUIVALENCIA_APOS_CONVERSAO
ou
EQUIVALENCIA_CONDICIONADA
```

Ressalvas:

- envio não equivale a entrega;
- entrega não equivale a abertura;
- abertura não equivale a leitura;
- mecanismos automáticos podem inflar aberturas;
- o universo tende a ser uma base elegível própria, não a população geral.

### Eventos, PDV e no media

Métrica de origem possível:

```text
participantes
visitantes
abordagens
interacoes
contatos estimados
```

Alternativa:

```text
contatos brutos / universo elegível × 100
```

Classificação esperada:

```text
EQUIVALENCIA_CONDICIONADA
ou
NAO_EQUIVALENTE
```

Ressalvas:

- presença, abordagem e interação são fenômenos diferentes;
- universos elegíveis podem ser locais e circunstanciais;
- contato pode ser mais intenso, mas isso não o torna numericamente equivalente a uma impressão de mídia.

---

## 6.5 Requisitos mínimos para conversão

Toda conversão multimídia deve registrar:

```text
midia_de_origem
metrica_de_origem
valor_bruto
definicao_de_exposicao
qualificador_da_exposicao
unidade_observada
universo
unidade_do_universo
target
praca
periodo
fonte
metodologia
nivel_de_deduplicacao
conversao_aplicada
estado_de_equivalencia
ressalvas
confianca
```

---

## 6.6 Regra de bloqueio

```text
SE a unidade observada não puder ser relacionada a pessoas, domicílios ou outra unidade de universo claramente definida
OU o universo estiver ausente
OU houver mistura incompatível de unidades
ENTAO NAO calcular pontos de pressão comparáveis
```

O sistema poderá manter a métrica original para análise própria do meio, mas não deve inseri-la em uma ordenação multimídia homogênea.

---

## 6.7 Comparação válida não significa soma válida

Duas métricas podem ser expressas em pontos de pressão e ainda assim não poderem ser somadas para produzir alcance ou frequência combinados.

```text
comparar pressão
≠
somar alcance
≠
deduplicar pessoas
```

A soma de pontos entre mídias somente representa pressão bruta agregada com ressalvas. Alcance combinado e frequência cross-media dependem de deduplicação ou modelagem específica.

---

## 6.8 Saída recomendada

O MediAd Planner deve apresentar simultaneamente:

```text
metrica_original
valor_original
pontos_de_pressao_convertidos
estado_de_equivalencia
qualificador_da_exposicao
universo
ressalvas
confianca
```

Exemplo:

```text
Métrica original: 1.200.000 impressões visíveis
Universo do target: 400.000 pessoas
Pressão convertida: 300 pontos
Equivalência: EQUIVALENCIA_APOS_CONVERSAO
Ressalva: alcance de pessoas depende de deduplicação entre dispositivos
```

---

## 7. Relações com outros núcleos

```text
KT_CONCEITO_GRP
DEPENDE_DE → KT_CONCEITO_UNIVERSO
DEPENDE_DE → KT_CONCEITO_IMPACTOS
RELACIONA_SE_COM → KT_CONCEITO_ALCANCE
RELACIONA_SE_COM → KT_CONCEITO_FREQUENCIA_MEDIA

KT_CALCULO_GRP
VALIDADO_POR → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO

KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
DEPENDE_DE → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
DEPENDE_DE → definição de exposição por tipologia de mídia
RESTRINGE → soma e comparação multimídia
```

---

## 8. Relação com indicadores e problemas

Indicadores relacionados da Biblioteca 15:

```text
GRP
TRP/TARP
impactos
alcance
frequência média
pressão de mídia
```

Problemas relacionados da Biblioteca 18:

```text
CALCULAR_PRESSAO_DE_MIDIA
COMPARAR_PRESSAO_ENTRE_ALTERNATIVAS
CONVERTER_METRICAS_PARA_BASE_COMUM
VALIDAR_COMPARABILIDADE_MULTIMIDIA
ESTIMAR_IMPACTOS
```

---

## 9. Fontes metodológicas

Fontes primárias recomendadas para validação e aprofundamento:

- Media Rating Council — Cross-Media Measurement Standard;
- Media Rating Council — padrões específicos para digital, áudio, vídeo, OOH e place-based;
- IAB/MRC — Ad Impression Measurement Guidelines;
- IAB/MRC — Audience Reach Measurement Guidelines;
- IAB — guias de mensuração de vídeo e CTV;
- World Federation of Advertisers — princípios e framework Halo para alcance e frequência cross-media;
- padrões e metodologias dos institutos de medição adotados em cada mercado.

A adoção de qualquer conversão deve preservar a versão e a metodologia da fonte efetivamente usada.

---

## 10. Decisões consolidadas

1. GRP permanece uma medida de pressão bruta, não de alcance líquido.
2. As diferentes fórmulas de GRP permanecem dentro de um único objeto de cálculo.
3. Métricas de outras mídias podem ser convertidas para pontos de pressão quando houver exposição bruta e universo compatível.
4. A conversão produz equivalência de escala, não identidade de qualidade de contato.
5. Impressão, oportunidade de ver, circulação, fluxo, entrega e interação não são sinônimos.
6. Toda equivalência multimídia deve registrar o qualificador da exposição.
7. Comparabilidade de pressão não autoriza soma de alcance ou frequência sem deduplicação.
8. A métrica original nunca deve ser apagada pela métrica convertida.
9. Conversões frágeis devem ser classificadas como condicionadas, e não apresentadas como equivalências diretas.
10. Não serão criados objetos separados para cada mídia; as diferenças permanecem como variantes internas da regra de equivalência.

---

## 11. Princípio consolidado

> O MediAd Planner pode converter diferentes métricas em uma escala comum de pressão quando a base populacional e a definição de exposição forem conhecidas. Essa conversão permite comparação técnica, mas não transforma contatos de naturezas distintas em experiências idênticas nem substitui a deduplicação necessária ao alcance e à frequência cross-media.
