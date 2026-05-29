# Sistema de Monitoramento Climático com ESP32 - PI Quarto Termo

**Integrantes:** João Henrique, Guilherme, Marcos e Thales

**Docente:** Professora Doutora Luciene Cristina Alves Rinaldi

---

# Estrutura

## Hardware

* ESP32 DevKit V1
* Sensor DHT22
* Sensor de Chuva
* Protoboard
* Jumpers

## Backend

* Python
* Flask
* Flask-CORS

## Banco de Dados

* MySQL

## Frontend

* React
* Axios
* CSS

---

# Como Rodar

## 1. Banco de Dados

Criar o banco de dados:

```sql
CREATE DATABASE clima_esp;
```

Importar o arquivo:

```bash
mysql -u root -p clima_esp < schema.sql
```

---

## 2. Backend

Acesse a pasta:

```bash
cd backend
```

Instale as dependências:

```bash
pip install flask flask-cors mysql-connector-python
```

Execute:

```bash
python app.py
```

---

## 3. Frontend

Acesse a pasta:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Execute:

```bash
npm start
```

ou

```bash
npm run dev
```

---

## 4. ESP32

Abra o arquivo:

```txt
clima_esp32.ino
```

Configure:

```cpp
const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";

const char* serverUrl =
"http://IP_DO_COMPUTADOR:5000/api/clima/leituras";
```

Depois envie o código para o ESP32 utilizando a Arduino IDE.

---

# Para Acessar

## Frontend

```txt
http://localhost:3000
```

## Backend API

```txt
http://localhost:5000
```

---

# Bibliotecas Arduino Utilizadas

Instalar na Arduino IDE:

```txt
DHT sensor library
Adafruit Unified Sensor
ArduinoJson
```

Bibliotecas nativas do ESP32:

```txt
WiFi.h
HTTPClient.h
```

---

# Funcionalidades

* Monitoramento de temperatura;
* Monitoramento de umidade;
* Monitoramento de chuva;
* Envio de dados via Wi-Fi;
* Armazenamento em banco de dados;
* Histórico das leituras;
* Dashboard web para visualização dos dados.

---

# Fluxo do Sistema

```txt
DHT22
   ↓
ESP32
   ↓
HTTP POST
   ↓
Backend Flask
   ↓
MySQL
   ↓
HTTP GET
   ↓
Frontend React
   ↓
Dashboard
```

---

# Materiais Utilizados Durante o PI

Todos os materiais do projeto encontram-se na pasta:

```txt
Materiais
```

Nesta pasta estão disponíveis:

* Relatório Final;
* Diagramas;
* Imagens do projeto;
* Apresentação;
* Documentação Técnica.

---

# Vídeo da Apresentação

```txt
https://drive.google.com/
```

---

# Link do Trello

```txt
https://trello.com/b/XZt7qCC6
```

---

# Relatório

O relatório completo e os arquivos do projeto encontram-se na pasta:

```txt
Materiais
```

---

# Objetivo do Projeto

Desenvolver um sistema de monitoramento climático baseado em Internet das Coisas (IoT), utilizando ESP32 para coleta de dados ambientais, backend Flask para processamento das informações, banco de dados MySQL para armazenamento das leituras e interface web React para visualização dos dados em tempo real.
