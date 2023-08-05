import zeep

URL = 'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'

def search_adress_correios(cep):
    try:
        client = zeep.Client(URL)
        address = client.service.consultaCEP(cep)

        return {
            'bairro': getattr(address, 'bairro', ''),
            'cep': getattr(address, 'cep', ''),
            'cidade': getattr(address, 'cidade', ''),
            'logradouro': getattr(address, 'end', ''),
            'uf': getattr(address, 'uf', ''),
            'complemento': getattr(address, 'complemento2', ''),
        }
    except:
        return 0

if __name__ == '__main__':
    print(search_adress_correios(1166825))