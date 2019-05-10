from django.shortcuts import render
from .models import News
from requests import get
import requests
import json
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import timedelta
import datetime

# Create your views here.
def news_list(request):
    news = News.objects.all().order_by('-hora')
    return render(request, "news/news_list.html", {'news': news})

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def publico():
    r = requests.get("https://www.publico.pt/api/list/ultimas")
    print(r.status_code)
    artigos = json.loads(r.text)

    for artigo in artigos:
        hiperligacao = "https://www.publico.pt" + artigo["fullUrl"]
        titulo = artigo["cleanTitle"]
        tempo = artigo["data"][11:16]

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://images-eu.ssl-images-amazon.com/images/I/4151SuVhgDL.png"
        nova_noticia.save()


def observador():
    r = requests.get("https://observador.pt/")
    print(r.status_code)
    raw_html = simple_get('https://observador.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul" ,class_='latest').children
    for artigo in artigos:
        for link in artigo.find_all('a'):
            hiperligacao = link.get('href')
            titulo = link.get_text('a').replace(u'\xa0', u' ').replace("a/premium", "")[12:]
            tempo = link.get_text('a')[:5]

            nova_noticia = News()
            nova_noticia.title = titulo
            nova_noticia.link = hiperligacao
            nova_noticia.hora = tempo
            nova_noticia.imagem_jornal = "https://www.gleba-nossa.pt/wp-content/uploads/2018/11/observador.png"
            nova_noticia.save()

def jornal_de_negocios():
    r = requests.get("https://www.jornaldenegocios.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.jornaldenegocios.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("div", id="ultimas").findChild().findChildren()
    for artigo in artigos:
        for link in artigo.find_all('a'):
            hiperligacao = "https://www.jornaldenegocios.pt/" + link.get('href').replace("?ref=HP_UltimasNoticias", "")
            titulo = link.get_text('a')[7:]
            tempo = link.get_text('a')[:5]

            nova_noticia = News()
            nova_noticia.title = titulo
            nova_noticia.link = hiperligacao
            nova_noticia.hora = tempo
            nova_noticia.imagem_jornal = "https://pbs.twimg.com/profile_images/467304327749455873/KRgRkhDE_400x400.jpeg"
            nova_noticia.save()

def correio_da_manha():
    r = requests.get("https://www.cmjornal.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.cmjornal.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("section", id="ultimasHp_move").find("ul").find_all("li")
    tempo_now_datetime = datetime.datetime.now()
    tempo_now_string = tempo_now_datetime.strftime('%H:%M')
    for artigo in artigos:
        if len(artigo.find("span", class_="hora").get_text()) == 5:
            tempo = artigo.find("span", class_="hora").get_text()
        else:
            minutos_atras = artigo.find("span", class_="hora").get_text().replace("Há ", "").replace(" minutos", "")
            time = datetime.datetime.strptime(minutos_atras, '%M')
            delta = timedelta(minutes=time.minute)
            tempo = (tempo_now_datetime - delta).strftime('%H:%M')
        hiperligacao = "https://www.cmjornal.pt" + artigo.find("a").get('href')
        titulo = artigo.find("a", class_="newsTitle").get_text().strip()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://media.portaldaqueixa.com/l/e096374ae000a66df353f2c7be1e2b62.jpg"
        nova_noticia.save()

def jornal_economico():
    r = requests.get("https://jornaleconomico.sapo.pt/")
    print(r.status_code)
    raw_html = simple_get('https://jornaleconomico.sapo.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul", class_="je-post-list-container").find_all("li")
    for artigo in artigos:
        hiperligacao = artigo.find("a").get('href')
        titulo = artigo.find("div", class_="je-title").get_text()
        tempo = artigo.find("div", class_="je-date").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://pbs.twimg.com/profile_images/1029077964913340417/TcMhaPla.jpg"
        nova_noticia.save()

def sabado():
    r = requests.get("https://www.sabado.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.sabado.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    coluna_com_publicidade = soup.find("div", class_="ultimas_barra bl_blocoUltimas col-sm-6 col-xs-12 ultimasHP")
    coluna_sem_publicidade = coluna_com_publicidade.find_next_sibling("div", class_="ultimas_barra bl_blocoUltimas col-sm-6 col-xs-12 ultimasHP").findChild()
    artigos = coluna_sem_publicidade.find_all("li")

    for artigo in artigos:
        hiperligacao = "https://www.sabado.pt" + artigo.find("figure").find("a").get('href')
        titulo = artigo.find("figure").find("a").find("img").get('alt')
        tempo = artigo.find("span").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://www.sabado.pt/i/partilha_sabado.jpg"
        nova_noticia.save()

def diario_de_noticias():
    r = requests.get("https://www.dn.pt/ultimas.html")
    print(r.status_code)
    raw_html = simple_get('https://www.dn.pt/ultimas.html')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("div", class_="t-article-list-1-body").findChild().find_all("a")

    for artigo in artigos:
        hiperligacao = "https://www.dn.pt" + artigo.get('href')
        titulo = artigo.find('strong').find('span').get_text()
        tempo = artigo.find('time').get_text('datetime')

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://static.globalnoticias.pt/storage/DN/2016/big/ng8068384.JPG"
        nova_noticia.save()

def jornal_de_noticias():
    r = requests.get("https://www.jn.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.jn.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("nav", class_="t-section-list-6").findChild()

    for artigo in artigos:
        hiperligacao = "https://www.jn.pt" + artigo.find("a").get('href')
        titulo = artigo.find('a').find('span').get_text()
        tempo = artigo.find("a").find("time").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "http://www.erreacomunicacion.com/wp-content/uploads/2018/06/JN-marca-1.png"
        nova_noticia.save()

def expresso():
    r = requests.get("https://expresso.pt/ultimas")
    print(r.status_code)
    raw_html = simple_get('https://expresso.pt/ultimas')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul", class_="listArticles latestList itemCount_10").find_all("li")

    for artigo in artigos:
        hiperligacao = "https://expresso.pt" + artigo.find("h1").find("a").get('href')
        titulo = artigo.find("h1").find("a").get_text()
        tempo = artigo.find("div", class_="inlineDateAndAuthor").find("p").get('datetime')[11:16]

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://1.bp.blogspot.com/-flBDktCjecY/WrgJSt8ZyGI/AAAAAAABSIk/Sz0VXGU7DMIctdHXOKdJBUNGkUI-GMKIQCKgBGAs/s1600/IMG_1325.PNG"
        nova_noticia.save()

def a_bola():
    r = requests.get("https://www.abola.pt/Nnh/Noticias")
    print(r.status_code)
    raw_html = simple_get('https://www.abola.pt/Nnh/Noticias')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find_all("div", class_="media-body")

    for artigo in artigos[:10]:
        titulo_original = artigo.find("h4", class_="media-heading").find('span').get_text()
        titulo_final = ""
        if titulo_original[0] == "«":
            titulo_final = "«" + titulo_original.replace("«", "", 1).capitalize()
        else:
            titulo_final = titulo_original.capitalize()

        hiperligacao = "https://www.abola.pt" + artigo.find("a").get('href')
        titulo = titulo_final
        tempo = artigo.find('span', class_='hora').get_text().replace("\n", "")

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://www.abola.pt/img/logoabola.png"
        nova_noticia.save()


def o_jogo():
    r = requests.get("https://www.ojogo.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.ojogo.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("section", class_="t-section-list-7").find('nav').find('ul').find_all('li')

    for artigo in artigos:
        hiperligacao = "https://www.ojogo.pt" + artigo.find("a").get('href')
        titulo = artigo.find("a").find("span").get_text()
        tempo = artigo.find("span").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://upload.wikimedia.org/wikipedia/commons/d/dd/O_Jogo_Logotipo.jpg"
        nova_noticia.save()

def record():
    r = requests.get("https://www.record.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.record.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul", class_="ultimasLista").find_all("li")

    for artigo in artigos:
        hiperligacao = "https://www.record.pt" + artigo.find("a", class_="ultimasLink").get('href')
        titulo = artigo.find("a", class_="ultimasLink").get_text().strip()
        tempo = artigo.find("a").find("span").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://www.record.pt/i/recordLogoShare.jpg"
        nova_noticia.save()


def eco():
    r = requests.get("https://eco.sapo.pt/")
    print(r.status_code)
    raw_html = simple_get('https://eco.sapo.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul", class_="trending__list").findChildren("li")

    for artigo in artigos:
        hiperligacao = artigo.find("a").get('href')
        titulo = artigo.find("a").find('p').get_text().strip()
        tempo = artigo.find("time").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://ecoonline.s3.amazonaws.com/uploads/2017/02/logo_eco-07.png"
        nova_noticia.save()

def dinheiro_vivo():
    r = requests.get("https://www.dinheirovivo.pt/")
    print(r.status_code)
    raw_html = simple_get('https://www.dinheirovivo.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("ul", class_="widget-list").findChildren("li")

    for artigo in artigos:
        hiperligacao = artigo.find("a").get('href')
        titulo = artigo.find("a").get_text()
        tempo = artigo.find("time").get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://upload.wikimedia.org/wikipedia/commons/f/f6/Dinheiro_vivo_logo.jpg"
        nova_noticia.save()


def i_online():
    r = requests.get("https://ionline.sapo.pt/")
    print(r.status_code)
    raw_html = simple_get('https://ionline.sapo.pt/')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.find("div", id="panel2").findChild("section").findChildren("article")

    for artigo in artigos:
        hiperligacao = "https://ionline.sapo.pt" + artigo.find("h3").find("a").get('href')
        titulo = artigo.find("h3").find("a").get_text()
        tempo = artigo.find('span').get_text()

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://www.dealema.pt/wp-content/uploads/2013/11/clipping-logo-jornal_i.jpg"
        nova_noticia.save()

def sol():
    r = requests.get("https://sol.sapo.pt/mod/ultimas-side-bar")
    print(r.status_code)
    raw_html = simple_get('https://sol.sapo.pt/mod/ultimas-side-bar')
    soup = BeautifulSoup(raw_html, 'html.parser')
    artigos = soup.findChildren("li")

    for artigo in artigos:
        hiperligacao = "https://sol.sapo.pt" + artigo.find("a").get('href')
        titulo = artigo.find("a").get_text()[5:].strip()
        tempo = artigo.find("a").get_text()[:5]

        nova_noticia = News()
        nova_noticia.title = titulo
        nova_noticia.link = hiperligacao
        nova_noticia.hora = tempo
        nova_noticia.imagem_jornal = "https://sol.sapo.pt/img/logo.png"
        nova_noticia.save()

def scrape():
    News.objects.all().delete()
    publico()
    observador()
    jornal_de_negocios()
    correio_da_manha()
    jornal_economico()
    print('5/16 jornais procurados')
    sabado()
    diario_de_noticias()
    jornal_de_noticias()
    expresso()
    a_bola()
    print('10/16 jornais procurados')
    o_jogo()
    record()
    eco()
    dinheiro_vivo()
    i_online()
    print('15/16 jornais procurados')
    sol()
    print('16/16 jornais procurados')
scrape()