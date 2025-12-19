"""
Testes unitários para o módulo friendly_arguments.named
"""

import sys
import unittest
from unittest.mock import patch

from friendly_arguments.named import get_args, get_arg, get_params_sys_args


class TestGetArgs(unittest.TestCase):
    """Testes para a função get_args()"""
    
    def setUp(self):
        """Salva o sys.argv original antes de cada teste"""
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Restaura o sys.argv original após cada teste"""
        sys.argv = self.original_argv
    
    def test_basic_parsing_with_equals(self):
        """Testa parsing básico com sintaxe --arg=value"""
        sys.argv = ['script.py', '--name=João', '--age=25']
        args = get_args()
        
        self.assertEqual(args['--name'], 'João')
        self.assertEqual(args['--age'], '25')
    
    def test_basic_parsing_with_space(self):
        """Testa parsing com sintaxe --arg value"""
        sys.argv = ['script.py', '--name', 'Maria', '--age', '30']
        args = get_args()
        
        self.assertEqual(args['--name'], 'Maria')
        self.assertEqual(args['--age'], '30')
    
    def test_short_arguments(self):
        """Testa argumentos curtos -a value"""
        sys.argv = ['script.py', '-n', 'Pedro', '-a', '35']
        args = get_args()
        
        self.assertEqual(args['-n'], 'Pedro')
        self.assertEqual(args['-a'], '35')
    
    def test_boolean_flags(self):
        """Testa flags booleanas"""
        sys.argv = ['script.py', '--verbose', '--debug']
        args = get_args()
        
        self.assertTrue(args['--verbose'])
        self.assertTrue(args['--debug'])
    
    def test_mixed_syntax(self):
        """Testa mistura de sintaxes"""
        sys.argv = ['script.py', '--name=João', '--age', '25', '-v']
        args = get_args()
        
        self.assertEqual(args['--name'], 'João')
        self.assertEqual(args['--age'], '25')
        self.assertTrue(args['-v'])
    
    def test_values_with_spaces(self):
        """Testa valores com espaços"""
        sys.argv = ['script.py', '--name', 'João Silva', '--city', 'São Paulo']
        args = get_args()
        
        self.assertEqual(args['--name'], 'João Silva')
        self.assertEqual(args['--city'], 'São Paulo')
    
    def test_values_with_equals_in_content(self):
        """Testa valores que contêm '=' no conteúdo"""
        sys.argv = ['script.py', '--equation=x=y+2']
        args = get_args()
        
        self.assertEqual(args['--equation'], 'x=y+2')
    
    def test_empty_value(self):
        """Testa valor vazio"""
        sys.argv = ['script.py', '--name=']
        args = get_args()
        
        self.assertEqual(args['--name'], '')
    
    def test_no_arguments(self):
        """Testa sem argumentos"""
        sys.argv = ['script.py']
        args = get_args()
        
        self.assertEqual(args, {})
    
    def test_with_defaults(self):
        """Testa com valores padrão"""
        sys.argv = ['script.py', '--name=João']
        args = get_args(defaults={'--name': 'Anonymous', '--age': '18'})
        
        self.assertEqual(args['--name'], 'João')
        self.assertEqual(args['--age'], '18')
    
    def test_defaults_not_overridden_when_not_provided(self):
        """Testa que defaults não são sobrescritos quando não fornecidos"""
        sys.argv = ['script.py']
        args = get_args(defaults={'--name': 'Default', '--age': '0'})
        
        self.assertEqual(args['--name'], 'Default')
        self.assertEqual(args['--age'], '0')
    
    def test_multiple_flags(self):
        """Testa múltiplas flags booleanas"""
        sys.argv = ['script.py', '--verbose', '--debug', '--force', '--quiet']
        args = get_args()
        
        self.assertTrue(args['--verbose'])
        self.assertTrue(args['--debug'])
        self.assertTrue(args['--force'])
        self.assertTrue(args['--quiet'])
    
    def test_numeric_values(self):
        """Testa valores numéricos (retornados como strings)"""
        sys.argv = ['script.py', '--port=8080', '--timeout=30']
        args = get_args()
        
        self.assertEqual(args['--port'], '8080')
        self.assertEqual(args['--timeout'], '30')
    
    def test_negative_numbers(self):
        """Testa números negativos"""
        # Com '=' funciona perfeitamente
        sys.argv = ['script.py', '--temperature=-10', '--balance=-500']
        args = get_args()
        
        self.assertEqual(args['--temperature'], '-10')
        self.assertEqual(args['--balance'], '-500')
    
    def test_negative_numbers_with_space(self):
        """Testa números negativos com espaço (limitação conhecida)"""
        # Nota: '--arg -500' interpreta -500 como flag, não como valor
        # Para números negativos, use sempre '=' : '--arg=-500'
        sys.argv = ['script.py', '--balance', '-500']
        args = get_args()
        
        # -500 é interpretado como uma flag booleana
        self.assertTrue(args['-500'])
    
    def test_special_characters(self):
        """Testa caracteres especiais"""
        sys.argv = ['script.py', '--email=user@example.com', '--url=https://example.com']
        args = get_args()
        
        self.assertEqual(args['--email'], 'user@example.com')
        self.assertEqual(args['--url'], 'https://example.com')


class TestGetArg(unittest.TestCase):
    """Testes para a função get_arg()"""
    
    def test_single_key(self):
        """Testa busca com uma única chave"""
        args = {'--name': 'João', '--age': '25'}
        result = get_arg(args, '--name')
        
        self.assertEqual(result, 'João')
    
    def test_multiple_keys_first_found(self):
        """Testa busca com múltiplas chaves - primeira encontrada"""
        args = {'--name': 'Maria', '--age': '30'}
        result = get_arg(args, '--name', '-n')
        
        self.assertEqual(result, 'Maria')
    
    def test_multiple_keys_second_found(self):
        """Testa busca com múltiplas chaves - segunda encontrada"""
        args = {'-n': 'Pedro', '--age': '35'}
        result = get_arg(args, '--name', '-n')
        
        self.assertEqual(result, 'Pedro')
    
    def test_no_key_found_with_default(self):
        """Testa quando nenhuma chave é encontrada - com default"""
        args = {'--age': '25'}
        result = get_arg(args, '--name', '-n', default='Anonymous')
        
        self.assertEqual(result, 'Anonymous')
    
    def test_no_key_found_without_default(self):
        """Testa quando nenhuma chave é encontrada - sem default"""
        args = {'--age': '25'}
        result = get_arg(args, '--name', '-n')
        
        self.assertIsNone(result)
    
    def test_default_none(self):
        """Testa default explicitamente None"""
        args = {}
        result = get_arg(args, '--name', default=None)
        
        self.assertIsNone(result)
    
    def test_default_false(self):
        """Testa default False"""
        args = {}
        result = get_arg(args, '--verbose', '-v', default=False)
        
        self.assertFalse(result)
    
    def test_default_zero(self):
        """Testa default 0"""
        args = {}
        result = get_arg(args, '--count', default=0)
        
        self.assertEqual(result, 0)
    
    def test_default_empty_string(self):
        """Testa default string vazia"""
        args = {}
        result = get_arg(args, '--text', default='')
        
        self.assertEqual(result, '')
    
    def test_boolean_value(self):
        """Testa valor booleano"""
        args = {'--verbose': True}
        result = get_arg(args, '--verbose', '-v')
        
        self.assertTrue(result)
    
    def test_priority_order(self):
        """Testa ordem de prioridade das chaves"""
        args = {'--name': 'Long', '-n': 'Short'}
        result = get_arg(args, '--name', '-n')
        
        self.assertEqual(result, 'Long')
    
    def test_many_aliases(self):
        """Testa múltiplos aliases"""
        args = {'-v': True}
        result = get_arg(args, '--verbose', '--verb', '-v', '-V', default=False)
        
        self.assertTrue(result)


class TestGetParamsSysArgs(unittest.TestCase):
    """Testes para a função get_params_sys_args() (API legada)"""
    
    def setUp(self):
        """Salva o sys.argv original antes de cada teste"""
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Restaura o sys.argv original após cada teste"""
        sys.argv = self.original_argv
    
    def test_basic_parsing(self):
        """Testa parsing básico com API legada"""
        sys.argv = ['script.py', '--text=hello', '--name=world']
        args = get_params_sys_args(['--text=', '--name='])
        
        self.assertEqual(args['--text='], 'hello')
        self.assertEqual(args['--name='], 'world')
    
    def test_missing_argument(self):
        """Testa argumento não fornecido"""
        sys.argv = ['script.py', '--text=hello']
        args = get_params_sys_args(['--text=', '--name='])
        
        self.assertIn('--text=', args)
        self.assertNotIn('--name=', args)
    
    def test_empty_value(self):
        """Testa valor vazio"""
        sys.argv = ['script.py', '--text=']
        args = get_params_sys_args(['--text='])
        
        self.assertEqual(args['--text='], '')
    
    def test_value_with_spaces(self):
        """Testa valor com espaços"""
        sys.argv = ['script.py', '--text=hello world']
        args = get_params_sys_args(['--text='])
        
        self.assertEqual(args['--text='], 'hello world')
    
    def test_short_arguments(self):
        """Testa argumentos curtos"""
        sys.argv = ['script.py', '-t=hello', '-n=world']
        args = get_params_sys_args(['-t=', '-n='])
        
        self.assertEqual(args['-t='], 'hello')
        self.assertEqual(args['-n='], 'world')
    
    def test_no_arguments(self):
        """Testa sem argumentos"""
        sys.argv = ['script.py']
        args = get_params_sys_args(['--text='])
        
        self.assertEqual(args, {})
    
    def test_silent_mode_default(self):
        """Testa modo silencioso por padrão"""
        sys.argv = ['script.py', '--text=hello']
        
        with patch('builtins.print') as mock_print:
            args = get_params_sys_args(['--text='])
            mock_print.assert_not_called()
    
    def test_silent_mode_true(self):
        """Testa modo silencioso explícito"""
        sys.argv = ['script.py', '--text=hello']
        
        with patch('builtins.print') as mock_print:
            args = get_params_sys_args(['--text='], silent=True)
            mock_print.assert_not_called()
    
    def test_verbose_mode(self):
        """Testa modo verbose"""
        sys.argv = ['script.py', '--text=hello']
        
        with patch('builtins.print') as mock_print:
            args = get_params_sys_args(['--text='], silent=False)
            mock_print.assert_called_once()
            call_args = str(mock_print.call_args)
            self.assertIn('--text=', call_args)
            self.assertIn('hello', call_args)
    
    def test_multiple_arguments_order(self):
        """Testa múltiplos argumentos em ordem"""
        sys.argv = ['script.py', '--first=1', '--second=2', '--third=3']
        args = get_params_sys_args(['--first=', '--second=', '--third='])
        
        self.assertEqual(args['--first='], '1')
        self.assertEqual(args['--second='], '2')
        self.assertEqual(args['--third='], '3')
    
    def test_argument_with_equals_in_value(self):
        """Testa argumento com '=' no valor"""
        sys.argv = ['script.py', '--equation=x=y+2']
        args = get_params_sys_args(['--equation='])
        
        self.assertEqual(args['--equation='], 'x=y+2')
    
    def test_numeric_values(self):
        """Testa valores numéricos"""
        sys.argv = ['script.py', '--port=8080', '--timeout=30']
        args = get_params_sys_args(['--port=', '--timeout='])
        
        self.assertEqual(args['--port='], '8080')
        self.assertEqual(args['--timeout='], '30')


