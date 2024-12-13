import queue
import threading
from bs4 import BeautifulSoup
from flask import Flask,Blueprint, request,jsonify
from queue import Queue
import requests

app = Blueprint("API",__name__)

@app.route("/solicitar/", methods=["GET"])
def Solicitar_consulta():

    Func_queu = queue.Queue() # inicializando o queue para pegar os dados da thread
    produto_busca = request.args.get("produto")
    quantidade = request.args.get("quantidade")
    # tratando os argumentos fornecidos 
    try:
        int(quantidade)

    except ValueError:
        return jsonify({"Error":403,
                        "Message":"Quantidade invalida"}),403
    except TypeError:        
        return jsonify({"Error":403,
                        "Message":"Quantidade invalida"}),403
    # verificando se os produtos sao validos 
    if not produto_busca or not quantidade:
        return jsonify({"erro": "Argumentos inválidos ou ausentes"}), 400
    
    if len(produto_busca) <= 4 and len(quantidade) < 4:
        return jsonify({"erro": "URL ou metodo invalido, lembre se de utilizar os argumentos na url : ?produto=geladeita  &metodo="}), 400
    # Criar o dicionário de produtos
    dicionario_produtos_ml = {}

    Pegar_requisiao_ML(produto_nome=produto_busca, dicionario_product=dicionario_produtos_ml,quantidade_produto=int(quantidade)) ## percorre os 2 sites ao mesmo tempo pra otimizar a consulta 
    zoom = threading.Thread(target=Pegar_requisiao_zoom, args=(Func_queu,produto_busca,dicionario_produtos_ml,int(quantidade)))
    zoom.start()
    zoom.join()
    produtos_juntos = {**Func_queu.get(), **dicionario_produtos_ml} # junta os dicionarios 
    if produtos_juntos.items():
        return jsonify(sorted(produtos_juntos.items(),key=lambda item: item[1]["valor"])) # funcao lambda para ordenar a lista 
    return jsonify({"Error":"404",
                   "message":"produto nao encontrado"})

## esta funcao verifica o valor e adiciona os produtos  
def adicionar_no_dicionario(nome_produto : str, link : str, valor : str, dicionario : dict, vendedor : str,quantidade : int):

## troca as , por . para nao dar erros na conversao de valor 
    valor = valor.replace(".", "").replace(",", ".")
    if len(dicionario) < quantidade:
        dicionario[nome_produto] = {
                    'valor' : float(valor),
                    'vendedor': vendedor,
                    'url' : link}
    else:
        maior_valor_produto = max(dicionario.items(), key=lambda x: x[1]["valor"])[0]  ## funcao lambda para pegar o maior valor dos produtos
        if float(valor) < float(dicionario[maior_valor_produto]["valor"]):

            del dicionario[maior_valor_produto] ## apaga o maior valor e substitui ele 

            dicionario[nome_produto] = {
                'valor': float(valor),
                'vendedor': vendedor,
                'url': link
            }


# pega os produtos do mercado livre filtra e retorna o dicionario 
def Pegar_requisiao_ML(produto_nome : str, dicionario_product : dict,quantidade_produto : int):

    for produto in Realizar_requisicao_e_filtrar_ML(produto_nome): ## pega e percorre os produtos 


        titulo_Mercado_livre = produto.find("h2",attrs={'class':'poly-box poly-component__title'}) #type:ignore
        

        valor_merc_liv = produto.find("span",attrs={'class':'andes-money-amount andes-money-amount--cents-superscript'}) #type:ignore
        

        link_Mercado_livre = titulo_Mercado_livre.find("a")#type:ignore

        print(titulo_Mercado_livre.text,valor_merc_liv.text)
        if titulo_Mercado_livre and valor_merc_liv and link_Mercado_livre: ## verifica se todos os valores sao validos 
            adicionar_no_dicionario(nome_produto=titulo_Mercado_livre.text,link=link_Mercado_livre["href"],valor=valor_merc_liv.text.strip("R$ "),dicionario=dicionario_product,vendedor="Mercado Livre",quantidade=quantidade_produto)#type:ignore


    return jsonify(dicionario_product)


 # pega os produtos do site zoom filtra e retorna em dicionario
def Realizar_requisicao_e_filtrar_ML(url_consulta : str):
            ## fazendo a requisicao e filtrando os dados diretamente  
    return BeautifulSoup(requests.get(f"https://lista.mercadolivre.com.br/{url_consulta}").text,"html.parser").find_all("div",attrs={'class':'ui-search-result__wrapper'}) # filtra pra pegar a parte dos produtos 
    

def Realizar_requisicao_e_filtrar_zoom(url_consulta : str):

    return BeautifulSoup(requests.get(f"https://www.zoom.com.br/search?q={url_consulta}").text,"html.parser").find_all("div",attrs={'class':'Hits_ProductCard__Bonl_'}) # filtra pra pegar a parte dos produtos 

def Pegar_requisiao_zoom(Func_queu, produto, dicionario_produto,quantidade):
    try:
        for produto_item in Realizar_requisicao_e_filtrar_zoom(produto):  # Iterar sobre os resultados
            vendedor_zoom = produto_item.find('h3', attrs={'class': 'Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_MobileLabelSAtLarge__m0whD ProductCard_ProductCard_BestMerchant__JQo_V'})  # type: ignore
            titulo_zoom = produto_item.find("h2", attrs={'class': 'Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_DesktopLabelSAtLarge__wWsED ProductCard_ProductCard_Name__U_mUQ'})  # type: ignore
            valor_zoom = produto_item.find("p", attrs={'class': 'Text_Text__ARJdp Text_MobileHeadingS__HEz7L'})  # type: ignore
            link_zoom = produto_item.find("a", attrs={'class': 'ProductCard_ProductCard_Inner__gapsh'})  # type: ignore

            if vendedor_zoom and titulo_zoom and valor_zoom and link_zoom and vendedor_zoom != "Mercado Livre":  # Verifica se os valores são válidos
                adicionar_no_dicionario(
                    nome_produto=titulo_zoom.text,
                    link=f"https://zoom.com.br{link_zoom.get('href')}",
                    valor=valor_zoom.text.strip("R$ "),
                    dicionario=dicionario_produto,
                    vendedor=vendedor_zoom.text,
                    quantidade=quantidade
                )

# prevenindo erros 
    except Exception as e:
        dicionario_produto["erro"] = {"Erro": str(e)}  # Captura qualquer erro e adiciona no dicionário

    Func_queu.put(dicionario_produto)  # Inserindo o dicionario no queue
