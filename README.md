# Weather App CLI

Aplicacao de linha de comando em Python para consultar o clima atual e a previsao de varios dias para uma ou mais cidades usando a API da Open-Meteo.

## Visao Geral

O projeto recebe uma ou mais cidades, converte cada nome em coordenadas geograficas e consulta tanto as condicoes atuais quanto a previsao diaria para exibir um resumo claro no terminal.

Fluxo principal:

1. Ler uma lista de cidades informada pelo usuario.
2. Buscar latitude e longitude de cada cidade na Geocoding API da Open-Meteo.
3. Consultar o clima atual e a previsao de 5 dias na Forecast API.
4. Exibir uma tabela comparativa entre cidades.
5. Mostrar temperatura, umidade, velocidade do vento, precipitacao, descricao do clima e previsao diaria.
6. Registrar cada resposta consultada em arquivo local.
7. Reaproveitar dados em cache quando ainda estiverem validos por 1 hora.

## Destaques

- Interface simples e objetiva no terminal
- Busca automatica de coordenadas por nome da cidade
- Consulta de varias cidades em uma unica execucao
- Comparacao entre cidades em formato de tabela
- Exibicao de temperatura, umidade, velocidade do vento e precipitacao
- Previsao de 5 dias com maximas e minimas
- Traducao basica do `weathercode` para descricao legivel
- Tratamento de erros para entrada invalida, cidade nao encontrada e falhas de conexao
- Registro das respostas em arquivo para historico simples
- Cache local com validade de 1 hora

## Instalacao

### Pre-requisitos

- Python 3.10 ou superior
- `pip`

### Passos

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd weather-app/src
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Guia de Uso

Execute com:

```bash
python main.py
```

Depois disso, informe a cidade desejada no terminal.

Voce pode informar varias cidades separadas por virgula.

## Exemplo de Resultado

```text
Digite uma ou mais cidades separadas por virgula: Sao Paulo, Rio de Janeiro

Comparacao entre cidades
+----------------+--------+---------+------------+---------+----------------------+--------------+
| Cidade         | Temp.  | Umidade | Vento      | Precip. | Condicao             | Origem       |
+----------------+--------+---------+------------+---------+----------------------+--------------+
| Sao Paulo      | 24.1 C | 78 %    | 12.3 km/h  | 0.4 mm  | Parcialmente nublado | API Open-Meteo |
| Rio de Janeiro | 28.0 C | 70 %    | 9.8 km/h   | 0.0 mm  | Ceu limpo            | cache local  |
+----------------+--------+---------+------------+---------+----------------------+--------------+

================================================
Clima atual - Sao Paulo
================================================
Origem dos dados: API Open-Meteo
Temperatura: 24.1 C
Umidade: 78 %
Velocidade do vento: 12.3 km/h
Precipitacao: 0.4 mm
Condicao: Parcialmente nublado
Atualizado em: 2026-04-17T21:00

Previsao para os proximos dias - Sao Paulo
+------------+--------+--------+
| Data       | Maxima | Minima |
+------------+--------+--------+
| 2026-04-18 | 26.0 C | 18.0 C |
| 2026-04-19 | 27.0 C | 19.0 C |
+------------+--------+--------+
```

## Funcionalidades

- Consulta de clima atual por nome da cidade
- Processamento de varias cidades na mesma execucao
- Geocodificacao automatica usando a Open-Meteo
- Comparacao lado a lado entre cidades em tabela
- Exibicao de temperatura, umidade, velocidade do vento e precipitacao
- Previsao de 5 dias com temperaturas maximas e minimas
- Resposta formatada para leitura rapida no terminal
- Mensagens de erro mais amigaveis
- Registro das respostas em `weather_log.jsonl`
- Cache local em `weather_cache.json`

## Privacidade e Armazenamento Local

O projeto nao usa chave de API e nao solicita GPS do dispositivo. A localizacao usada na consulta e inferida apenas a partir do nome da cidade digitado pelo usuario.

