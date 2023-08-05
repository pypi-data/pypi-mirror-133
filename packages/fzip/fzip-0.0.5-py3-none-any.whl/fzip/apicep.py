import requests
import json

def search_adress_apicep(cep):
    req = requests.get(f'https://ws.apicep.com/cep/{cep}.json')
    
    if req.status_code == 200:

        address = json.loads(req.text)
        
        return{
            'bairro': address.get('district', ''),
            'cep': address.get('code', ''),
            'cidade': address.get('city', ''),
            'logradouro': address.get('address', ''),
            'uf': address.get('state', ''),
            'complemento': address.get('complemento', ''),
        }
    else:
        return 0

if __name__ == '__main__':
    print(search_adress_apicep(116683))