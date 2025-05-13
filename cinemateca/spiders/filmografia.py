from datetime import datetime

import scrapy


class FilmografiaSpider(scrapy.Spider):
    name = "filmografia"
    allowed_domains = ["cinemateca.org.br"]
    start_urls = [
        "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p"
    ]

    def form_request_factory(self, page=1):
        form_data = {
            "IsisScript": "iah/iah.xis",
            "environment": "^d/iah/^cf:/web/cinemateca/www/wwwroot/cinemateca/cgi-bin/iah/^bf:/web/cinemateca/www/wwwroot/cinemateca/bases/iah/^siah/iah.xis^v2.5.2",
            "avaibleFormats": [
                "^nstandard.pft^pSimples",
                "^ndetailed.pft^pCompleto",
                "^nfontes.pft^pFontes",
                "^nDEFAULT^fstandard.pft",
            ],
            "apperance": "^c#FFFFFF^t#1C1C1C^lblue^b#EE9A00^eiah@bireme.br^rOFF^mOFF",
            "helpInfo": "^nNOTE FORM^vfilmografia_notas.htm",
            "gizmoDecod": "",
            "avaibleForms": "F,A",
            "logoImage": "",
            "logoURL": "",
            "headerImage": "",
            "headerURL": "",
            "form": "F",
            "pathImages": "/iah/P/image/",
            "navBar": "OFF",
            "hits": "10",
            "format": "detailed.pft",
            "lang": "p",
            "user": "GUEST",
            "baseFeatures": "^eOFF",
            "nextAction": "search",
            "base": "FILMOGRAFIA",
            "exprSearch": "",
            f"Page{page}.x" if page > 1 else "x": "39",
            f"Page{page}.y" if page > 1 else "y": "13",
            "conectSearch": "and",
        }

        return scrapy.FormRequest(
            url="https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/",
            formdata=form_data,
            callback=self.parse_results,
        )

    def parse(self, response):
        # simulate the form submission when clicking the search button
        yield self.form_request_factory()

    def parse_results(self, response):
        pages = response.css("table tr td font sup b i ::text").re(
            r"página (\d+) de (\d+)"
        )
        current_page = int(pages[0])
        total_pages = int(pages[1])

        for td in response.xpath('//table//tr/td[2][.//b[@class="title"]]'):
            yield {
                "created_at": str(datetime.now()),
                "url": response.url,
                "page": current_page,
                "titulo": td.xpath('.//b[@class="title"]/text()').get(),
                "codigo_do_filme": td.xpath(
                    './/b[contains(text(),"Código do Filme")]/following::blockquote[1]/text()'
                ).get(),
                "categorias": self.get_text_next_to(td, "Categorias"),
                "material_original": self.get_text_next_to(td, "Material original"),
                "ano_de_producao": self.get_text_next_to(td, "Ano:"),
                "pais_da_producao": self.get_text_next_to(td, "País: "),
                "cidade_da_producao": self.get_text_next_to(td, "Cidade:"),
                "estado_da_producao": self.get_text_next_to(td, "Estado:"),
                "certificados": self.get_text_next_to_blockquote(td, "Certificados"),
                "data_do_lancamento": self.get_text_next_to(td, "Data:"),
                "local_do_lancamento": self.get_text_next_to(td, "Local:"),
                "sala_do_lancamento": self.get_text_next_to(td, "Sala(s):"),
                "circuito_exibidor": self.get_text_next_to_blockquote(
                    td, "Circuito exibidor"
                ),
                "sinopse": self.get_text_next_to_blockquote(td, "Sinopse"),
                "genero": self.get_text_next_to_blockquote(td, "Gênero"),
                "termos_descritores": self.get_text_next_to_blockquote(
                    td, "Termos descritores"
                ),
                "companhia_produtora": self.get_text_next_to(
                    td, "Companhia(s) produtora(s): "
                ),
                "producao": self.get_text_next_to(td, "Produção: "),
                "companhia_distribuidora": self.get_text_next_to(
                    td, "Companhia(s) distribuidora(s): "
                ),
                "argumento": self.get_text_next_to(td, "Argumento: "),
                "roteiro": self.get_text_next_to(td, "Roteiro: "),
                "dialogos": self.get_text_next_to(td, "Diálogos: "),
                "estoria": self.get_text_next_to(td, "Estória: "),
                "direcao": self.get_text_next_to(td, "Direção: "),
                "direcao_de_fotografia": self.get_text_next_to(
                    td, "Direção de fotografia: "
                ),
                "camera": self.get_text_next_to(td, "Câmera: "),
                "direcao_de_som": self.get_text_next_to(td, "Direção de som: "),
                "cenografia": self.get_text_next_to(td, "Cenografia: "),
                "identidades_elenco": self.get_text_next_to(
                    td, "Identidades/elenco: ", return_all=True
                ),
                "conteudo_examinado": self.get_text_next_to(td, "Conteúdo examinado: "),
                "fontes_utilizadas": td.xpath(
                    './/b[contains(text(), "Fontes utilizadas:")]/following-sibling::a[count(preceding-sibling::b[contains(text(), "Fontes consultadas:")]) = 0]/text()'
                ).getall(),
                "fontes_consultadas": self.get_sources(
                    td, "Fontes consultadas:", "Observações:"
                ),
                "observacoes": self.get_text_next_to(
                    td, "Observações: ", return_all=True
                ),
                "cancoes": self.parse_songs(td),
            }

        if current_page < total_pages:
            next_page = current_page + 1
            yield self.form_request_factory(next_page)

    def get_text_next_to_blockquote(self, td, label):
        result = td.xpath(
            f'.//b[text()="{label}"]/following-sibling::blockquote[1]/text()'
        ).get()
        return self.clean_text(result)

    def get_text_next_to(self, td, label, return_all=False):
        result = td.xpath(f'.//b[text()="{label}"]/following-sibling::text()')

        if not return_all:
            result = result.get()
            return self.clean_text(result)

        results = result.getall()
        return "\n".join([self.clean_text(result) for result in results])

    @staticmethod
    def clean_text(text):
        if not text:
            return text
        return text.strip("; ").strip()

    def get_sources(self, td, left_label, right_label):
        text_only = td.xpath(
            f'.//b[contains(text(), "{left_label}")]/following-sibling::text()[count(preceding-sibling::b[contains(text(), "{right_label}")]) = 0]'
        ).getall()
        with_link = td.xpath(
            f'.//b[contains(text(), "{left_label}")]/following-sibling::a[count(preceding-sibling::b[contains(text(), "{right_label}")]) = 0]/text()'
        ).getall()
        return text_only + with_link

    def parse_songs(self, td):
        songs = []

        labels = td.xpath(
            './/b[contains(text(), "Canção")]/following-sibling::b/text()[count(preceding-sibling::b[contains(text(), "Identidades/elenco:")]) = 0]'
        ).getall()
        values = td.xpath(
            './/b[contains(text(), "Canção")]/following-sibling::text()[count(preceding-sibling::b[contains(text(), "Identidades/elenco:")]) = 0]'
        ).getall()

        names = {
            "Título:": "titulo",
            "Autor da canção:": "autor",
            "Intérprete:": "interprete",
            "Componentes:": "componentes",
        }

        tmp = {}
        for label, value in zip(labels, values):
            label = label.strip()
            label = names.get(label, label)
            if label == "titulo" and tmp.get("titulo"):
                songs.append(tmp)
                tmp = {}

            value = value.strip("; ").strip()
            tmp[label] = value

        return songs
