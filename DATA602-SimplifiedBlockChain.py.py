# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 01:31:31 2019

@author: josemawyin
"""

import datetime as dt
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unittest
import uuid

class PandasChain:
    # 5 pts - Complete this constructor
    def __init__(self, name):
        self.__name = name.upper() # Convert name to upper case and store it here
        self.__chain = list() # Create an empty list for chain
        self.Coin_Purse = list() # Create an empty list for coins in chain
        self.Transacation_DataTime = list() # Create an empty list for time of transactions
        self.__id = hashlib.sha256(str(str(uuid.uuid4())+self.__name+str(dt.datetime.now())).encode('utf-8')).hexdigest()
        # Create a sequence ID and set to zero
        self.__prev_hash = "None" # Set to None
        self.__col_names = ['Timestamp','Sender','Receiver','Value','TxHash']
        self.current_block = pd.DataFrame(columns=self.__col_names)# Create a new Block
        self._chainblock = self.current_block
        self.__chain.append(self.current_block)
        print(self.__name,'PandasChain created with ID',self.__id,'chain started.')
        self.Merkle = 0
        self.BHash = 0
        self.All_BlockMeta = list()
        self.Block_Seq = 0




    # 5 pts - This method should loop through all committed and uncommitted blocks and display all transactions in them
    def display_chain(self):
        print("\nThe following are all committed and uncommitted blocks including all transactions in them:",self.__chain,"\n")


    # This method accepts a new transaction and adds it to current block if block is not full.
    # If block is full, it will delegate the committing and creation of a new current block
    def add_transaction(self,s,r,v):
        ts = dt.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S:%f') # Get current timestamp
        Time = dt.datetime.utcnow()# Get current timestamp
        value = str(v)  # value as string
        StringTrans = ts+s+r+value
        ByteTrans = StringTrans.encode('utf-8')
        tx_hash = hashlib.sha256(ByteTrans)# Hash of timestamp, sender, receiver, value
        hex_dig = tx_hash.hexdigest()
        TransList = [[ts, s, r, value, hex_dig]]
        new_transaction = pd.DataFrame(TransList, columns=self.__col_names) # Create DataFrame with transaction data (a DataFrame with only 1 row)
        self.current_block = pd.concat([self.current_block, new_transaction]) # Append to the transactions data
        block_hash = block.set_block_hash(self.__prev_hash)

        self.Coin_Purse.append(v)
        self.Transacation_DataTime.append(Time)
        print("Coins in Purse:\n",self.Coin_Purse,"\n")
        if len(self.current_block) >= 10:
            self.Merkle = block.get_simple_merkle_root()
            self.BHash = block.set_block_hash(self.__prev_hash)
            self.Block_Seq = self.Block_Seq + 1
            self.__commit_block(self.current_block)
        #self.add_transaction(s,r,v)



    # 10 pts - This method is called by add_transaction if a block is full (i.e 10 or more transactions).
    # It is private and therefore not public accessible. It will change the block status to committed, obtain the merkle
    # root hash, generate and set the block's hash, set the prev_hash to the previous block's hash, append this block
    # to the chain list, increment the seq_id and create a new block as the current block
    def __commit_block(self,block):
        block._Block__status = "Committed"      #change the block status to committed
        self.__chain.append(block)
        self.current_block = []# Add code here
        self.current_block = pd.DataFrame(columns=self.__col_names)
        print("The total coin amount in this commited block is:",sum(self.Coin_Purse),"Coins\n")# Add code here
        BlockMeta = dict({"Block Sequence":self.Block_Seq,
                    "Block Status": block._Block__status,
                    "Merkle Root Hash": self.Merkle,
                    "Block Hash": self.BHash,
                    "Previous Hash":"",
                    "Sequence ID":self.__id
                    })
        print("\nThis Complete Block Meta Data:",BlockMeta,"\n")
        self.All_BlockMeta.append(BlockMeta)
        print('Block committed\n')

    # 10 pts - Display just the metadata of all blocks (committed or uncommitted), one block per line.
    # You'll display the sequence Id, status, block hash, previous block's hash, merkle hash and total number (count)
    # of transactions in the block
    def display_block_headers(self):
        print(self.All_BlockMeta)

    # 5 pts - return int total number of blocks in this chain (committed and uncommitted blocks combined)
    def get_number_of_blocks(self):
        #return len(self.__chain.index)
        return len(self.__chain)

    # 10 pts - Returns all of the values (Pandas coins transferred) of all transactions from every block as a single list
    def get_values(self):
        return self.Coin_Purse

    def get_size(self):
        return len(self._PandasChain__current_block)

class Block(PandasChain):
    # 5 pts for constructor
    def __init__(self,seq_id,prev_hash):
        self.__seq_id = seq_id # Set to what's passed in from constructor
        self.__prev_hash = prev_hash # From constructor
        self.__col_names = ['Timestamp','Sender','Receiver','Value','TxHash']
        self.__transactions = pd.DataFrame(columns=self.__col_names) # Create a new blank DataFrame with set headers
        self.__status = "Start Block" # Initial status. This will be a string.
        self.__block_hash = None
        self.__merkle_tx_hash = None
        ts = dt.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S:%f')



    #5 pts -  Display on a single line the metadata of this block. You'll display the sequence Id, status,
    # block hash, previous block's hash, merkle hash and number of transactions in the block
    def display_header(self):
        return ("\nThis block's metadata is:", "\nid:",self.__seq_id,"\nStatus:",self.__status,
              "\nBlock Hash:",self.__block_hash,"\nPrevious Hash:",
              self.__prev_hash,"\nThe Block Merkle Hash is:",Block.get_simple_merkle_root(self),"\nNumber of transactions:",len(self.__transactions.index))

    # 10 pts - This is the interface for how transactions are added
    def add_transaction(self,s,r,v):
        ts = dt.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S:%f') # Get current timestamp
        value = str(v)  # value as string
        StringTrans = ts+s+r+value
        ByteTrans = StringTrans.encode('utf-8')
        tx_hash = hashlib.sha256(ByteTrans)# Hash of timestamp, sender, receiver, value
        hex_dig = tx_hash.hexdigest()
        TransList = [[ts, s, r, value, hex_dig]]
        new_transaction = pd.DataFrame(TransList, columns=self.__col_names) # Create DataFrame with transaction data (a DataFrame with only 1 row)
        self.__transactions = pd.concat([self.__transactions, new_transaction]) # Append to the transactions data

    # 10 pts -Print all transactions contained by this block
    def display_transactions(self):
        print("\nBlock Transactions:\n",self.__transactions,"\n")

    # 5 pts- Return the number of transactions contained by this block
    def get_size(self):
        return len(self.__transactions.index)

    # 5 pts - Setter for status - Allow for the change of status (only two statuses exist - COMMITTED or UNCOMMITTED).
    # There is no need to validate status.
    def set_status(self,status):
        self.__status = status

    # 5 pts - Setter for block hash
    def set_block_hash(self,hash):
        StringBHash = hash+Block.get_simple_merkle_root(self)+pandas_chain._PandasChain__id
        ByteBHash = StringBHash.encode('utf-8')
        tx_BHash = hashlib.sha256(ByteBHash)# Hash of timestamp, sender, receiver, value
        hex_digBHash = tx_BHash.hexdigest()
        return hex_digBHash

    # 10 pts - Return and calculate merkle hash by taking all transaction hashes, concatenate them into one string and
    # hash that string producing a "merkle root" - Note, this is not how merkle tries work but is instructive
    # and indicative in terms of the intent and purpose of merkle tries
    def get_simple_merkle_root(self):
        TransHashList = (self.__transactions.iloc[:, 4].tolist())   #Creates list of Transaction Hashes
        TransHashChain = ""
        for i in TransHashList:     #Chains all the Hashes as string into a single string
            TransHashChain = TransHashChain+str(i)
        #Create a hash, encodes hash and transforms the has into binary.
        Byte_TransHashChain = TransHashChain.encode('utf-8')
        TransHashChain_hash = hashlib.sha256(Byte_TransHashChain)
        hex_dig2 = TransHashChain_hash.hexdigest()
        return (hex_dig2)


    def get_values(self):
        coin_sum = sum(list(map(int, self.__transactions.iloc[:, 3].tolist())))
        return coin_sum


#I need to intialize the Block and Chain with the statements below.
block = Block(1,"test")
pandas_chain = PandasChain('testnet')

class TestAssignment4(unittest.TestCase):
    def test_chain(self):
        block = Block(1,"test")
        self.assertEqual(block.get_size(),0)
        block.add_transaction("Bob","Alice",50)
        self.assertEqual(block.get_size(),1)
        pandas_chain = PandasChain('testnet')
        self.assertEqual(pandas_chain.get_number_of_blocks(),1)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),2)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),3)
        print("**--"*10,"\nAll Committed Blocks Metadata:\n")
        print(pandas_chain.All_BlockMeta)
        print("**--"*10,"\nPlotting All Transaction Values and the Time of Transactions")
        plt.plot(pandas_chain.Coin_Purse)
        plt.ylabel('Coin Values Added to Block Chain')
        plt.xlabel('Transaction Index')
        plt.show()
        plt.plot(pandas_chain.Transacation_DataTime)
        plt.gcf().autofmt_xdate()
        plt.ylabel('DateTime of Coins Added to Block Chain')
        plt.xlabel('Transaction Index')
        plt.show()

if __name__ == '__main__':
    unittest.main()

