import random
import copy
import sys
#Creating the board
board = [ [0, 1, 0, 0, 0, 1, 0, 1],
 		  [1, 0, 2, 0, 0, 0, 1, 0],
 		  [0, 0, 0, 0, 0, 4, 0, 0],
 		  [0, 0, 0, 0, 2, 0, 0, 2],
 		  [0, 4, 0, 0, 0, 0, 0, 0],
 		  [3, 0, 1, 0, 2, 0, 1, 0],
 		  [0, 0, 0, 0, 0, 0, 0, 0],
 		  [2, 0, 2, 0, 2, 0, 0, 0]]
#board = [[0, 1, 0, 1, 0, 1, 0, 1],
# 		  [1, 0, 1, 0, 1, 0, 1, 0],
#		  [0, 1, 0, 1, 0, 1, 0, 1],
# 		  [0, 0, 0, 0, 0, 0, 0, 0],
 #		  [0, 0, 0, 0, 0, 0, 0, 0],
 #		  [2, 0, 2, 0, 2, 0, 2, 0],
# 		  [0, 2, 0, 2, 0, 2, 0, 2],
# 		  [2, 0, 2, 0, 2, 0, 2, 0]]
board_size=8  
y=0
playeR= 1
playerB=2
playerKR=3
playerKB=4
turn=0
#Converts numbers from the board into characters
def intToText(num):
	if(num == 0): 
		return ' '
	if(num == 1): 
		return 'r'
	if(num == 2): 
		return 'b'
	if(num==3):
		return 'R'
	if(num==4):
		return 'B'

#Prints the grid and updates the board if any pieces have been converted to a King during the last turn
def printGrid():
	CheckKing()
	print(' 0 1 2 3 4 5 6 7')
	print('┌─┬─┬─┬─┬─┬─┬─┬─┐')
	#Loops through the grid printing it
	for y in range(board_size):
		print('│' + intToText(board[y][0]) + '│' + intToText(board[y][1]) + '│' + intToText(board[y][2]) + '│' + intToText(board[y][3]) + '│' + intToText(board[y][4]) + '│' + intToText(board[y][5]) + '│' + intToText(board[y][6]) + '│' + intToText(board[y][7]) + '│'+' ' +str(y)+'\n'
	      '├─┼─┼─┼─┼─┼─┼─┼─┤')

	print('│0│1│2│3│4│5│6│7│')
	print('└─┴─┴─┴─┴─┴─┴─┴─┘')

#Controls turns checking between the computer and the user
def arcadeMode():
	if(turn==0):
		validateR()

	if (turn==1):
		validateAI()
#Controls turns between two users changing the variable turn after they choose a move	
def twoPlayerMode():
	if(turn==0):
		validateR()

	if (turn==1):
		validateB()
#Checks the coordinates given are valid
def validateR():
	#This variables are global so they can be used in other definitions
	global piece, pieceX, pieceY, move, moveX, moveY, board,turn, board2, copyBoard
	piece = input('\n' 'It is player Rs turn. Choose your piece to move or EXIT to quit:' '\n')
	if ( piece == 'help'):
	    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3,2) or EXIT to quit''\n')
	if (piece == "EXIT" or piece=='exit'):
		sys.exit()
	#Checks if the input is on the correct format and splits it into two X and Y variables
	if (len(piece) == 3):
		splitcord= piece.split(',')
		pieceX=int(splitcord[0])
		pieceY=int(splitcord[1])
		if(pieceX <8 and pieceX >=0 and pieceY <8 and pieceY >=0 ):	
			#Checks if the chosen piece belongs to the user
			if(board[pieceY][pieceX]== playeR or board[pieceY][pieceX]== playerKR):
				print('\n' 'Right piece!' '\n')
				#Stores board before and after the user moves the piece: used for Undo and Redo action
				copyBoard= board[:]
				copyBoard= copy.deepcopy(board)
				board2=board[:]
				#Depending of the selected piece legal moves will become avalible
				if(board[pieceY][pieceX]== playeR):
					possibleMovesR()
				if(board[pieceY][pieceX]== playerKR):
					possibleMovesRKing()
				undoRedo()	
			else:
				print('Cannot move this piece. Try again :)')

	else:
		print('Invalid input. Type \'help\' if you\'re stuck')
