# -*- encoding: utf-8 -*-

# libs utilizadas
#PIP:
  #pip install requests2
  #pip install pandas
  #pip install lxml
  #pip install beautifulsoup4
  #pip install selenium


# import das libs
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Pegar conteudo HTML a partir da URL
# url de acesso
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
 # definição do ranking
top10ranking = {}

# estrutura base de rankings
rankings = {
  "3points": {'field': "FG3M", "label": "3PM"},
  "points": {'field': "PTS", "label": "PTS"},
  "assistants": {'field': "AST", "label": "AST"},
  "rebounds": {'field': "REB", "label": "REB"},
  "steals": {'field': "STL", "label": "STL"},
  "blocks": {'field': "BLK", "label": "BLK"}
}

def buildrank(type):
  
  field = rankings[type]['field']
  label = rankings[type]['label']
  
  # caminho q será buscado no xpath
  #//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']
  driver.find_element_by_xpath(
  f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

  elemento = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
  html_content = elemento.get_attribute("outerHTML")

  # Parsear o conteudo HTML - BeeaultifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')
  table = soup.find(name='table')

  # Estruturar conteudo em um Data Frame - Pandas
    # criando um dataframe com base na table filtrada a cima
    # ele transforma em um array
    # head(10) -> filtrando pelos top 10 do resultado total da table
  df_full = pd.read_html( str(table) )[0].head(10)

  # geranando um df novo somente com os valores de interesse
  df_novo = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
  # redefinindo os nomes das colunas
  df_novo.columns = ['pos', 'player', 'team', 'total']

  # Transformar os Dados em um Dicionario de dados próprio
  return df_novo.to_dict('records') 


option = Options()
# opção q faz que o navegador não fique aparecendo na tela
# é para deixar o navegador rodando em background
option.headless = True
# setando a configuração de headless para o driver
driver = webdriver.Firefox(options=option) # options=option -> quando adicionamos as options ele não abre o navegador

# executando a navegação da url
driver.get(url)

sleep(10)

for r in rankings:
  top10ranking[r] = buildrank(r)
 
sleep(2)
# fechando o navegador
driver.quit()

# Converter e salvar em um arquivo JSON
arquivojson = json.dumps(top10ranking)
try:
  abrindoarquivo = open('rankingFinal.json', 'w')
  abrindoarquivo.write(arquivojson)
  abrindoarquivo.close()
  print('arquivo json gerado!')
except:
  print('arquivo json não gerado!')
