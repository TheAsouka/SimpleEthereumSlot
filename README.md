# SimpleEthereumSlot
A simple slot machine in Python working on a local Ethereum blockchain using Web3 library.   
We love slots, we love blockchain.  

# WARNING 
Don't use this script on the Ethereum Mainnet !  
Private keys are exposed and network fees (in mid 2021) are way too expensive.  
Exposing your private key may result in funds loss.  
Don't send Ether on address exposed in this script or in this readme, it will result in funds loss.

# How to use
You need Ganache in order to have your own local blockchain. You can download it by clicking [this link](https://www.trufflesuite.com/ganache).  
Note that ganache-cli works fine for this purpose too.  
You might need to modify the line ```233``` to use your local blockchain RPC server (http://127.0.0.1:7545 by default).

You also need the Web3 Python library, install it via pip.\
```pip install -r requirements.txt```

Once Ganache is installed, copy the first account (casino) address and replace lines ```240``` and ```258```.  
Then copy the first account (casino) private key and replace line ```259```.  
When lauching the script a prompt is asking to copy the user's address and private key.  
Copy these from the second Ganache account.  
![alt text](https://github.com/TheAsouka/SimpleEthereumSlot/blob/main/img/ganache.PNG "Ganache UI")

# How it works
The principle of this slot is basic. It's a 3 lines 5 reels slot.  
If 3 or more symbols are adjacent on different reels and maximum one line away there is a connection.  
![alt text](https://github.com/TheAsouka/SimpleEthereumSlot/blob/main/img/example.PNG "Spin example")  
Is this example 4 symbols are connected (blue line). Other symbols aren't connected because there are too far away from other symbols (red line).  
![alt text](https://github.com/TheAsouka/SimpleEthereumSlot/blob/main/img/example.PNG "Spin explanation")  

The symbols occurence is setup in the ```createReels()``` function.  
The symbols payrate is setup in the ```calculateWins()``` function line ```157```.  

# Improvements
There is many things to improve in this script. Especially the randomness and payrate, to be fairer for both parts (casino and user).  
I will glade to discuss about it, just open an issue on this repo.  
Next step could be to developp this kind of slot to a webapp using Javascript and front-end libraries and also use Metamask to deal with key management.  

# Support
If you like this project and want to be genereous, feel free to send ETH on this address.  
```0xc02EBD0FE478d8690236D1e211383B32c28f3969```  
