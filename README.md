# Blockchain with Flask and Ethash

The script is a simple blockchain implementation using Flask web framework and Ethash algorithm. The script uses Ethash, an ASIC-resistant algorithm that is designed to secure transactions on the blockchain.
Classes
Block

The Block class represents a block in the blockchain. It has the following attributes:

*   `index`: the index of the block in the blockchain
*   `transactions`: the transactions included in the block
*   `timestamp`: the timestamp of when the block was created
*   `nonce`: the nonce used in the proof-of-work algorithm
*   `previous_hash`: the hash of the previous block in the blockchain

## Blockchain

The Blockchain class represents the entire blockchain. It has the following attributes:

*   `unconfirmed_transactions`: a list of unconfirmed transactions
*   `chain`: a list of blocks in the blockchain

And it has several important methods:

*    `create_genesis_block`: creates the first block in the blockchain (also known as the "genesis block") and adds it to the chain attribute.
*    `proof_of_work`: performs the proof-of-work algorithm to secure new blocks using Ethash algorithm.
*    `add_block`: adds a new block to the blockchain after verifying that it is a valid block and that the previous_hash attribute matches the last block in the chain
*    `is_valid_proof`: verifies that the proof of work is valid by checking that the Ethash digest is less than the difficulty
*    `add_new_transaction`: adds a new transaction to the list of unconfirmed transactions
*    `mine`: mines new block by getting the last_block, creating a new block, and adding it to the chain after proving that it is a valid block.

## Flask Server

The script also starts a Flask web server that has two routes:

*    `/chain` returns the entire blockchain data
*    `/mine` mines a new block using the unconfirmed_transactions
