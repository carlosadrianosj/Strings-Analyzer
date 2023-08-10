import os
import sys
import zipfile
import rarfile
import gzip
import shutil
import py7zr

#  Função para extrair arquivos zip
def extract_zip(file_path, output_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)

# Função para extrair arquivos rar
def extract_rar(file_path, output_path):
    with rarfile.RarFile(file_path) as rf:
        rf.extractall(path=output_path)

# Função para extrair arquivos gzip
def extract_gzip(file_path, output_path):
    with gzip.open(file_path, 'rb') as f_in:
        with open(os.path.join(output_path, os.path.splitext(os.path.basename(file_path))[0]), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Função para extrair arquivos 7z
def extract_7z(file_path, output_path):
    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(path=output_path)

# Função para percorrer diretórios e extrair arquivos
def extract_files_in_directory(search_directory):
    for dirpath, dirs, files in os.walk(search_directory):
        for filename in files:
            file_path = os.path.join(dirpath, filename)

            # Cria um diretório de saída para cada arquivo
            output_path = os.path.join(dirpath, os.path.splitext(filename)[0])
            os.makedirs(output_path, exist_ok=True)

            # Verifica o tipo de arquivo e chama a função apropriada para extraí-lo
            if filename.lower().endswith(".zip"):
                extract_zip(file_path, output_path)
            elif filename.lower().endswith(".rar"):
                extract_rar(file_path, output_path)
            elif filename.lower().endswith(".gzip"):
                extract_gzip(file_path, output_path)
            elif filename.lower().endswith(".7z"):
                extract_7z(file_path, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python Extract_Compression.py <directory_path>")
        sys.exit(1)

    search_directory = sys.argv[1]
    if not os.path.exists(search_directory):
        print(f"Error: Diretório '{search_directory}' não existe.")
        sys.exit(1)

    extract_files_in_directory(search_directory)
