from sortedcontainers import SortedList


class Mempool:
    def __init__(self, key=lambda tx: tx.sats_per_byte):
        self.key = key
        self.mempool = SortedList([], key=key)

    def add(self, tx):
        self.mempool.add(tx)

    def get_top_1mb_transactions(self) -> SortedList:
        txs = []
        size_so_far = 0
        for tx in self.mempool:
            if tx.size + size_so_far > 1_000_000:
                break
            txs.append(tx)
        return SortedList(txs, key=self.key)

    def get_value_of_transactions(self):
        return sum(tx.tx_fee for tx in self.mempool)

    def get_transaction_list(self) -> SortedList:
        return self.mempool

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        new_mempool = self.mempool.copy()
        new_o = Mempool()
        new_o.mempool = new_mempool
        return new_o

    def __len__(self):
        return len(self.mempool)