# AutoGA
Ferramenta de automaçao para transformar planilhas entre dois sistemas de automação (Extração de contatos  whatsapp -> botConversas) 

# 1 Clonando o projeto pra sua maquina
git clone https://github.com/samdamazio/AutoGA.git
ou baixar o zip por aqui e extrair

# 2 AMBIENTE VIRTUAL (pode pular)
## criando
python3 -m venv venv
## ativando em windows:
venv/Scripts/activate
## ativando em MacOS or Linux:
source venv/bin/activate

# 3 INSTALAÇÃO DE DEPENDENCIAS

pip install -r requirements.txt

# 4 RODANDO APLICAÇÃO
python3 main.py

## IGNORE POR ENQUANTO
# CRIANDO EXECUTAVEL (obs: antivirus/debugs/etc)
pyinstaller --noconsole --onefile --add-data "db/ibge-fem-10000.csv;db" --add-data "db/ibge-mas-10000.csv;db" master.py

