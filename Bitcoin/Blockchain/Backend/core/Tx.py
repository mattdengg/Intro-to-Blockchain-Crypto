from Blockchain.Backend.core.Script import Script

class Tx:
    def __init__(self, version, tx_inputs, tx_outputs, locktime):
        self.version = version
        self.tx_inputs = tx_inputs
        self.tx_outputs = tx_outputs
        self.locktime = locktime

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig = None, seq = 0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.seq = seq

class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount                # how much we are sending
        self.script_pubkey = script_pubkey  # to who we are sending