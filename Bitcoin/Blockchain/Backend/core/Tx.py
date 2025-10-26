from Blockchain.Backend.core.Script import Script
from Blockchain.Backend.util.util import int_to_little_endian, bytes_needed, decode_base58, little_endian_to_int, encode_varint, hash256

ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '11006542436963211066068844580937223233186503174135729272920753217244439735835'
MINER_ADDRESS = '1EGizaAaBHhRSqdebu2mkrqzfxdUaEKChN'

class CoinbaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight, bytes_needed(BlockHeight))

    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xFFFFFFFF

        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)

        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount = target_amount, script_pubkey= target_script))
        coinBaseTx = Tx(1, tx_ins, tx_outs, 0)
        coinBaseTx.TxId = coinBaseTx.id()
        return coinBaseTx


class Tx:
    def __init__(self, version, tx_inputs, tx_outputs, locktime):
        self.version = version
        self.tx_inputs = tx_inputs
        self.tx_outputs = tx_outputs
        self.locktime = locktime

    def id(self):
        """
        Human-readable Tx id
        """
        return self.hash().hex()

    def hash(self):
        """
        Binary hash of serialization
        """
        return hash256(self.serialize())[::-1]

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_inputs))

        for tx_in in self.tx_inputs:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outputs))

        for tx_out in self.tx_outputs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)
        return result


    def is_coinbase(self):
        """
        Checks that there is exactly one input
        Grabs the first input and check if the prev_tx is b'\x00' * 32
        Check that the first input prev_index is 0xffffffff
        """
        if len(self.tx_inputs) != 1:
            return False

        first_input = self.tx_inputs[0]

        if first_input.prev_tx != b"\x00" * 32:
            return False

        if first_input.prev_index != 0xFFFFFFFF:
            return False

        return True

    def to_dict(self):
        """
        Converts Coinbase Transaction
            Converts prev_tx Hash in hex from bytes
            Converts BlockHeight in hex which is stores in Script signature
        """

        if self.is_coinbase():
            self.tx_inputs[0].prev_tx = self.tx_inputs[0].prev_tx.hex()
            self.tx_inputs[0].script_sig.cmds[0] = little_endian_to_int(self.tx_inputs[0].script_sig.cmds[0])
            self.tx_inputs[0].script_sig = self.tx_inputs[0].script_sig.__dict__

        self.tx_inputs[0] = self.tx_inputs[0].__dict__

        """
        Convert Transaction Output to dic
            If there are numbers, we don't need to do anything
            If values is in bytes, convert to hex
            Loop through all the TxOut objects and convert them to dict
        """
        self.tx_outputs[0].script_pubkey.cmds[2] = self.tx_outputs[0].script_pubkey.cmds[2].hex()
        self.tx_outputs[0].script_pubkey = self.tx_outputs[0].script_pubkey.__dict__
        self.tx_outputs[0] = self.tx_outputs[0].__dict__

        return self.__dict__


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig = None, seq = 0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.seq = seq

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.seq, 4)
        return result

class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount                # how much we are sending
        self.script_pubkey = script_pubkey  # to who we are sending

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result