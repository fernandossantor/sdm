# Auditoria Final de Consistência Documental

**Documento:** `30_AUDITORIA_FINAL_DE_CONSISTENCIA_DOCUMENTAL.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado para início da implementação  
**Natureza:** Auditoria de coerência, precedência e transição  
**Última revisão:** 29/07/2026

---

## 1. Escopo

Esta auditoria revisa o conjunto `docs/new_app` como corpo documental único, com atenção a:

- continuidade do fluxo Campanha → Briefing → Tradução → Arquitetura → Simulação → Consolidação;
- fronteiras entre documentos funcionais, bibliotecas, conhecimentos, problemas, motores e implementação;
- duplicações, contradições e termos históricos;
- dependências entre os documentos 01–18, 23–29 e o Plano Mestre;
- segurança para início da implementação no repositório `fernandossantor/sdm`.

---

## 2. Conclusão geral

O conjunto está **suficientemente coerente e completo para iniciar a implementação**.

A arquitetura vigente é:

```text
Documentos 01–11
→ fluxo funcional da campanha

Documentos 12–18 e complementos
→ bibliotecas, conhecimento técnico e problemas técnicos

Documentos 23–24
→ necessidade, fronteiras e validação da economia de motores

Documento 25
→ contrato comum dos motores

Documentos 26–28
→ especificação dos três motores

Documento 29
→ arquitetura de implementação e transição técnica
```

Não foi identificada necessidade de criar novos motores, novas bibliotecas estruturais ou nova etapa funcional antes da implementação.

---

## 3. Regra de precedência documental

Quando houver formulação histórica incompatível com uma definição posterior mais específica, aplicar a seguinte precedência:

```text
1. documento específico mais recente do mesmo domínio;
2. documentos 25–29 para contratos e implementação dos motores;
3. documentos 23–24 para fronteiras e economia dos motores;
4. documentos 12–18 para bibliotecas, conhecimento e problemas;
5. documentos 01–11 para etapas funcionais;
6. Plano Mestre como visão geral;
7. materiais de referência não normativos.
```

A precedência não autoriza alterar regras silenciosamente. Ela orienta a implementação quando uma redação mais antiga ainda não tiver sido atualizada.

---

## 4. Inconsistências históricas identificadas e resolução normativa

### 4.1 Objetivo de mídia no Briefing

O Plano Mestre antigo lista objetivo de mídia entre os conteúdos do Briefing. O documento `02_BRIEFING.md` e a especificação posterior consolidam que:

```text
Briefing
→ recebe objetivos declarados de Marketing e Comunicação

