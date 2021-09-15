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


## Used Concepts and Several More Technical Features <a name="concepts"></a>
1. Graphical User Interface, built both with ```Pygame``` library and ```Tkinter``` framework
2. Console-based User Interface. The default UI is the graphical one, but the console-based one can be used too, if needed. However, the latter lacks several features that are available in the GUI version.
3. Layered Architecture: ```presentation layer``` (application UI), ```business layer``` (application service), ```persistence layer``` (application repositories)
4. ```Sqlite3``` database used for storing user accounts. For each user, its email address, username, key (i.e., password hash and salt) and photo are stored in the database
5. The passwords are NOT stored in the database, in order to prevent attacks. Instead, the passwords are hashed, using the ```PBKDF2``` key derivation function, where the user can set the computational cost; this aims to slow down the calculation of the key to make it more impractical to attempt ```brute force attacks```. In usage terms, it takes a password, salt and a number of iterations to produce a certain key. The salt is randomly generated. ```SHA256``` is the hash digest algorithm for HMAC and the number of iterations to produce the key is set to 100.000.
6. The user accounts are verified by sending a ```random six digits verification code``` to the user provided email address. In order to activate the account, the user must provide the code that was sent to its email address (if no email was received, please check the ```spam``` section as well)
7. Each user has an account photo (a default one is set if none was chosen). The photo is stored in the database and it can be changed at any moment by the user
8. Unit testing for most chess related basic functionalities
9. Code commentaries for most of the relevant classes and functions
10. Exceptions handling


## Other Application Features
1. all chess functionalities, together with the chess special moves (e.g., castling and pawn promotion)
2. the user can play as a guest (without creating an account)
3. the user can create an account, which must be verified. In order to verify the account, the user must provide a special ```verification code``` sent to its ```email address```
4. in case of pawn promotion situation (when a pawn reaches the opposite part of the board), a new window pops up and the user can choose a new piece to use instead of that pawn
5. the user can change its account's password. Again, a verification code sent to its account's email must be provided in order to proceed
6. the user can change its ```account's photo```
7. short tutorial section
8. while playing, the user can restart the current game
9. if one player wins, a special message is displayed
