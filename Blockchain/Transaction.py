from Utils.hashlib_util import sha

class Transaction:
    def __init__(self, size, tx_fee):
        # self.value = tx_value
        self.tx_fee = tx_fee
        self.size = size
        self.sats_per_byte = tx_fee / size

    @property
    def tx_hash(self):
        return sha(str(self.tx_fee) + str(self.size))

    def __hash__(self):
        return self.tx_hash

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return Transaction(self.size, self.tx_fee)