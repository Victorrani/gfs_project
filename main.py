import requests
from bs4 import BeautifulSoup
import subprocess
import os


print('')
print('#############')
print('Script main.py')
print('#############')
print('')


print('Este script é o script principal que irá controlar todo o processo para download e geração de figuras de dados meteorológicos.')

diretorio_atual = os.getcwd()
print("O diretório atual é:", diretorio_atual)

## criação de diretórios
if not os.path.exists('DADOS'):
    print('Criando o diretório DADOS')
    os.makedirs('DADOS')

if not os.path.exists('FIGURAS'):
    print('Criando o diretório FIGURAS')
    os.makedirs('FIGURAS')


subprocess.run(["python", "get_data.py"])

quit()





## Define a continuação do código ou não
resposta_usuario = input(str('Você gostaria de plotar alguns gráficos desse arquivo?[s, n]: '))
if resposta_usuario != 's':
    print('')
    print('Saindo do código get_gfs.py')
    print('')
    quit()
else:
    print('Começando o código gera_mapas.py')
    print('Em desenvolvimento')
    quit()
