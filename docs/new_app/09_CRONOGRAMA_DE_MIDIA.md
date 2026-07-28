# Cronograma de Mídia

O **Cronograma de Mídia** é a visão temporal, sintética e visual do Plano Consolidado de Mídia. Ele representa como a presença e a pressão de mídia se distribuem ao longo do tempo, sem substituir o detalhamento técnico do Mapa de Veiculação.

Sua pergunta orientadora é:

> Como a presença, a intensidade e a função da mídia se distribuem entre fases, períodos, semanas, meios, veículos, públicos, praças, etapas da jornada e pontos de contato?

O Cronograma não constitui uma base independente. Ele é gerado por agregação das linhas de programação e das ocorrências registradas no Plano.

```text
Plano Consolidado
        ↓
Linhas de Programação
        ↓
Ocorrências de Veiculação
        ↓
Agregação temporal
        ↓
Cronograma de Mídia
```

## 1. Natureza do artefato

O Cronograma deve ser:

- visual;
- temporal;
- sintético;
- filtrável;
- auditável;
- recalculável;
- derivado da mesma fonte de verdade do Mapa.

Ele não deve ser preenchido manualmente de forma desconectada das ocorrências de veiculação.

## 2. Perspectiva principal

Sua estrutura básica é matricial:

```text
Linhas   → meios, canais, veículos, fases, jornadas ou pontos de contato
Colunas  → semanas, dias, quinzenas, meses ou períodos configuráveis
Células  → presença, intensidade, pressão ou outra medida selecionada
```

Exemplo conceitual:

| Meio/veículo | Sem. 1 | Sem. 2 | Sem. 3 | Sem. 4 |
|---|---|---|---|---|
| TV | Alta | Alta | Média | Baixa |
| Rádio | Média | Média | Média | Média |
| Social | Alta | Alta | Alta | Média |
| Busca | Baixa | Média | Alta | Alta |
| OOH | Alta | Alta | Alta | Alta |

## 3. Unidade temporal

O Cronograma deve admitir:

- dia;
- semana;
- quinzena;
- mês;
- fase;
- período personalizado.

A visualização padrão pode ser semanal, mas o sistema não deve limitar o domínio a semanas fixas.

Cada período deve possuir:

- data inicial;
- data final;
- número ou rótulo;
- fase associada;
- eventos e marcos;
- duração;
- estado.

## 4. Relação entre estratégia temporal, flight e cronograma

O Cronograma não é o flight.

```text
Estratégia temporal
        ↓
Fases
        ↓
Períodos
        ↓
Regra de flight
        ↓
Distribuição das ocorrências
        ↓
Pressão por período
        ↓
Cronograma
```

O **flight** é a regra de distribuição temporal. O **Cronograma** mostra a aplicação concreta dessa regra.

Flights possíveis:

- contínuo;
- pulsado;
- ondas;
- concentrado;
- crescente;
- decrescente;
- personalizado.

O sistema deve comparar:

- flight planejado;
- flight programado;
- flight contratado;
- flight realizado.

## 5. Pressão de mídia

A cor ou intensidade visual das células não deve representar apenas presença ou ausência.

Ela pode representar:

- quantidade de inserções;
- investimento;
- GRP ou TRP;
- impactos equivalentes;
- alcance incremental;
- frequência;
- pressão relativa;
- participação no total;
- índice composto de pressão.

A medida utilizada deve ser explicitamente identificada na legenda.

Cada célula deve preservar metadados, por exemplo:

```text
TV — Semana 2
pressão: alta
inserções: 18
GRP: 42
impactos equivalentes: 325.000
investimento: R$ 14.800,00
```

## 6. Escalas de pressão

O sistema pode admitir escalas:

### 6.1 Categórica

```text
sem presença
baixa
média
alta
muito alta
```

### 6.2 Numérica

- valores absolutos;
- percentuais;
- índices de 0 a 100;
- faixas configuráveis.

### 6.3 Relativa

A célula representa a intensidade em relação:

- ao maior valor do período;
- ao maior valor da linha;
- à pressão total da campanha;
- à meta daquele meio;
- à pressão desejada da fase.

A regra de normalização deve ser registrada.

## 7. Legenda e cores

Cada Cronograma deve conter:

