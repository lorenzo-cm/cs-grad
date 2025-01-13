import sys
import grpc

import pedidos_pb2
import pedidos_pb2_grpc

import estoque_pb2
import estoque_pb2_grpc

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 cln_pedidos.py <estoque_addr:port> <pedidos_addr:port>")
        sys.exit(1)
        
    _estoque_addr = sys.argv[1]
    _pedidos_addr = sys.argv[2]
    
    # Conexão com os servidores
    _estoque_channel = grpc.insecure_channel(_estoque_addr)
    _pedidos_channel = grpc.insecure_channel(_pedidos_addr)
    
    estoque_stub = estoque_pb2_grpc.EstoqueServiceStub(_estoque_channel)
    pedidos_stub = pedidos_pb2_grpc.PedidosServiceStub(_pedidos_channel)
    
    # List products
    request = estoque_pb2.ListaProdutosRequest()
    response = estoque_stub.ListaProdutos(request)
    
    for prod in response.produtos:
        print(prod.prod_id, prod.descricao, prod.quantidade)
        
    
    # Start get the inputs
    for line in sys.stdin:
        line = line.strip()
        
        # linha vazia
        if not line:
            continue
        
        # particionar nos espaços
        parts = line.split(' ')
        
        cmd = parts[0]
        
        if cmd == 'P':
            # pares de dados + cmd
            # caso o input esteja faltante, ignorar
            if len(parts) % 2 == 0:
                continue
            
            # adicionar os produtos e quantidades nas listas
            # para isso itero de 2 em 2 visto que são pares produto e quantidade
            # assim, o par tem o mesmo indice nas duas listas
            try:
                list_prod_id = []
                list_quantidade = []
                # iterar sobre os pares
                for i in range(1, len(parts), 2):
                    list_prod_id.append(int(parts[i]))
                    list_quantidade.append(int(parts[i+1]))
            except:
                continue
            
            
            request = pedidos_pb2.CriaPedidoRequest(
                list_prod_id = list_prod_id,
                list_quantidade = list_quantidade
            )
            
            response = pedidos_stub.CriaPedido(request)
            
            list_status = response.list_status
            
            for prod, stat in zip(list_prod_id, list_status):
                print(prod, stat)
                
                
        elif cmd == 'X':
            # X pedido_id
            if len(parts) != 2:
                continue
            
            try:
                pedido_id = int(parts[1])
                
                request = pedidos_pb2.CancelaPedidoRequest(pedido_id=pedido_id)
                response = pedidos_stub.CancelaPedido(request)
                
                print(response.status)
                
            except Exception:
                continue
            
        
        elif cmd == 'T':            
            request = pedidos_pb2.FimExecucaoRequest()
            response = pedidos_stub.FimExecucao(request)
            
            num_produtos = response.num_produtos
            num_pedidos = response.num_pedidos
            
            print(num_produtos, num_pedidos)
            sys.exit(0)
        
        else:
            continue
                
if __name__ == "__main__":
    main()
