# Blockchain Core


---

## Key Concepts Learned

### SHA256
- **Definition**: Secure Hash Algorithm 256 bits is a cryptographic hash function that takes any input (file, password, or message) and produces a fixed length output. (64 hexadecimal characters)
- **How it works**: 
  - Feed any amount of data and SHA-256 will always return a 64 character string
  - One-way function, impossible to figure out the original input or find two inputs that will produce the same output
- **Steps to Convert**:
  - Converts message to binary on a 512-bit block, with each character being 8-bits
  - Add a single 1-bit -> then add 0's until total length = 448 mod 512 (512-448)
  - Add the length of your message for the remaining 64-bits

### Merkle Root
- **Definition**: The single hash value at the top of a Merkle tree that represents all transactions in a block
- **How it works**: 
  - Each transaction is hashed
  - Transaction hashes are paired and hashed together to create parent nodes
  - Process continues until one hash remains at the top
- **Benefits**:
  - Ensures data integrity - any change to a transaction changes the Merkle root
  - Enables efficient verification without downloading entire blocks
  - Provides cryptographic proof of transaction inclusion
  
### Genesis Block
- **Definition**: 
  - First Block ever created in a blockchain
  - Has no previous block,so its previous block has field is just all zeros
  
### Block Header
- **Version**
  - A number that tells the network what "rules" or "format" this block follows
  - Makes sure every node understands how to interpret the block
  
- **PrevBlockHash**
  - Links blocks together into a chain, ensuring that if someone tries to change an old block, every block after becomes invalid (hashes break)
  
- **Merkle Root**
  - Single has that summarizes all transactions in the block
  - Built by repeatedly hashing pairs of transactions until only one hash remains
  - Lets you prove that a transaction is included in a block without downloading the whole block (SPVs: Simplified Payment Verification use this)
  - "Summary signature"
  
- **Timestamp**
  - Time when miner created the block 
  - Keeps blocks ordered and allows nodes to estimate when each was mined
  
- **nBits**
  - Compact representation of how hard it is to find a valid block hash
  - Determines how many leading zeros the block hash must have
  
- **Nonce**
  - Miners keep changing to try to find a hash that satisfies the difficulty target
  - Proof of work 
  - Hash the header billions of times with different nonces until one result meets the difficulty requirement

### Implementation Notes
- Used SHA-256 hashing for blocks and transactions
- Built Merkle tree construction for transaction verification
- Implemented basic proof-of-work mining simulation
- Created block validation and chain integrity checks

---

## Code Implementation

### Files Created
- `Block` class - block creation and validation
- `Blockchain` class - chain management and mining
- `BlockHeader` class - block metadata
- Utility functions for hashing and Merkle root calculation

### Key Features
- SHA-256 hashing
- Merkle tree construction
- Basic proof-of-work
- Block validation
- Chain integrity checks

---

## Questions & Further Learning
- [ ] How does proof-of-work difficulty adjustment work?
- [ ] What are the different consensus mechanisms?
- [ ] How do transaction fees work in practice?
- [ ] What are the scalability challenges?

---

## Resources & References
- [What is SHA-256? (Video)](https://youtu.be/PbFVTb7Pndc)
- [SHA-256 Algorithm](https://www.simplilearn.com/tutorials/cyber-security-tutorial/sha-256-algorithm)

