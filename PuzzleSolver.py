from time import strftime

class Logger:
    ALL = 0
    DEBUG = 1
    MESSAGE = 2
    WARNING = 3
    ERROR = 4

    def __init__(self):
        self.log_threshold = self.MESSAGE
        self.logOutput(self.ALL, 'Created Logger instance, logging threshold is ' + self.getDebugLevelString(self.log_threshold) + ' level messages.')

    def getDebugLevelString(self, threshold):
        if threshold == self.ALL:
            debug_level = 'ALL'
        elif threshold == self.DEBUG:
            debug_level = 'DEBUG'
        elif threshold == self.MESSAGE:
            debug_level = 'MESSAGE'
        elif threshold == self.WARNING:
            debug_level = 'WARNING'
        elif threshold == self.ERROR:
            debug_level = 'ERROR'
        else:
            debug_level = 'UNDEFINED!'
        return debug_level

    def logOutput (self, level, statement):
        if level >= self.log_threshold:
            print self.getDebugLevelString(level) + '|' + strftime("%Y-%m-%d %H:%M:%S") + '|' + statement

class LoggableBaseClass:
    def setLogger(self, logger):
        self.classlogger = logger

    def getLogger(self):
        return self.classlogger

    def log(self, level, statement):
        self.classlogger.logOutput(level, statement)

class PuzzlePieceSide(LoggableBaseClass):
    #image types
    image_chevron = 1
    image_checkers = 2
    image_stripes = 3
    image_eagle = 4

    #image halves
    image_positive_half = 1 #top of image or left side of image
    image_negative_half = -1 #bottom of image or rights side of image

    #image directions (measured from radial top position)
    #image_direction_standard = 1 #up or left side down
    #image_direction_reverse = -1 # down or right side down

    def __init__(self, logger, image_type, image_half):
        self.setLogger(logger)
        self.log(Logger.DEBUG, "Creating a puzzle piece side.")
        self.puzzle_piece_type = image_type
        self.puzzle_piece_half = image_half
        #self.puzzle_piece_direction = image_direction

    def __str__(self):
        return 'Puzzle Piece Side: type %i, half %i' % (self.puzzle_piece_type, self.puzzle_piece_half)

    def __unicode__(self):
        return u'Puzzle Piece Side: type %i, half %i' % (self.puzzle_piece_type, self.puzzle_piece_half)

    def sidesMatch(self, side1, side2):
        self.log(Logger.DEBUG, 'Testing if sides match.')

        sideTypeSum = side1.puzzle_piece_type - side2.puzzle_piece_type
        sideHalfSum = side1.puzzle_piece_half + side2.puzzle_piece_half

        if (sideTypeSum==0 and sideHalfSum==0):
            self.log(Logger.DEBUG, 'Sides match.')
            return True
        else:
            self.log(Logger.DEBUG, 'Sides do not match.')
            return False

