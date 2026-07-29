# Mapa de Necessidade e Fronteiras dos Motores Especialistas

**Documento:** `23_MAPA_DE_NECESSIDADE_E_FRONTEIRAS_DOS_MOTORES.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em validação arquitetural  
**Natureza:** Documento normativo de delimitação funcional  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

Este documento identifica quais motores especialistas são realmente necessários ao MediAd Planner antes da especificação individual de cada um.

O objetivo é evitar:

- criar um motor para cada cálculo, meio, KPI ou etapa de tela;
- confundir motor com serviço de aplicação, função matemática, procedimento técnico ou fluxo de interface;
- duplicar validação, explicação, custos, alcance e comparação em componentes concorrentes;
- transformar a arquitetura em um conjunto de motores pequenos, acoplados e difíceis de utilizar.

A decisão sobre um motor deve partir de uma responsabilidade decisória estável e reutilizável, e não da existência de uma fórmula ou documento autônomo.

---

## 2. Definição canônica de motor especialista

Um motor especialista é um componente de domínio que:

1. recebe um contexto decisório estruturado;
2. identifica problemas da Biblioteca 18;
3. consulta conhecimentos versionados da Biblioteca 17 e objetos das Bibliotecas 13 a 16;
4. seleciona e executa procedimentos aplicáveis;
5. produz uma resposta de domínio com alternativas, restrições, confiança, justificativa e rastreabilidade.

Um motor não é:

- uma tela;
- uma etapa da navegação;
- uma fórmula isolada;
- uma consulta ao banco;
- um relatório;
- um validador genérico;
- um gerador de texto;
- um serviço de persistência;
- um motor separado para cada meio.

---

## 3. Critérios para justificar um motor autônomo

Um candidato somente deve permanecer como motor autônomo quando atender conjuntamente à maior parte dos critérios abaixo:

```text
responsabilidade decisória própria
+ conjunto coerente de entradas e saídas
+ uso recorrente em diferentes projetos ou fluxos
+ necessidade de combinar vários conhecimentos e problemas
+ ciclo de execução identificável
+ possibilidade de teste independente
+ fronteira clara com outros motores
```

Não justificam um novo motor, isoladamente:

- possuir fórmula diferente;
- usar indicadores próprios;
- atuar em uma mídia específica;
- produzir uma seção diferente do plano;
- exigir uma regra de validação;
- possuir uma tela própria;
- gerar uma explicação específica.

---

## 4. Cadeia decisória do produto

A cadeia funcional consolidada é:

```text
Briefing e dados do projeto
        ↓
Tradução estratégica
        ↓
Composição da arquitetura de mídia
        ↓
Simulação técnica e econômica
        ↓
Comparação e aperfeiçoamento de cenários
        ↓
Decisão humana
        ↓
