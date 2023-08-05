from . import apicep, correios, viacep

def Code(cep):
    searchadresscorreios = correios.search_adress_correios(cep)
    searchadressapicep = apicep.search_adress_apicep(cep)
    searchadressviacep = viacep.search_adress_viacep(cep)
    if searchadresscorreios != 0:
        return f'{searchadresscorreios}'
    elif searchadressapicep != 0:
        return f'{searchadressapicep}'
    elif searchadressviacep != 0:
        return f'{searchadressviacep}'

def Correios(cep):
    searchadresscorreios = correios.search_adress_correios(cep)
    if searchadresscorreios != 0:
        return f'{searchadresscorreios}'
    else:
        return 'error'

def Apicep(cep):
    searchadressapicep = apicep.search_adress_apicep(cep)
    if searchadressapicep != 0:
        return f'{searchadressapicep}'
    else:
        return 'error'

def Viacep(cep):
    searchadressviacep = viacep.search_adress_viacep(cep)
    if searchadressviacep != 0:
        return f'{searchadressviacep}'
    else:
        return 'error'