class PuzzlePiece(LoggableBaseClass):
    TOPSIDE=1
    RIGHTSIDE=2
    BOTTOMSIDE=3
    LEFTSIDE=4

    #side1 top, side2 right, side3 bottom, side4 left
    def __init__(self, logger, side1, side2, side3, side4):
        self.setLogger(logger)
        self.log(Logger.DEBUG, "Creating a puzzle piece.")
        self.puzzlePieceSide1=side1
        self.puzzlePieceSide2=side2
        self.puzzlePieceSide3=side3
        self.puzzlePieceSide4=side4
        self.puzzlePieceName=None

    def __str__(self):
        return 'PuzzlePiece \"%s\": \nSide1:%s \nSide2:%s \nSide3:%s \nSide4:%s.' % (self.getName(), self.puzzlePieceSide1, self.puzzlePieceSide2, self.puzzlePieceSide3, self.puzzlePieceSide4)

    def __unicode__(self):
        return u'PuzzlePiece \"%s\": \nSide1:%s \nSide2:%s \nSide3:%s \nSide4:%s.' % (self.getName(), self.puzzlePieceSide1, self.puzzlePieceSide2, self.puzzlePieceSide3, self.puzzlePieceSide4)

    def setName(self, name):
        self.puzzlePieceName=name

    def getName(self):
        return self.puzzlePieceName

    def getSide(self, requestedSide):
        return self.getSide(requestedSide, None)

    def getSide(self, requestedSide, orientation):
        self.log(Logger.DEBUG, 'Requesting side %i, orientation %i.' % (requestedSide, orientation))
        #standard orientation, or no orientation set
        if orientation == PuzzleGridPosition.NOORIENTATION or orientation == PuzzleGridPosition.ORIENTATION1:
            if requestedSide == self.TOPSIDE:
                return self.puzzlePieceSide1
            elif requestedSide == self.RIGHTSIDE:
                return self.puzzlePieceSide2
            elif requestedSide == self.BOTTOMSIDE:
                return self.puzzlePieceSide3
            elif requestedSide == self.LEFTSIDE:
                return self.puzzlePieceSide4
            else:
                self.log(Logger.ERROR, "Unexpected side requested.")
                return None
        #piece rotated 90 degrees clockwise
        elif orientation == PuzzleGridPosition.ORIENTATION2:
            if requestedSide == self.TOPSIDE:
                return self.puzzlePieceSide4
            elif requestedSide == self.RIGHTSIDE:
                return self.puzzlePieceSide1
            elif requestedSide == self.BOTTOMSIDE:
                return self.puzzlePieceSide2
            elif requestedSide == self.LEFTSIDE:
                return self.puzzlePieceSide3
            else:
                self.log(Logger.ERROR, "Unexpected side requested.")
                return None
        #piece rotated 180 degrees clockwise
        elif orientation == PuzzleGridPosition.ORIENTATION3:
            if requestedSide == self.TOPSIDE:
                return self.puzzlePieceSide3
            elif requestedSide == self.RIGHTSIDE:
                return self.puzzlePieceSide4
            elif requestedSide == self.BOTTOMSIDE:
                return self.puzzlePieceSide1
            elif requestedSide == self.LEFTSIDE:
                return self.puzzlePieceSide2
            else:
                self.log(Logger.ERROR, "Unexpected side requested.")
                return None
        #piece rotated 270 degrees clockwise
        elif orientation == PuzzleGridPosition.ORIENTATION4:
            if requestedSide == self.TOPSIDE:
                return self.puzzlePieceSide2
            elif requestedSide == self.RIGHTSIDE:
                return self.puzzlePieceSide3
            elif requestedSide == self.BOTTOMSIDE:
                return self.puzzlePieceSide4
            elif requestedSide == self.LEFTSIDE:
                return self.puzzlePieceSide1
            else:
                self.log(Logger.ERROR, "Unexpected side requested.")
                return None
        else:
            self.log(Logger.ERROR, "Unexpected orientation requested.")
            return None

class PuzzleGridPosition(LoggableBaseClass):
    ROWS = 3
    COLUMNS = 3

    EMPTY=None

    #no orientation
    NOORIENTATION=0
    #standard orientation
    ORIENTATION1=1
    #orientation shifted 90 degrees clockwise
    ORIENTATION2=2
    #orientation shifted 180 degrees clockwise
    ORIENTATION3=3
    #orientation shifted 270 degrees clockwise
    ORIENTATION4=4

    ORIENTATIONS=[ORIENTATION1, ORIENTATION2, ORIENTATION3, ORIENTATION4]

    def __init__(self, logger, parent_puzzle_grid, row, column):
        self.setLogger(logger)
        self.log(Logger.DEBUG, "Creating puzzle grid position, row " + str(row) + ", column " + str(column) + ".")
        self.row_index=row
        self.column_index=column
        self.parentPuzzleGrid=parent_puzzle_grid
        self.puzzlePiece=self.EMPTY
        self.puzzlePieceOrientation=self.NOORIENTATION

    def __unicode__(self):
        return u'PuzzleGridPosition (row %i, column %i): \n Parent Puzzle Grid: %s \n Puzzle Piece: %s \n Puzzle Piece Orientation: %i' % (self.getRow(), self.getColumn(), self.parentPuzzleGrid, self.getPiece(), self.getPieceOrientation())

    #def setRow(self, row):
    # self.row_index = row

    def getRow(self):
        return self.row_index

    #def setColumn(self, column):
    # self.column_index = column

    def getColumn(self):
        return self.column_index

    def setPiece(self, pieceToPlace):
        self.puzzlePiece=pieceToPlace

    def getPiece(self):
        return self.puzzlePiece

    def setPieceOrientation(self, orientation):
        self.puzzlePieceOrientation=orientation

    def getPieceOrientation(self):
        return self.puzzlePieceOrientation

    def clearPuzzleGridPosition(self):
        self.log(Logger.DEBUG, 'Clearing PuzzleGridPosition (row %i, column %i)' %(self.getRow(), self.getColumn()))
        self.setPiece(self.EMPTY)
        self.setPieceOrientation(self.NOORIENTATION)