Por padrao:

- o cache local fica ativado em `weather_cache.json` por ate 1 hora
- o log detalhado fica desativado para reduzir persistencia desnecessaria do historico de consultas

Se quiser alterar esse comportamento, configure variaveis de ambiente antes de executar:

```powershell
$env:WEATHER_APP_ENABLE_CACHE="1"
$env:WEATHER_APP_ENABLE_LOGGING="0"
python main.py
```

Valores aceitos: `1`, `true`, `yes`, `on`, `0`, `false`, `no`, `off`.

Se voce compartilhar este projeto ou rodar em uma maquina de terceiros, trate `weather_cache.json` e `weather_log.jsonl` como dados locais de uso e historico.

## Tratamento de Erros

O app lida com os casos mais comuns:

- Entrada vazia
- Cidade nao encontrada
- Falha de conexao ou erro HTTP
- Resposta incompleta da API

Quando uma cidade falha, as outras ainda continuam sendo processadas.

Se houver cache valido para a cidade, o app pode responder sem nova chamada a API.

## Registro em Arquivo

Cada consulta bem-sucedida e salva no arquivo `weather_log.jsonl`, em formato JSON Lines.

Esse arquivo pode ser usado para:

- manter um historico simples das consultas
- inspecionar respostas da API
- servir de base para analises futuras

## Cache de Dados

O projeto salva consultas em `weather_cache.json` e reutiliza os dados por ate 1 hora quando `WEATHER_APP_ENABLE_CACHE` estiver ativado.

Isso ajuda a:

- reduzir chamadas redundantes a API
- melhorar o tempo de resposta para cidades consultadas recentemente
- demonstrar uma funcionalidade avancada comum em apps reais

## Informacoes da API

Este projeto usa a [Open-Meteo](https://open-meteo.com/) como fonte de dados.

### Endpoints utilizados

- `https://geocoding-api.open-meteo.com/v1/search`
- `https://api.open-meteo.com/v1/forecast`

### Campos consultados

- `latitude`
- `longitude`
- `temperature_2m`
- `relative_humidity_2m`
- `wind_speed_10m`
- `precipitation`
- `weathercode`
- `time`
- `temperature_2m_max`
- `temperature_2m_min`

## Licencas e Atribuicoes

- Dependencia Python: `requests`, sob licenca Apache 2.0
- Dados meteorologicos: Open-Meteo, com dados da API sob licenca CC BY 4.0
- Termos de uso da Open-Meteo: o plano gratuito se aplica a uso nao comercial, sujeito aos limites e condicoes publicados pelo provedor

Detalhes e links oficiais estao em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Estrutura do Projeto

```text
src/
|-- main.py
|-- geocoding.py
|-- weather.py
|-- display.py
|-- cache.py
|-- logger.py
|-- tests/
|   |-- test_weather_app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Testes

O projeto inclui cenarios de teste automatizados com `unittest`.

Para executar:

```bash
python -m unittest tests.test_weather_app
```

Cenarios cobertos:

- parse da lista de cidades separadas por virgula
- tratamento de entrada vazia
- processamento bem-sucedido de uma cidade
- tratamento de cidade nao encontrada sem interromper o fluxo
- registro da resposta durante o processamento bem-sucedido
- validacao de dados atuais incompletos
- validacao de previsao diaria incompleta
- normalizacao da chave de cache

## Melhorias Futuras

- Aceitar argumentos pela linha de comando
- Registrar consultas recentes
- Exportar comparacoes para CSV
- Permitir configurar o tempo de validade do cache

## Tecnologias

- Python
- Requests
- Open-Meteo API

## Portfolio Tips

Para o repositorio ficar ainda mais forte no GitHub, voce pode adicionar depois:

- screenshot real do terminal em funcionamento
- GIF curto mostrando a execucao
- descricao curta do projeto na pagina principal do repositorio
- topicos como `python`, `api`, `weather`, `cli`
