# AutoGA
Ferramenta de automaçao para transformar planilhas entre dois sistemas de automação (Extração de contatos  whatsapp -> botConversas) 

# INSTALAÇÃO DE DEPENDENCIAS
pip install -r requirements.txt

# CRIANDO EXECUTAVEL
pyinstaller --onefile --add-data "db/ibge-fem-10000.csv;db" --add-data "db/ibge-mas-10000.csv;db" master.py
