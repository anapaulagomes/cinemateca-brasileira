import scrapy


class FilmografiaSpider(scrapy.Spider):
    name = 'filmografia'
    allowed_domains = ['cinemateca.org.br']
    start_urls = [
        "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p"
    ]

    def parse(self, response):
        # simulate the form submission when clicking the search button
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
            "x": "39",
            "y": "11",
            "conectSearch": "and",
        }

        yield scrapy.FormRequest(
            url="https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/",
            formdata=form_data,
            callback=self.parse_results,
        )

    def parse_results(self, response):
        for td in response.xpath('//table//tr/td[2][.//b[@class="title"]]'):
            yield {
                'titulo': td.xpath('.//b[@class="title"]/text()').get(),
                'codigo_do_filme': td.xpath('.//b[contains(text(),"Código do Filme")]/following::blockquote[1]/text()').get(),
                'categorias': td.xpath('.//b[text()="Categorias"]/following-sibling::text()').get(),
                'material_original': td.xpath('.//b[text()="Material original"]/following-sibling::text()').get(),
                'ano_de_producao': td.xpath('.//b[text()="Ano:"]/following-sibling::text()').get(),  # TODO .strip() etc
                'pais_da_producao': td.xpath('.//b[text()="País: "]/following-sibling::text()').get(),  # TODO .strip() etc
                'cidade_da_producao': td.xpath('.//b[text()="Cidade:"]/following-sibling::text()').get(),  # TODO .strip() etc
                'estado_da_producao': td.xpath('.//b[text()="Estado:"]/following-sibling::text()').get(),  # TODO .strip() etc
                'certificados': td.xpath(f'.//b[text()="Certificados"]/following-sibling::blockquote[1]/text()').get(),  # TODO .strip() etc
                'data_do_lancamento': td.xpath('.//b[text()="Data:"]/following-sibling::text()').get(),
                'local_do_lancamento': td.xpath('.//b[text()="Local:"]/following-sibling::text()').get(),
                'sala_do_lancamento': td.xpath('.//b[text()="Sala(s):"]/following-sibling::text()').get(),
                'circuito_exibidor': td.xpath('.//b[text()="Circuito exibidor"]/following-sibling::blockquote[1]/text()').get(),
                'sinopse': td.xpath('.//b[text()="Sinopse"]/following-sibling::blockquote[1]/text()').get(),
                'genero': td.xpath('.//b[text()="Gênero"]/following-sibling::blockquote[1]/text()').get(),
                'termos_descritores': td.xpath('.//b[text()="Termos descritores"]/following-sibling::blockquote[1]/text()').get(),
                'companhia_produtora': td.xpath('.//b[text()="Companhia(s) produtora(s): "]/following-sibling::text()').get(),
                'producao': td.xpath('.//b[text()="Produção: "]/following-sibling::text()').get(),
                'companhia_distribuidora': td.xpath('.//b[text()="Companhia(s) distribuidora(s): "]/following-sibling::text()').get(),  # the space here matters
                'argumento': td.xpath('.//b[text()="Argumento: "]/following-sibling::text()').get(),  # the space here matters
                'roteiro': td.xpath('.//b[text()="Roteiro: "]/following-sibling::text()').get(),  # the space here matters
                'dialogos': td.xpath('.//b[text()="Diálogos: "]/following-sibling::text()').get(),  # the space here matters
                'estoria': td.xpath('.//b[text()="Estória: "]/following-sibling::text()').get(),  # the space here matters
                'direcao': td.xpath('.//b[text()="Direção: "]/following-sibling::text()').get(),  # the space here matters
                'direcao_de_fotografia': td.xpath('.//b[text()="Direção: "]/following-sibling::text()').get(),  # FIXME
                'camera': td.xpath('.//b[text()="Câmera: "]/following-sibling::text()').get(),  # the space here matters
                'direcao_de_som': td.xpath('.//b[text()="Direção de som: "]/following-sibling::text()').get(),  # the space here matters
                'cenografia': td.xpath('.//b[text()="Direção de som: "]/following-sibling::text()').get(),  # FIXME the space here matters
                'identidades_elenco': td.xpath('.//b[text()="Identidades/elenco: "]/following-sibling::text()').getall(),
                'conteudo_examinado': td.xpath('.//b[text()="Conteúdo examinado:  "]/following-sibling::text()').get(),
                'fontes_utilizadas': td.xpath('.//b[contains(text(), "Fontes utilizadas:")]/following-sibling::a[count(preceding-sibling::b[contains(text(), "Fontes consultadas:")]) = 0]/text()').getall(),
                'fontes_consultadas': self.get_sources(td, "Fontes consultadas:", "Observações:"),
                'observacoes': td.xpath('.//b[text()="Observações: "]/following-sibling::text()').getall(),  # TODO to text
                'cancoes': self.parse_songs(td)
            }

    # TODO pagination

    def get_sources(self, td, left_label, right_label):
        text_only = td.xpath(f'.//b[contains(text(), "{left_label}")]/following-sibling::text()[count(preceding-sibling::b[contains(text(), "{right_label}")]) = 0]').getall()
        with_link = td.xpath(f'.//b[contains(text(), "{left_label}")]/following-sibling::a[count(preceding-sibling::b[contains(text(), "{right_label}")]) = 0]/text()').getall()
        return text_only + with_link

    def parse_songs(self, td):
        songs = []

        labels = td.xpath(
            './/b[contains(text(), "Canção")]/following-sibling::b/text()[count(preceding-sibling::b[contains(text(), "Identidades/elenco:")]) = 0]').getall()
        values = td.xpath('.//b[contains(text(), "Canção")]/following-sibling::text()[count(preceding-sibling::b[contains(text(), "Identidades/elenco:")]) = 0]').getall()

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
