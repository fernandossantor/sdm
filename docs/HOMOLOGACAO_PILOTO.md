# Homologação e piloto controlado

Revisão: 31 de julho de 2026 (UTC).

## Estado atual

O gate automatizado conectado foi repetido e aprovado em 31 de julho de 2026, antes e depois da desativação das chaves legadas:

- 195 testes pytest aprovados e 3 integrações opcionais ignoradas;
- regressão funcional;
- health check de 20 estruturas operacionais e multiusuário;
- auditoria de bloqueio público;
- 3 testes de integração autenticados;
- 27 migrations locais e remotas sincronizadas;
- chaves legadas `anon` e `service_role` desativadas.

Executar novamente depois da rotação de segredos:

```bash
python -m scripts.homologar --connected --saida /tmp/planos-homologacao.json
```

O arquivo de evidência fica fora do repositório e não deve conter segredos.

## Gates anteriores ao piloto

Parâmetros confirmados em 31 de julho de 2026:

- participante inicial e responsável primário: Fernando Santor;
- canal de suporte: GitHub Issues do repositório `fernandossantor/sdm`;
- período: 1 a 7 de agosto de 2026 (UTC);
- retenção: 90 dias após o encerramento;
- continuidade individual: conta alternativa privada do próprio responsável;
- substituto independente: não aplicável; a indisponibilidade do responsável suspende o piloto.

- [x] chave administrativa rotacionada;
- [ ] `.env` local atualizado sem versionamento;
- [x] segredos da hospedagem atualizados;
- [x] `PLANOS_ENV=production`;
- [x] `PLANOS_AUTH_ENABLED=true`;
- [x] gate conectado aprovado após a rotação e a desativação das chaves legadas;
- [x] backup completo posterior à rotação validado;
- [x] restauração desse backup ensaiada;
- [x] CI do commit candidato aprovado;
- [x] participantes e período do piloto registrados;
- [x] aviso de privacidade e limitações apresentado e aceito pelo participante ([modelo](AVISO_PILOTO.md));
- [x] continuidade operacional individual formalizada; indisponibilidade do responsável suspende o piloto;
- [x] canal de suporte e registro de incidentes definido.

Qualquer item aberto impede o início do piloto.

## Escopo do piloto do novo app

O aplicativo legado está arquivado e não integra o escopo funcional. A fonte normativa é `docs/new_app`, conforme a decisão registrada em `docs/implementation/05_DECISAO_ARQUIVAMENTO_LEGADO.md`.

A homologação é incremental e acompanha capacidades efetivamente implementadas. A ausência de uma funcionalidade prevista para etapa futura não deve ser mascarada como aprovação nem tratada como regressão do legado.

## Roteiro funcional da etapa atual

1. entrar com autenticação habilitada;
2. selecionar um espaço autorizado;
3. criar uma Campanha com o planejador responsável válido para o espaço;
4. confirmar que Nova campanha não retoma silenciosamente um registro anterior;
5. confirmar persistência, código e snapshot administrativo da Campanha;
6. iniciar o Briefing v1 de forma atômica;
7. confirmar herança do contexto da Campanha no Briefing;
8. confirmar que etapas futuras aparecem somente com o grau de disponibilidade real;
9. validar que usuário sem vínculo não acessa dados do espaço;
10. registrar falhas, ressalvas e evidências no issue do piloto.

## Gates funcionais posteriores

Serão abertos progressivamente, conforme `docs/new_app`:

1. Briefing estruturado completo;
2. Motor de Tradução Estratégica;
3. Motor de Decisão de Arquitetura e Cenários;
4. Motor de Simulação Técnica e Econômica;
5. comparação, otimização e escolha de cenário;
6. plano consolidado, cronograma, mapa e exportações;
7. acompanhamento, compartilhamento e demais controles previstos.

Cada gate posterior exigirá implementação, testes e homologação próprios.

## Aceite

O piloto é aprovado somente quando:

- nenhuma falha crítica de isolamento, autenticação ou perda de dados ocorrer;
- cálculos e exportações forem reproduzíveis;
- orçamento, quantidades e cronograma reconciliarem;
- lacunas e limitações forem visíveis;
- leitor não editar e usuário sem vínculo não acessar;
- revogação retirar o acesso;
- erros relevantes tiverem registro e resposta;
- feedback dos participantes estiver classificado e rastreável.

## Interrupção imediata

Suspender o piloto e desabilitar o acesso quando houver:

- exposição de segredo ou dado pessoal;
- acesso cruzado não autorizado;
- perda, alteração indevida ou corrupção de dados;
- backup não recuperável;
- indisponibilidade persistente sem diagnóstico;
- divergência financeira ou metodológica silenciosa.
