"""Entrada canônica da primeira fatia vertical de tradução estratégica.

Os valores ``None`` representam informação não fornecida. Eles não devem ser
convertidos em zero por consumidores desta fixture.
"""

CAMPANHA_CANONICA = {
    "identificacao": {
        "id": "campanha-canonica-lume-2026",
        "nome": "Lume Casa — Primavera 2026",
        "marca": "Lume Casa",
        "produto_ou_servico": "assinatura de energia solar residencial",
    },
    "situacao_marca_mercado": {
        "resumo": (
            "A Lume Casa tem notoriedade alta na praça, mas poucas pessoas que "
            "visitam sua página concluem o pedido de proposta. O mercado tem "
            "ofertas semelhantes e o público relata receio sobre economia real "
            "e prazo de retorno."
        ),
    },
    "objetivos_marketing": [
        {
            "ordem_declarada": 1,
            "categoria": "aumento de vendas",
            "prioridade": "muito alta",
        },
        {
            "ordem_declarada": 2,
            "categoria": "crescimento",
            "prioridade": "alta",
        },
    ],
    "objetivos_comunicacao_candidatos": [
        "intenção",
        "redução de incerteza",
        "notoriedade",
    ],
    "publico_prioritario": {
        "nome": "Responsáveis pela decisão de energia residencial",
        "descricao": (
            "Pessoas de 30 a 55 anos, responsáveis pela decisão financeira do "
            "domicílio, que pesquisaram redução da conta de energia."
        ),
        "praca": "Campinas (SP)",
        "prioridade": "muito alta",
        "tamanho_estimado": None,
    },
    "segmento_secundario": {
        "nome": "Interessados sem pesquisa recente",
        "descricao": (
            "Responsáveis pela decisão financeira do domicílio que demonstram "
            "interesse em sustentabilidade, sem pesquisa recente sobre redução "
            "da conta de energia."
        ),
        "praca": "Campinas (SP)",
        "prioridade": "média",
        "tamanho_estimado": None,
    },
    "praca": {
        "nome": "Campinas (SP)",
        "tipo_territorial": "município",
        "universo_populacional": None,
    },
    "periodo": {
        "data_inicial": "2026-09-01",
        "data_final": "2026-10-31",
    },
    "verba": {
        "valor_total": 300_000,
        "moeda": "BRL",
        "natureza_do_limite": "rígido",
        "margem_de_flexibilidade": None,
    },
    "prioridade": {
        "entidade": "publico_prioritario",
        "nivel": "muito alta",
    },
    "restricao": {
        "categoria": "orçamentária",
        "descricao": "A verba total não pode ultrapassar BRL 300.000.",
        "entidade_afetada": "campanha",
        "intensidade": "muito alta",
        "prioridade": "muito alta",
        "origem": "anunciante",
        "justificativa": "Teto financeiro aprovado para o período.",
    },
    "tensao_estrategica": {
        "descricao": (
            "Aumento de vendas no curto período e crescimento disputam a mesma "
            "verba rígida."
        ),
        "elementos": [
            "aumento de vendas",
            "crescimento",
            "período de dois meses",
            "verba rígida",
        ],
    },
    "indicadores_disponiveis": [
        {
            "metrica": "notoriedade auxiliada",
            "valor": 78,
            "unidade_de_mensuracao": "percentual",
            "natureza_do_valor": "OBSERVADO",
            "publico_ou_target": "Responsáveis pela decisão de energia residencial",
            "territorio": "Campinas (SP)",
            "periodo_de_referencia": "2026-06",
            "fonte": "Pesquisa fictícia Lume Tracking",
            "metodologia": "levantamento amostral declarado pelo anunciante",
            "nivel_de_confianca": "MEDIA",
        },
        {
            "metrica": "taxa de conclusão do pedido de proposta",
            "valor": 1.1,
            "unidade_de_mensuracao": "percentual",
            "natureza_do_valor": "OBSERVADO",
            "publico_ou_target": "visitantes da página de proposta",
            "territorio": "Campinas (SP)",
            "periodo_de_referencia": "2026-06",
            "fonte": "Analytics fictício Lume Casa",
            "metodologia": "pedidos concluídos divididos por visitas à página",
            "nivel_de_confianca": "MEDIA",
        },
    ],
    "dados_ausentes": {
        "meta_de_vendas": None,
        "linha_de_base_de_vendas": None,
        "indicador_de_intencao": None,
        "tamanho_do_publico_prioritario": None,
        "tamanho_do_segmento_secundario": None,
        "universo_populacional_da_praca": None,
        "ciclo_de_compra": None,
    },
}
