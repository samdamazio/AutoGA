# AutoGA
Ferramenta de automaçao para transformar planilhas entre dois sistemas de automação (Extração de contatos  whatsapp -> botConversas) 

# AMBIENTE VIRTUAL
## criando
python3 -m venv venv
## ativando em windows:
venv/Scripts/activate
## ativando em MacOS or Linux:
source venv/bin/activate

# INSTALAÇÃO DE DEPENDENCIAS

pip install -r requirements.txt

# RODANDO APLICAÇÃO
python main.py

## IGNORE POR ENQUANTO
# CRIANDO EXECUTAVEL (obs: antivirus/debugs/etc)
pyinstaller --noconsole --onefile --add-data "db/ibge-fem-10000.csv;db" --add-data "db/ibge-mas-10000.csv;db" master.py

