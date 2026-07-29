# Sistema de Bibliotecas do MediAd Planner

## 1. Finalidade

O Sistema de Bibliotecas organiza os conhecimentos reutilizáveis que sustentam o planejamento de mídia no MediAd Planner.

Seu objetivo é evitar que cada projeto reconstrua do zero conceitos, parâmetros, referências, classificações, inventários, públicos, objetivos, métricas, custos e modelos de planejamento.

As bibliotecas não substituem o julgamento do planejador. Elas fornecem objetos estruturados, versionados e rastreáveis para apoiar:

- o Briefing;
- a Tradução Estratégica;
- a Arquitetura de Mídia;
- as Simulações;
- a Comparação de Cenários;
- a Otimização;
- o Plano Consolidado;
- o Cronograma;
- o Mapa de Veiculação.

```text
Base de conhecimento fornece referências.
Motores processam relações.
Usuários tomam decisões.
Planos preservam as versões utilizadas.
```

---

## 2. Posição na arquitetura

```text
Catálogos
   ↓
Bibliotecas
   ↓
Relações e parâmetros
   ↓
Motores de planejamento
   ↓
Artefatos do projeto
```

O Sistema de Bibliotecas é transversal a todos os ambientes do aplicativo. Ele não constitui uma etapa isolada do planejamento.

Seus objetos são consultados, selecionados, adaptados e instanciados ao longo do fluxo.

---

## 3. Distinções fundamentais

### 3.1 Catálogo

Catálogo é um vocabulário controlado utilizado para classificar objetos.

Exemplos:

- tecnologia;
- canal;
- ambiente;
- formato;
- modalidade de compra;
- unidade comercial;
- tipo de objetivo;
- categoria de KPI;
- etapa de jornada;
- interesse;
- comportamento;
- tipo territorial;
- unidade métrica.

### 3.2 Biblioteca

Biblioteca é uma coleção de objetos reutilizáveis e contextualizados.

Exemplos:

- inventários;
- públicos;
- universos;
- modelos de jornada;
- objetivos;
- KPIs;
- parâmetros;
- fórmulas;
- regras;
- benchmarks;
- modelos de arquitetura.

Bibliotecas podem possuir versões, fontes, escopos, validade, autoria, confiança e relações com outros objetos.

### 3.3 Relação de conhecimento

Relação de conhecimento conecta dois ou mais objetos.

Exemplos:

- inventário aderente a objetivo;
- interesse do público compatível com proposta editorial;
- comportamento do público compatível com contexto de contato;
- território do público sobreposto à cobertura do veículo;
- afinidade observada entre público e veículo ou programa;
- KPI compatível com objetivo;
- ponto de contato atendido por meio;
- formato compatível com ambiente;
- unidade compatível com modalidade de compra.

Relações não devem ser tratadas automaticamente como verdades universais. Quando necessário, devem admitir contexto, fonte, versão, território, período e nível de confiança.

### 3.4 Parâmetro

Parâmetro é um valor utilizado por regras, fórmulas ou motores.

Exemplos:

- peso de aderência;
- limite de saturação;
- frequência desejada;
- faixa de confiança;
- coeficiente de equivalência;
- tolerância de orçamento;
- fator de sobreposição.

### 3.5 Instância de projeto

Uma instância de projeto é a cópia contextual de um objeto da biblioteca utilizada em um planejamento específico.

```text
Objeto da biblioteca
        ↓
Seleção
        ↓
Instância no projeto
        ↓
Adaptação contextual
        ↓
Uso no planejamento
```

A instância pode manter vínculo com a origem, mas deve preservar os dados efetivamente utilizados no projeto.

---

## 4. Núcleos do Sistema de Bibliotecas

O sistema será composto pelos seguintes núcleos:

1. Biblioteca de Inventários de Mídia;
2. Biblioteca de Públicos e Segmentos;
3. Biblioteca de Objetivos, Resultados e KPIs;
4. Biblioteca de Jornadas, Pontos de Contato e Funções;
5. Biblioteca de Parâmetros, Métricas e Fórmulas;
6. Biblioteca de Custos e Condições Comerciais;
7. Biblioteca de Regras, Restrições e Referências Metodológicas;
8. Biblioteca de Modelos e Componentes Reutilizáveis.

Sequência documental:

```text
12_SISTEMA_DE_BIBLIOTECAS.md
        ↓
13_BIBLIOTECA_DE_INVENTARIOS.md
        ↓
14_BIBLIOTECA_DE_PUBLICOS_E_SEGMENTOS.md
        ↓
15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md
        ↓
16_BIBLIOTECA_DE_JORNADAS_PONTOS_DE_CONTATO_E_FUNCOES.md
        ↓
17_BIBLIOTECA_DE_PARAMETROS_METRICAS_E_FORMULAS.md
        ↓
18_BIBLIOTECA_DE_CUSTOS_E_CONDICOES_COMERCIAIS.md
        ↓
19_BIBLIOTECA_DE_REGRAS_E_REFERENCIAS.md
        ↓
20_BIBLIOTECA_DE_MODELOS_REUTILIZAVEIS.md
```

Cada núcleo possuirá entidades próprias. Não será criada uma tabela genérica única para todos os tipos de biblioteca.

---

## 5. Princípio das dimensões compartilhadas