- título da medida visualizada;
- legenda;
- faixas de valores;
- unidade;
- regra de cálculo;
- fonte;
- versão do Plano;
- data de geração.

As cores devem ser configuráveis e não devem constituir a única forma de leitura. O valor ou categoria precisa permanecer acessível por texto, rótulo ou tooltip.

## 8. Visões por dimensão

O mesmo Cronograma deve poder ser reorganizado por:

- meio;
- canal;
- veículo;
- inventário;
- fase;
- praça;
- público;
- objetivo;
- função de mídia;
- papel estratégico;
- etapa da jornada;
- ponto de contato;
- fornecedor;
- responsável.

Não devem existir cronogramas independentes e divergentes para cada visão.

## 9. Jornada e pontos de contato

O Cronograma deve permitir uma leitura temporal da jornada.

Exemplo:

| Etapa da jornada | Sem. 1 | Sem. 2 | Sem. 3 | Sem. 4 |
|---|---|---|---|---|
| Conhecimento | Alta | Alta | Média | Baixa |
| Consideração | Média | Alta | Alta | Média |
| Conversão | Baixa | Média | Alta | Alta |
| Retenção | — | Baixa | Média | Média |

Essa visão permite detectar:

- excesso de pressão em uma única etapa;
- ausência de presença em consideração;
- conversão concentrada cedo demais;
- pontos de contato sem continuidade;
- sobreposição sem função clara;
- lacunas entre fases da campanha.

## 10. Fases e marcos

O Cronograma deve representar:

- fases;
- transições;
- lançamento;
- eventos;
- datas sazonais;
- feriados;
- deadlines de produção;
- períodos de compra;
- marcos de avaliação;
- janelas de reotimização.

As fases devem poder aparecer como faixas superiores ou agrupamentos das colunas.

## 11. Relação com audiências equivalentes

A pressão visual pode ser baseada em audiências equivalentes.

```text
Ocorrências programadas
        ↓
Métricas nativas
        ↓
Conversão pelo motor de equivalências
        ↓
Impactos equivalentes por período
        ↓
Pressão equivalente
        ↓
Escala visual do Cronograma
```

O sistema deve preservar:

- métricas nativas agregadas;
- métricas equivalentes agregadas;
- método de equivalência;
- confiança;
- limitações.

## 12. Relação com overlap e saturação

O Cronograma deve permitir visualizar:

- pressão bruta;
- pressão líquida após overlap;
- frequência acumulada;
- aproximação de saturação;
- períodos de redundância;
- intervalos sem presença.

Uma célula de alta intensidade não deve ser interpretada automaticamente como eficiente.

## 13. Relação com custos

O Cronograma pode alternar ou combinar visões de:

- investimento por período;
- investimento acumulado;
- participação por meio;
- custo por fase;
- custo por etapa da jornada;
- custo por praça;
- custo por ponto de contato;
- custo por pressão equivalente.

Os custos devem ser derivados das mesmas linhas e ocorrências usadas pelo Mapa.

## 14. Camadas planejada, contratada e realizada

O Cronograma deve admitir comparação entre:

```text
planejado
contratado
programado
realizado
```

Pode haver visualização:

- lado a lado;
- sobreposta;
- por diferença;
- por percentual de execução.

O realizado nunca deve sobrescrever o planejado.

## 15. Cálculo da célula

Cada célula deve ser resultado de uma agregação explícita.

Estrutura conceitual:

```text
filtro de dimensão
+ intervalo temporal
+ ocorrências elegíveis
+ métrica selecionada
+ regra de agregação
+ regra de normalização
= valor da célula
```

Regras de agregação possíveis:

- soma;
- média;
- máximo;
- mínimo;
- valor acumulado;
- participação percentual;
- índice composto.

## 16. Pressão mínima, desejada e máxima

O Cronograma deve poder comparar a pressão agregada com:

```text
pressão mínima
pressão desejada
pressão máxima
tolerância
```

Estados possíveis:

- abaixo do mínimo;
- dentro da faixa;
- acima da faixa;
- crítico;
- sem meta definida.

## 17. Alertas

O Cronograma pode gerar alertas para:

- período sem mídia;
- pressão abaixo do mínimo;
- pressão acima do máximo;
- concentração excessiva;
- ruptura de continuidade;
- mudança não autorizada de flight;
- ausência de etapa da jornada;
- gasto acima da previsão;
- baixa confiança da equivalência;
- saturação provável;
- dependência de único canal.