#Controls the Kings special moves
def possibleMovesRKing():
	#Making these values global so they can be used accross functions 
	global newPosX, newPosY, turn
	#Handles exception in case values checked are out of range
	try:
		#Checks if there's any empty gaps that the king can jump to after eating a piece
		if(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			#Checks in every direction if there's an enemy's piece that can be eaten
			if(board[pieceY+1][pieceX-1]==playerKB or board[pieceY+1][pieceX-1]==playerB):
				#Updates board values
				board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY+2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpR()
				printGrid()
				#Changes turn to the other player
				turn=1
			if(board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB):
				board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX+1]=0
				newPosY=pieceY+2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
			if(board[pieceY-1][pieceX-1]==playerKB or board[pieceY-1][pieceX-1]==playerB):
				board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX-1]=0
				newPosY=pieceY-2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
			if(board[pieceY-1][pieceX+1]==playerKB or board[pieceY-1][pieceX+1]==playerB):
				board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX+1]=0
				newPosY=pieceY-2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
	except:
		pass
def possibleMovesR():
	global newPosX, newPosY,turn
	#Handles exception incase values are out of range
	try:
		#Checks if the chosen piece has a enemy's piece nearby
		if((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX-1]==playerKB or board[pieceY+1][pieceX+1]==playerKB) and(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0)):
			eat=input('\n' 'Available piece to be eaten.Press Y to eat or N not to' '\n')					
			#If yes is chosen, the eating action will be processed automatically
			if(eat=='Y' or eat=='y'):
				if(board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX-1]==playerKB):
					#Updates board
					board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY+1][pieceX-1]=0
					#Stores piece's new coordinates
					newPosY=pieceY+2
					newPosX=pieceX-2
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					#Checks if there's another immediate piece to be eaten and executes it 
					doubleJumpR()
					printGrid()
					#Changes turn to the other player
					turn=1		
				elif(board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB):
					board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY+1][pieceX+1]=0
					newPosY=pieceY+2
					newPosX=pieceX+2
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					doubleJumpR()
					printGrid()
					turn=1			
			#For strategic reasons user does not want to eat the piece it will offer to move it somewhere else
			if(eat=='N' or eat=='n'):
				move=input('\n' 'Where do you want it instead?' '\n')
				#Checks the input is on the correct format
				if (len(move) == 3):
					splitcord= move.split(',')
					moveX=int(splitcord[0])
					moveY=int(splitcord[1])
					#Checks there isn't another piece and that values are on the range
					if(board[moveY][moveX]!=0):
						if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
							if(moveY==pieceY+1 and (moveX== pieceX+1 or moveX== pieceX-1)):
								#Updates board
								board[moveY][moveX]=board[pieceY][pieceX]
								board[pieceY][pieceX]=0
								printGrid()
								turn=1				
							else:
								print('This move is not allowed')

					else:
						print('A piece is already there!')
			else:
				possibleMovesR()
		#Makes user aware there's no moves
		elif(((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB) or (board[pieceY+1][pieceX-1]==playerKB or board[pieceY+1][pieceX+1]==playerKB)) and (board[pieceY+2][pieceX+2]!=0 and board[pieceY+2][pieceX-2]!=0)):
			print('...but there is not legal moves available. Try again :D')
	except:
		pass
	try:	
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0)and turn==0): 
			move=input('Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				#Divides input into two values or coordinates
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playeR):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY+1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board values
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							#Prints grid and changes turn
							printGrid()
							turn=1
						else:
							print('This move is not allowed')

				else:
					print('A piece is already there!')
			#Will keep executing function till a valid value is written
			else:
				possibleMovesR()
	except:
		pass
