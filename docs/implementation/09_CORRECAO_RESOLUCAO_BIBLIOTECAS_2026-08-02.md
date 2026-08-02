# Correção da resolução de bibliotecas — 2 de agosto de 2026

## Problema confirmado

O primeiro núcleo consultava apenas as Bibliotecas 15, 17 e 18 e oferecia na
edição somente os objetivos já derivados. Quando o objetivo de Comunicação não
possuía regra no núcleo reduzido, o componente de seleção recebia lista vazia.

## Correção

- Biblioteca 14 passou a resolver o contexto de público e segmento;
- Biblioteca 16 passou a resolver jornada e etapa, inclusive o estado explícito
  de não aplicabilidade;
- relações Comunicação–Mídia documentadas na Biblioteca 15 foram ampliadas;
- o seletor passou a consumir objetivos de mídia da Biblioteca 15;
- inclusão humana é distinguida de derivação automática, exige justificativa e
  preserva `NAO_DERIVADO` como valor calculado original;
- traduções do catálogo anterior podem ser reprocessadas como nova versão;
- versões anteriores permanecem preservadas e passam ao estado `SUPERADO` pela
  operação transacional já existente.

## Limite

As bibliotecas são consultadas seletivamente, conforme o contrato comum. O fato
de as Bibliotecas 14–18 aparecerem neste fluxo decorre da presença obrigatória
de público, objetivos, jornada, conhecimento e problema no Briefing concluído;
não constitui autorização para consultar inventários ou preços da Biblioteca
13 nesta etapa.
