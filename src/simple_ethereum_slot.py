#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random, time, sys
from web3 import Web3

def getRandomness():
    f_my_random = random.uniform(0,100)
    return f_my_random

def createReels():
    #Create spin reels with controlled randomness
    #Attribute a symbol if a ramdom number is in range of values
    #Modifying these ranges values change the symbol occurrence rate
    #To change to be fairer for both parts
    #Random - 40% / 0 - 1% / 1 - 30% / 2 - 18% / 3 - 6% / 4 - 3% / 5 - 2%

    l_l_reels = []
    for i in range(0,3):
        l_line = []
        for j in range(0,5):
            f_my_random = getRandomness()
            
            if 0 <= f_my_random <= 40:
                l_line.append(random.randint(0,5)) #40% of the time put a random symbol
    
            if 40 <= f_my_random <= 41:
                l_line.append(0)
    
            if 41 <= f_my_random <= 71:
                l_line.append(1)
    
            if 71 <= f_my_random <= 89:
                l_line.append(2)
    
            if 89 <= f_my_random <= 95:
                l_line.append(3)
    
            if 95 <= f_my_random <= 98:
                l_line.append(4)
    
            if 98 <=f_my_random <= 100:
                l_line.append(5)

        l_l_reels.append(l_line)

    return l_l_reels #List of Lists with symbols per lines

def displayReels(l_my_reels,d_spin_connections):
    #Display the spin's symbols one by one

    print(" ---------------------")
    l_symbol_connected = list(d_spin_connections.keys()) #List of int
    for j in range(3):
        to_display = ""
        for i in range(5):
            s_symbol = str(l_my_reels[j][i])

            if len(l_symbol_connected) > 0 :

                if s_symbol in map(str,l_symbol_connected): # Colorize the symbols even if not connected, TO IMPROVE
                    to_display += " | " + colorizeString(s_symbol)
                else :
                    to_display += " | " + s_symbol

            else:
                to_display += " | " + s_symbol
                 
            sys.stdout.write("\r{0}".format(to_display))
            time.sleep(0.5)

        i = 0
        print(" |\n",end='')
    print(" ---------------------")

def colorizeString(s_to_colorize):
    string = "\033[1;33m"+s_to_colorize+"\033[0;m"
    return string

def checkConnection(l_l_reels):
    #Check connections for each symbol of the spin
    # A reel is a column of the 3x5 array (2D)
    d_connect_ok = {0:[],1:[],2:[],3:[],4:[],5:[]}

    for i in range(0,5): # For each lines of the 3x5 array
        l_current_reel = [] #I love lists
        l_next_reel = []
        l_current_pos = []
        l_next_pos = []
        l_prev_reel = []
        l_prev_pos = []
        for j in range(0,3): # For each column

            if i+1 > 4 or i-1 < 0: #Avoid index out of range error
                break
            
            l_prev_pos.append(str(j)+str(i-1))
            l_current_pos.append(str(j)+str(i))
            l_next_pos.append(str(j) + str(i+1))

            # Turns 3x5 array to kind of 5x3 array (to iterate on)
            l_prev_reel.append(l_l_reels[j][i-1]) # Previous Column
            l_current_reel.append(l_l_reels[j][i]) # Column
            l_next_reel.append(l_l_reels[j][i+1]) # Next Column
        

        x=0

        for symbol in l_current_reel:
            m = 0
            for prev_symbol in l_prev_reel:
                n = 0
                for next_symbol in l_next_reel:
                    if prev_symbol == symbol == next_symbol:
                        
                        i_prev_space = int(l_prev_pos[m])
                        i_current_space = int(l_current_pos[x])
                        i_next_space = int(l_next_pos[n])

                        if -12 < i_next_space - i_current_space < 12 and -12 < i_prev_space - i_current_space < 12: # If symbols are close enough, connection is accepted

                            if i==1: #If previous_reel is the first reel (left) append the symbol if there is a connection
                                d_connect_ok[symbol].append(l_prev_pos[m])

                            d_connect_ok[symbol].append(l_next_pos[n])
                            d_connect_ok[symbol].append(l_current_pos[x])
                            
                    n+=1
                m+=1
            x+=1

    for key,value in d_connect_ok.items(): # Delete duplicates
        value = list(set(value))
        value.sort()
        d_connect_ok[key] = value

    l_key_ok = []
    for key,value in d_connect_ok.items(): #If there is no connection in the first reel (left), there is no "line", don't count it
        for pos in value:
            if pos[1] == "0":
                l_key_ok.append(key)

        if key in l_key_ok:
            d_connect_ok[key] = len(value) # Number of connected symbols
        else :
            d_connect_ok[key] = 0
    
    for i in range(0,6): # Delete unecessary key,value in the dictionnary
        if d_connect_ok[i] == 0:
            del d_connect_ok[i]

    return d_connect_ok #Dictionnary -> symbol:number of symbols

