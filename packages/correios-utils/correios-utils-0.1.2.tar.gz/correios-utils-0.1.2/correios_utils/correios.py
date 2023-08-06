from enum import Enum

from typing import List
from dataclasses import dataclass

import requests
import xmltodict

class FormatoEncomenda(Enum):
    CAIXA_PACOTE = 1
    ROLO_PRISMA = 2
    ENVELOPE = 3

class Servico(Enum):
    PAC = "04510"
    SEDEX = "04014"
    SEDEX_10 = "04790"
    SEDEX_12 = "04782"
    SEDEX_HOJE = "04804"

class SimNao(Enum):
    SIM = "S"
    NAO = "N"

@dataclass
class Cotacao:
    codigo: str
    valor: float
    prazo_entrega: int
    valor_sem_adicionais: float
    valor_mao_propria: float
    valor_aviso_recebimento: float
    valor_valor_declarado: float
    entrega_domiciliar: str
    entrega_sabado: str
    obs_fim: str
    erro: int
    msg_erro: str

    @staticmethod
    def from_dict(d: dict) -> 'Cotacao':
        return Cotacao(
            codigo=d.get('Codigo'),
            valor=float((d.get('Valor') or "0").replace(',', '.')),
            prazo_entrega=int(d.get('PrazoEntrega')),
            valor_sem_adicionais=float((d.get('ValorSemAdicionais') or "0").replace(",", ".")),
            valor_mao_propria=float((d.get('ValorMaoPropria') or "0").replace(",", ".")),
            valor_aviso_recebimento=float((d.get('ValorAvisoRecebimento') or "0").replace(",", ".")),
            valor_valor_declarado=float((d.get('ValorValorDeclarado') or "0").replace(",", ".")),
            entrega_domiciliar=d.get('EntregaDomiciliar'),
            entrega_sabado=d.get('EntregaSabado'),
            obs_fim=d.get('obsFim'),
            erro=int(d.get('Erro')),
            msg_erro=d.get('MsgErro')
        )


def get_descricao_servico(codigo: str):
    if codigo == "04510":
        return "PAC"
    elif codigo == "04014":
        return "SEDEX"
    elif codigo == "04790":
        return "SEDEX 10"
    elif codigo == "04782":
        return "SEDEX 12"
    elif codigo == "04804":
        return "SEDEX HOJE"
    else:
        return "Não identificado"

"""
https://www.correios.com.br/atendimento/ferramentas/sistemas/arquivos/manual-de-implementacao-do-calculo-remoto-de-precos-e-prazos/view
"""
def realizar_cotacao(
    cep_origem: str,
    cep_destino: str,
    codigos_servicos: List[Servico],
    peso: float,
    comprimento: float,
    altura: float,
    largura: float,
    diametro: float = 0,
    formato_encomenda: FormatoEncomenda = FormatoEncomenda.CAIXA_PACOTE,
    valor_declarado: float = 0,
    mao_propria: SimNao = SimNao.NAO,
    aviso_recebimento: SimNao = SimNao.NAO,
    codigo_empresa: str = "",
    senha_empresa: str = ""
) -> List[Cotacao]:
    servicos = ",".join(servico.value for servico in codigos_servicos)

    if (codigo_empresa == "" or senha_empresa == "") and len(codigos_servicos) > 1:
        raise ValueError("É necessário informar o código da empresa e a senha para realizar a cotação com mais de um serviço")

    base_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?{}"
    url_cotacao = base_url.format(
        (
            f"nCdEmpresa={codigo_empresa}&"       
            f"sDsSenha={senha_empresa}&"
            f"sCepOrigem={cep_origem}&"
            f"sCepDestino={cep_destino}&"
            f"nVlPeso={peso}&"
            f"nCdFormato={formato_encomenda.value}&"
            f"nVlComprimento={comprimento}&"
            f"nVlAltura={altura}&"
            f"nVlLargura={largura}&"
            f"sCdMaoPropria={mao_propria.value}&"
            f"nVlValorDeclarado={valor_declarado}&"
            f"sCdAvisoRecebimento={aviso_recebimento.value}&"
            f"nCdServico={servicos}&"
            f"nVlDiametro={diametro}&"
            "StrRetorno=xml&"
            "nIndicaCalculo=3"
        )
    )

    req = requests.get(url_cotacao)

    if req.status_code != 200:
        raise RuntimeError(f"Erro ao realizar a cotação. Código de erro: {req.status_code}")

    parsed_xml = xmltodict.parse(req.text)
    servicos = parsed_xml['Servicos']['cServico']

    print(url_cotacao, "\n")

    return [Cotacao.from_dict(servico) for servico in servicos]



if __name__ == '__main__':
    servicos = realizar_cotacao(
        cep_origem="70002900",
        cep_destino="04547000",
        codigos_servicos=[Servico.PAC, Servico.SEDEX, Servico.SEDEX_10],
        peso=5,
        comprimento=50,
        altura=35,
        largura=45,
        diametro=0,
        formato_encomenda=FormatoEncomenda.CAIXA_PACOTE,
        valor_declarado=300,
        mao_propria=SimNao.NAO,
        aviso_recebimento=SimNao.NAO,
        codigo_empresa="08082650",
        senha_empresa="564321",
    )

    for servico in servicos:
        if servico.erro == 0:
            print(f"Correios {get_descricao_servico(servico.codigo)}")
            print(f"Valor: R$ {servico.valor}")
            print(f"Prazo: {servico.prazo_entrega} dias", "\n")