## 18. Interações e filtros

O usuário deve poder:

- expandir ou recolher níveis;
- filtrar período;
- filtrar praça;
- filtrar público;
- filtrar etapa da jornada;
- escolher métrica;
- escolher base financeira;
- alternar planejado e realizado;
- abrir a composição de uma célula;
- navegar da célula para as linhas e ocorrências correspondentes.

## 19. Drill-down

A navegação deve seguir:

```text
Cronograma
    ↓
Célula temporal
    ↓
Linhas de programação agregadas
    ↓
Ocorrências individuais
    ↓
Mapa de Veiculação
```

Isso garante auditabilidade.

## 20. Exportações

O Cronograma deve poder ser exportado como:

- planilha;
- PDF;
- imagem;
- apresentação;
- relatório executivo;
- componente de dashboard.

A exportação deve preservar legenda, filtros, versão e data de geração.

## 21. Validação

Antes da emissão, o sistema deve verificar:

- períodos válidos;
- fases coerentes;
- ocorrências dentro do período da campanha;
- ausência de duplicidade indevida;
- métrica disponível;
- regra de agregação definida;
- legenda coerente;
- pressão calculável;
- correspondência com o Mapa;
- versão do Plano identificada.

Resultados possíveis:

```text
Cronograma válido
Cronograma válido com ressalvas
Cronograma inconsistente
Cronograma incompleto
```

## 22. Versionamento

O Cronograma deve registrar:

- Plano de origem;
- versão do Plano;
- parâmetros de visualização;
- filtros;
- métrica;
- regra de agregação;
- data de geração;
- responsável.

Alterações no Plano, nas linhas ou nas ocorrências devem invalidar cronogramas derivados desatualizados.

## 23. Contrato de entrada

O Cronograma recebe:

- Plano Consolidado;
- linhas de programação;
- ocorrências;
- fases;
- períodos;
- flight;
- públicos;
- praças;
- jornada;
- pontos de contato;
- papéis;
- métricas nativas;
- audiências equivalentes;
- overlap;
- saturação;
- custos;
- metas de pressão;
- filtros;
- regra de agregação.

## 24. Contrato de saída

O Cronograma entrega:

- matriz temporal;
- níveis de pressão;
- valores agregados;
- legenda;
- fases e marcos;
- totais por período;
- totais por linha;
- alertas;
- comparações entre planejado e realizado;
- vínculos para as linhas e ocorrências de origem;
- versão e parâmetros de geração.

## 25. Relação com o Plano Consolidado

O Plano é a fonte de verdade. O Cronograma é uma visão derivada.

Ele não pode:

- criar inserções;
- alterar custos;
- modificar o flight sem gerar alteração no Plano;
- substituir o Mapa;
- ocultar a métrica usada na cor;
- manter dados divergentes da base.

## 26. Relação com o Mapa de Veiculação

O Mapa mostra o detalhe técnico. O Cronograma agrega esse detalhe.

```text
Mapa de Veiculação
        ↓ agregação temporal
Cronograma de Mídia
```

Qualquer alteração válida em uma ocorrência deve atualizar ambos.

## 27. Limites

O Cronograma deve:

- representar presença e pressão no tempo;
- relacionar flight, fases e períodos;
- permitir leitura por jornada e pontos de contato;
- incorporar audiências equivalentes;
- permitir leitura financeira;
- gerar alertas;
- permitir drill-down;
- manter rastreabilidade.

Ele não deve:

- ser uma planilha paralela;
- usar cores sem legenda;
- confundir quantidade com pressão;
- confundir projeção com realizado;
- substituir a programação detalhada;
- sobrescrever o Plano.

## 28. Formulação canônica

O **Cronograma de Mídia** é a representação temporal, visual e agregada do Plano Consolidado, gerada a partir das linhas de programação e das ocorrências de veiculação, capaz de mostrar como meios, veículos, fases, jornadas, pontos de contato, audiências, custos e níveis de pressão se distribuem ao longo do tempo.

Ele responde:

```text
quando há presença
onde está concentrada
qual é a intensidade
que função desempenha
que etapa da jornada cobre
quanto custa
qual audiência produz
se respeita o flight planejado
se há lacunas, excesso ou saturação
```
