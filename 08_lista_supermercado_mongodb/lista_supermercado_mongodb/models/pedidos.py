"""Modelos usados para a criação das tabelas no banco de dados"""

# Bibliotecas
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from typing import Optional

try:
    from models.PyObjectId import PyObjectId

except:
    from lista_supermercado_mongodb.models.PyObjectId import PyObjectId


class PedidoModel(BaseModel):
    item: str
    quantidade: int

    def as_dict(self):
        return {"item": self.item,
                "quantidade": self.quantidade}

class PedidoUpdateModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    item: str = Field(..., title="Descricao do item", max_length=500)
    quantidade: int = Field(..., title="Quantidade de itens")

    def as_dict(self):
        return {"id": self.id,
                "item": self.item,
                "quantidade": self.quantidade}

def ResponseModel(message, code):
    return JSONResponse(
        status_code=code,
        content=message,
    )

