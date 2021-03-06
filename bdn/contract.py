import os
import json
import web3
from django.conf import settings


w3 = web3.Web3(web3.HTTPProvider(os.environ['ETHEREUM_NODE']))


_contracts = {}


def contract(contract_name):
    global _contracts

    if _contracts.get(contract_name):
        return _contracts.get(contract_name)

    json_path = os.path.join(
        settings.BASE_DIR, 'contracts', '{0}.json'.format(contract_name))
    contract_interface = json.load(open(json_path))
    for _, network in contract_interface['networks'].items():
        _contracts[contract_name] = w3.eth.contract(
            address=web3.Web3.toChecksumAddress(network['address']),
            abi=contract_interface['abi'])
    return _contracts[contract_name]
