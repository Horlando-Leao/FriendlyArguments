# Testes Unitários - Friendly Arguments

Este diretório contém os testes unitários para o pacote `friendly_arguments`.

## Estrutura

```
tests/
├── __init__.py
├── test_named.py      # Testes para o módulo named
└── README.md          # Este arquivo
```

## Executar os Testes

### Executar todos os testes

```bash
python3 -m unittest discover tests -v
```

### Executar um arquivo específico

```bash
python3 -m unittest tests.test_named -v
```

### Executar uma classe específica

```bash
python3 -m unittest tests.test_named.TestGetArgs -v
```

### Executar um teste específico

```bash
python3 -m unittest tests.test_named.TestGetArgs.test_basic_parsing_with_equals -v
```

## Cobertura dos Testes

Os testes cobrem:

### ✅ Função `get_args()`
- Parsing com sintaxe `--arg=value`
- Parsing com sintaxe `--arg value`
- Argumentos curtos `-a value`
- Flags booleanas `--verbose`
- Valores padrão
- Valores com espaços
- Valores com caracteres especiais
- Valores vazios
- Múltiplas sintaxes combinadas

### ✅ Função `get_arg()`
- Busca com chave única
- Busca com múltiplas chaves (aliases)
- Valores padrão
- Ordem de prioridade
- Diferentes tipos de valores padrão

### ✅ Função `get_params_sys_args()` (API legada)
- Parsing básico
- Modo silencioso
- Modo verbose
- Argumentos faltantes
- Valores vazios
- Valores com espaços

### ✅ Testes de Integração
- Combinação de `get_args()` e `get_arg()`
- Cenários complexos
- Retrocompatibilidade

### ✅ Casos Extremos
- Números negativos
- Caracteres Unicode
- Valores muito longos
- Muitos argumentos
- Argumentos duplicados
- Strings vazias

## Estatísticas

- **Total de testes**: 49
- **Classes de teste**: 5
- **Cobertura**: ~100% do código principal

## Adicionar Novos Testes

Para adicionar novos testes:

1. Abra `test_named.py`
2. Escolha a classe apropriada ou crie uma nova
3. Adicione um método de teste começando com `test_`
4. Use `setUp()` e `tearDown()` para preparar/limpar o ambiente
5. Execute os testes para verificar

Exemplo:

```python
def test_meu_novo_teste(self):
    """Descrição do que este teste faz"""
    sys.argv = ['script.py', '--arg=value']
    args = get_args()
    
    self.assertEqual(args['--arg'], 'value')
```

## Requisitos

- Python 3.7+
- Módulo `unittest` (incluído na biblioteca padrão)

## Notas

- Todos os testes manipulam `sys.argv` diretamente
- `setUp()` salva o `sys.argv` original
- `tearDown()` restaura o `sys.argv` original
- Isso garante que os testes não interfiram uns com os outros

