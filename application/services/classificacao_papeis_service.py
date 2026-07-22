from engine.classificacao_papeis_engine import ClassificacaoPapeisEngine


class ClassificacaoPapeisService:

    def __init__(self):

        self.engine = ClassificacaoPapeisEngine()

    def calcular_score(self, afinidade, cobertura, consumo, objetivo=None, jornada=0, pesos=None):

        return self.engine.calcular_score(
            afinidade,
            cobertura,
            consumo,
            jornada=jornada,
            pesos=pesos,
        )

    def classificar(self, scores):

        return self.engine.classificar(scores)
