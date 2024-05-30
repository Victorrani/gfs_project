gfs_project

Projeto para a criação de um script que faça toda a organização, download e plot de dados meteorológicos NCEP/NOAA.
O projeto é dividido 3 scripts principais:
1 - main.py 
  Script principal que organiza o diretório criando caminhos para os dados e figuras do usuário e chama os scripts de download e plots
2 - get_data.py
  Script que faz o download do servidor da NOAA de arquivos tipo grb mostrando para o usuário quais datas, hora de inicialização e resolução disponiveis
3 - mapas.py
  Cria os mapas de analise e previsão pré definidos pelo usuário
  
Fase atual - Melhorias no script get_data.py. Criação de código para o usuário baixar a priori o dado de analise e 1 dia de previsão 4 arquivos de 6 em 6 horas
