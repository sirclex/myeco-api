from crud.base import CRUDBase
from models.wallet import Wallet
from schemas import WalletCreate, WalletUpdate

class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):
    pass

wallet = CRUDWallet(Wallet)