class PuzzleGrid(LoggableBaseClass):
    POSITION1 = None
    POSITION2 = None
    POSITION3 = None
    POSITION4 = None
    POSITION5 = None
    POSITION6 = None
    POSITION7 = None
    POSITION8 = None
    POSITION9 = None
    POSITIONS = None
    ORDERED_POSITIONS = None

    def __init__(self, logger, parent_puzzle):
        self.setLogger(logger)
        self.log(Logger.DEBUG, "Creating puzzle grid.")
        self.puzzle = parent_puzzle
        self.populatePositions(logger)

    def populatePositions(self, logger):
        if PuzzleGrid.POSITIONS == None:
            PuzzleGrid.POSITION1 = PuzzleGridPosition(logger, self, 1, 1)
            PuzzleGrid.POSITION2 = PuzzleGridPosition(logger, self, 1, 2)
            PuzzleGrid.POSITION3 = PuzzleGridPosition(logger, self, 1, 3)
            PuzzleGrid.POSITION4 = PuzzleGridPosition(logger, self, 2, 1)
            PuzzleGrid.POSITION5 = PuzzleGridPosition(logger, self, 2, 2)
            PuzzleGrid.POSITION6 = PuzzleGridPosition(logger, self, 2, 3)
            PuzzleGrid.POSITION7 = PuzzleGridPosition(logger, self, 3, 1)
            PuzzleGrid.POSITION8 = PuzzleGridPosition(logger, self, 3, 2)
            PuzzleGrid.POSITION9 = PuzzleGridPosition(logger, self, 3, 3)
            PuzzleGrid.POSITIONS = [PuzzleGrid.POSITION1, PuzzleGrid.POSITION2, PuzzleGrid.POSITION3, PuzzleGrid.POSITION4, PuzzleGrid.POSITION5, PuzzleGrid.POSITION6, PuzzleGrid.POSITION7, PuzzleGrid.POSITION8, PuzzleGrid.POSITION9]
            PuzzleGrid.ORDERED_POSITIONS = [PuzzleGrid.POSITION5, PuzzleGrid.POSITION6, PuzzleGrid.POSITION3, PuzzleGrid.POSITION2, PuzzleGrid.POSITION1, PuzzleGrid.POSITION4, PuzzleGrid.POSITION7, PuzzleGrid.POSITION8, PuzzleGrid.POSITION9]

    def __unicode__(self):
        return u'PuzzleGrid: \n Parent Puzzle%s' % (self.puzzle)

    def setPuzzlePiece(self, puzzle_piece, puzzle_piece_location, puzzle_piece_orientation):
        self.log(Logger.DEBUG, "Setting puzzle piece.")
        puzzle_piece_location.setPiece(puzzle_piece)
        puzzle_piece_location.setPieceOrientation(puzzle_piece_orientation)
        return True

    def removePuzzlePiece(self, puzzle_piece):
        self.log(Logger.DEBUG, "Removing puzzle piece.")
        puzzlePiecePosition = self.findPuzzlePieceGridPosition(puzzle_piece)
        if puzzlePiecePosition != None:
            puzzlePiecePosition.clearPuzzleGridPosition
            return True
        return False

    #Return the PuzzlePieceGridPosition (if any) for the PuzzlePiece provided
    def findPuzzlePieceGridPosition(self, puzzle_piece_to_find):
        self.log(Logger.DEBUG, "Finding puzzle piece.")
        for position in self.POSITIONS:
            if position.getPiece() == puzzle_piece_to_find:
                self.log(Logger.DEBUG, 'Piece %s has been found.' % (puzzle_piece_to_find))
                return position
        #PuzzlePiece has not been placed on the PuzzlePieceGrid
        self.log(Logger.DEBUG, "Piece " + str(puzzle_piece_to_find) + " has not been found on grid.")
        return None

    def addPiecesToArray(self, returnArray, puzzleGridPosition):
        if puzzleGridPosition.getPiece() is not None:
            returnArray.append(puzzleGridPosition.getPiece())

    def getNeighboringPieces(self, puzzlePiece):
        self.log(Logger.DEBUG, "Getting neighboring pieces for " + str(puzzlePiece))
        returnArray = []

        puzzle_piece_grid_position = self.findPuzzlePieceGridPosition(puzzlePiece)
        if puzzle_piece_grid_position == self.POSITION1:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 1.")
            self.addPiecesToArray(returnArray, self.POSITION2)
            self.addPiecesToArray(returnArray, self.POSITION4)
        elif puzzle_piece_grid_position == self.POSITION2:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 2.")
            self.addPiecesToArray(returnArray, self.POSITION1)
            self.addPiecesToArray(returnArray, self.POSITION3)
            self.addPiecesToArray(returnArray, self.POSITION5)
        elif puzzle_piece_grid_position == self.POSITION3:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 3.")
            self.addPiecesToArray(returnArray, self.POSITION2)
            self.addPiecesToArray(returnArray, self.POSITION6)
        elif puzzle_piece_grid_position == self.POSITION4:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 4.")
            self.addPiecesToArray(returnArray, self.POSITION1)
            self.addPiecesToArray(returnArray, self.POSITION5)
            self.addPiecesToArray(returnArray, self.POSITION7)
        elif puzzle_piece_grid_position == self.POSITION5:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 5.")
            self.addPiecesToArray(returnArray, self.POSITION2)
            self.addPiecesToArray(returnArray, self.POSITION4)
            self.addPiecesToArray(returnArray, self.POSITION6)
            self.addPiecesToArray(returnArray, self.POSITION8)
        elif puzzle_piece_grid_position == self.POSITION6:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 6.")
            self.addPiecesToArray(returnArray, self.POSITION3)
            self.addPiecesToArray(returnArray, self.POSITION5)
            self.addPiecesToArray(returnArray, self.POSITION9)
        elif puzzle_piece_grid_position == self.POSITION7:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 7.")
            self.addPiecesToArray(returnArray, self.POSITION4)
            self.addPiecesToArray(returnArray, self.POSITION8)
        elif puzzle_piece_grid_position == self.POSITION8:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 8.")
            self.addPiecesToArray(returnArray, self.POSITION5)
            self.addPiecesToArray(returnArray, self.POSITION7)
            self.addPiecesToArray(returnArray, self.POSITION9)
        elif puzzle_piece_grid_position == self.POSITION9:
            self.log(Logger.DEBUG, "Returning pieces neighboring PuzzlePiece in position 9.")
            self.addPiecesToArray(returnArray, self.POSITION6)
            self.addPiecesToArray(returnArray, self.POSITION8)
        else:
            self.log(Logger.ERROR, "Invalid PuzzlePieceGridPosition supplied: " + str(puzzle_piece_grid_position))

        return returnArray

    def puzzlePiecesMate(self, puzzlePiece1GridPosition, puzzlePiece2GridPosition):
        self.log(Logger.DEBUG, "Testing if pieces mate.")
        puzzlePiece1 = puzzlePiece1GridPosition.getPiece()
        puzzlePiece1PuzzleGridOrientation = puzzlePiece1GridPosition.getPieceOrientation()
        puzzlePiece2 = puzzlePiece2GridPosition.getPiece()
        puzzlePiece2PuzzleGridOrientation = puzzlePiece2GridPosition.getPieceOrientation()

        puzzlePiece1Side = None
        puzzlePiece2Side = None

        #Puzzle pieces should be in the same row or column, otherwise they will not have a shared edge
        #Same row?
        if(puzzlePiece1GridPosition.getRow()==puzzlePiece2GridPosition.getRow()):
            self.log(Logger.DEBUG, "Puzzle pieces in same row.")
            #Is piece1 to the right of piece2?
            if(puzzlePiece1GridPosition.getColumn()>puzzlePiece2GridPosition.getColumn() and puzzlePiece1GridPosition.getColumn()-puzzlePiece2GridPosition.getColumn()==1):
                self.log(Logger.DEBUG, "Piece1 to the right of piece2.")
                #Piece 1 is to the right of piece 2, so try to match the right side of piece 2 to the
                #left side of piece 1, as adjusted for rotation
                puzzlePiece1Side = puzzlePiece1.getSide(PuzzlePiece.LEFTSIDE, puzzlePiece1PuzzleGridOrientation)
                puzzlePiece2Side = puzzlePiece2.getSide(PuzzlePiece.RIGHTSIDE, puzzlePiece2PuzzleGridOrientation)
            #Is piece1 to the left of piece2?
            elif(puzzlePiece2GridPosition.getColumn()>puzzlePiece1GridPosition.getColumn() and puzzlePiece2GridPosition.getColumn()-puzzlePiece1GridPosition.getColumn()==1):
                self.log(Logger.DEBUG, "Piece2 to the left of piece1.")
                puzzlePiece1Side = puzzlePiece1.getSide(PuzzlePiece.RIGHTSIDE, puzzlePiece1PuzzleGridOrientation)
                puzzlePiece2Side = puzzlePiece2.getSide(PuzzlePiece.LEFTSIDE, puzzlePiece2PuzzleGridOrientation)
                #The pieces are not next to each other, log an error and return false
            else:
                self.log(Logger.ERROR, 'Piece1 and piece2 are in the same row, but not contiguous. Piece1 at (row %i, col %i), and Piece 2 is at (row %i, col %i).' % (puzzlePiece1GridPosition.getRow(), puzzlePiece1GridPosition.getColumn(), puzzlePiece2GridPosition.getRow(), puzzlePiece2GridPosition.getColumn()))
                return False
        #Same column?
        elif(puzzlePiece1GridPosition.getColumn()==puzzlePiece2GridPosition.getColumn()):
            self.log(Logger.DEBUG, "Puzzle pieces in same column.")
            #Is piece1 above piece2?
            if(puzzlePiece2GridPosition.getRow()>puzzlePiece1GridPosition.getRow() and puzzlePiece2GridPosition.getRow()-puzzlePiece1GridPosition.getRow()==1):
                self.log(Logger.DEBUG, "Piece1 is above piece2.")
                #Piece 1 is above piece 2, so try to match the bottom side of piece 1 to the
                #top side of piece 2, as adjusted for rotation
                puzzlePiece1Side = puzzlePiece1.getSide(PuzzlePiece.BOTTOMSIDE, puzzlePiece1PuzzleGridOrientation)
                puzzlePiece2Side = puzzlePiece2.getSide(PuzzlePiece.TOPSIDE, puzzlePiece2PuzzleGridOrientation)
            #Is piece2 above piece1?
            elif(puzzlePiece1GridPosition.getRow()>puzzlePiece2GridPosition.getRow() and puzzlePiece1GridPosition.getRow()-puzzlePiece2GridPosition.getRow()==1):
                self.log(Logger.DEBUG, "Piece2 is above piece1.")
                puzzlePiece1Side = puzzlePiece1.getSide(PuzzlePiece.TOPSIDE, puzzlePiece1PuzzleGridOrientation)
                puzzlePiece2Side = puzzlePiece2.getSide(PuzzlePiece.BOTTOMSIDE, puzzlePiece2PuzzleGridOrientation)
            #The pieces are not next to each other, log an error and return false
            else:
                self.log(Logger.ERROR, 'Piece1 and piece2 are in the same column, but not contiguous. Piece1 at (row %i, col %i), and Piece 2 is at (row %i, col %i).' % (puzzlePiece1GridPosition.getRow(), puzzlePiece1GridPosition.getColumn(), puzzlePiece2GridPosition.getRow(), puzzlePiece2GridPosition.getColumn()))
                return False
        else:
            self.log(Logger.ERROR, "Puzzle pieces are not in same row or same column.")
            return False

        if puzzlePiece1Side != None and puzzlePiece2Side != None:
            #There are contiguous sides, determine if they match
            return puzzlePiece1Side.sidesMatch(puzzlePiece1Side, puzzlePiece2Side)
        else:
            self.log(Logger.ERROR, "Does not have two sides to compate")
            return False

    def tryToPlacePiece(self, puzzlePieceToPlace, puzzlePieceGridPosition, puzzlePieceOrientation):
        #if the piece is already on the board it cannot be placed
        existingPosition = self.findPuzzlePieceGridPosition(puzzlePieceToPlace)
        if existingPosition != None:
            self.log(Logger.DEBUG, '%s has already been placed on board at %s.' % (puzzlePieceToPlace.getName(), existingPosition))
            return False

        self.log(Logger.DEBUG, 'Attempting to place %s at %s.' % (puzzlePieceToPlace.getName(), puzzlePieceGridPosition))
        self.setPuzzlePiece(puzzlePieceToPlace, puzzlePieceGridPosition, puzzlePieceOrientation)
        neighboringPieces = self.getNeighboringPieces(puzzlePieceToPlace)
        self.log(Logger.DEBUG, '%s has %i neighboring pieces to check.' % (puzzlePieceToPlace.getName(), len(neighboringPieces)))
        for neighboringPiece in neighboringPieces:
            if self.puzzlePiecesMate(puzzlePieceGridPosition, self.findPuzzlePieceGridPosition(neighboringPiece)) == False:
                puzzlePieceGridPosition.clearPuzzleGridPosition()
                return False

        self.log(Logger.DEBUG,'%s can be placed at %s.' % (puzzlePieceToPlace.getName(), puzzlePieceGridPosition))
        return True

