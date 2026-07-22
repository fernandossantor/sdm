from pathlib import Path


ASSETS_DIR = Path(__file__).parents[1] / "assets"
PAGE_ICON = ASSETS_DIR / "barra.png"
PAGE_TITLE = "PlanOS — Plataforma Inteligente de Planejamento Híbrido de Mídia"


def titulo_pagina(nome=None):
    return f"{nome} — {PAGE_TITLE}" if nome else PAGE_TITLE