Plano consolidado e artefatos operacionais
```

Essa cadeia não exige necessariamente um motor para cada seta. Ela serve para identificar responsabilidades distintas.

---

## 5. Candidatos inicialmente considerados

Foram avaliados os seguintes candidatos:

- Motor Estratégico;
- Motor de Seleção;
- Motor de Cobertura;
- Motor de Pressão;
- Motor Econômico;
- Motor de Comparação;
- Motor de Otimização;
- Motor de Validação;
- Motor de Explicação;
- Motor de Consolidação;
- motores separados por meio ou formato.

A análise indica que essa lista é excessivamente fragmentada.

---

## 6. Motores especialistas necessários na versão 1.0

A versão 1.0 deve possuir quatro responsabilidades especializadas principais.

### 6.1 Motor de Tradução Estratégica

**Necessidade:** confirmada.

Transforma briefing, objetivos declarados, públicos, jornada, restrições e prioridades em uma estrutura estratégica utilizável pelo planejamento de mídia.

Responsabilidades centrais:

- classificar objetivos de marketing, comunicação e mídia;
- relacionar resultados pretendidos e indicadores prioritários;
- estabelecer prioridades entre públicos, praças, etapas, necessidades e funções;
- normalizar pesos e registrar mínimos obrigatórios;
- identificar incoerências ou lacunas estratégicas;
- produzir diretrizes para a composição da arquitetura.

Não deve:

- selecionar ofertas comerciais específicas;
- calcular toda a programação de mídia;
- otimizar verba diretamente;
- redigir o plano final.

Saída principal:

```text
contrato_estrategico_do_planejamento
```

---

### 6.2 Motor de Composição da Arquitetura de Mídia

**Necessidade:** confirmada.

Converte o contrato estratégico em alternativas coerentes de meios, pontos de contato, tipologias, inventários, papéis e combinações.

Responsabilidades centrais:

- filtrar alternativas incompatíveis ou indisponíveis;
- relacionar funções comunicacionais a pontos de contato e inventários;
- avaliar aderência a público, praça, contexto, objetivo e restrições;
- atribuir papéis principal, complementar e apoio;
- construir arquiteturas candidatas;
- preservar diversidade suficiente sem apresentar combinações irrelevantes.

Este motor incorpora o que antes poderia ser chamado separadamente de:

- motor de seleção;
- motor de elegibilidade;
- motor de afinidade;
- motor de combinação de canais.

Essas funções são procedimentos internos, não motores autônomos.

Saída principal:

```text
arquiteturas_candidatas
```

---

### 6.3 Motor de Simulação Técnica

**Necessidade:** confirmada.

Projeta o comportamento técnico, econômico, temporal e territorial de uma arquitetura ou cenário.

Responsabilidades centrais:

- calcular ou estimar audiência, impactos, alcance, frequência e pressão;
- tratar overlap, deduplicação, saturação e rendimento marginal;
- calcular investimentos, descontos, comissão, custos líquidos e métricas de eficiência;
- aplicar cronograma, flights, praça e disponibilidade;
- executar fórmulas e procedimentos das Bibliotecas 17 e 18;
- devolver resultados com estados de validade, comparabilidade e confiança.

Não haverá motores autônomos de:

- cobertura;
- pressão;
- frequência;
- custos;
- mídia digital;
- mídia tradicional;
- OOH;
- televisão;
- programática.

Esses domínios são conjuntos de procedimentos especializados acionados pelo mesmo motor conforme a composição do cenário.

Saída principal:

```text
resultado_de_simulacao
```

---

### 6.4 Motor de Avaliação de Cenários

**Necessidade:** confirmada.

Compara cenários simulados, identifica dominâncias, compensações, restrições e oportunidades de aperfeiçoamento.

Responsabilidades centrais:

- validar comparabilidade entre cenários;
- comparar desempenho estratégico, técnico e econômico;
- identificar alternativas dominadas;
- reconhecer empates técnicos e incomparabilidades;
- aplicar prioridades e pesos do projeto;
- sugerir ajustes de verba, pressão, mix, praça ou período;
- registrar por que uma alternativa é preferível em determinado critério;
- preservar a decisão final do planejador.

Otimização não constitui motor autônomo na versão 1.0. Ela será um modo de execução deste motor:

```text
AVALIAR
COMPARAR
SUGERIR_AJUSTES
BUSCAR_MELHOR_CONFIGURACAO
```

A busca por melhor configuração deve operar dentro de limites e alternativas explícitas. Não deve produzir uma suposta solução universal nem ocultar trade-offs.

Saída principal:

```text
avaliacao_comparativa_e_recomendacoes
```

---

## 7. Capacidades transversais que não serão motores autônomos

### 7.1 Validação

Validação é uma capacidade comum executada em cada motor e em cada procedimento relevante.

Exemplos:

- completude do briefing;
- identidade de universo;
- disponibilidade de inventário;
- validade de fórmula;
- comparabilidade entre cenários;
- limite orçamentário.

Pode existir um serviço técnico compartilhado de validação, mas não um Motor de Validação como etapa decisória independente.

### 7.2 Explicação

Explicabilidade deve acompanhar todas as respostas dos motores.

Cada execução deve preservar:

- entradas utilizadas;
- problema identificado;
- conhecimentos consultados;
- regras e procedimentos aplicados;
- alternativas rejeitadas;
- resultado;
- alertas;
- confiança.

Pode existir um compositor compartilhado de explicações, mas não um Motor de Explicação separado que tente reconstruir posteriormente decisões opacas.

### 7.3 Orquestração

A coordenação da sequência entre os quatro motores pertence à camada de aplicação.

O orquestrador:

- recebe comandos da interface;
- determina qual motor deve ser chamado;
- controla dependências e estados do fluxo;
- persiste resultados;
- solicita reexecução quando houver alterações.

Ele não raciocina sobre mídia e, portanto, não é motor especialista.

### 7.4 Consolidação e geração de artefatos

A produção do Plano Consolidado, mapa de veiculação, relatórios e exportações pertence a serviços de composição documental.

Esses serviços utilizam resultados aprovados, mas não selecionam alternativas nem alteram decisões.

### 7.5 Persistência, consulta e versionamento

Repositórios, gateways e serviços de aplicação não são motores especialistas.

---

## 8. Matriz de decisão dos candidatos

| Candidato | Decisão | Destino |
|---|---|---|
| Tradução Estratégica | manter | motor autônomo |
| Seleção de meios e inventários | consolidar | Motor de Composição da Arquitetura |
| Cobertura e alcance | incorporar | procedimentos do Motor de Simulação |
| Pressão e frequência | incorporar | procedimentos do Motor de Simulação |
| Econômico | incorporar | procedimentos do Motor de Simulação |
| Comparação | manter | Motor de Avaliação de Cenários |
| Otimização | incorporar | modo do Motor de Avaliação |
| Validação | transversal | serviço e regras compartilhadas |
| Explicação | transversal | contrato obrigatório de saída |
| Consolidação do plano | retirar | serviço de aplicação/documento |
| Motor por meio | rejeitar | procedimentos por tipologia |
| Motor por KPI | rejeitar | conhecimentos e cálculos reutilizáveis |

---

## 9. Fronteiras entre os quatro motores

```text
Motor de Tradução Estratégica
responde: o que o planejamento precisa priorizar?

