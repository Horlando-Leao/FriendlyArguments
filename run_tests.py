#!/usr/bin/env python3
"""
Script para executar os testes unitários do friendly_arguments

Uso:
    python3 run_tests.py              # Executar todos os testes
    python3 run_tests.py -v           # Modo verbose
    python3 run_tests.py --help       # Mostrar ajuda
"""

import sys
import unittest

def main():
    """Executa os testes unitários"""
    
    # Verificar argumentos
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    show_help = '--help' in sys.argv or '-h' in sys.argv
    
    if show_help:
        print(__doc__)
        print("\nOpções:")
        print("  -v, --verbose    Modo verbose (mostra cada teste)")
        print("  -h, --help       Mostra esta mensagem")
        return 0
    
    # Descobrir e executar testes
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    # Mostrar resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print(f"❌ Falhas: {len(result.failures)}")
    
    if result.errors:
        print(f"❌ Erros: {len(result.errors)}")
    
    if result.skipped:
        print(f"⏭️  Pulados: {len(result.skipped)}")
    
    print("=" * 70)
    
    # Retornar código de saída apropriado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(main())

