import sys
import grpc

import estoque_pb2
import estoque_pb2_grpc

def main():
    if len(sys.argv) != 2:
        print("Uso: python cln_estoque.py <host:porta>", file=sys.stderr)
        sys.exit(1)
    
    server_address = sys.argv[1]
    
    channel = grpc.insecure_channel(server_address)
    stub = estoque_pb2_grpc.EstoqueServiceStub(channel)

    for line in sys.stdin:
        line = line.strip()
        
        # linha vazia
        if not line:
            continue

        # maxsplit é necessário para não cortar a descricao em substrings
        parts = line.split(' ', maxsplit=2)
        
        # maximo de partes é 3 (na instrucao P)
        if len(parts) > 3:
            continue
        
        cmd = parts[0]

        if cmd == "P":
            # P quantidade descricao...
            
            # wrong format
            if len(parts) < 3:
                continue
            
            qtd_str, descricao = parts[1], parts[2]
            
            try:
                qtd = int(qtd_str)
            except ValueError: # caso haja erro na conversao para int, ignorar
                continue

            request = estoque_pb2.AdicionaProdutoRequest(
                descricao=descricao,
                quantidade=qtd
            )
            response = stub.AdicionaProduto(request)
            print(response.prod_id)

        elif cmd == "Q":
            # Q prod_id valor
            
            # wrong format
            if len(parts) < 3:
                continue
            
            try:
                prod_id = int(parts[1])
                valor = int(parts[2])
            except ValueError:
                continue
            
            request = estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=valor)
            response = stub.AlteraQuantidadeProduto(request)
            print(response.status)

        elif cmd == "L":
            # lista todos os produtos
            request = estoque_pb2.ListaProdutosRequest()
            response = stub.ListaProdutos(request)
            
            # print "id descricao quantidade"
            for prod in response.produtos:
                print(prod.prod_id, prod.descricao, prod.quantidade)

        elif cmd == "F":
            # Encerra o servidor
            request = estoque_pb2.FimExecucaoRequest()
            response = stub.FimExecucao(request)
            print(response.n_prod)
            break
        
        else:
            continue


if __name__ == "__main__":
    main()