class PuzzleSolvingUtil(LoggableBaseClass):
    REVERSE_ORDERED_POSITIONS=None

    def __init__(self, puzzle_to_solve):
        self.setLogger(Logger())
        self.log(Logger.DEBUG, "Creating PuzzleUtil.")
        self.puzzle=puzzle_to_solve
        self.puzzle_grid=self.puzzle.puzzle_grid
        self.puzzle_pieces=self.puzzle.puzzle_pieces
        if PuzzleSolvingUtil.REVERSE_ORDERED_POSITIONS==None:
            PuzzleSolvingUtil.REVERSE_ORDERED_POSITIONS=PuzzleGrid.ORDERED_POSITIONS[:]
            PuzzleSolvingUtil.REVERSE_ORDERED_POSITIONS.reverse()

    def clearDependentPositions(self, puzzleGridPositionToTest):
        for puzzleGridPosition in PuzzleSolvingUtil.REVERSE_ORDERED_POSITIONS:
            if puzzleGridPosition == puzzleGridPositionToTest:
                break
            else:
                puzzleGridPosition.clearPuzzleGridPosition()

    def tryPiecesInPosition(self, puzzleGridPositionToTest):
        nextpuzzleGridPositionToTest=None
        indexOfPosition=PuzzleGrid.ORDERED_POSITIONS.index(puzzleGridPositionToTest)
        if(indexOfPosition < len(PuzzleGrid.ORDERED_POSITIONS)-1):
            nextpuzzleGridPositionToTest=PuzzleGrid.ORDERED_POSITIONS[indexOfPosition+1]

        for piece in self.puzzle_pieces:
            PuzzleSolvingUtil(self.puzzle).clearDependentPositions(puzzleGridPositionToTest)
            #no need to rotate the center piece that is being tried
            if puzzleGridPositionToTest == PuzzleGrid.POSITION5:
                pieceIsPlaced = self.puzzle_grid.tryToPlacePiece(piece, puzzleGridPositionToTest, PuzzleGridPosition.ORIENTATION1)
                if pieceIsPlaced:
                    puzzle_util=PuzzleSolvingUtil(self.puzzle)
                    puzzle_util.tryPiecesInPosition(nextpuzzleGridPositionToTest)
            #no need to call additional positions if in the final position, but do need to rotate piece
            elif puzzleGridPositionToTest == PuzzleGrid.POSITION9:
                for orientation in PuzzleGridPosition.ORIENTATIONS:
                    self.log(Logger.DEBUG, 'Trying orientation %i for %s' % (orientation, piece))
                    pieceIsPlaced = self.puzzle_grid.tryToPlacePiece(piece, puzzleGridPositionToTest, orientation)
                    if pieceIsPlaced:
                        self.log(Logger.MESSAGE, "Found solution")
                        i=1
                        for solutionPosition in self.puzzle_grid.POSITIONS:
                            self.log(Logger.MESSAGE, 'Position %i has piece %s with an orientation of %i' % (i, solutionPosition.getPiece(), solutionPosition.getPieceOrientation()))
                            i=i+1
            else:
                for orientation in PuzzleGridPosition.ORIENTATIONS:
                    self.log(Logger.DEBUG, 'Trying orientation %i for %s' % (orientation, piece))
                    pieceIsPlaced = self.puzzle_grid.tryToPlacePiece(piece, puzzleGridPositionToTest, orientation)
                    #if puzzleGridPositionToTest == PuzzleGrid.POSITION8:
                    # self.log(Logger.MESSAGE, 'Got to position 8')

                    if pieceIsPlaced:
                        puzzle_util=PuzzleSolvingUtil(self.puzzle)
                        puzzle_util.tryPiecesInPosition(nextpuzzleGridPositionToTest)
                        return False

