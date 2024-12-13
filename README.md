## Pagina de Documentacaao da API
![image](https://github.com/user-attachments/assets/3a3700ff-5f50-4e37-9d61-310333e7bc99)
## Descricao 
Esta API foi criada com a finalidade de fornecer a busca automatizada por produtos por meio de requisicoes, fornecendo os produtos mais baratos e de fontes confiaveis, Todas as respostas da API sao feitas em JSON 

## Tecnologias usadas
- Python3.12.3
- Biblioteca Requests
- Biblioteca Flask
- Biblioteca BeautifulSoup
- Threading

## Otimizacoes 
- Foram Utilizadas Threads para fazer as buscas de forma rapida e mais eficiente
- Foram mantidas somente as variaveis importantes para o projeto, Todas as variaveis que eram e poderiam ser inuteis foram removidas para maior performance

## Seguranca  
Todos os argumentos fornecidos pelo usuario Sao tratados e caso o usuario informe um valor invalido e retornado um erro no formato JSON

## Erros

- Caso o usuario informe um valor invalido no campo de quantidade sera retornada este erro
  
```
{"Error":403,"Message":"Quantidade invalida"}
```
- Caso o usuario nao informe nenhum argumento ou se forem invalidos sera retornado este erro
```
  {"erro": "Argumentos inválidos ou ausentes"})
```

- Caso o produto fornecido tenha menos de 4 caracteres e a quantidade de produtos seja menor que 0 sera retornado um erro
```
  {"erro": "URL ou quantidade invalido, lembre se de utilizar os argumentos na url : ?produto=geladeita  &quantidade="}
```


## Rota principal 
``` /api/solicitar```
A url deve ser passada com os argumentos Produtos e quantidade ( /api/solicitar/?produto=" Produto para a pesquisa " &quantidade= "Quantidade de produtos que devem ser retornados" )
apos a pesquisa a api retornara um JSON com os produtos 

```
[
  [
    "Monitor Fullhd Pctop Led 19 60hz Hdmi Vga Mlp190hdmi  Barato",
    {
      "url": "https://produto.mercadolivre.com.br/MLB-3927328251-monitor-fullhd-pctop-led-19-60hz-hdmi-vga-mlp190hdmi-barato-_JM?searchVariation=182440147750#polycard_client=search-nordic&searchVariation=182440147750&position=50&search_layout=grid&type=item&tracking_id=5af5f48c-bb53-49f8-a4fa-88879cfc0054",
      "valor": 86.25,
      "vendedor": "Mercado Livre"
    }
  ]
]
```
