from engine.classificacao_papeis_engine import ClassificacaoPapeisEngine


class ClassificacaoPapeisService:

    def __init__(self):

        self.engine = ClassificacaoPapeisEngine()

    def calcular_score(self, afinidade, cobertura, consumo, objetivo=None):

        return self.engine.calcular_score(
            afinidade,
            cobertura,
            consumo,
        )

    def classificar(self, scores):

        return self.engine.classificar(scores)
