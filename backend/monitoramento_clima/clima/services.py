from .models import LeituraSensor, PrevisaoClimatica

def gerar_previsao(leitura: LeituraSensor) -> PrevisaoClimatica:
    probabilidade = 15.0

    if leitura.umidade >= 85:
        probabilidade += 35
    elif leitura.umidade >= 70:
        probabilidade += 22
    elif leitura.umidade >= 60:
        probabilidade += 10

    if leitura.pressao is not None:
        if leitura.pressao < 1005:
            probabilidade += 30
        elif leitura.pressao < 1012:
            probabilidade += 15

    if leitura.chuva is not None:
        if leitura.chuva >= 70:
            probabilidade += 30
        elif leitura.chuva >= 40:
            probabilidade += 15

    probabilidade = min(probabilidade, 100.0)

    if probabilidade >= 75:
        condicao = 'Chuva provável'
        alerta = 'Alerta de chuva'
        recomendacao = 'Evitar exposição de equipamentos e levar guarda-chuva.'
    elif probabilidade >= 45:
        condicao = 'Tempo instável'
        alerta = 'Atenção'
        recomendacao = 'Acompanhar as próximas leituras antes de atividades externas.'
    elif leitura.temperatura >= 32 and leitura.umidade < 55:
        condicao = 'Quente e seco'
        alerta = 'Calor elevado'
        recomendacao = 'Reforçar hidratação e ventilação do ambiente.'
    else:
        condicao = 'Tempo estável'
        alerta = 'Sem alerta crítico'
        recomendacao = 'Condições normais para o ambiente monitorado.'

    return PrevisaoClimatica.objects.create(
        leitura=leitura,
        condicao=condicao,
        probabilidade_chuva=probabilidade,
        alerta=alerta,
        recomendacao=recomendacao,
    )
