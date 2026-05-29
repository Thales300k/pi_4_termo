-- Schema de referência. O Django cria as tabelas automaticamente via migrations.
CREATE TABLE dispositivo_esp (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome VARCHAR(100) NOT NULL,
  codigo VARCHAR(80) UNIQUE NOT NULL,
  localizacao VARCHAR(150),
  ativo BOOLEAN DEFAULT 1,
  criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leitura_sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dispositivo_id INTEGER NOT NULL,
  temperatura REAL NOT NULL,
  umidade REAL NOT NULL,
  pressao REAL,
  chuva REAL,
  luminosidade REAL,
  criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (dispositivo_id) REFERENCES dispositivo_esp(id)
);

CREATE TABLE previsao_climatica (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  leitura_id INTEGER UNIQUE NOT NULL,
  condicao VARCHAR(80) NOT NULL,
  probabilidade_chuva REAL DEFAULT 0,
  alerta VARCHAR(120),
  recomendacao TEXT,
  criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (leitura_id) REFERENCES leitura_sensor(id)
);
