# Proposta de remodelação do núcleo de planejamento

Status: proposta documentada para execução futura.  
Escopo atual: documentação; nenhuma mudança funcional é feita por este documento.

## Contexto

O aplicativo já possui autenticação, multiusuário, espaços de trabalho,
catálogos e um fluxo completo de planejamento. A experiência, porém, tornou-se
mais extensa do que operacional: há campos textuais que apenas registram
contexto, controles repetidos em etapas diferentes e configurações avançadas
misturadas com decisões essenciais.

O objetivo desta proposta é reduzir a carga cognitiva e fazer com que cada
informação estruturada produza uma consequência observável no ranking, na
alocação ou na explicação do plano.

## Diagnóstico registrado

### Briefing

- A página contém muitos campos de texto úteis para memória e documentação,
  mas que não participam de cálculos.
- Jornada, pontos de contato e praça são predominantemente texto livre; não há
  uma representação estruturada suficiente para medir aderência.
- O usuário não distingue com clareza o que é obrigatório para gerar um plano,
  o que é recomendado e o que é apenas informativo.

### Papéis dos Meios

- O MCP já calcula uma pontuação e ordena os inventários, mas o ranking precisa
  ser apresentado como decisão principal, com justificativa por critério.
- Os papéis Principal, Complementar e Apoio devem ser derivados da posição no
  ranking e permanecer editáveis como revisão explícita.
- A validação atual dos pesos estratégicos precisa ser revista: há cinco pesos
  exibidos na tela do Plano de Mídia, mas a soma validada considera apenas
  quatro deles.

### Plano de Mídia

- A página concentra mais de mil linhas de interface e lógica.
- Repete dados do Briefing e mistura resumo estratégico, campos narrativos,
  metas operacionais e configurações por inventário.
- Textos como diretriz, racional e alternativas rejeitadas são importantes para
  auditoria, mas não devem ocupar o mesmo nível visual dos controles que alteram
  a alocação.
- As janelas por meio possuem muitas configurações simultâneas, dificultando a
  leitura do que realmente afeta quantidade, custo, alcance e frequência.

## Desenho proposto

### Fase 1 — Briefing estruturado

1. Classificar cada campo como obrigatório, recomendado ou informativo.
2. Transformar praça em seleção estruturada de Universo/mercado, mantendo
   observações livres separadas.
3. Transformar jornada em etapas selecionáveis e pontos de contato em itens
   estruturados, com opção de observação complementar.
4. Exibir indicadores de completude e bloquear a geração somente pelos campos
   realmente necessários.
5. Preservar textos de contexto em uma seção recolhida de documentação.

### Fase 2 — Ranking e papéis dos meios

1. Calcular o ranking automaticamente após a seleção dos critérios e pesos.
2. Exibir score total e contribuição de cada critério por inventário.
3. Atribuir automaticamente Principal, Complementar e Apoio pela posição.
4. Permitir revisão manual do papel, registrando que houve override.
5. Fazer jornada, praça e adequação ao objetivo influenciarem o score quando
   houver dados estruturados disponíveis.

### Fase 3 — Plano de Mídia enxuto

1. Mostrar no topo um resumo somente leitura do Briefing, dos públicos, da
   jornada e do ranking de meios.
2. Manter na camada principal apenas orçamento, período, KPI, inventários,
   metas de entrega e restrições de compra.
3. Mover racional, auditoria e alternativas rejeitadas para uma seção avançada.
4. Mover configurações específicas por inventário para painéis recolhidos,
   exibindo primeiro apenas os campos que alteram o cálculo.
5. Eliminar duplicidade: o Plano deve consumir o Briefing e o MCP, não pedir
   novamente a mesma informação.
6. Explicar, após a geração, como os pesos e restrições determinaram a ordem e
   a alocação.

## Regras de produto a preservar

- Nenhum campo textual deve ser apresentado como se alimentasse um cálculo se
  não alimentar.
- Toda seleção que influenciar score ou alocação deve aparecer na explicação do
  resultado.
- Dados medidos, estimados e informados manualmente permanecem identificados.
- A revisão manual de um ranking não pode apagar o ranking calculado original.
- Compatibilidade com registros legados e espaços de trabalho deve ser mantida.

## Critérios de aceite futuros

- Um usuário consegue identificar, em cada etapa, o que precisa preencher para
  gerar um plano.
- Praça, jornada e pontos de contato aparecem como dados estruturados e têm
  efeito demonstrável na aderência do plano.
- O MCP apresenta um ranking ordenado, justificável e editável.
- O Plano de Mídia não repete campos do Briefing e separa claramente operação
  de documentação.
- Alterar um peso produz uma mudança verificável no score, ranking ou
  alocação, com explicação na interface.
- Os fluxos existentes de autenticação, espaços, legados e permissões continuam
  funcionando.

## Ordem recomendada de execução

Implementar e testar a Fase 1, depois a Fase 2, e somente então simplificar a
interface e a lógica da Fase 3. A remodelação não deve começar por apagar
campos: primeiro é preciso definir quais dados estruturados substituem cada
campo e quais registros históricos precisam continuar compatíveis.
