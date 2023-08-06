# Correios Python 🚚

> **correios-utils** - Biblioteca para a realização de cotação de frete de encomendas no serviço dos Correios

## Instalação 📦

```bash
pip install correios-utils
```

## Exemplo de uso 📚

```python
from correios_utils import (
    Cotacao,
    FormatoEncomenda,
    SimNao,
    Servico,
    realizar_cotacao,
    get_descricao_servico,
)


if __name__ == '__main__':
    servicos = realizar_cotacao(
        cep_origem="70002900",
        cep_destino="04547000",
        codigos_servicos=[Servico.PAC, Servico.SEDEX, Servico.SEDEX_10],
        peso=1,
        comprimento=20,
        altura=20,
        largura=20,
        diametro=0,
        formato_encomenda=FormatoEncomenda.CAIXA_PACOTE,
        valor_declarado=0,
        mao_propria=SimNao.NAO,
        aviso_recebimento=SimNao.NAO,
        codigo_empresa="08082650",
        senha_empresa="564321",
    )

    for servico in servicos:
        if not servico.erro:
            print(f"Correios {get_descricao_servico(servico.codigo)}")
            print(f"Valor: R$ {servico.valor}")
            print(f"Prazo: {servico.prazo_entrega} dias", "\n")
```

### Saída 📋

```
Correios PAC
Valor: R$ 27.8
Prazo: 7 dias 

Correios SEDEX
Valor: R$ 53.1
Prazo: 1 dias 
```