class Puzzle(LoggableBaseClass):
    def __init__(self):
        self.setLogger(Logger())
        self.log(Logger.MESSAGE, "Creating puzzle.")
        self.puzzle_grid = PuzzleGrid(self.getLogger(), self)
        self.puzzle_pieces = []
        self.createPieces()

    def createPieces(self):
        self.log(Logger.DEBUG, "Creating pieces.")

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_positive_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_negative_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_negative_half)
        self.piece1 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece1.setName("Piece 1")
        self.puzzle_pieces.append(self.piece1)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_positive_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_positive_half)
        self.piece2 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece2.setName("Piece 2")
        self.puzzle_pieces.append(self.piece2)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_negative_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_positive_half)
        self.piece3 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece3.setName("Piece 3")
        self.puzzle_pieces.append(self.piece3)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_positive_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_positive_half)
        self.piece4 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece4.setName("Piece 4")
        self.puzzle_pieces.append(self.piece4)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_negative_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_negative_half)
        self.piece5 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece5.setName("Piece 5")
        self.puzzle_pieces.append(self.piece5)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_positive_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_positive_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_negative_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        self.piece6 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece6.setName("Piece 6")
        self.puzzle_pieces.append(self.piece6)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_negative_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        self.piece7 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece7.setName("Piece 7")
        self.puzzle_pieces.append(self.piece7)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_negative_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_positive_half)
        self.piece8 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece8.setName("Piece 8")
        self.puzzle_pieces.append(self.piece8)

        s1 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_eagle, PuzzlePieceSide.image_negative_half)
        s2 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_chevron, PuzzlePieceSide.image_negative_half)
        s3 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_stripes, PuzzlePieceSide.image_positive_half)
        s4 = PuzzlePieceSide(self.getLogger(), PuzzlePieceSide.image_checkers, PuzzlePieceSide.image_negative_half)
        self.piece9 = PuzzlePiece(self.getLogger(), s1, s2, s3, s4)
        self.piece9.setName("Piece 9")
        self.puzzle_pieces.append(self.piece9)

        self.log(Logger.DEBUG, "Done creating pieces.")

    def solve(self):
        self.log(Logger.DEBUG, "Solve function started.")
        puzzle_util=PuzzleSolvingUtil(self)
        puzzle_util.tryPiecesInPosition(PuzzleGrid.POSITION5)
        self.log(Logger.DEBUG, "Exiting Solve function.")

if __name__ == "__main__":
    puz = Puzzle()
    puz.solve()
