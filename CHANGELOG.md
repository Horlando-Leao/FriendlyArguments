# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2024-12-18

### Adicionado
- Nova função `get_args()` para parsing automático e flexível de argumentos
- Nova função `get_arg()` para buscar argumentos com aliases
- Suporte a múltiplas sintaxes: `--arg=value`, `--arg value`, `-a value`
- Suporte a flags booleanas: `--verbose`, `--debug`
- Suporte a valores padrão via parâmetro `defaults`
- Documentação completa em português no README
- Exemplos práticos de uso
- Arquivo CHANGELOG.md
- Arquivo .gitignore

### Modificado
- Função `get_params_sys_args()` agora tem parâmetro `silent=True` (não imprime por padrão)
- README.md completamente reescrito com exemplos detalhados
- test_args.py atualizado com exemplos abrangentes

### Mantido
- Retrocompatibilidade completa com versão 0.1.0
- API antiga `get_params_sys_args()` continua funcionando

## [0.1.0] - Data anterior

### Adicionado
- Primeira versão do pacote
- Função `get_params_sys_args()` básica
- Suporte a argumentos nomeados com sintaxe `--arg=value`

