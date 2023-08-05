import requests
import json

def search_adress_viacep(cep):
    req = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    
    if req.status_code == 200:
        address = json.loads(req.text)
        return{
            'bairro': address.get('bairro', ''),
            'cep': address.get('cep', ''),
            'cidade': address.get('localidade', ''),
            'logradouro': address.get('logradouro', ''),
            'uf': address.get('uf', ''),
            'complemento': address.get('complemento', ''),
        }
    else:
        0
        

if __name__ == '__main__':
    print(search_adress_viacep(1166835))