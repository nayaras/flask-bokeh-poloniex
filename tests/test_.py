import json

def test_my_view(client, captured_templates):
    response = client.get("/")

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "index.html"

    assert "moedas" in context
    assert context["moedas"] == ['USDT_BTC','USDC_BTC', 'BTC_BTS', 'BTC_DASH', 'BTC_DOGE', 'BTC_LTC']
    
    #testa se o request a api do poloniex deu certo e se obteve todos os dados
    assert "cotacao" in context
    assert type(context["cotacao"]) == dict
    assert len(context["cotacao"]) == 336
    
    #testa se a data da requisição veio (em erro viria undefined ou none)
    assert "data_requisicao" in context
    assert type(context["data_requisicao"]) == str