#Another jump will be taken if there's an enemy's piece to be eaten
def doubleJumpR():
	#Checks that there's another immidiate enemy's piece and that the next square is an empty gap
	while((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX+1]==playerKB or board[newPosY+1][newPosX-1]==playerKB) and (board[newPosY+2][newPosX+2]==0 or board[newPosY+2][newPosX-2]==0)):
		#Checks for left and right directions for a Black piece
		if(board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB):
			input('Another available piece to be eaten. Press enter to continue')
			# Updates board values
			board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
			board[newPosY][newPosX]=0
			board[newPosY+1][newPosX-1]=0
		if(board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB):
			input('Another available piece to be eaten. Press enter to continue')
			board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
			board[newPosY][newPosX]=0
			board[newPosY+1][newPosX+1]=0
	#If the piece that's being move is a King, enemy's pieces can be eaten backwards and forwards
	if(board[newPosY][newPosX]==playerKR):
		while(((board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB) and board[newPosY+2][newPosX-2]==0) or((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB) and board[newPosY+2][newPosX+2]==0) or((board[newPosY-1][newPosX-1]==playerB or board[newPosY-1][newPosX-1]==playerKB)and board[newPosY-2][newPosX-2]==0) or ((board[newPosY-1][newPosX+1]==playerB or board[newPosY-1][newPosX+1]==playerKB) and board[newPosY-2][newPosX+2]==0)):
			#Checks every direction for enemy's pieces
			if((board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB) ):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX-1]=0
			if((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB)):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX+1]=0
			if((board[newPosY-1][newPosX-1]==playerB or board[newPosY-1][newPosX-1]==playerKB)):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX-1]=0
			if((board[newPosY-1][newPosX+1]==playerB or board[newPosY-1][newPosX+1]==playerKB) ):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX+1]=0

def validateAI():
	#Assings a random number with the 0-7 range
	pieceY=(random.randint(0,7))
	pieceX=(random.randint(0,7))
	#Checks the values selected are correct
	if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
		if((board[pieceY][pieceX]== playerB) and((board[pieceY-1][pieceX+1]==0 or board[pieceY-1][pieceX-1]==0) or (board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR))):
			if(((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)  and board[pieceY-2][pieceX-2]==0) or ((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR) and board[pieceY-2][pieceX+2]==0)):
				if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
					print('\n''Your enemy has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR):
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						global turn
						turn=0
					elif(board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
			if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0) and turn==1):
				if(pieceX-1 >=0 and pieceX+1 <8 and pieceY-1 >=0 and pieceY+1 <8):
					print('\n''Your enemy has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==0 and turn!=0):
						board[pieceY-1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY-1][pieceX+1]==0 and turn!=0):
						board[pieceY-1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=0
		if(board[pieceY][pieceX]== playerKB):
			if (board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR or board[pieceY+1][pieceX-1]==playeR or board[pieceY+1][pieceX+1]==playeR or board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR or board[pieceY+1][pieceX-1]==playerKR or board[pieceY+1][pieceX+1]==playerKR):
				if (pieceX-2 >=0 and pieceX+2 <8 and pieceY-2 >=0 and pieceY+2 <8):
					if(board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR):
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if(board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceY+2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if(board[pieceY+1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR):
						board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceÝ+1][pieceX-1]=0
						newPosY=pieceY+2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if(board[pieceY+1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR):
						board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY+1][pieceX+1]=0
						newPosY=pieceY+2
						newPosX=pieceY+2
						printGrid()
						print('\n' 'Oh no! Enemy ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
			if(board[pieceY-1][pieceX+1]==0 or board[pieceY-1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0 or board[pieceY+1][pieceX-1]==0):
				if (pieceX-1 >=0 and pieceX+1 <8 and pieceY-1 >=0 and pieceY+1 <8):
					print('\n''Your enemy has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==0 and turn!=0):
						board[pieceY-1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY-1][pieceX+1]==0 and turn!=0):
						board[pieceY-1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY+1][pieceX-1]==0 and turn!=0):
						board[pieceY+1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY+1][pieceX+1]==0 and turn!=0):
						board[pieceY+1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=0
def validateB():
		global piece, pieceX, pieceY, move, moveX, moveY, board,turn,board2,copyBoard
		piece = input('\n' 'Its player B turn! Choose your piece to move or EXIT to quit:' '\n')
		if ( piece == 'help'):
		    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3,2) or EXIT to quit''\n')
		if(piece=='exit'or piece=='EXIT'):
			sys.exit()	
		#Checks if the input is on the correct format and splits it into two X and Y variables	    
		if (len(piece) == 3):
			splitcord= piece.split(',')
			pieceX=int(splitcord[0])
			pieceY=int(splitcord[1])
			if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
				#Checks if the chosen piece belongs to the user
				if(board[pieceY][pieceX]== playerB or board[pieceY][pieceX==playerKR]):
					print('\n''Right piece!''\n')
					#Stores board before and after the user moves the piece: used for Undo and Redo action
					copyBoard= board[:]
					copyBoard= copy.deepcopy(board)
					board2=board[:]
					if(board[pieceY][pieceX]== playerB):
						possibleMovesB()
					if(board[pieceY][pieceX]== playerKB):
						possibleMovesBKing()
					undoRedo()
				else:
					print('Cannot move this piece. Try again :)')
				
		else:
			print('Invalid input. Type \'help\' if you\'re stuck')
def possibleMovesBKing():
	global newPosX, newPosY, turn
	try:
		if(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			if(board[pieceY+1][pieceX-1]==playerKR or board[pieceY+1][pieceX-1]==playeR):
				#Updates board
				board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY+2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpB()
				printGrid()
				#Changes turn to the other player
				turn=0
			if(board[pieceY+1][pieceX+1]==playeR or board[pieceY+1][pieceX+1]==playerKR):
				board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX+1]=0
				newPosY=pieceY+2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				printGrid()
				turn=0
			if(board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX-1]==playeR):
				board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX-1]=0
				newPosY=pieceY-2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				printGrid()
				turn=0
			if(board[pieceY-1][pieceX+1]==playerKR or board[pieceY-1][pieceX+1]==playeR):
				board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX+1]=0
				newPosY=pieceY-2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				printGrid()
				turn=0
	except:
		pass
