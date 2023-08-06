from .correios import (
    Cotacao,
    FormatoEncomenda,
    SimNao,
    Servico,
    realizar_cotacao,
    get_descricao_servico,
)

__all__ = [
    "Cotacao",
    "Servico",
    "FormatoEncomenda",
    "SimNao",
    "realizar_cotacao",
    "get_descricao_servico",
]

__version__ = "0.1.2"