Públicos e inventários precisam ser descritos por dimensões comparáveis para que a Arquitetura de Mídia possa calcular sua relação.

Essas dimensões não devem ser duplicadas como vocabulários independentes em cada biblioteca.

Devem existir catálogos compartilhados, associados por relações N:N:

- interesses;
- comportamentos;
- contextos de consumo e contato;
- etapas da jornada;
- pontos de contato;
- funções de mídia;
- variáveis demográficas;
- territórios e praças;
- temas e gêneros editoriais.

Exemplo:

```text
Catálogo de interesses
        ↙            ↘
Públicos–interesses   Inventários–interesses
```

Cada vínculo deve registrar seus próprios atributos, como intensidade, relevância, origem, fonte, validade e confiança.

---

## 6. Separação entre públicos e audiência

A Biblioteca de Públicos e Segmentos define **quem se pretende alcançar e onde esse público se encontra**.

Ela não armazena como atributos permanentes do público:

- audiência;
- alcance;
- cobertura;
- frequência;
- impactos;
- afinidade medida.

Essas variáveis dependem da relação entre público, veículo ou inventário, praça, período, fonte e metodologia.

```text
Público
+
Veículo, programa ou inventário
+
Praça
+
Período
+
Fonte e metodologia
=
Evidência ou resultado de mídia
```

Audiência e cobertura são associadas a veículos, programas, redes, plataformas, disponibilizações ou inventários. Alcance e frequência são resultados calculados de veiculações, cenários ou planos.

Afinidade observada é uma relação medida entre público e mídia, não um atributo isolado de qualquer uma das bibliotecas.

---

## 7. Qualificação público–inventário

A descrição comparável das duas bibliotecas alimenta a Arquitetura de Mídia.

```text
Biblioteca de Públicos e Segmentos
├── demografia
├── interesses
├── comportamentos
├── jornada
├── pontos de contato
└── territórios

Biblioteca de Inventários
├── estrutura operacional
├── proposta editorial
├── temas
├── contextos de contato
├── funções de jornada
├── segmentações disponíveis
└── cobertura territorial

                ↓

Componente de Qualificação Público–Inventário
                ↓

Arquitetura de Mídia
```

Essa qualificação acrescenta variáveis ao cálculo dinâmico de adequação já existente. Não cria um processo separado nem substitui objetivos, KPIs, orçamento, restrições, complementaridade, overlap, saturação ou demais parâmetros.

---

## 8. Escopos

Todo objeto reutilizável deve possuir escopo explícito:

### Global

Disponível para todos os espaços autorizados e governado pela administração.

### Espaço de trabalho

Disponível apenas aos membros do espaço e governado pelo proprietário.

### Projeto

Disponível apenas em um projeto específico. Deve ser o escopo predominante para públicos criados em campanhas particulares.

### Pessoal ou rascunho

Área de preparação ainda não compartilhada.

Itens pessoais não participam dos motores compartilhados até serem promovidos.

---

## 9. Estados editoriais

Estados recomendados:

```text
RASCUNHO
PROPOSTO
EM_REVISAO
VALIDADO
PUBLICADO
SUSPENSO
SUBSTITUIDO
ARQUIVADO
REJEITADO
```

O estado editorial deve permanecer separado do estado operacional.

---

## 10. Inclusão de informações

Toda inclusão deve declarar, no mínimo:

- tipo de objeto;
- nome ou título;
- escopo;
- autor;
- estado editorial;
- fonte, quando aplicável;
- data da fonte;
- território ou praça, quando aplicável;
- período de validade, quando aplicável;
- unidade, quando aplicável;
- natureza do dado;
- nível de confiança;
- restrições de uso;
- observações metodológicas.

O sistema deve impedir a publicação de itens que não atendam aos campos obrigatórios de seu domínio.

---

## 11. Natureza dos dados

Categorias recomendadas:

- observado;
- declarado;
- fornecido comercialmente;
- benchmark;
- estimado;
- calculado;
- convertido;
- modelado;
- inferido;
- recomendado;
- padrão do sistema.

A natureza do dado deve acompanhar o valor até seu uso em uma simulação ou plano.

---

## 12. Proveniência e confiança

Cada objeto, relação ou versão deve poder registrar:

- fonte original;
- responsável pela coleta;
- método de coleta;
- data de obtenção;
- documento de suporte;
- transformações realizadas;
- unidade original;
- território;
- período;
- limitações;
- nível de confiança.

O sistema deve distinguir ausência de informação de valor nulo, não aplicável ou sem restrição.

---

## 13. Versionamento e snapshot

Ao selecionar um item reutilizável, o projeto deve guardar uma fotografia versionada das informações utilizadas.

```text
Cadastro mestre
      ↓
Seleção no projeto
      ↓
Snapshot
      ↓
Ajustes locais
      ↓
Uso nos motores
```

Alterações futuras no cadastro mestre não devem modificar retroativamente campanhas anteriores.

---

## 14. Princípio consolidado

> As bibliotecas descrevem objetos e relações reutilizáveis. A Arquitetura de Mídia combina essas informações com o Briefing e a Tradução Estratégica. Audiência, alcance, cobertura, frequência e afinidade observada não são atributos permanentes do público, mas evidências ou resultados produzidos na relação entre públicos, alternativas de mídia, território, período e metodologia.
