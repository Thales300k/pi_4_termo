import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { CloudRain, Cpu, Droplets, RefreshCw, Thermometer, Wifi, Gauge, Database } from 'lucide-react';
import './styles.css';

type Dispositivo = { id:number; nome:string; codigo:string; localizacao:string; ativo:boolean; criado_em:string };
type Leitura = { id:number; dispositivo_id:number; temperatura:number; umidade:number; pressao?:number|null; chuva?:number|null; luminosidade?:number|null; criado_em:string };
type Previsao = { id:number; leitura_id:number; condicao:string; probabilidade_chuva:number; alerta:string; recomendacao:string; criado_em:string };

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/clima';

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!response.ok) throw new Error(await response.text() || 'Erro ao conectar com a API');
  return response.json();
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('pt-BR', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' }).format(new Date(value));
}

function App() {
  const [dispositivos, setDispositivos] = useState<Dispositivo[]>([]);
  const [leituras, setLeituras] = useState<Leitura[]>([]);
  const [previsao, setPrevisao] = useState<Previsao | null>(null);
  const [codigo, setCodigo] = useState('ESP-CLIMA-01');
  const [mensagem, setMensagem] = useState('');
  const [loading, setLoading] = useState(false);
  const [formDispositivo, setFormDispositivo] = useState({ nome:'ESP Clima 01', codigo:'ESP-CLIMA-01', localizacao:'Laboratório' });
  const [formLeitura, setFormLeitura] = useState({ temperatura:26, umidade:70, pressao:1012, chuva:20, luminosidade:650 });

  const ultima = leituras[0];
  const dadosGrafico = useMemo(() => [...leituras].reverse().slice(-20).map(l => ({ horario: formatDate(l.criado_em), temperatura:l.temperatura, umidade:l.umidade, pressao:l.pressao || 0 })), [leituras]);

  async function carregar(codigoAtual = codigo) {
    setLoading(true); setMensagem('');
    try {
      const disp = await api<Dispositivo[]>('/dispositivos');
      setDispositivos(disp);
      const alvo = codigoAtual || disp[0]?.codigo || '';
      if (alvo) {
        setCodigo(alvo);
        setLeituras(await api<Leitura[]>(`/leituras?codigo_dispositivo=${encodeURIComponent(alvo)}`));
        setPrevisao(await api<Previsao>(`/previsao-atual/${encodeURIComponent(alvo)}`).catch(() => null));
      }
    } catch (err) {
      setMensagem(err instanceof Error ? err.message : 'Erro inesperado');
    } finally { setLoading(false); }
  }

  useEffect(() => { carregar(); }, []);

  async function cadastrarDispositivo(e: React.FormEvent) {
    e.preventDefault(); setLoading(true);
    try {
      await api<Dispositivo>('/dispositivos', { method:'POST', body: JSON.stringify({ ...formDispositivo, ativo:true }) });
      setMensagem('Dispositivo cadastrado.');
      await carregar(formDispositivo.codigo);
    } catch (err) { setMensagem(err instanceof Error ? err.message : 'Erro ao cadastrar ESP'); }
    finally { setLoading(false); }
  }

  async function enviarLeitura(e: React.FormEvent) {
    e.preventDefault(); setLoading(true);
    try {
      await api<Leitura>('/leituras', { method:'POST', body: JSON.stringify({ codigo_dispositivo: codigo, ...formLeitura }) });
      setMensagem('Leitura enviada para o banco e previsão atualizada.');
      await carregar(codigo);
    } catch (err) { setMensagem(err instanceof Error ? err.message : 'Erro ao enviar leitura'); }
    finally { setLoading(false); }
  }

  return <main className="page">
    <section className="hero">
      <div>
        <span className="badge"><Wifi size={16}/> ESP32 + Sensores + Interface</span>
        <h1>Monitoramento de Temperatura e Clima</h1>
        <p>Interface para receber leituras do sensor, armazenar no backend Django e visualizar temperatura, umidade, pressão, chuva e previsão.</p>
      </div>
      <button className="refresh" onClick={() => carregar()} disabled={loading}><RefreshCw size={18}/> Atualizar</button>
    </section>

    {mensagem && <div className="message">{mensagem}</div>}

    <section className="cards">
      <div className="card status"><CloudRain size={32}/><span>Previsão</span><strong>{previsao?.condicao || 'Sem dados'}</strong><small>{previsao?.recomendacao || 'Envie uma leitura para gerar previsão.'}</small></div>
      <div className="card"><Thermometer size={30}/><span>Temperatura</span><strong>{ultima ? `${ultima.temperatura} °C` : '--'}</strong></div>
      <div className="card"><Droplets size={30}/><span>Umidade</span><strong>{ultima ? `${ultima.umidade}%` : '--'}</strong></div>
      <div className="card"><Gauge size={30}/><span>Pressão</span><strong>{ultima?.pressao ? `${ultima.pressao} hPa` : '--'}</strong></div>
    </section>

    <section className="grid-two">
      <form className="panel" onSubmit={cadastrarDispositivo}>
        <h2><Cpu size={20}/> Cadastro do ESP</h2>
        <label>Nome<input value={formDispositivo.nome} onChange={e => setFormDispositivo({...formDispositivo, nome:e.target.value})}/></label>
        <label>Código<input value={formDispositivo.codigo} onChange={e => setFormDispositivo({...formDispositivo, codigo:e.target.value})}/></label>
        <label>Localização<input value={formDispositivo.localizacao} onChange={e => setFormDispositivo({...formDispositivo, localizacao:e.target.value})}/></label>
        <button disabled={loading}>Cadastrar dispositivo</button>
      </form>

      <form className="panel" onSubmit={enviarLeitura}>
        <h2><Database size={20}/> Enviar leitura teste</h2>
        <label>Dispositivo<select value={codigo} onChange={e => carregar(e.target.value)}>{dispositivos.map(d => <option key={d.id} value={d.codigo}>{d.nome} - {d.codigo}</option>)}<option value="ESP-CLIMA-01">ESP-CLIMA-01</option></select></label>
        <div className="form-grid">
          <label>Temperatura<input type="number" value={formLeitura.temperatura} onChange={e => setFormLeitura({...formLeitura, temperatura:Number(e.target.value)})}/></label>
          <label>Umidade<input type="number" value={formLeitura.umidade} onChange={e => setFormLeitura({...formLeitura, umidade:Number(e.target.value)})}/></label>
          <label>Pressão<input type="number" value={formLeitura.pressao} onChange={e => setFormLeitura({...formLeitura, pressao:Number(e.target.value)})}/></label>
          <label>Chuva<input type="number" value={formLeitura.chuva} onChange={e => setFormLeitura({...formLeitura, chuva:Number(e.target.value)})}/></label>
        </div>
        <button disabled={loading}>Salvar leitura</button>
      </form>
    </section>

    <section className="panel chart-panel">
      <h2>Histórico das leituras</h2>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={dadosGrafico}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="horario"/><YAxis/><Tooltip/><Area type="monotone" dataKey="temperatura" name="Temperatura"/><Area type="monotone" dataKey="umidade" name="Umidade"/></AreaChart>
      </ResponsiveContainer>
    </section>

    <section className="panel">
      <h2>Últimas medições recebidas</h2>
      <div className="table-wrap"><table><thead><tr><th>Data</th><th>Temp.</th><th>Umidade</th><th>Pressão</th><th>Chuva</th></tr></thead><tbody>{leituras.map(l => <tr key={l.id}><td>{formatDate(l.criado_em)}</td><td>{l.temperatura} °C</td><td>{l.umidade}%</td><td>{l.pressao || '-'}</td><td>{l.chuva || '-'}</td></tr>)}</tbody></table></div>
    </section>
  </main>;
}

createRoot(document.getElementById('root')!).render(<App/>);
