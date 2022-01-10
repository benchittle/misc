import java.util.Scanner;
import java.util.Random;


public class Main {
    private static final Scanner scan = new Scanner(System.in);
    private static final Random random = new Random();

    public static String[][] board = new String[][] {{" ", " ", " "}, {" ", " ", " "}, {" ", " ", " "}};
    public static int turn;
    public static String P1char;
    public static String P2char;
    public static int boardSize = 3;

    public static void main(String[] args) {
        boolean isPlaying = true;

        System.out.println("Welcome to Tic Tac Toe!\n");
        int choice = getNum(1, 2, "Would you like to play the text based (1) or graphical (2) version?", "Choose either 1 or 2.");

        if (choice == 1) {
            int players = getNum(1, 2, "How many players are there?", "Choose either 1 or 2.");

            P1char = getInput("^[^ ]$", "P1: What symbol would you like to use as your marker? (single non-space character)", "P1: Choose a single non-space character.");
            if(players == 2) {
                P2char = getInput("^[^ " + P1char + "]$", "P2: What symbol would you like to use as your marker? (single non-space character)", "P2: Choose a single non-space character (cannot be the same as P1).");
            } else {
                P2char = P1char.matches("^[xX]$") ? "O" : "X";
                System.out.printf("> Player 2 (A.I.) will use %s", P2char);

            }

            turn = 1 + random.nextInt(1);
            System.out.printf("\n> Player %d will go first\n", turn);

            while(isPlaying) {
                drawBoard();
                doMove();
                isPlaying = winCheck();
                if (isPlaying) {
                    turn = turn == 1 ? 2 : 1;
                } else {
                    showOutcome();
                    isPlaying = getInput("^[y|n]$", "Would you like to play again? (y/n)", "Use y/n.") == "y";
                }
            }



        } else if (choice == 2) {
            System.out.println("WIP");
        }


        System.out.println("Done!");

    }


    private static String getInput(String regex, String msg, String errorMsg) {
        String input;
        do {
            System.out.println(msg);
            input = scan.nextLine().toLowerCase();

            msg = "INVALID INPUT: " + input + "\n" + errorMsg;
        } while (!input.matches(regex));

        return input;
    }


    private static int getNum(int min, int max, String msg, String errorMsg) {
        int num;
        do {
            num = Integer.parseInt(getInput("^[0-9]+$", msg, "Input must be an integer."));
            msg = "INVALID INPUT: " + num + "\n" + errorMsg;
        } while(num < min || num > max);

        return num;
    }


    private static void drawBoard() {
        System.out.printf("\nP%d: Your turn.\n", turn);
        System.out.printf( "[7]  |[8]  |[9]  \n"
                         + "  %s  |  %s  |  %s  \n", board[2][0], board[2][1], board[2][2]);
        System.out.printf( "     |     |     \n"
                         + "-----------------\n"
                         + "[4]  |[5]  |[6]  \n"
                         + "  %s  |  %s  |  %s  \n", board[1][0], board[1][1], board[1][2]);
        System.out.printf( "     |     |     \n"
                         + "-----------------\n"
                         + "[1]  |[2]  |[3]  \n"
                         + "  %s  |  %s  |  %s  \n", board[0][0], board[0][1], board[0][2]);
        System.out.println("     |     |     ");
    }


    private static void doMove() {
        int choice = getNum(1, 9, "", "P" + turn + ": Choose a position from 1 to 9.") - 1;
        board[choice / 3][choice % 3] = turn == 1 ? P1char : P2char;
    }


    private static boolean winCheck() {
        for(int xy = 0; xy < boardSize; xy++) {
            if (!board[xy][xy].equals(" ")) {

                columns: {
                    for(int x = 1; x < boardSize; x++) {
                        if(!board[x][xy].equals(board[x - 1][xy])) {
                            break columns;
                        }
                    }
                    return true;
                }
                rows: {
                    for (int y = 1; y < boardSize; y++) {
                        if (!board[xy][y].equals(board[xy][y - 1])) {
                            break;
                        }
                    }
                }



/*
                if (board[num][0].equals(board[num][1]) && board[num][0].equals(board[num][2])) {
                    return false;
                }
                if (board[0][num].equals(board[1][num]) && board[0][num].equals(board[2][num])) {
                    return false;
                }
            }
        }
        if(!board[1][1].equals(" ")) {
            if ((board[0][0].equals(board[1][1]) && board[0][0].equals(board[2][2])) || (board[0][2].equals(board[1][1]) && board[0][2].equals(board[2][0]))) {
                return false;
*/
            }
        }
        return true;
    }


    private static void showOutcome() {
        if(turn == 1){

        }
    }
}