# MediAd Planner

Este repositório contém a reconstrução limpa do MediAd Planner.

## Fonte normativa

A única especificação funcional, metodológica e arquitetural vigente está em:

```text
docs/new_app/
```

Documentos e código do aplicativo anterior foram preservados na branch:

```text
archive/mixed-state-before-clean-restart-2026-08-02
```

O legado não integra a aplicação ativa e não deve ser usado como contrato funcional.

## Estrutura ativa

```text
app.py
mediad_planner/
assets/
docs/new_app/
tests/
```

As duas imagens vigentes são `assets/Marca_nova.png` e `assets/favicon2.png`.

## Execução

```bash
streamlit run app.py
```

## Testes

```bash
pytest
```
