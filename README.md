# AutoGA
Ferramenta de automaçao para transformar planilhas entre dois sistemas de automação (Extração de contatos  whatsapp -> botConversas) 

# INSTALAÇÃO DE DEPENDENCIAS

python3 -m venv venv

in windows:
venv/Scripts/activate
in MacOS or Linux:
source venv/bin/activate

pip install -r requirements.txt

# RODANDO APLICAÇÃO
python main.py

# CRIANDO EXECUTAVEL (obs: antivirus/debugs/etc)
pyinstaller --noconsole --onefile --add-data "db/ibge-fem-10000.csv;db" --add-data "db/ibge-mas-10000.csv;db" master.py

