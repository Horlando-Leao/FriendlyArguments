# FriendlyArguments

Uma biblioteca Python simples e flexível para parsing de argumentos de linha de comando.

[![PyPI version](https://badge.fury.io/py/friendly-arguments.svg)](https://pypi.org/project/friendly-arguments/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Instalação

```bash
pip install friendly-arguments
```

##  Características

- **Sintaxe flexível**: Suporta `--arg=value`, `--arg value`, `-a value`
- **Flags booleanas**: `--verbose`, `--debug` retornam `True`
- **Valores padrão**: Defina defaults facilmente
- **Aliases**: Suporte para nomes curtos e longos (`-n` e `--name`)
- **Simples**: API minimalista e intuitiva
- **Zero dependências**: Usa apenas a biblioteca padrão do Python
- **Retrocompatível**: Mantém a API antiga funcionando

## 📖 Uso Básico

### Exemplo 1: Uso Simples

```python
from friendly_arguments import get_args

# Parse todos os argumentos automaticamente
args = get_args()

# Acesse os valores
name = args.get('--name', 'World')
print(f"Hello, {name}!")
```

**Execute:**
```bash
python script.py --name João
# Output: Hello, João!

python script.py --name=Maria
# Output: Hello, Maria!

python script.py
# Output: Hello, World!
```

### Exemplo 2: Com Valores Padrão

```python
from friendly_arguments import get_args

# Defina valores padrão
args = get_args(defaults={
    '--name': 'Anonymous',
    '--age': '18',
    '--city': 'Unknown'
})

print(f"Name: {args['--name']}")
print(f"Age: {args['--age']}")
print(f"City: {args['--city']}")
```

**Execute:**
```bash
python script.py --name João --age 25
# Output:
# Name: João
# Age: 25
# City: Unknown
```

### Exemplo 3: Flags Booleanas

```python
from friendly_arguments import get_args

args = get_args()

# Flags sem valor retornam True
verbose = args.get('--verbose', False)
debug = args.get('--debug', False)

if verbose:
    print("Modo verbose ativado!")

if debug:
    print("Modo debug ativado!")
```

**Execute:**
```bash
python script.py --verbose --debug
# Output:
# Modo verbose ativado!
# Modo debug ativado!
```

### Exemplo 4: Aliases (Nomes Curtos e Longos)

```python
from friendly_arguments import get_args, get_arg

args = get_args()

# Busca --name OU -n (o que encontrar primeiro)
name = get_arg(args, '--name', '-n', default='World')

# Busca --verbose OU -v
verbose = get_arg(args, '--verbose', '-v', default=False)

if verbose:
    print(f"Hello, {name}!")
```

**Execute:**
```bash
python script.py -n João -v
# Output: Hello, João!

python script.py --name Maria --verbose
# Output: Hello, Maria!
```

### Exemplo 5: Todas as Sintaxes Suportadas

```python
from friendly_arguments import get_args

args = get_args()

# Todas essas formas funcionam:
# python script.py --name=João
# python script.py --name João
# python script.py -n João
# python script.py --verbose
# python script.py --city "São Paulo"
```

##  Retrocompatibilidade

A versão antiga ainda funciona para não quebrar código existente:

```python
from friendly_arguments import get_params_sys_args

# API antiga (ainda funciona)
my_args = get_params_sys_args(['--text='])
text = my_args.get('--text=', 'default')
print(text)
```

**Execute:**
```bash
python script.py --text=hello
# Output: hello
```

##  Documentação da API

### `get_args(defaults=None)`

Parse todos os argumentos da linha de comando.

**Parâmetros:**
- `defaults` (dict, opcional): Dicionário com valores padrão

**Retorna:**
- `dict`: Dicionário com os argumentos parseados

**Exemplo:**
```python
args = get_args(defaults={'--port': '8080'})
```

### `get_arg(args, *keys, default=None)`

Busca um argumento por múltiplos nomes possíveis.

**Parâmetros:**
- `args` (dict): Dicionário retornado por `get_args()`
- `*keys`: Nomes de chaves para buscar
- `default`: Valor padrão se nenhuma chave for encontrada

**Retorna:**
- O valor da primeira chave encontrada, ou `default`

**Exemplo:**
```python
args = get_args()
port = get_arg(args, '--port', '-p', default=8080)
```

### `get_params_sys_args(keys, silent=True)`

Função legada para retrocompatibilidade.

**Parâmetros:**
- `keys` (list): Lista de chaves esperadas com sufixo `=`
- `silent` (bool): Se `True`, não imprime valores (padrão: `True`)

**Retorna:**
- `dict`: Dicionário com argumentos encontrados

## Exemplos Práticos

### Script de Configuração de Servidor

```python
from friendly_arguments import get_args, get_arg

args = get_args(defaults={
    '--host': 'localhost',
    '--port': '8080'
})

host = get_arg(args, '--host', '-h')
port = get_arg(args, '--port', '-p')
debug = get_arg(args, '--debug', '-d', default=False)

print(f"Starting server on {host}:{port}")
if debug:
    print("Debug mode enabled")
```

### Script de Processamento de Dados

```python
from friendly_arguments import get_args, get_arg

args = get_args()

input_file = get_arg(args, '--input', '-i')
output_file = get_arg(args, '--output', '-o')
verbose = get_arg(args, '--verbose', '-v', default=False)

if not input_file:
    print("Error: --input is required")
    exit(1)

if verbose:
    print(f"Processing {input_file}...")

# Seu código aqui...
```

## Testes

O pacote inclui uma suíte completa de testes unitários.

### Executar os testes

```bash
# Executar todos os testes
python3 -m unittest discover tests -v

# Ou usar o script helper
python3 run_tests.py -v
```

### Cobertura

- ✅ 49 testes unitários
- ✅ ~100% de cobertura do código
- ✅ Testes de integração
- ✅ Testes de casos extremos

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

MIT License - veja [LICENSE.md](LICENSE.md) para detalhes.

## Autor

**Horlando Leão**
- GitHub: [@Horlando-Leao](https://github.com/Horlando-Leao)
- Email: horlandojcleao.developer@gmail.com

## Links

- [PyPI](https://pypi.org/project/friendly-arguments/)
- [GitHub](https://github.com/Horlando-Leao/FriendlyArguments)
- [Issues](https://github.com/Horlando-Leao/FriendlyArguments/issues)