def calculateWins(d_connections,f_bet):
    #Calculate the user's wins by spin
    i_total_win = 0
    l_wins = [2,0.115,0.25,0.5,1,1.5] #Symbols payrate, to change to be fairer (ex : each connected 0 pays 2*bet_value / each connected 1 pays 0.115*bet_value)

    for symbol in d_connections:
        i_win = l_wins[symbol] * d_connections[symbol] * f_bet # win = symbol payrate x number of symbol x bet value
        print("Symbol :",symbol,"Number of connections :",d_connections[symbol],"Win :",round(i_win,6))
        i_total_win += round(i_win,6)
    i_total_win = round(i_total_win,6)
    return i_total_win

def addWinToBalance(web3,i_win,f_bet,user_address,user_privkey):
    #Send a transaction between the user and casino for each spin

    if i_win > f_bet: #If total win is greater than bet value the casino pays the user
        value_to_send = i_win - f_bet
        if value_to_send == 0: #If win = bet value do nothing
            return 0
        ret = casinoSendTransaction(web3,user_address, value_to_send)
        return ret
    
    else :
        #If bet value is greater than the total win the user pays the difference to the casino
        value_to_send = f_bet - i_win
        if value_to_send == 0:
            return 0
        ret = userSendTransaction(web3,user_address, user_privkey, value_to_send)
        return ret

def getUserBalance(web3,user_address):
    balance = web3.eth.getBalance(user_address)
    return web3.fromWei(balance,'ether')

def checkBalance(web3,balance,f_bet,s_choice):
    #Check is user's can afford to play
    s_choice = s_choice

    i_gas_price = web3.toWei('50','gwei') #/!\ Gas price is set for development purpose only /!\
    i_gas_per_transaction = 21000 # A transaction need at least 21000gas to be sent
    f_network_fee = float(web3.fromWei(i_gas_price*i_gas_per_transaction,'ether'))

    if balance < (f_bet + f_network_fee):
        print ("You don't have enough fund to pay network fees, please fill up your account.")
        s_choice = "1"
        
    if balance < f_bet :
        print ("The bet is greater than your balance, please modify your bet.")
        s_choice = "1"

    return s_choice

def Spin(web3,balance,f_bet,user_address,user_privkey):
    #The main spin function, where the magic happens

    l_my_reels = createReels()
    d_spin_connections = checkConnection(l_my_reels)
    displayReels(l_my_reels,d_spin_connections)
    b_spin_win = bool(d_spin_connections) #if dictionnary empty False (loose), True if not (win)

    if b_spin_win is True :
        i_win = calculateWins(d_spin_connections,f_bet)
        addWinToBalance(web3,i_win,f_bet,user_address,user_privkey)
        print("\033[1;32m"+"WIN !!"+"\033[0;m") #GREEN
        print ("\033[1;32m"+"You won"+"\033[0;m",round(i_win,6),"ETH")
        print ("Your balance is",round(getUserBalance(web3,user_address),6),"ETH")

    if b_spin_win is False:
        print ("\033[1;31m"+"You lost !"+"\033[0;m") #RED
        i_win = 0
        addWinToBalance(web3,i_win,f_bet,user_address,user_privkey)
        print ("Your balance is",round(getUserBalance(web3,user_address),6),"ETH")
    
    print ("==========================")
    
    return b_spin_win #Returns True if spin is a win , False if not

def connectToBlockchain():
    #Initiate connection with a blockchain using web3
    s_blockchain_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(s_blockchain_url))
    print ("Connection to the blockchain...",web3.isConnected())
    return web3

