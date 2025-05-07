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
            yield parse_film_td(td)

def extract_text(selector):
    return selector.get(default="").strip()

def extract_blockquote(td, label):
    sel = td.xpath(f'.//b[text()="{label}"]/following-sibling::blockquote[1]/text()')
    return extract_text(sel)

def extract_after_label(td, label):
    sel = td.xpath(f'.//b[text()="{label}"]/following-sibling::text()[1]')
    return extract_text(sel)

def extract_all_after_label(td, label):
    return [t.strip() for t in td.xpath(f'.//b[text()="{label}"]/following-sibling::text()').getall() if t.strip()]

def extract_person_list(td, label):
    return [
        t.strip()
        for t in td.xpath(f'.//b[text()="{label}"]/following-sibling::br/following-sibling::text()').getall()
        if t.strip()
    ]


def parse_film_td(td):
    film = {
        "titulo": extract_text(td.xpath('.//b[@class="title"]/text()')),
    }

    """
    ['\r\n\r\n\t\t', 
    'BANANA DA TERRA', 
    'Código do Filme', 
    '000302',
    'Categorias',
    'Longa-metragem / Sonoro / Ficção',
    'Material original',
    '35mm, BP, 75min, 2.099m, 24q',
    'Data e local de produção',
    'Ano:',
    ' 1939',
    'País: ',
    'BR', 
    'Cidade:', 
    ' Rio de Janeiro', 
    'Estado:', 
    ' DF', 
    'Certificados', 
    'Certificado de Censura Federal, entre 01 e 15.02.1939.Certifcado de Censura Federal, entre 16 e 31.01.1939, trailer, 88m.', 
    'Data e local de lançamento', 
    'Data:', 
    ' 1939.02.10; 1939.02.10', 
    'Local:', 
    ' São Paulo; Rio de Janeiro', 
    'Sala(s):', 
    ' Metro; Metro', 
    'Circuito exibidor', 
    'Exibido em São Paulo de 10 a 23.02.1939, no Metro; de 15 a 28.05, no Astória; a 21.05, no São José e no Moderno; de 23 a 28.05, no São José e no Moderno; de 13 a 18.06, no Paulistano; de 14 a 18.06, no Ideal; de 19 a 25.06, no Rialto e no Marconi; de 29.06 a 04.07, no Fênix; de 30.06 a 02.07, no Ipiranga-Palácio; de 07 a 13.07, no Esperia; de 28 a 30.07, no Cambuci e de 16 a 18.10, no Rialto.',
    '     Exibido em Curitiba a 12.05.1939, no Avenida, no Imperial e no Odeon.',
    'Sinopse',
    '"Bananolândia, uma ilha, produz muitas bananas, mas não consegue vendê-las, causando pânico na população. A rainha da ilha, por sugestão do chefe da campanha publicitária a favor da banana, resolve viajar para o Brasil para tentar vender sua produção".(Extraído de ALSN/DFB-LM)',
    'Gênero',
    'Comédia; Musical',
    'Termos descritores',
    'Música popular brasileira; Política',
    'Produção',  # section
    'Companhia(s) produtora(s): ',
    'Sonofilms',
    'Produção: ',
    'Downey, Wallace',
    'Distribuição',  # section
    'Companhia(s) distribuidora(s): ',
    'Metro Goldwyn Mayer do Brasil',
    'Argumento/roteiro',  # section
    'Argumento: ',
    'Barro, João de; Lago, Mário',
    'Roteiro: ',
    'Barro, João de; Lago, Mário',
    'Direção',
    'Direção: ',
    'Costa, Ruy', 
    'Fotografia',   # section
    'Direção de fotografia: ', 'Brasil, Edgar', 
    'Câmera: ', 'Brasil, Edgar', 
    'Som',    # section 
    'Direção de som: ', 'Whally, Charles; Downey, Wallace', 
    'Direção de arte',
    'Cenografia: ',
    'Costa, Ruy; Vieira, Eduardo',
    'Canção',   # section
    'Título: ',
    'Amei demais; ',
    'Autor da canção: ',
    'Castro, Barbosa; ',
    'Intérprete: ', 'Barbosa, Castro; ',
    'Título: ', 'Eu vou pra farra; ', 
    'Autor da canção: ', 
    'Barro, João de; ', 
    'Intérprete: ', 
    'Bando da Lua; ', 
    'Componentes: ', 
    'Ozório, Afonso; Ozório, Stênio; Oliveira, Aluízio de; Jordão, Hélio Pereira; Éboli, Oswaldo e Astolfi, Ivo; ', 
    'Título: ', 
    'Jardineira, A; ',
     'Autor da canção: ', 
     'Lacerda, Benedito e Porto, Humberto; ', 
     'Intérprete: ', 
     'Silva, Orlando; ', 
     'Título: ', 
     'Mares da China; ', 
     'Autor da canção: ', 
     'Barro, João de e Ribeiro, Alberto; ', 
     'Intérprete: ', 
     'Galhardo, Carlos; ', 
     'Título: ', 
     'Menina do reÍä; ',
     'Título: ',
     'Não sei porque; ',
     'Autor da canção: ',
     'Barro, João de e Vermelho, Alcir Pires; ',
     'Intérprete: ',
     'Bando da Lua; ',
     'Componentes: ',
     'Ozório, Afonso; Ozório, Stênio; Oliveira, Aluízio de; Jordão, Hélio Pereira; Éboli, Oswaldo  e Astolfi, Ivo',
     'Título: ',
     'O que é que a baiana tem?; ',
     'Autor da canção: ',
     'Caymmi, Dorival; ',
     'Intérprete: ',
     'Miranda, Carmen; ',
     'Título: ',
     'Pirulito, O; ',
     'Autor da canção: ',
     'Barro, João de e Ribeiro, Alberto; ', 
     'Intérprete: ', 'Miranda, Carmen e Almirante; ', 
     'Título: ', 'Não sei se é covardia; ', 
     'Autor da canção: ', 
     'Alves, Ataulfo e Cruz, Claudionor; ', 
     'Intérprete: ',
     'Galhardo, Carlos; ',
     'Título: ',
     'Sem banana macaco se arranja; ', 
     'Autor da canção: ', 
     'Barro, João de e Ribeiro, Alberto; ', 
     'Intérprete: ', 
     'Galhardo, Carlos; ', 
     'Título: ', 
     'Tirolesa, A', 
     'Autor da canção: ', 
     'Barbosa, Paulo e Santiago, Osvaldo', 
     'Intérprete: ', 
     'Batista, Dircinha', 
     'Identidades/elenco: ', 
     'Batista, Dircinha', 
     'Oscarito', 
     'Oliveira, Aluízio de', 
     'Borges, Lauro', 
     'Murad, Jorge', 
     'Martins, Neide', 
     'Silva, Mário', 
     'Paulo Neto', 
     'Almirante', 
     'Barbosa, Castro', 
     'Batista, Linda', 
     'Galhardo, Carlos',
     'Miranda, Aurora', 
     'Miranda, Carmen', 
     'Silva, Orlando', 
     'Alvarenga e Bentinho', 
     'Bando da Lua [Ozório, Afonso; Ozório, Stênio; Oliveira, Aluízio de; Jordão, Hélio Pereira; Éboli, Oswaldo e Astolfi, Ivo] ', 
     'Napoleão Tavares e sua orquestra',
     'Romeu Silva e sua orquestra', 
     'Artistas do Cassino da Urca', 
     'Conteúdo examinado:  ', 
     'S', 
     'Fontes utilizadas:  ', 
     'CB/Ficha filmográfica', 
     'ALSN/DFB-LM', 
     'CENS/DOU', 
     'JIMS/OESP', 
     'CEPA/CBCP', 
     ', citando O Dia, 09.05; Gazeta do Povo, 12.05 e Diário da Tarde, 06.06.1939, Curitiba', 
     'JCB/Chan', 
     'MB/MFCA', 
     'Fontes consultadas:  ', 
     'AV/ICB', 'FCB LOTE 2/FF', 'CS/FF', 'FCB/FF', 'JRT/MPTC', 'MAM/Retrospectiva Carmen Miranda', 'Cinearte', 'HH/FEB', 'JN/Imigrantes - Portugueses II', 'JN/Imigrantes - Americanos I', 'JN/Imigrantes - Espanhóis I', 'MAM/Retrospectiva Oscarito', 'ACPJ/I', 
     'Observações: ',
     '     Algumas fontes consultadas atribuem a direção do filme a <Barro, João de> e indicam 1938 como data de produção.',
     '     JCB/Chan informa que o filme teve grande sucesso, mas, para conseguir o bom lançamento da <Metro>, submeteu-se às condições da distribuidora/exibidora americana: "(...) o filme só poderia ser reapresentado \'depois de sessenta dias de exibição no Metro\'." Em dúvida, a mesma fonte acrescenta no elenco <Barbosa Jr.>; <Nobre, Olga>; <Ladeira, Cesar> e <Rodrigues, Linda>, e nos números musicais acrescenta <Alves, Francisco>; <Amaral, Arnaldo>; <Barbosa, Luis>; <Borba, Emilinha>; <Caymmi, Dorival> e <Lane, Virginia>. Também coloca em dúvida o título da marcha de <Barro, João de>: "<Eu vou>" ou "<Eu vou pra farra>".', '     JIMS/OESP indica supervisão técnica de som de <Downey, Wallace>.', '     FCB LOTE 2/FF informa que "segundo <Ribeiro, Alberto> além de <Sem banana>, havia outras músicas que falavam em banana; uma delas, com letra diferente, transformou-se em <Veneno para dois>, gravada por <Miranda, Carmen>. Também indica, citando Cine Reporter de 11.02.1939, a apresentação da dança <Pirolito, O>.', '     CEPA/CBCP especifica, no elenco, alguns "artistas do <Cassino da Urca>, como <Alvarez, Fernando>; <Lenny, Jack> e as <Slater Twins>." Chama <Oliveira, Aloísio de> de <Oliveira, Aluísio de> e <Martins, Neide> de <Martins, Neyde>. Informa também que houve "em Curitiba, em 13.05, irradiação simultânea pela rádio PRB-2". Cita Diário da Tarde de 06.06.1939: "É a primeira vez que num mesmo dia são lançados 4 cópias de um filme nacional ao mesmo tempo nos principais cinemas das capitais brasileiras (...)".', '     JRT/MPTC relaciona alguns atores com os respectivos personagens, no entanto entra em contradição com a sinopse de JCB/Chan: <Oliveira, Aluísio de> é o galã; <Batista, Linda> é a rainha da Bananolândia; <Oscarito> é o conselheiro mor; <Batista, Dircinha> é a namorada do galã; <Miranda, Carmen> vem caracterizada como baiana e os componentes do <Bando da Lua> vêm caracterizados com suas camisas de malandro. É a única fonte que inclui o número musical <Boneca de pixe>, interpretado por <Miranda, Carmen> e <Almirante>.',
     '     ACPJ/I é a única fonte que indica: montagem de <Sá, E.> que, segundo MB/MFCA, é um dos pseudônimos de <Costa, Ruy>. Para esta última fonte, <Fenelon, Moacyr> esteve envolvido com o som, a montagem e a produção do filme.', 
     '     Cinearte 15.01.1939, 15.03.1939 e 01.06.1939 contém fotos do filme.', 
     '     Esta obra foi processada no âmbito do Projeto <Nitratos da Cinemateca Brasileira - Preservação e Acesso>-<Pronac 212939>, 2021, patrocinado pelo <Instituto Cultural Vale> e <Shell do Brasil>.']

    """

    film["ano"] = extract_after_label(td, "Ano:")
    film["codigo"] = extract_blockquote(td, "Código do Filme")
    film["categorias"] = extract_all_after_label(td, "Categorias")
    film["material_original"] = extract_all_after_label(td, "Material original")
    film["pais"] = extract_after_label(td, "País:")
    film["cidade"] = extract_after_label(td, "Cidade:")
    film["estado"] = extract_after_label(td, "Estado:")
    film["certificados"] = extract_blockquote(td, "Certificados")
    film["lancamento_data"] = extract_after_label(td, "Data:")
    film["lancamento_local"] = extract_after_label(td, "Local:")
    film["lancamento_salas"] = extract_after_label(td, "Sala(s):")
    film["sinopse"] = extract_blockquote(td, "Sinopse")
    film["genero"] = extract_blockquote(td, "Gênero")

    film["companhias_produtoras"] = extract_after_label(td, "Companhia(s) produtora(s):")
    film["producao"] = extract_after_label(td, "Produção:")
    film["companhias_distribuidoras"] = extract_after_label(td, "Companhia(s) distribuidora(s):")
    film["argumento"] = extract_after_label(td, "Argumento:")
    film["autoria"] = extract_after_label(td, "Autoria:")
    film["roteirista"] = extract_after_label(td, "Roteirista:")
    film["estoria"] = extract_after_label(td, "Estória:")
    film["direcao"] = extract_after_label(td, "Direção:")
    film["camera"] = extract_after_label(td, "Câmera:")
    film["direcao_som"] = extract_after_label(td, "Direção de som:")
    film["tecnico_som"] = extract_after_label(td, "Técnico de som:")
    film["musica"] = extract_after_label(td, "Música de:")
    film["elenco"] = extract_person_list(td, "Identidades/elenco:")

    return film