def possibleMovesB():
	global newPosX, newPosY,turn
	#Handles exception incase values are out of range
	try:
		#Checks if the chosen piece has a enemy's piece nearby
		if (board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			if(board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR):
				eat=input('\n' 'Available piece to be eaten.Press Y to eat or N not to' '\n')					
				#If yes is chosen, the eating action will be processed automatically
				if(eat=='Y' or eat=='y'):
					if(board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR):
						#Updates board
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						#Stores piece's new coordinates
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
						doubleJumpB()
						printGrid()
						turn=0
					elif(board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
						#Checks if there's another immediate piece to be eaten and executes it 
						doubleJumpB()
						printGrid()
						turn=0
				#For strategic reasons user does not want to eat the piece it will offer to move it somewhere else
				if(eat=='N' or eat=='n'):
					move=input('\n' 'Where do you want it instead?' '\n')
					if (len(move) == 3):
						splitcord= move.split(',')
						moveX=int(splitcord[0])
						moveY=int(splitcord[1])
						if(board[moveY][moveX]!=0):
							if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
								if(moveY==pieceY-1 and (moveX== pieceX+1 or moveX== pieceX-1)):
									#Updates board piece positions
									board[moveY][moveX]=board[pieceY][pieceX]
									board[pieceY][pieceX]=0
									printGrid()
									turn=0
								else:
									print('This move is not allowed')
						else:
							print('A piece is already there!')
				else:
					possibleMovesB()
			elif(((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR) or (board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR)) and(board[pieceY+2][pieceX+2]!=0 and board[pieceY+2][pieceX-2]!=0)):
				print('...but there is not legal moves available. Try again :D')
		
	except:
		pass
	try:
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0) and turn==1):
			move=input( 'Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playerB):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY-1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board piece positions
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							printGrid()
							turn=0
						else:
							print('This move is not allowed')
				else:
					print('A piece is already there!')
			else:
				possibleMovesB()
	except:
		pass	
#Another jump will be taken if there's an enemy's piece to be eaten				
def doubleJumpB():
	while((board[newPosY-1][newPosX-1]==playeR or board[newPosY-1][newPosX+1]==playeR or board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR) and (board[newPosY-2][newPosX+2]==0 or board[newPosY-2][newPosX-2]==0)):
		if(board[newPosY-1][newPosX-1]==playerR or board[pieceY-1][pieceX-1]==playerKR):
			input('Your enemy has a double jump available. Press enter to continue')
			#Updates board piece positions
			board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
			board[newPosY][newPosX]=0
			board[newPosY-1][newPosX-1]=0
			#newPosY=newPosY-2
			#newPosX=newPosX-2
			#doubleJumpB()
		elif(board[newPosY-1][newPosX+1]==playerR or board[pieceY-1][pieceX+1]==playerKR):
			input('Your enemy has a double jump available. Press enter to continue')
			board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
			board[newPosY][newPosX]=0
			board[newPosY-1][newPosX+1]=0
			#newPosY=newPosY-2
			#newPosX=newPosX+2
	if(board[newPosY][newPosX]==playerKB):
		while(((board[newPosY+1][newPosX-1]==playeR or board[newPosY+1][newPosX-1]==playerKR) and board[newPosY+2][newPosX-2]==0) or((board[newPosY+1][newPosX+1]==playeR or board[newPosY+1][newPosX+1]==playerKR) and board[newPosY+2][newPosX+2]==0) or((board[newPosY-1][newPosX-1]==playeR or board[newPosY-1][newPosX-1]==playerKR)and board[newPosY-2][newPosX-2]==0) or ((board[newPosY-1][newPosX+1]==playeR or board[newPosY-1][newPosX+1]==playerKR) and board[newPosY-2][newPosX+2]==0)):
			if((board[newPosY+1][newPosX-1]==playeR or board[newPosY+1][newPosX-1]==playerKR) ):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX-1]=0
			if((board[newPosY+1][newPosX+1]==playeR or board[newPosY+1][newPosX+1]==playerKR)):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX+1]=0
			if((board[newPosY-1][newPosX-1]==playeR or board[newPosY-1][newPosX-1]==playerKR)):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX-1]=0
			if((board[newPosY-1][newPosX+1]==playeR or board[newPosY-1][newPosX+1]==playerKR) ):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX+1]=0
