# Environment Setup

1.Install NodeJS at https://nodejs.org/en/, you could choose either version for the purpose of running this program.

2.Install back-end libraries with the following command under project directory after you clone it from Gitlab (Please checkout to the develop branch):
    
    pip install -r requirements.txt

“requirements.txt” is a pre-written text that contains all the required back-end libraries needed for this program.

3.Install front-end libraries with the following command under the “chess_ui” directory: 
    
    npm install

This command will install all the required front-end libraries that are contained in the “package.json” file in the chess_ui directory.

4.Open “team5_chess” as a project with PyCharm.

5.Run “app.py” in PyCharm (in the “api” folder).
This will run a flask-app and expose all back-end functions that will be used in front-end.

6.Run the following command under the “chess_ui” directory:
    
    npm start

This will start our front-end server and automatically open the browser with the chess UI.

# Main Menu
### New Game: 
Click on the “New Game” button to start a new session of chess game against the computer AI. This will lead you to a user interface of a standard chess game board with 8 files, 8 rank with black and white pieces on their initial positions. The user will always be the white side.
### Resume Game: 
Click on the “Resume Game” button to resume an unfinished session of chess game. A list of all saved game sessions boxes will show up. Each box includes the session ID, the start time, and the last updated time of a session. To resume a game, click on the box that has the session ID for the game you want to continue. Be cautious that you must remember the session ID of a game session if you intend to pause and resume the session later. 
### Replays: 
Not Implemented Yet.

# The Game Board UI: 
### Game Info Box
Once you entered the chess gameboard UI by clicking on the “New Game” button on the main menu, you will see a game info box on the top left corner which keep track of the status of the current game. “Time” includes a running clock that record the date and time you started and time you spent on the current session; “Turn” keeps track of whose turn it is next; and “Status” shows the current game status.
There are four possible game status: “Continue”, “Draw”, “WhiteLoss” and “BlackLoss”. “Continue” will appear in the “Status” line whenever either player can make a valid move; “Draw” will appear when both players had made more than 50 moves in total, and the game comes to a draw; “WhiteLoss” and “BlackLoss” will appear when the respective side lose the game.
### The Menu Bar
On the top right corner is the drop-down menu navigation bar. Click on the “MENU” bar to see the “quit” option that allow you to pause the current game session. Any quitted game will be automatically saved with its game info. The quit button redirects you to the main menu. You may choose to resume the game through the “Resume Game” option on the main menu page. To resume a session, you will have to remember your session ID before quitting.  You can find the session ID number of your current game session in the URL bar at the end of the address. 
### The Gameboard 
A standard chess gameboard. When you click on a piece, valid moves of that piece will be highlighted with green dots. Check https://www.chesscoachonline.com/chess-articles/chess-rules to see specific rule of moving each type of piece and the special cases. Click on a highlighted grid, the piece will be moved to that grid.
If a grid is on the possible route of a piece but you will be checked after moved to that grid, this move is not allowed and hence not highlighted. If the black side makes a move, the original position and the target position of the moving piece will be heighted light yellow and dark yellow respectively, so you can always check what the last move of the black side was. 
### Promotion Option Bar
The drop-off bar on the top right corner allows you to choose what type of piece (Queen, Bishop, Knight, Rook) you want to promote a pawn piece to. You must choose a type BEFORE you move a pawn to an edge rank and a promotion is about to happen, otherwise, the pawn will be promoted to a queen by default.  
### Pop-up Windows
One of the following pop-up windows will appear on the top of the gameboard when you run into their indicated game status: 
1. Check: Reminds you that you are being check right now. You can move any move unless it resolves your status of being checked. 
2. Draw: When there are more than 50 moves in total, the game will end in a draw.
3. WhiteLoss: When the white side lose, i.e., is being checked but there are no more valid moves (to resolve the state of being checked) can be made. 
4. BlackLoss: When the black side lose.


