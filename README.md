# filmografia-brasileira

Raspador da base de dados da [filmografia brasileira](https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p) 📽️🇧🇷

Dados disponíveis em formato JSON na página de [releases](https://github.com/anapaulagomes/cinemateca-brasileira/releases).

## Uso

> Antes de executar o raspador, verifique no site da Cinemateca
> quando foi a última atualização para evitar requisições desnecessárias.
> A base de dados publicada aqui tem em sua última versão 57.495 registros.

Para executar o código, você precisa ter o Python 3.13 ou superior instalado,
junto com o [uv](https://docs.astral.sh/uv/). Então, execute: `uv sync` para instalar as dependências.
Ative o ambiente virtual com `source .venv/bin/activate` e execute o raspador com:

```bash
scrapy crawl filmografia -o filmografia.json
```