def undoRedo():
	global board, copyBoard,board2, turn
	undoBoard=input ('\n''Type undo if you would like to retake the turn. Otherwise press enter''\n')
	if(undoBoard=='undo' or undoBoard=='Undo'):
		board=copyBoard[:]
		board=copy.deepcopy(copyBoard)
		printGrid()
		redoBoard=input('\n''Type redo if you would like to retake the turn. Otherwise press enter''\n')
		if(redoBoard=='redo' or redoBoard=='Redo'):
			board=board2[:]
			board=copy.deepcopy(board2)
			printGrid()
			if(turn==1):
				turn=1
			elif(turn==0):
				turn=0
		elif(redoBoard!='redo' and turn==1):
			validateR()
		elif(redoBoard!='redo' and turn==0):
			validateB()
def CheckKing():
	for i in range(8):
		if(board[7][i]==1):
		    board[7][i]=3
		    print('\n' 'WOW! Your piece is now a Red King' '\n')
		if(board[0][i]==2):
		    board[0][i]=4
		    print('\n' 'WOW! Your enemy has a Black King now' '\n')

def welcomeStart():
	input('Welcome to checkers! Press enter to start')
	gameMode=input('\n''ARCADE MODE: Press 1 │ TWO PLAYER: Press 2 │ HELP: Press 3 │ QUIT: exit''\n')
	if ( gameMode=='3'):
		print('\n''Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3 2)''\n')
		welcomeStart() #once it has shown help, it calls it´self again, asking for another number, until it is 1 or 2

	print('\n' 'You are playing as Rs')
	printGrid()
	if(gameMode=='1'):
		while(True):
			try:	
				arcadeMode()
			except ValueError:
				print('Incorrect input')
	if(gameMode=='2'):
		while(True):
			try:	
				twoPlayerMode()
			except ValueError:
				print('Incorrect input')
	if(gameMode=='exit'):
		sys.exit()
	else:
		welcomeStart()

#starts the game
welcomeStart()

sys.exit()