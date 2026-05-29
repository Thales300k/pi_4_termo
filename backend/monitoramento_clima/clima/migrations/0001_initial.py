from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='DispositivoESP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=80, unique=True)),
                ('localizacao', models.CharField(blank=True, default='', max_length=150)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Dispositivo ESP', 'verbose_name_plural': 'Dispositivos ESP', 'ordering': ['nome']},
        ),
        migrations.CreateModel(
            name='LeituraSensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.FloatField(help_text='Temperatura em °C')),
                ('umidade', models.FloatField(help_text='Umidade em %')),
                ('pressao', models.FloatField(blank=True, help_text='Pressão em hPa', null=True)),
                ('chuva', models.FloatField(blank=True, help_text='Valor analógico ou percentual do sensor de chuva', null=True)),
                ('luminosidade', models.FloatField(blank=True, help_text='Valor opcional do sensor de luminosidade', null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leituras', to='clima.dispositivoesp')),
            ],
            options={'verbose_name': 'Leitura do Sensor', 'verbose_name_plural': 'Leituras dos Sensores', 'ordering': ['-criado_em']},
        ),
        migrations.CreateModel(
            name='PrevisaoClimatica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicao', models.CharField(max_length=80)),
                ('probabilidade_chuva', models.FloatField(default=0)),
                ('alerta', models.CharField(blank=True, default='', max_length=120)),
                ('recomendacao', models.TextField(blank=True, default='')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('leitura', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='previsao', to='clima.leiturasensor')),
            ],
            options={'verbose_name': 'Previsão Climática', 'verbose_name_plural': 'Previsões Climáticas', 'ordering': ['-criado_em']},
        ),
    ]