Tradução Estratégica
→ deriva os objetivos de Mídia
```

Portanto, objetivo de mídia **não é solução declarada obrigatória do Briefing**. Uma expectativa de mídia informada pelo anunciante pode ser registrada como pretensão, restrição ou indicação contextual, mas não substitui a derivação do Motor de Tradução Estratégica.

### 4.2 “Motor comum” e arquitetura de três motores

Referências antigas a “motor comum” devem ser entendidas como exigência de uma única base quantitativa, e não como obrigação de haver somente um motor no sistema.

A arquitetura vigente possui três motores:

1. Tradução Estratégica;
2. Decisão de Arquitetura e Cenários;
3. Simulação Técnica e Econômica.

Todos os cálculos quantitativos reutilizáveis pertencem ao terceiro motor e aos objetos versionados da Biblioteca 17. Comparação e otimização não duplicam fórmulas.

### 4.3 Comparação e otimização

Os documentos `06_COMPARACAO_DE_CENARIOS.md` e `07_OTIMIZACAO_DE_CENARIOS.md` permanecem válidos como especificações funcionais, mas suas operações são executadas como modos e procedimentos do Motor de Decisão de Arquitetura e Cenários, conforme o documento 27.

Não devem ser implementados motores independentes de Comparação ou Otimização.

### 4.4 Validação e insights

Validação e explicação são responsabilidades locais e compartilhadas dos motores. Não haverá Motor de Validação nem Motor de Insights autônomos.

### 4.5 Bibliotecas 19–21

Qualquer referência histórica a bibliotecas separadas de custos, regras ou modelos deve ser interpretada segundo a consolidação vigente:

- custos e inventários: Biblioteca 13;
- conhecimento, regras e procedimentos: Biblioteca 17;
- problemas e gatilhos: Biblioteca 18;
- modelos reutilizáveis: componentes e configurações versionadas.

---

## 5. Coerência do fluxo

O fluxo consolidado é:

```text
Campanha
→ Briefing estruturado
→ Motor de Tradução Estratégica
→ contrato estratégico
→ Motor de Decisão de Arquitetura e Cenários
→ arquiteturas e cenários candidatos
→ Motor de Simulação Técnica e Econômica
→ resultados quantitativos
→ retorno ao Motor de Decisão para comparação ou otimização
→ cenário escolhido
→ plano consolidado
→ validação e aprovação
→ acompanhamento posterior
```

O acompanhamento do realizado permanece fora dos motores de planejamento e não altera retroativamente snapshots ou planos aprovados.

---

## 6. Coerência das responsabilidades

### Motor de Tradução Estratégica

Produz objetivos operacionalizados, prioridades, pesos, relações, restrições, tensões, públicos e critérios estratégicos. Não seleciona inventários finais nem calcula resultados de mídia.

### Motor de Decisão de Arquitetura e Cenários

Gera e qualifica alternativas, atribui papéis, organiza candidatos, compara resultados e busca ajustes. Não duplica os cálculos técnicos.

### Motor de Simulação Técnica e Econômica

Calcula entrega, custos, eficiência, performance, overlap, saturação, equivalências e confiança. Não escolhe autonomamente a alternativa preferida.

As fronteiras são coerentes e não apresentam sobreposição estrutural impeditiva.

---

## 7. Coerência das bibliotecas

A distribuição vigente é:

- Biblioteca 13 — inventários, propriedades comerciais, custos e capacidades;
- Biblioteca 14 — públicos e segmentos;
- Biblioteca 15 — objetivos, resultados e KPIs;
- Biblioteca 16 — jornadas, etapas, necessidades, funções e pontos de contato;
- Biblioteca 17 — conhecimento técnico, fórmulas, regras e procedimentos;
- Biblioteca 18 — problemas técnicos, gatilhos e relações.

Os motores devem consultar essas bibliotecas por referência e versão, sem copiar catálogos para o código de orquestração.

---

## 8. Documentos normativos e materiais de referência

O arquivo `MODELO DE PLANEJAMENTO CROSS MEDIA.md` deve ser tratado como material de referência metodológica, não como contrato superior aos documentos numerados.

Durante a implementação, o Codex não deve inferir regras vigentes apenas pelo nome ou pela data de um arquivo. Deve aplicar a hierarquia desta auditoria.

---

## 9. Pontos que permanecem deliberadamente abertos

Não constituem lacunas impeditivas:

- escolha entre `dataclasses`, Pydantic ou solução equivalente;
- desenho físico definitivo das tabelas do Supabase;
- algoritmos específicos de otimização;
- fórmulas ainda dependentes de objetos da Biblioteca 17;
- granularidade final de cache;
- composição visual detalhada do Streamlit.

Essas decisões devem surgir incrementalmente, sem alterar as fronteiras conceituais.

---

## 10. Condições para iniciar a implementação

A implementação está autorizada desde que:

1. o legado seja preservado antes de exclusões;
2. a branch `main` continue recuperável por tag ou branch de preservação;
3. o esquema e dados relevantes do Supabase sejam inventariados e exportados;
4. nenhuma credencial seja impressa, versionada ou copiada para arquivos;
5. a fundação técnica seja implementada antes dos motores completos;
6. cada entrega possua testes e commit verificável;
7. mudanças destrutivas exijam confirmação explícita após apresentação do inventário.

---

## 11. Parecer final

> O diretório `docs/new_app` constitui uma especificação coerente e suficiente para iniciar a reconstrução do MediAd Planner. As inconsistências encontradas são de sedimentação histórica, não de arquitetura essencial, e ficam resolvidas pela precedência e pelas interpretações normativas deste documento.
