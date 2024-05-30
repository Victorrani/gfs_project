import requests
from bs4 import BeautifulSoup
import subprocess
import os
import wget

print('')
print('##############################')
print('Iniciando o script get_data.py')
print('##############################')
print('')

diretorio_atual = os.getcwd()

## URL do site
url = "https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/"

print(f'Fazendo Download disponíveis no endereço: {url}')
print('')

## Listas importantes
datas_disponiveis = []
hora_inicializacao = ['00', '06', '12', '18']
resolucao = ['0p25', '0p50', '1p00']

## Tratamento dos dados do site
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

## Determinando as datas disponíveis
for link in soup.find_all('a'):
    href = link.get('href')
    if href.startswith('gfs'):
        datas_disponiveis.append(href[4:12])

## Dados disponíveis para o usuário
print(f'Estão disponíveis as datas: {datas_disponiveis}')
print('')
print(f'Estão disponíveis esses horários de inicialização do modelo {hora_inicializacao}')
print('')
print(f'Estão disponíveis essas resoluções: {resolucao}')
print('')

## Condição para escolha dos arquivos para download
while True:
    data_inicio_escolha = input(str('Qual data você quer fazer download? '))
    if data_inicio_escolha in datas_disponiveis:
        data_inicio = data_inicio_escolha
        break
    else:
        print(f'Escolha corretamente. As opções são {datas_disponiveis}')

while True:
    hora_inicio_escolha = input(str('Qual horário de inicialização você quer? '))
    if hora_inicio_escolha in hora_inicializacao:
        hora_inicio = hora_inicio_escolha
        break
    else:
        print(f'Escolha corretamente. As opções são {hora_inicializacao}')

while True:
    resolucao_inicio_escolha = input(str('Qual resolução você quer? '))
    if resolucao_inicio_escolha in resolucao:
        resolucao_inicio = resolucao_inicio_escolha
        break
    else:
        print(f'Escolha corretamente. As opções são {resolucao}')


nome_arquivo = 'gfs.t'+hora_inicio+'z.pgrb2.'+resolucao_inicio+'.f000'
## Arquivo para download
arquivo_download = url+'gfs.'+data_inicio+'/'+hora_inicio+'/atmos/gfs.t'+hora_inicio+'z.pgrb2.'+resolucao_inicio+'.f000'
diretorio_dados = data_inicio+hora_inicio
arquivo_nome = 'gfs.t'+hora_inicio+'z.pgrb2b.'+resolucao_inicio+'.f000.'+diretorio_dados
## Download do arquivo selecionado na pasta DADOS+data
print(f'Será feito o download do arquivo {nome_arquivo}')
diretorio_destino = os.path.join(diretorio_atual, 'DADOS')
os.chdir(diretorio_destino)
if not os.path.exists(data_inicio+hora_inicio):
    print(f'Criando o diretório {diretorio_dados}')
    os.makedirs(diretorio_dados)
diretorio_atual = os.getcwd()
diretorio_destino = os.path.join(diretorio_atual, diretorio_dados)
os.chdir(diretorio_destino)
print("Baixando arquivo...")
wget.download(arquivo_download, arquivo_nome)


