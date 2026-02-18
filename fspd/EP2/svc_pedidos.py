import sys
import grpc
from concurrent import futures
import threading

import estoque_pb2
import estoque_pb2_grpc

import pedidos_pb2
import pedidos_pb2_grpc

class PedidosServiceServicer(pedidos_pb2_grpc.PedidosServiceServicer):
    def __init__(self, server_estoque_addr, stop_event):
        self._stop_event = stop_event
        
        self.pedidos = {}
        self.next_id = 1
        
        channel = grpc.insecure_channel(server_estoque_addr)
        self.stub = estoque_pb2_grpc.EstoqueServiceStub(channel)

    def CriaPedido(self, request, context):
        # Recebe lista de produtos e suas respectivas quantidades
        list_prod_id = request.list_prod_id
        list_quantidade = request.list_quantidade
        
        # Reduzir quantidade dos itens
        # Caso o servidor de estoque me retorne >= 0, quer dizer que deu certo e retorno zero
        # Caso contrario retorno o mesmo que o servidor de estoque
        list_status = []
        for prod_id, quant in zip(list_prod_id, list_quantidade):
            request = estoque_pb2.AlteraQuantidadeRequest(
                prod_id=prod_id,
                valor=-quant
            )
            
            # has only status
            response = self.stub.AlteraQuantidadeProduto(request)
            
            status = response.status
            
            if status >= 0:
                list_status.append(0)
            elif status == -1:
                list_status.append(-1)
            elif status == -2:
                list_status.append(-2)
        
        # Conforme descrito no fórum, implementarei o caso em que todos
        # os itens são inálidos, de maneira que o pedido é criado somente quando
        # existe pelo menos algum produto válido
        if 0 in list_status:
            self.pedidos[self.next_id] = {
                'list_prod_id': list_prod_id,
                'list_quantidade': list_quantidade,
                'list_status': list_status,
                'cancelado': False
            }
            
            self.next_id += 1
            
        return pedidos_pb2.CriaPedidoResponse(list_prod_id=list_prod_id,
                                              list_status=list_status)
    
    
    def CancelaPedido(self, request, context):
        pedido_id = request.pedido_id
        
        # se o pedido não existe
        try:
            pedido = self.pedidos[pedido_id]
        except Exception:
            return pedidos_pb2.CancelaPedidoResponse(status=-1)
        
        # se o pedido já foi cancelado anteriormente
        if pedido['cancelado']:
            return pedidos_pb2.CancelaPedidoResponse(status=-1)
        
        list_prod_id = pedido['list_prod_id']
        list_quantidade = pedido['list_quantidade']
        list_status = pedido['list_status']
        zip_lists = zip(list_prod_id, list_quantidade, list_status)
        
        # Dar rollback nas quantidades
        for prod_id, quant, status in zip_lists:
            if status == 0:
                request = estoque_pb2.AlteraQuantidadeRequest(
                    prod_id=prod_id,
                    valor=quant
                )
                
                # Retorna os status, mas não preciso
                response = self.stub.AlteraQuantidadeProduto(request)
                
        pedido['cancelado'] = True
        
        return pedidos_pb2.CancelaPedidoResponse(status=0)
    
    
    def FimExecucao(self, request, context):
        # pede fim da execucao do servidor de estoque
        request = estoque_pb2.FimExecucaoRequest()
        response = self.stub.FimExecucao(request)
        num_produtos = response.n_prod
        
        # Retorna o número de produtos e pedidos ativos e finaliza
        num_pedidos_ativos = sum(1 for pedido in self.pedidos.values() if not pedido['cancelado'])

        
        return_value = pedidos_pb2.FimExecucaoResponse(
            num_produtos=num_produtos,
            num_pedidos=num_pedidos_ativos
        )
             
        self._stop_event.set()
        
        return return_value
    

def serve(port, estoque_server_addr):
    # Mesmo esquema de finalização do servidor
    stop_event = threading.Event()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registramos nossa implementação do serviço no servidor
    pedidos_pb2_grpc.add_PedidosServiceServicer_to_server(
        PedidosServiceServicer(estoque_server_addr, stop_event),
        server
    )
    
    # O servidor escuta na porta especificada
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    stop_event.wait()
    
    server.stop(1)
   
   
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python3 svc_pedidos.py <porta> <estoque_server_addr>")
        sys.exit(1)

    port = int(sys.argv[1])
    if port < 2048 or port > 65535:
        print("A porta deve ser um inteiro entre 2048 e 65535")
        sys.exit(1)

    estoque_server_addr = sys.argv[2]

    serve(port, estoque_server_addr)