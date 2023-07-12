"""Lista de Supermercado"""

# Bibliotecas
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

try:
    from routes.api import router as api_router
    from models.produto import ProdutoModel, ResponseModel
    from db import database
except:
    from lista_supermercado_mongodb.routes.api import router as api_router
    from lista_supermercado_mongodb.models.produto import ProdutoModel, ResponseModel
    from lista_supermercado_mongodb.db import database

class Produto(BaseModel):
    item: str
    quantidade: int
    tipo: str

# Cria uma instância da classe FastAPI para habilitar a interação com nossa API
app = FastAPI()
lista_supermercado = []

origins = ["http://0.0.0.0:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# ============================================================================================
# ============================================================================================
# ============================================================================================

@app.get('/carrinho')
async def listar_produtos():
    """Método que será chamado quando for requisitada a rota GET /produtos"""

    if len(lista_supermercado) > 0 :
        message = lista_supermercado
    else:
        message = {"message": "A lista do supermercado está vazia!"}

    return JSONResponse(
        status_code = 200,
        content = message,
    )

@app.get('/carrinho/comida')
async def listar_produtos_comida():
    """Método que será chamado quando for requisitada a rota GET /produtos"""

    if len(lista_supermercado) > 0 :
        message = lista_supermercado
    else:
        message = {"message": "A lista do supermercado está vazia!"}

    return JSONResponse(
        status_code = 200,
        content = message,
    )

@app.get('/carrinho/bebida')
async def listar_produtos_bebida():
    """Método que será chamado quando for requisitada a rota GET /produtos"""

    if len(lista_supermercado) > 0 :
        message = lista_supermercado
    else:
        message = {"message": "A lista do supermercado está vazia!"}

    return JSONResponse(
        status_code = 200,
        content = message,
    )

@app.get('/carrinho/pesquisar/{item}')
async def obter_produto(item: str):
    """Método que será chamado quando for requisitada a rota GET /produtos/{item}"""

    found = False
    for produto in lista_supermercado:
        if produto['item'] == item:
            message = produto
            found = True
            break

    if not found:
        message = {"message": "Produto " + item + " não foi encontrado na lista!"}

    return JSONResponse(
        status_code=200,
        content=message,
    )

@app.post('/carrinho')
async def adicionar_produto(produto : Produto):
    """Método que será chamado quando for requisitada a rota POST /produtos"""

    lista_supermercado.append(produto.dict())

    message = {"message": "Produto adicionado com sucesso!"}

    return JSONResponse(
        status_code = 200,
        content = message,
    )


@app.put('/carrinho/atualizar/{item}')
async def atualizar_produto(item: str, produto: Produto):
    """Método que será chamado quando for requisitada a rota PUT /produtos/{item}"""

    found = False
    for produto_a_atualizar in lista_supermercado:
        if produto_a_atualizar['item'] == item:
            lista_supermercado.remove(produto_a_atualizar)
            found = True
            break

    if not found:
        message = {"message": "Produto " + item + " não foi encontrado na lista!"}
    else:
        lista_supermercado.append(produto.dict())
        message = {"message": "Produto " + item + " atualizado com sucesso na lista!"}

    return JSONResponse(
        status_code=200,
        content=message,
    )

@app.delete('/carrinho')
async def apagar_lista():
    """Método que será chamado quando for requisitada a rota DELETE /produtos/"""

    lista_supermercado.clear()
    message = {"message": "Lista apagada com sucesso!"}

    return JSONResponse(
        status_code=200,
        content=message,
    )

@app.delete('/carrinho/apagar/{item}')
async def apagar_lista_item(item:str):
    """Método que será chamado quando for requisitada a rota DELETE /produtos/"""

    lista_supermercado.pop()
    message = {"message": "Lista apagada com sucesso!"}

    return JSONResponse(
        status_code=200,
        content=message,
    )

@app.get('/carrinho/valor')
async def obter_valor():
    """Método que será chamado quando for requisitada a rota GET /produtos/{item}"""
    quantidade_ok = False
    cardapio = await database.listar_produtos()
    soma = 0

# =====================================================================================================================
    somas = {}

    for item in lista_supermercado:
        nome = item["item"]
        quantidade = item["quantidade"]

        if nome in somas:
            somas[nome] += quantidade
        else:
            somas[nome] = quantidade

    new_carrinho = [{"item": nome, "quantidade": quantidade,"tipo":"carrinho"} for nome, quantidade in somas.items()]

    lista_supermercado.clear()
    for i in new_carrinho:
        lista_supermercado.append(i)
# =====================================================================================================================
    for item1 in lista_supermercado:
        for item2 in cardapio:
            if item1["item"] == item2["item"]:
                soma+=item2["preco"]*item1["quantidade"]
                break
# =====================================================================================================================

    for item1 in lista_supermercado:
        for item2 in cardapio:
            if item1["item"] == item2["item"]:
                if item1["quantidade"]<=item2["quantidade"]:
                    quantidade_ok = True

    if not len(cardapio) > 0:
        message = {"message": "Nao existem produtos no cardapio."}
    elif not len(lista_supermercado) > 0:
        message = {"message": "Nao existem produtos no carrinho."}
    elif not quantidade_ok:
        message = {"message": "Nao existem produtos suficientes."}
    else:
        message = {"message": "Total do pedido: R$" + str(soma)}

    return JSONResponse(
        status_code=200,
        content=message,
    )

@app.post('/carrinho/finalizar')
async def finalizar_pedido():
    """Método que será chamado quando for requisitada a rota POST /produtos"""

    message = {"message": "Pedido finalizado com sucesso!"}

    return JSONResponse(
        status_code = 200,
        content = message,
    )

# ============================================================================================
# ============================================================================================
# ============================================================================================



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, log_level="info", reload=True)
    print("running")