Motor de Composição da Arquitetura
responde: quais estruturas de mídia são coerentes com essas prioridades?

Motor de Simulação Técnica
responde: o que cada estrutura pode entregar, custar e exigir?

Motor de Avaliação de Cenários
responde: como as alternativas se comparam e o que pode ser aperfeiçoado?
```

Uma responsabilidade não deve migrar para outro motor apenas porque a informação está disponível naquele ponto do fluxo.

---

## 10. Relações de dependência

Dependência principal:

```text
Tradução Estratégica
        ↓
Composição da Arquitetura
        ↓
Simulação Técnica
        ↓
Avaliação de Cenários
```

Entretanto:

- o usuário pode simular manualmente uma arquitetura sem aceitar uma recomendação automática;
- uma arquitetura pode ser ajustada e reenviada diretamente à simulação;
- a avaliação pode comparar cenários criados manualmente;
- mudanças estratégicas invalidam, conforme o alcance da alteração, os resultados posteriores;
- nenhum motor deve alterar silenciosamente uma decisão já aprovada.

---

## 11. Contrato mínimo comum de execução

Todos os motores devem receber ou produzir, conforme aplicável:

```text
id_do_projeto
versao_do_contexto
problemas_tecnicos_identificados
entradas_utilizadas
objetos_consultados
procedimentos_executados
restricoes_aplicadas
resultado
alternativas
estado_de_resultado
nivel_de_confianca
alertas
justificativa
rastreabilidade
```

Esse contrato é interno. A interface deve apresentar apenas o necessário à decisão do usuário.

---

## 12. Critérios para evitar confusão funcional

1. Nenhum motor terá nome de tela.
2. Nenhum motor será criado apenas para um meio ou KPI.
3. Cálculos permanecem funções ou procedimentos consultados pelo Motor de Simulação.
4. Regras de exclusão e validação permanecem próximas do objeto ou problema que condicionam.
5. Explicação é parte da resposta, não processamento posterior independente.
6. Otimização é comparação iterativa sob restrições, não uma caixa-preta separada.
7. O planejador pode criar, editar, rejeitar e comparar alternativas manualmente.
8. Os motores não devem duplicar campos ou entidades das bibliotecas.
9. Uma nova responsabilidade somente vira motor quando não puder ser acomodada sem perda de coesão em um dos quatro existentes.

---

## 13. Ordem recomendada de especificação

A especificação individual deve seguir a ordem:

1. contrato comum dos motores;
2. Motor de Tradução Estratégica;
3. Motor de Composição da Arquitetura;
4. Motor de Simulação Técnica;
5. Motor de Avaliação de Cenários;
6. orquestração entre motores;
7. serviços transversais de validação, explicação e rastreabilidade.

A ordem não implica que todos devam ser implementados integralmente antes de testes. Recomenda-se implementar um fluxo vertical mínimo que atravesse os quatro motores com poucos objetos e procedimentos validados.

---

## 14. Decisão arquitetural preliminar

A versão 1.0 do MediAd Planner deve trabalhar com quatro motores especialistas:

```text
MOTOR_DE_TRADUCAO_ESTRATEGICA
MOTOR_DE_COMPOSICAO_DA_ARQUITETURA
MOTOR_DE_SIMULACAO_TECNICA
MOTOR_DE_AVALIACAO_DE_CENARIOS
```

Validação, explicação, orquestração, persistência e geração de artefatos são capacidades ou serviços compartilhados, não motores especialistas autônomos.

Esta decisão deve ser validada contra casos completos de uso antes da especificação detalhada de cada motor.

---

## 15. Próximo passo

Antes de detalhar qualquer motor, devem ser construídos casos de uso ponta a ponta que permitam verificar:

- em qual ponto cada motor é acionado;
- quais decisões realmente produz;
- quais entradas recebe;
- quais saídas são reutilizadas;
- onde existe sobreposição;
- quais capacidades podem permanecer como procedimentos internos;
- quais intervenções pertencem ao usuário.

Somente depois dessa validação o catálogo de motores será declarado definitivo.
