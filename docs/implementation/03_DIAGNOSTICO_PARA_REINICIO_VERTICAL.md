# Diagnóstico para reinício vertical

## Registro de restauração

- Branch verificada: `main`.
- SHA anterior ao reinício vertical: `ae3c6ae906c1d6c8a7fbe11e98b64eda6b995b14`.
- Tag anotada: `legacy/antes-do-reinicio-vertical`.
- O working tree continha alterações preexistentes em `assets/Marca.png`,
  `assets/PlanOS.png`, `assets/barra.png`, `assets/favicon.png`,
  `docs/PLANO_EVOLUCAO_INTEGRADO.md` e `docs/materials/`. Por orientação
  expressa, elas foram preservadas e ignoradas para os fins desta entrega.

Para restaurar ou consultar o código anterior, deve-se usar a tag acima. Não
foi criada uma cópia `legacy` dentro da aplicação.

## Escopo e método

Este diagnóstico inventaria o código operacional existente e define apenas seu
tratamento esperado durante a reconstrução. A classificação não autoriza
remoção nesta etapa. Os documentos normativos em `docs/new_app/`, as
configurações do Codespace, os segredos e os dados do Supabase permanecem fora
do escopo de alteração.

## Preservar temporariamente

Estes arquivos sustentam o comportamento observável atual ou sua verificação e
devem continuar disponíveis enquanto a substituição vertical ainda não cobrir
os mesmos casos:

| Arquivos | Papel atual | Motivo para preservação temporária |
| --- | --- | --- |
| `app.py` | Entrada da aplicação | Mantém o aplicativo atual executável. |
| `pages/*.py` | Telas Streamlit | Representam fluxos e comportamentos observáveis existentes. |
| `components/**/*.py` | Componentes e controles de interface | São dependências diretas das telas atuais. |
| `presentation/*.py` | Composição, navegação e estado da apresentação | Conecta a interface ao código operacional atual. |
| `tests/*.py` e `tests/sql/*.sql` | Suíte de regressão existente | Registra comportamentos e restrições que precisam ser avaliados durante a transição. |
| `requirements.txt`, `package.json` e `package-lock.json` | Dependências e ferramentas | Permitem reproduzir e testar o estado atual. |

## Substituir

Estes conjuntos contêm lógica que deve migrar para a estrutura mínima em
`src/`. A substituição será orientada por comportamento e exige etapas futuras;
nada desta seção foi removido ou copiado agora.

| Arquivos | Destino conceitual | Observação |
| --- | --- | --- |
| `domain/**/*.py` | `src/domain/` | Modelos e regras atuais devem ser reavaliados caso a caso contra os contratos normativos. |
| `engine/**/*.py` | `src/engines/` | Motores legados não são adotados automaticamente como referência. |
| `engines/**/*.py` | `src/engines/` | Implementação mais recente também precisa de validação comportamental antes de migrar. |
| `application/**/*.py` | `src/application/` | Casos de uso e serviços serão substituídos apenas quando houver comportamento especificado e testado. |

O diretório `src/knowledge/` é o destino reservado para conhecimento
formalizado em etapas futuras. Nenhum arquivo operacional atual foi promovido
automaticamente a essa camada.

## Descartar

Os itens abaixo são candidatos a descarte futuro por serem artefatos duplicados
ou não constituírem fonte operacional canônica. O descarte depende de uma etapa
explicitamente autorizada.

| Arquivos | Justificativa |
| --- | --- |
| `projeto.zip` | Cópia empacotada do repositório; o histórico Git é o mecanismo de preservação definido para o reinício. |
| `database/sql/*.sql` e `database/sql/seed/*.sql` | Série SQL paralela às migrações do Supabase; deve deixar de ser mantida como segunda fonte após confirmação de cobertura. |

## Avaliar posteriormente

Estes arquivos têm dependência externa, função de apoio ou situação que não pode
ser decidida com segurança nesta preparação:

| Arquivos | Questão a avaliar |
| --- | --- |
| `infrastructure/**/*.py` | Definir adaptadores necessários somente depois dos contratos independentes de Supabase. |
| `supabase/migrations/*.sql`, `supabase/rollbacks/*.sql` e `supabase/config.toml` | Preservar o estado de persistência; avaliar compatibilidade quando houver portas e adaptadores novos. |
| `scripts/*.py` | Confirmar quais rotinas ainda são necessárias e quais dependem do modelo legado. |
| `data/*.csv` | Verificar proveniência, validade e eventual papel como fonte de conhecimento. |
| `assets/*` | Confirmar uso pela interface que sobreviver à reconstrução; inclui alterações preexistentes fora desta entrega. |

## Estrutura mínima preparada

Foram reservados, sem lógica de negócio, os diretórios:

```text
src/
├── domain/
├── engines/
├── knowledge/
└── application/

tests/
├── fixtures/
└── unit/
```

Arquivos `.gitkeep` mantêm os diretórios vazios sob controle de versão. Não há
motores, modelos, serviços, regras, fórmulas, taxonomias ou estados novos.

## Limites desta etapa

- Nenhum arquivo operacional existente foi removido.
- Nenhuma lógica foi implementada ou migrada.
- Nenhuma alteração foi feita em `docs/new_app/`.
- Nenhuma operação foi executada contra o Supabase.
- A classificação registra intenção de transição, não uma decisão de remoção
  imediata.
