from django.db import models

class DispositivoESP(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=80, unique=True)
    localizacao = models.CharField(max_length=150, blank=True, default='')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Dispositivo ESP'
        verbose_name_plural = 'Dispositivos ESP'

    def __str__(self):
        return f'{self.nome} ({self.codigo})'

class LeituraSensor(models.Model):
    dispositivo = models.ForeignKey(DispositivoESP, on_delete=models.CASCADE, related_name='leituras')
    temperatura = models.FloatField(help_text='Temperatura em °C')
    umidade = models.FloatField(help_text='Umidade em %')
    pressao = models.FloatField(null=True, blank=True, help_text='Pressão em hPa')
    chuva = models.FloatField(null=True, blank=True, help_text='Valor analógico ou percentual do sensor de chuva')
    luminosidade = models.FloatField(null=True, blank=True, help_text='Valor opcional do sensor de luminosidade')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Leitura do Sensor'
        verbose_name_plural = 'Leituras dos Sensores'

    def __str__(self):
        return f'{self.dispositivo.codigo}: {self.temperatura}°C / {self.umidade}%'

class PrevisaoClimatica(models.Model):
    leitura = models.OneToOneField(LeituraSensor, on_delete=models.CASCADE, related_name='previsao')
    condicao = models.CharField(max_length=80)
    probabilidade_chuva = models.FloatField(default=0)
    alerta = models.CharField(max_length=120, blank=True, default='')
    recomendacao = models.TextField(blank=True, default='')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Previsão Climática'
        verbose_name_plural = 'Previsões Climáticas'

    def __str__(self):
        return f'{self.condicao} - {self.probabilidade_chuva}%'
