# ChessGame
Chess game written in Python, providing account registering and all the usual chess functionalities. Accounts are verified via a verification code sent to the user's email.
Passwords are not stored in the database, they are hashed and their hash and salt is stored instead (see more at [Concepts](#concepts)).

<p align="center"> <img src="https://github.com/EmanuelPutura/ChessGame/blob/main/git_images/main_menu.png" height="500"/> </p>


## Setup
 1. Clone the repo:
    ```sh
    $ git clone https://github.com/EmanuelPutura/ChessGame
    ```
 2. From the project's location:
    ```sh
    $ python main.py
    ```


## Used Concepts and Several Application Features <a name="concepts"></a>


## Features
1. all chess functionalities, together with the chess special moves (e.g., castling and pawn promotion)
2. the user can play as a guest (without creating an account)
3. the user can create an account, which must be verified. In order to verify the account, the user must provide a special ```verification code``` sent to its ```email address```
4. in case of pawn promotion situation (when a pawn reaches the opposite part of the board), a new window pops up and the user can choose a new piece to use instead of that pawn
5. the user can change its account's password. Again, a verification code sent to its account's email must be provided in order to proceed
6. 
7. short tutorial section
8. while playing, the user can restart the current game
9. if one player wins, a special message is displayed
