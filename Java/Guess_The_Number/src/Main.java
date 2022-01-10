import java.util.Random;
import java.util.Scanner;

public class Main {
    public static final Scanner scan = new Scanner(System.in);

    public static void main(String[] args) {
        Random rand = new Random();
        int randint;

        boolean isPlaying = getYesOrNo("Welcome to the number guessing game! Would you like to play");

        while(isPlaying) {
            randint = 1 + rand.nextInt(20);

            for(int attempts = 5; attempts >= 0; attempts--) {
                int guess = getGuess();

                if(guess == randint) {
                        System.out.printf("> Congratulations, you have guessed the number with %d attempt(s) left!\n", attempts);
                        break;
                } else if(attempts == 0) {
                    System.out.printf("> Game over man! Game over! The number was %d.\n", randint);
                } else if(guess > randint) {
                    System.out.printf("> Aim lower, chief. You have %d attempt(s) left.\n", attempts);
                } else {
                    System.out.printf("> You gotta' aim higher! You have %d attempt(s) left.\n", attempts);
                }
            }
            isPlaying = getYesOrNo("\nWould you like to play again?");
        }
        System.out.println("\nFine then, be that way!");
    }


    private static int getGuess() {
        int num;

        while(true) {
            System.out.println("\nGuess a number from 1 to 20." + 7/3);
            String input = scan.nextLine();

            if(input.matches("^[0-9]+$")) {
                num = Integer.parseInt(input);

                if(num > 0 && num <= 20) {
                    return num;
                } else {
                    System.out.println("> INVALID INPUT: " + input + " IS OUTSIDE OF RANGE");
                }
            } else {
                System.out.println(" INVALID INPUT: " + input + " IS NOT AN INTEGER");
            }
        }
    }


    private static boolean getYesOrNo(String text) {
        String input;

        do {
            System.out.println(text + " (y/n)");
            input = scan.nextLine().toLowerCase();

            text = "INVALID RESPONSE: " + input + "\n";
        } while(!input.matches("^[y|n]$"));

        return input.equals("y");
    }




}
