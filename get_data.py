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
#url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
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

## Colocar aqui uma validação para digitação errada... ##
print('')
data_inicio = input(str('Qual data você quer fazer download? '))
print('')
hora_inicio = input(str('Qual horário de inicialização você quer? '))
print('')
resolucao_inicio = input(str('Qual resolução você quer? '))
print('')

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
comando_wget = ['wget', '--timeout=30', '--tries=5', '-c', '-O', arquivo_nome, arquivo_download]

print("Baixando arquivo...")

## Encontrado um problema no download do dado.

## Eventualmente esse wget via subprocess não é muito eficiente, preciso testar outras possibilidades

#processo = subprocess.Popen(comando_wget, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#saida, erro = processo.communicate()
wget.download(arquivo_download, arquivo_nome)
# Verificar se houve algum erro
#if processo.returncode != 0:
#    # Imprimir a saída de erro se houver
#    print("Erro ao baixar o arquivo:")
#    print(erro)
#else:
#    print("Download concluído.")


#subprocess.Popen(comando_wget)
#print("Download concluído.")
#print('')

