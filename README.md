# How to run the ChessGame

1.Install docker at https://www.docker.com/products/docker-desktop, this is the only thing you need to run our app.

2.Install all dependencies with the following command under project directory after you clone it from Gitlab:
    
    docker-compose build --no-cache

3.Run following command under project directory to start both backend and frontend server:
    
    docker-compose up -d

4.Go to http://localhost:3000 to play the game

# How to play the ChessGame
## Sign-in Page
You will first see the sign-in page with several quotes about chess. One top right, click "Sign in" and a pop up sign-in window will show. You can log in with our test account with the username and password both as "admin", or you can create your own account by clicking on "Become New Member." After creating your own username and password, hit submit to go back to the sign-in page and log in. 

This brings you to the Main Menu page.
## Main Menu
### New Game: 
This gives you the options of different playing modes. Choose either "Easy" or "PvP" to play against the computer AI or with yourself or your friend. Once you create a new game session, a user interface of a standard chess gameboard UI with 8 files, 8 rank with black and white pieces on their initial positions will show up. The user will always be the white side.
### Resume Game: 
Allows you to resume an unfinished session of chess game. 
Whenever you interrupt your onging game session by leaving the chessboard UI page, the session will be automatically saved for resuming. To resume a session, you will have to remember your session ID before leaving the chessboard UI. You can find the session ID number of your current game session in the URL bar at the end of the address while you are playing. 
Click on the resume button on the main menu to choose the game session you want to resume. A list of all saved game sessions boxes will show up. Each box includes information about the mode, the session ID, the start time, and the last updated time of a session. All the sessions are sorted by the last updated time so you can also find your last saved game at the top. To resume a game, click on the box that has the session ID for the game you want to continue and you will go back to the chessboard with where you left off. 
### Replays: 
Allows you to playback any games one step by one step. Likewise, the replay button will list all ongoing and finished games in sorted order. You can choose one with the session ID for the game you want to replay. Then the chessboard will show up with the left and right arrows under the board. You can view the previous or next move by clicking on them.   
There won't be a game info box, menu bar, and promotion options when you enter the UI through the "replay" button.   

## The Game Board UI: 
### Game Info Box
Once you entered the chess gameboard UI, you will see a game info box on the top left corner which keep track of the information of the current game. “Time” includes a running clock that tells you the current date and time; "Mode" indicates the mode the user has chosen for the current game; “Turn” keeps track of whose turn it is next; and “Status” shows the current game status.
There are four possible game status: “Continue”, “Draw”, “WhiteLoss” and “BlackLoss”. “Continue” will appear in the “Status” line whenever either player can make a valid move; “Draw” will appear when both players had made more than 50 moves in total, and the game comes to a draw; “WhiteLoss” and “BlackLoss” will appear when the respective side loses the game.

### The Account Menu 
The account menu is on the top right corner and above the menu bar. 
1. Total Hours Played: Allows you to check your total hours played under the current user account.
2. Profile: Not Implemented Yet.
3. Settings: Not Implemented Yet.
4. Log out: Clicking on log out brings you back to the sign-in page. 

### The Menu Bar
On the top right corner is the drop-down menu navigation bar that allows you to takeback a step, resign to your component, or ask for a draw. Click on it to open/collapse. 
1. Takeback: Under "PvP" mode, every time when you click on takeback, the game will withdrawl the very last piece that's just been moved. You are allowed to take back steps until the game restore to the starting point. Under "Easy" mode, since the black side is the computer and it moves immediately after you move, each time you click on "takeback", the game will withdrwal both your and the computer's move so you can redo your last move.  
2. Resign: Allows you to resign to the other player. (Not Implemented Yet)
3. Draw: Allows you to ask for a draw with the other player. (Not Implementd Yet)

### The Gameboard 
A standard chess gameboard. When you click on a piece, valid moves of that piece will be highlighted with green dots. Check https://www.chesscoachonline.com/chess-articles/chess-rules to see specific rule of moving each type of piece and the special cases. Click on a highlighted grid, the piece will be moved to that grid.
If a grid is on the possible route of a piece but you will be checked after moved to that grid, this move is not allowed and hence not highlighted. If the black side makes a move, the original position and the target position of the moving piece will be heighted light yellow and dark yellow respectively, so you can always check what the last move of the black side was. 
### Promotion Option Bar
The drop-off bar on the top right corner allows you to choose what type of piece (Queen, Bishop, Knight, Rook) you want to promote a pawn piece to. You must choose a type BEFORE you move a pawn to an edge rank and a promotion is about to happen, otherwise, the pawn will be promoted to a queen by default.  
### Pop-up Windows
One of the following pop-up windows will appear on the top of the gameboard when you run into their indicated game status: 
1. Check: Reminds you that you are being check right now. You can move any move unless it resolves your status of being checked. 
2. Draw: The game will end in a draw if no capture has been made and no pawn has been moved in the last fifty round(a player completing a turn followed by the opponent completing a turn). 
3. WhiteLoss: When the white side loses, i.e., is being checked but there are no more valid moves (to resolve the state of being checked) can be made. 
4. BlackLoss: When the black side loses.

# How to test ChessGame
1.Open backend/ as a project in PyCharm

2.In Pycharm, right click test/ folder and click "Run Unittests in tests" (You need to install required python libraries first)

    pip install -r requirements.txt
    
You can always check our CI/CD pipeline to see all tests are passed and code coverage.

# Work Distribution (sprint 1)
Zijian Zhang: 17%
1. Flask and react interact, implement highlighting history moves and learn how to create a game menu
2. The chessboard.jsx works in react and learned how to fetch data. Managed to show the valid moves and high light them in the UI.

Zhenghang Hu: 17%
1. Helped design the structure of backend including pieces and chess game; implemented and reviewed some functions in chessgame.py
2. Designed and implemented a simple chess AI

Ying Liu: 17%
1. Chess game back-end board and game implementation
2. Chess game back-end game implementation testing

Xiao Yang: 17%
1. Implementation of all chess pieces.
2. implementation of testing functions of chess pieces.

Cicong Tian: 16%
1. User Documents
2. Helped test the computer AI

Yiting Wang: 16%
1. Make databases to store all chess elements
2. Drive and driver testing

# Work Distribution (sprint 2)
Zijian Zhang: 17%
1. Restructure the project and dockerize the project.
2. Put database in AWS.
3. Refactor UI, add user log in, sign up, replay, game mode choose, takeback feature for the frontend.

Zhenghang Hu: 17%
1. Built api for user login system
2. Re-designed tables in database 

Ying Liu: 17%
1. Implemented backend game undo function.
2. Adjusted game history recoding contents format
3. Refactored chess game coding smell and completed test cases for it.

Xiao Yang: 17%
1. According to the new features, undo and playback, rewrite the piece classes and other functions.
2. Add tests to make sure each functions implemented correctly
3. Refactor code, fix bugs and add comments

Cicong Tian: 16%
1. User Documents
2. Tested api.py

Yiting Wang: 16%
1. Exposed api through flask in app.py
2. Tested app.py
3. Fixed bugs in api.py