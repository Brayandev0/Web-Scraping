## Pagina de Documentacaao da API
![image](https://github.com/user-attachments/assets/df77125d-a6ec-4aaa-9f80-777484a86d52)

## Descricao 
Esta API foi criada com a finalidade de fornecer a busca automatizada por produtos por meio de requisicoes, fornecendo os produtos mais baratos e de fontes confiaveis, Todas as respostas da API sao feitas em JSON, a api pega os produtos e filtra 
para pegar os produtos mais baratos, o retorno da api e ordenado do menor valor ao valor maximo

## Tecnologias usadas
- Python3.12.3
- Biblioteca Requests
- Biblioteca Flask
- Biblioteca BeautifulSoup
- Threading

## Otimizacoes 
- Foram Utilizadas Threads para fazer as buscas de forma rapida e mais eficiente.
- Foram mantidas somente as variaveis importantes para o projeto, Todas as variaveis que eram e poderiam ser inuteis foram removidas para maior performance.

  
**Tempo de Resposta**
  o tempo de resposta da api varia de acordo com a velocidade de busca e a quantidade de produtos solicitados
  - 10 Produtos : 1.59 segundos
  - 50 produtos : 2.0 segundos

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
A url deve ser passada com os argumentos Produtos e quantidade .


``` ( /api/solicitar/?produto=" Produto para a pesquisa " &quantidade= "Quantidade de produtos que devem ser retornados" )```.


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
