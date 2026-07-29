# Status da Arquitetura e Próximos Passos

## Objetivo
Este documento registra, de forma provisória, o estado atual da arquitetura conceitual do MediAd Planner para permitir a retomada do desenvolvimento sem perda de contexto.

## Situação Atual

A arquitetura conceitual do MediAd Planner encontra-se estabilizada.

O projeto passou a ser definido como uma plataforma de inteligência de mídia baseada em sistemas especialistas, composta por:

- ontologias do domínio;
- catálogos controlados;
- bibliotecas de conhecimento;
- motores especialistas;
- modelos reutilizáveis;
- mecanismos de explicabilidade.

## Bibliotecas

Consolidadas:
- 12 Sistema de Bibliotecas
- 13 Inventários
- 15 Objetivos, Resultados e KPIs
- 16 Jornadas, Necessidades, Funções e Pontos de Contato

Em revisão:
- 14 Públicos e Segmentos
- 17 Conhecimento Técnico

Criada neste ciclo:
- 18 Problemas Técnicos de Planejamento de Mídia

Pendentes:
- 19 Custos e Condições Comerciais
- 20 Regras, Restrições e Referências Metodológicas
- 21 Modelos e Componentes Reutilizáveis

## Principal evolução deste ciclo

A principal mudança arquitetural foi separar:

- Ontologia (o que existe);
- Conhecimento (o que se sabe);
- Problemas (o que precisa ser resolvido);
- Motores (quem resolve);
- Modelos (como reutilizar).

Os motores deixam de executar fórmulas diretamente e passam a resolver problemas utilizando conhecimentos técnicos.

## Próximas etapas

1. Revisar definitivamente a Biblioteca 14.
2. Formalizar o inventário completo da Biblioteca 17.
3. Catalogar os problemas técnicos da Biblioteca 18.
4. Definir o relacionamento N:N entre problemas e conhecimentos.
5. Projetar a Biblioteca 19.
6. Projetar a Biblioteca 20.
7. Projetar a Biblioteca 21.
8. Especificar os Motores Especialistas a partir da Biblioteca 18.
9. Modelar o banco de dados definitivo.
10. Definir a arquitetura de inferência e explicabilidade.

## Observação

Considera-se encerrada a fase de reorganização conceitual da arquitetura. As próximas atividades deverão concentrar-se na formalização do conhecimento, povoamento das bibliotecas e implementação dos motores especialistas.