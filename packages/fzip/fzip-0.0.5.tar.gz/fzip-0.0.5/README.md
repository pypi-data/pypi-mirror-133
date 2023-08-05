<p align="center">
    <img src="https://github.com/JohnnyDev2001/fast_zipcode/blob/main/image/ceplogo.png?raw=true" width="30%">
</p>
<h2 align="center" color="green">Fast_ZipCode</h2>


## Instalação

O modulo Fast_ZipCode pode ser facilmente instalado utilizando o comando abaixo:

```

pip install fzip
```

## Comece agora

#Aviso:# O Fast_ZipCode foi desenvolvido para pequenas aplicações, não é recomendado para aplicações em massa.

<h3>Exemplo de uso padrão</h3>

```python
from fzip import zcode

address = zcode.Code(70160900)
```

descrição: Usando esse codigo acima caso uma api esteja fora do ar a proxima será chamada.

<h3>Exemplo de uso da api dos correios</h3>

```python
from fzip import zcode

address = zcode.Correios(70160900)
```
descrição: Usará a api dos correios.

<h3>Exemplo de uso da api viacep</h3>

```python
from fzip import zcode

address = zcode.Viacep(70160900)
```
descrição: Usará a api viacep.

<h3>Exemplo de uso da apicep</h3>

```python
from fzip import zcode

address = zcode.Apicep(70160900)
```
descrição: Usará a apicep.

<h3>o Retorno será sempre em forma de um objeto 'dict':</h3>

```python
{
    'bairro': 'str',
    'cep': 'str',
    'cidade': 'str',
    'logradouro': 'str',
    'uf': 'str',
    'complemento': 'str',
}
```