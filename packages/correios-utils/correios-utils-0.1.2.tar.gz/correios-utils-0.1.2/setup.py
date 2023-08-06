# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['correios_utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'correios-utils',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Correios Python 🚚\n\n> **correios-utils** - Biblioteca para a realização de cotação de frete de encomendas no serviço dos Correios\n\n## Instalação 📦\n\n```bash\npip install correios-utils\n```\n\n## Exemplo de uso 📚\n\n```python\nfrom correios_utils import (\n    Cotacao,\n    FormatoEncomenda,\n    SimNao,\n    Servico,\n    realizar_cotacao,\n    get_descricao_servico,\n)\n\n\nif __name__ == \'__main__\':\n    servicos = realizar_cotacao(\n        cep_origem="70002900",\n        cep_destino="04547000",\n        codigos_servicos=[Servico.PAC, Servico.SEDEX, Servico.SEDEX_10],\n        peso=1,\n        comprimento=20,\n        altura=20,\n        largura=20,\n        diametro=0,\n        formato_encomenda=FormatoEncomenda.CAIXA_PACOTE,\n        valor_declarado=0,\n        mao_propria=SimNao.NAO,\n        aviso_recebimento=SimNao.NAO,\n        codigo_empresa="08082650",\n        senha_empresa="564321",\n    )\n\n    for servico in servicos:\n        if not servico.erro:\n            print(f"Correios {get_descricao_servico(servico.codigo)}")\n            print(f"Valor: R$ {servico.valor}")\n            print(f"Prazo: {servico.prazo_entrega} dias", "\\n")\n```\n\n### Saída 📋\n\n```\nCorreios PAC\nValor: R$ 27.8\nPrazo: 7 dias \n\nCorreios SEDEX\nValor: R$ 53.1\nPrazo: 1 dias \n```\n',
    'author': 'Douglas Gusson',
    'author_email': 'douglasgusson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
