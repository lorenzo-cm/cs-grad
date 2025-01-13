.PHONY: clean stubs run_serv_estoque run_cli_estoque run_serv_pedidos run_cli_pedidos

PROTO_ESTOQUE = estoque.proto
PROTO_PEDIDOS = pedidos.proto

ESTOQUE_STUBS = estoque_pb2.py estoque_pb2_grpc.py
PEDIDOS_STUBS = pedidos_pb2.py pedidos_pb2_grpc.py

STUB_FILES = $(ESTOQUE_STUBS) $(PEDIDOS_STUBS)


all: stubs

stubs: $(STUB_FILES)

# Gera os stubs do estoque.proto, caso estejam desatualizados ou não existam
$(ESTOQUE_STUBS): $(PROTO_ESTOQUE)
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<

# Gera os stubs do pedidos.proto, caso estejam desatualizados ou não existam
$(PEDIDOS_STUBS): $(PROTO_PEDIDOS)
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<


run_serv_estoque: stubs
	python3 svc_estoque.py $(arg1)

run_cli_estoque: stubs
	python3 cln_estoque.py $(arg1)

run_serv_pedidos: stubs
	python3 svc_pedidos.py $(arg1) $(arg2)

run_cli_pedidos: stubs
	python3 cln_pedidos.py $(arg1) $(arg2)


clean:
	rm -f $(STUB_FILES)