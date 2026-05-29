from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from .models import DispositivoESP, LeituraSensor, PrevisaoClimatica
from .schemas import (
    DispositivoSchema,
    DispositivoCreateSchema,
    LeituraSchema,
    LeituraCreateSchema,
    PrevisaoSchema,
    ResumoSchema,
)
from .services import gerar_previsao

router = Router()

@router.get('/health')
def health(request):
    return {'status': 'online', 'servico': 'monitoramento-climatico'}

@router.post('/dispositivos', response=DispositivoSchema)
def criar_dispositivo(request, payload: DispositivoCreateSchema):
    if DispositivoESP.objects.filter(codigo=payload.codigo).exists():
        raise HttpError(400, 'Já existe um ESP com esse código.')
    return DispositivoESP.objects.create(**payload.dict())

@router.get('/dispositivos', response=list[DispositivoSchema])
def listar_dispositivos(request):
    return DispositivoESP.objects.all()

@router.post('/leituras', response=LeituraSchema)
def receber_leitura(request, payload: LeituraCreateSchema):
    dispositivo = get_object_or_404(DispositivoESP, codigo=payload.codigo_dispositivo, ativo=True)
    leitura = LeituraSensor.objects.create(
        dispositivo=dispositivo,
        temperatura=payload.temperatura,
        umidade=payload.umidade,
        pressao=payload.pressao,
        chuva=payload.chuva,
        luminosidade=payload.luminosidade,
    )
    gerar_previsao(leitura)
    return leitura

@router.get('/leituras', response=list[LeituraSchema])
def listar_leituras(request, codigo_dispositivo: str = None):
    queryset = LeituraSensor.objects.select_related('dispositivo')
    if codigo_dispositivo:
        queryset = queryset.filter(dispositivo__codigo=codigo_dispositivo)
    return queryset[:100]

@router.get('/previsoes', response=list[PrevisaoSchema])
def listar_previsoes(request):
    return PrevisaoClimatica.objects.select_related('leitura')[:100]

@router.get('/previsao-atual/{codigo_dispositivo}', response=PrevisaoSchema)
def previsao_atual(request, codigo_dispositivo: str):
    previsao = PrevisaoClimatica.objects.filter(
        leitura__dispositivo__codigo=codigo_dispositivo
    ).order_by('-criado_em').first()
    if not previsao:
        raise HttpError(404, 'Nenhuma previsão encontrada para esse dispositivo.')
    return previsao

@router.get('/resumo', response=ResumoSchema)
def resumo(request):
    ultima = LeituraSensor.objects.first()
    previsao = getattr(ultima, 'previsao', None) if ultima else None
    return {
        'total_dispositivos': DispositivoESP.objects.count(),
        'total_leituras': LeituraSensor.objects.count(),
        'ultima_temperatura': ultima.temperatura if ultima else None,
        'ultima_umidade': ultima.umidade if ultima else None,
        'ultima_condicao': previsao.condicao if previsao else None,
    }
