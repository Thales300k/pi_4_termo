from datetime import datetime
from typing import Optional
from ninja import Schema

class DispositivoSchema(Schema):
    id: int
    nome: str
    codigo: str
    localizacao: str
    ativo: bool
    criado_em: datetime

class DispositivoCreateSchema(Schema):
    nome: str
    codigo: str
    localizacao: Optional[str] = ''
    ativo: Optional[bool] = True

class LeituraSchema(Schema):
    id: int
    dispositivo_id: int
    temperatura: float
    umidade: float
    pressao: Optional[float] = None
    chuva: Optional[float] = None
    luminosidade: Optional[float] = None
    criado_em: datetime

class LeituraCreateSchema(Schema):
    codigo_dispositivo: str
    temperatura: float
    umidade: float
    pressao: Optional[float] = None
    chuva: Optional[float] = None
    luminosidade: Optional[float] = None

class PrevisaoSchema(Schema):
    id: int
    leitura_id: int
    condicao: str
    probabilidade_chuva: float
    alerta: str
    recomendacao: str
    criado_em: datetime

class ResumoSchema(Schema):
    total_dispositivos: int
    total_leituras: int
    ultima_temperatura: Optional[float] = None
    ultima_umidade: Optional[float] = None
    ultima_condicao: Optional[str] = None