def userSendTransaction(web3,user_address,user_privkey,value_to_send):
    #Create a raw transaction from user's address to casino address and send it
    casino_address = "0xFC466c0f3B9Dda4cE33272DEC384D6F8FFaC52c5"
    nonce = web3.eth.getTransactionCount(user_address)

    tx = {
        'nonce' : nonce,
        'to' : casino_address,
        'value' : web3.toWei(value_to_send,'ether'),
        'gas' : 21000, # A transaction is 21000 at least gas
        'gasPrice' : web3.toWei('50','gwei') #/!\ Gas price is set for development purpose only /!\
    }

    signed_tx = web3.eth.account.signTransaction(tx,user_privkey)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction) #Sendtransac

    return web3.toHex(tx_hash)

def casinoSendTransaction(web3,user_address,value_to_send):
    #Create a raw transaction from casino's address to user address and send it
    casino_address = "0xFC466c0f3B9Dda4cE33272DEC384D6F8FFaC52c5"
    casino_privkey = "0ba451736a84457d8d2f1520844ca2954b119c6e0173fd6b7d521ca7a7d25e56" #Csafetkt
    nonce = web3.eth.getTransactionCount(casino_address)

    tx = {
        'nonce' : nonce,
        'to' : user_address,
        'value' : web3.toWei(value_to_send,'ether'),
        'gas' : 21000, # A transaction is 21000 at least gas
        'gasPrice' : web3.toWei('50','gwei') #/!\ Gas price is set for development purpose only /!\
    }

    signed_tx = web3.eth.account.signTransaction(tx,casino_privkey)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction) #Sendtransac

    return web3.toHex(tx_hash)

def checkAddressFormat(s_address):
    #Check if user's address is an ethereum address
    if len(s_address) == 42 and s_address[:2] == "0x":
        return True
    else :
        print ("Invalid address format. Please check your address.")
        return False
        
def checkPrivKeyFormat(s_privkey):
    #Check if user's private key is an ethereum private key
    if len(s_privkey) == 64:
        return True
    else :
        print ("Invalid private key format. Please check your private key.")
        return False

def main():
    f_bet = 1.0
    s_choice = ""
    print ("*** Welcome to LuckySticky ***")

    user_account = input("Your Ethereum address : ")
    while checkAddressFormat(user_account) != True:
        user_account = input("Your Ethereum address : ")

    user_privkey = input("Your Ethereum private key (tktcsafemdr) : ")
    while checkPrivKeyFormat(user_privkey) != True:
        user_privkey = input("Your Ethereum private key (tktcsafemdr) : ")

    web3 = connectToBlockchain()
    
    while s_choice != "0":
        #Menu
        balance = getUserBalance(web3,user_account)
        print ("0 - Quit")
        print ("1 - Modify bet")
        print ("2 - Spin !!")
        print ("3 - AutoSpin !!")
        print("Your balance is",round(balance,6),"ETH")
        print ("Bet is",f_bet,"ETH")
        s_choice = input("Your choice : ")
        print ("==========================")
        
        if s_choice == "0":
            print ("Goodbye !")
            exit(0)
        
        if s_choice == "1":
            i_new_bet = input("New bet value : ")
            f_bet = float(i_new_bet)
            s_choice = checkBalance(web3,balance,f_bet,s_choice)

        if s_choice == "2":
            if checkBalance(web3,balance,f_bet,s_choice) == "1": #If there is not enough money for the next spin don't spin
                able_to_spin = False
            else:
                able_to_spin = True
            
            if able_to_spin == True:
                Spin(web3,balance,f_bet,user_account,user_privkey)

        if s_choice == "3":
            i_count_spins = input("Number of auto spins : ")
            f_bet_total = f_bet * float(i_count_spins)
            s_choice = checkBalance(web3,balance,f_bet_total,s_choice)
            x = 0

            while x != int(i_count_spins):
                time.sleep(1)

                if s_choice == "1": #If there is not enough money for the next spin don't spin
                    break
                
                print ("Spin n#",x+1)
                Spin(web3,balance,f_bet,user_account,user_privkey)
                x+=1
        
        if getUserBalance(web3, user_account) <= 0.0001 :
            print ("You're broke, get out !")
            exit(0)

main()
