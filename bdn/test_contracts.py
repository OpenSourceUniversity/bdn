# flake8: noqa
import unittest
from unittest.mock import mock_open, patch
from bdn import contract


CONTRACT_JSON = """
{
  "contractName": "test",
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "name": "IpfsHash",
          "type": "bytes"
        },
        {
          "indexed": false,
          "name": "learner",
          "type": "address"
        }
      ],
      "name": "IPFSverification",
      "type": "event"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_ipfsHash",
          "type": "bytes"
        },
        {
          "name": "_learnerAddress",
          "type": "address"
        }
      ],
      "name": "sendHash",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ],
  "networks": {
    "5888": {
      "events": {},
      "links": {},
      "address": "0xc0fc2e45e3165a9758bcee23ec54315f023cd054",
      "transactionHash": "0x3c1a214b4d613509968f3e8f2b4867a7138248cd9ce8549424ca0803b71b954e"
    }
  },
  "schemaVersion": "2.0.1",
  "updatedAt": "2018-08-11T12:00:17.665Z"
}
"""


class ContractsTest(unittest.TestCase):
    @patch('bdn.contract.open',
           mock_open(read_data=CONTRACT_JSON))
    def test_contract(self):
        for _ in range(2):  # iterate twice to check reading from cache
            result = contract.contract('test')
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
