import sys
import grpc
from concurrent import futures
import threading

import estoque_pb2
import estoque_pb2_grpc

class EstoqueServiceServicer(estoque_pb2_grpc.EstoqueServiceServicer):
    def __init__(self, stop_event):
        #   prod_id (int) -> { 'descricao': str, 'quantidade': int }
        self.produtos = {}
        self.next_id = 1
        self.max_produtos = 100

        self._stop_event = stop_event

    def AdicionaProduto(self, request, context):
        # Descricao e quantidade são inteiros
        descricao = request.descricao
        quantidade = request.quantidade

        # Se já existir um produto com a mesma descrição, incrementa a quantidade
        for prod_id, dados in self.produtos.items():
            if dados['descricao'] == descricao:
                dados['quantidade'] += quantidade
                return estoque_pb2.AdicionaProdutoResponse(prod_id=prod_id)

        # Caso a descrição não exista em nenhum produto
        # Verifica se não passamos do limite de 100 produtos
        if len(self.produtos) >= self.max_produtos:
            pass

        # Cria um novo produto
        self.produtos[self.next_id] = {
            'descricao': descricao,
            'quantidade': quantidade
        }
        prod_id_retornado = self.next_id
        self.next_id += 1
        return estoque_pb2.AdicionaProdutoResponse(prod_id=prod_id_retornado)

    def AlteraQuantidadeProduto(self, request, context):
        prod_id = request.prod_id
        valor = request.valor

        # Verifica se o produto existe
        if prod_id not in self.produtos:
            # Retorna -2 se não existir
            return estoque_pb2.AlteraQuantidadeResponse(status=-2)

        produto = self.produtos[prod_id]
        quantidade_final = produto['quantidade'] + valor

        # Verifica se a nova quantidade não ficará negativa (return -1)
        if quantidade_final < 0:
            return estoque_pb2.AlteraQuantidadeResponse(status=-1)

        # Altera a quantidade e retorna a quantidade final
        produto['quantidade'] = quantidade_final
        return estoque_pb2.AlteraQuantidadeResponse(status=quantidade_final)

    def ListaProdutos(self, request, context):
        # Retorna todos os produtos em ordem de identificador
        lista_produtos = []
        for pid in sorted(self.produtos.keys()):
            dados = self.produtos[pid]
            lista_produtos.append(
                estoque_pb2.Produto(
                    prod_id=pid,
                    descricao=dados['descricao'],
                    quantidade=dados['quantidade']
                )
            )

        return estoque_pb2.ListaProdutosResponse(produtos=lista_produtos)

    def FimExecucao(self, request, context):
        # Retorna o número de produtos existentes e finaliza a execução
        n_prod = len(self.produtos)
        # Prepare a resposta antes de encerrar
        response = estoque_pb2.FimExecucaoResponse(n_prod=n_prod)
        
        self._stop_event.set()
        
        return response


def serve(port):
    
    # Criar thread para parar o servidor através de comando
    stop_event = threading.Event()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registramos nossa implementação do serviço no servidor
    estoque_pb2_grpc.add_EstoqueServiceServicer_to_server(
        EstoqueServiceServicer(stop_event),
        server
    )
    
    # O servidor escuta na porta especificada
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    # Aguardar pelo evento de finalização
    stop_event.wait()
    
    server.stop(1)
   
   
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 svc_estoque.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])
    if port < 2048 or port > 65535:
        print("A porta deve ser um inteiro entre 2048 e 65535")
        sys.exit(1)

    serve(port)
