import datetime
import urllib.request
import json
import urllib.parse

print("Alan Corp: Online e pronta em português!")

while True:
    comando = input("Tu: ").strip()
    comando_lower = comando.lower()
    
    if not comando:
        continue
        
    if "sair" in comando_lower or "tchau" in comando_lower:
        print("Alan Corp: Até logo!")
        break
        
    elif "olá" in comando_lower or "oi" in comando_lower:
        print("Alan Corp: Olá! Tudo bem contigo?")
        
    elif "horas" in comando_lower:
        agora = datetime.datetime.now().strftime("%H:%M")
        print(f"Alan Corp: Agora são exatamente {agora}.")
        
    else:
        try:
            # Usa a API de busca geral da Wikipedia em português para encontrar o artigo correto independentemente de maiúsculas
            query_encoded = urllib.parse.quote(comando)
            search_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={query_encoded}&format=json"
            
            req = urllib.request.Request(search_url, headers={'User-Agent': 'AlanCorp/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                search_data = json.loads(response.read().decode())
                search_results = search_data.get('query', {}).get('search', [])
                
                if search_results:
                    # Pega o título do primeiro resultado relevante
                    title = search_results[0]['title']
                    title_encoded = urllib.parse.quote(title)
                    
                    # Busca o resumo desse artigo
                    summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{title_encoded}"
                    req_sum = urllib.request.Request(summary_url, headers={'User-Agent': 'AlanCorp/1.0'})
                    
                    with urllib.request.urlopen(req_sum, timeout=5) as sum_response:
                        sum_data = json.loads(sum_response.read().decode())
                        extract = sum_data.get('extract')
                        if extract:
                            print(f"Alan Corp ({title}): {extract}")
                        else:
                            print(f"Alan Corp: Encontrei o tópico '{title}', mas sem resumo disponível.")
                else:
                    print(f"Alan Corp: Não encontrei resultados para '{comando}' em português.")
        except Exception as e:
            print("Alan Corp: Erro ao ligar à internet ou processar o pedido.")
      
