from web3 import Web3


class TokenBalanceChecker:

    def __init__(self):
        self.provider_url = provider_url
        self.web3 = Web3(Web3.HTTPProvider(provider_url))

    def get_token_balance(self, address):
        contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
        balance = contract.functions.balanceOf(
            Web3.to_checksum_address(address)).call()
        decimals = contract.functions.decimals().call()
        balance_in_token = balance / 10 ** decimals
        return balance_in_token

    def check_address(self, address):
        return Web3.is_address(address)


provider_url = 'https://mainnet.infura.io/v3/5a45911c58bd4c42b335168f91866991'
token_address = '0x2ecba91da63c29ea80fbe7b52632ca2d1f8e5be0'  # 替换为目标代币的合约地址

# ERC20 ABI (需要替换为特定代币的 ABI)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]
