# Modelo de planejamento cross-media

O PlanOS propõe configurações, mas não inventa dados. Novos planos exigem
audiência, alcance e frequência por inventário. Dados cadastrados são
sugestões editáveis; substituições ficam registradas nas premissas do plano.

## Camadas

1. **Fatos:** preço, unidade, medição, fonte, universo, público, jornada e período.
2. **Premissas:** equivalências, alcance incremental, frequência, resposta,
   conversão, retorno e limites de saturação.
3. **Decisões:** pesos, pisos, tetos, obrigatoriedade, quantidades e reserva.
4. **Resultados:** investimento, alcance líquido, frequência combinada, GRP,
   impressões, cliques, conversões, custos e ROI.

## Fórmulas principais

- `quantidade = teto((alcance × frequência) ÷ audiência por unidade)` para inserções.
- `investimento = quantidade × preço líquido` para unidades discretas.
- `impressões = quantidade × 1.000` para milheiros.
- `GRP do meio = alcance do meio (%) × frequência do meio`.
- `GRP total = soma dos GRPs dos meios`.
- `frequência combinada = GRP total ÷ alcance líquido (%)`.
- `CPP = investimento ÷ GRP`.
- `ROI = (retorno − investimento) ÷ investimento`.

O alcance líquido usa o incremental informado. Na ausência dele, o motor
aplica independência probabilística e registra o método na auditoria.

O modo padrão parte das metas e calcula a quantidade. O planejador também pode
fixar a compra; nesse caso, o motor recalcula GRP e frequência efetivamente
entregues. Pisos e tetos limitam a solução nos dois modos.

## Comparação

O Comparador não possui vencedor universal. O usuário pondera alcance,
frequência, conversões, ROI, cobertura da jornada, saturação e investimento.
O resultado informa a estratégia mais aderente àquela configuração e preserva
as vantagens da alternativa.

## Compatibilidade

Planos antigos continuam restauráveis. O cálculo legado existe apenas para
leitura; uma nova geração requer as premissas do modelo cross-media.
