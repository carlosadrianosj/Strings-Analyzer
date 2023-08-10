import os
import subprocess
import argparse
import shlex
from collections import defaultdict
import csv

def create_parser():
    '''
    Função para criar um ArgumentParser para lidar com argumentos da linha de  comando.
    '''
    parser = argparse.ArgumentParser(description='Busca strings em arquivos dentro de um diretório.')
    parser.add_argument('dir', type=str, help='O diretório onde a busca será realizada.')
    parser.add_argument('-fast', action='store_true', help='Executa a busca usando utilitários do Linux.')
    return parser


def get_target_strings():
    '''
    Função para ler o arquivo de strings alvo e retornar uma lista das strings.
    '''
    with open('target_strings.txt', 'r') as f:
        target_strings = [line.strip() for line in f]
    return target_strings

def execute_command(search_directory, target_string):
    '''
    Função para executar o comando grep e retornar a saída.
    '''
    command = f"grep -riwoE '{target_string}' {search_directory}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return out

def parse_results(out):
    '''
    Função para analisar a saída do comando grep e retornar um dicionário dos resultados.
    '''
    lines = out.decode('utf-8').splitlines()
    results = defaultdict(list)
    for line in lines:
        if ':' in line:
            filepath, match = line.split(':', 1)
            results[filepath].append(match)
    return results

def print_results(results):
    '''
    Função para imprimir os resultados como uma tabela.
    '''
    print(f"{'Arquivo':<150} {'Strings'}")
    for filepath, matches in results.items():
        filename = os.path.basename(filepath)
        print(f"{filename:<150} {matches}")

def save_results(results):
    '''
    Função para salvar os resultados em um arquivo CSV.
    '''
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Caminho', 'Strings'])
        for filepath, matches in results.items():
            writer.writerow([filepath, ', '.join(matches)])

def main():
    '''
    Função principal que coordena a execução do script.
    '''
    parser = create_parser()
    args = parser.parse_args()
    target_strings = get_target_strings()
    target_string = '|'.join(target_strings)
    search_directory = shlex.quote(args.dir)
    
    if args.fast:
        out = execute_command(search_directory, target_string)
        results = parse_results(out)
        print_results(results)
        save_results(results)

if __name__ == "__main__":
    main()