class TestIntegration(unittest.TestCase):
    """Testes de integração combinando múltiplas funções"""
    
    def setUp(self):
        """Salva o sys.argv original antes de cada teste"""
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Restaura o sys.argv original após cada teste"""
        sys.argv = self.original_argv
    
    def test_get_args_with_get_arg(self):
        """Testa combinação de get_args() e get_arg()"""
        sys.argv = ['script.py', '-n', 'João', '--age', '25', '-v']
        args = get_args()
        
        name = get_arg(args, '--name', '-n', default='Anonymous')
        age = get_arg(args, '--age', '-a', default='0')
        verbose = get_arg(args, '--verbose', '-v', default=False)
        
        self.assertEqual(name, 'João')
        self.assertEqual(age, '25')
        self.assertTrue(verbose)
    
    def test_complex_scenario(self):
        """Testa cenário complexo com múltiplos tipos de argumentos"""
        sys.argv = [
            'script.py',
            '--host=localhost',
            '--port', '8080',
            '-d',
            '--config', '/path/to/config.json',
            '--verbose'
        ]
        args = get_args(defaults={'--host': '0.0.0.0', '--port': '3000'})
        
        host = get_arg(args, '--host', '-h')
        port = get_arg(args, '--port', '-p')
        debug = get_arg(args, '--debug', '-d', default=False)
        config = get_arg(args, '--config', '-c')
        verbose = get_arg(args, '--verbose', '-v', default=False)
        
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, '8080')
        self.assertTrue(debug)
        self.assertEqual(config, '/path/to/config.json')
        self.assertTrue(verbose)
    
    def test_backward_compatibility(self):
        """Testa retrocompatibilidade entre APIs"""
        sys.argv = ['script.py', '--text=hello', '--name=world']
        
        # API antiga
        old_args = get_params_sys_args(['--text=', '--name='])
        
        # API nova
        new_args = get_args()
        
        # Ambas devem funcionar
        self.assertEqual(old_args['--text='], 'hello')
        self.assertEqual(new_args['--text'], 'hello')


class TestEdgeCases(unittest.TestCase):
    """Testes de casos extremos e situações incomuns"""
    
    def setUp(self):
        """Salva o sys.argv original antes de cada teste"""
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Restaura o sys.argv original após cada teste"""
        sys.argv = self.original_argv
    
    def test_argument_starting_with_dash(self):
        """Testa valor que começa com traço"""
        sys.argv = ['script.py', '--number=-42']
        args = get_args()
        
        self.assertEqual(args['--number'], '-42')
    
    def test_empty_string_value(self):
        """Testa string vazia como valor"""
        sys.argv = ['script.py', '--text=']
        args = get_args()
        
        self.assertEqual(args['--text'], '')
    
    def test_unicode_characters(self):
        """Testa caracteres unicode"""
        sys.argv = ['script.py', '--name=José', '--emoji=😀']
        args = get_args()
        
        self.assertEqual(args['--name'], 'José')
        self.assertEqual(args['--emoji'], '😀')
    
    def test_very_long_value(self):
        """Testa valor muito longo"""
        long_value = 'a' * 1000
        sys.argv = ['script.py', f'--text={long_value}']
        args = get_args()
        
        self.assertEqual(args['--text'], long_value)
    
    def test_many_arguments(self):
        """Testa muitos argumentos"""
        sys.argv = ['script.py'] + [f'--arg{i}=value{i}' for i in range(100)]
        args = get_args()
        
        self.assertEqual(len(args), 100)
        for i in range(100):
            self.assertEqual(args[f'--arg{i}'], f'value{i}')
    
    def test_duplicate_arguments(self):
        """Testa argumentos duplicados (último prevalece)"""
        sys.argv = ['script.py', '--name=First', '--name=Second']
        args = get_args()
        
        # O último valor deve prevalecer
        self.assertEqual(args['--name'], 'Second')


if __name__ == '__main__':
    unittest.main()

