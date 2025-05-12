import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Leitor de mapa para busca de caminhos")
    parser.add_argument("filename", type=str, help="Caminho para o arquivo do mapa")
    parser.add_argument("method", type=str, help="Identificador do método a ser utilizado")
    parser.add_argument("xi", type=int, help="Coordenada x inicial")
    parser.add_argument("yi", type=int, help="Coordenada y inicial")
    parser.add_argument("xf", type=int, help="Coordenada x final")
    parser.add_argument("yf", type=int, help="Coordenada y final")

    return parser.parse_args()