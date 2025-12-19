# Como Publicar no PyPI

## Pré-requisitos

```bash
pip install --upgrade pip setuptools wheel twine
```

Token de API: https://pypi.org/manage/account/token/

## Passos

### 1. Atualizar versão
Edite `friendly_arguments/__init__.py`:
```python
__version__ = '0.2.0'
```

### 2. Executar testes
```bash
python3 run_tests.py -v
```

### 3. Limpar builds anteriores
```bash
rm -rf build/ dist/ *.egg-info friendly_arguments.egg-info
```

### 4. Criar pacotes
```bash
python3 setup.py sdist bdist_wheel
```

### 5. Verificar pacotes
```bash
twine check dist/*
```

### 6. Publicar no PyPI
```bash
twine upload dist/*
```

**Com token:**
```bash
twine upload dist/* -u __token__ -p pypi-SEU_TOKEN_AQUI
```

### 7. Verificar
https://pypi.org/project/friendly-arguments/

### 8. Git tag (após sucesso)
```bash
git add .
git commit -m "Release version 0.2.0"
git tag -a v0.2.0 -m "Version 0.2.0"
git push origin main --tags
```

## Comandos Rápidos

```bash
# Testes
python3 run_tests.py -v

# Build e publicação
rm -rf build/ dist/ *.egg-info && \
python3 setup.py sdist bdist_wheel && \
twine check dist/* && \
twine upload dist/*
```

## Checklist

- [ ] Versão atualizada em `__init__.py`
- [ ] CHANGELOG.md atualizado
- [ ] Testes passando
- [ ] Pacotes verificados (`twine check` - PASSED)
- [ ] Publicado no PyPI
- [ ] Tag criada no Git

## Solução de Problemas

**Erro: "File already exists"**
- Incremente a versão em `__init__.py`

**Erro: "403 Forbidden"**
- Verifique o token de API
- Certifique-se de que a versão não existe ainda

**Erro: "Invalid distribution"**
- Execute `twine check dist/*` para detalhes
- Verifique README.md (formato Markdown válido)

## Links

- PyPI: https://pypi.org/project/friendly-arguments/
- Token: https://pypi.org/manage/account/token/
