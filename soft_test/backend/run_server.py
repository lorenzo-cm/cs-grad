import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    import uvicorn

    print("Iniciando servidor Wordle API...")
    print("Servidor: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")

    try:
        from app.main import app
        print("Aplicação carregada.")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[current_dir]
    )
