/*
 * Prompts the user for integer input until valid input is supplied and then
 * returns the integer. 
 */
int get_valid_int() {
    int input;
    // Prompt again if the user inputs anything other than integer input 
    // followed by a new line.
    while (!(scanf("%d", &input) && getchar() == '\n')) {
        // Clear the scanf buffer.
        while (getchar() != '\n'); 
        printf("Invalid. Must enter an integer:\n");
    }
    return input;
}

/*
 * Prompts the user for integer input until valid input is supplied and the
 * integer is in the specified range, then returns the integer. 
 */
int get_valid_int_ranged(int min, int max) {
    int input;
    // Prompt again if the user inputs anything other than integer input 
    // followed by a new line.
    while (1) {
        if (!(scanf("%d", &input) && getchar() == '\n')) {
            printf("Invalid. Must enter an integer:\n");
            while (getchar() != '\n');
        } else if (input < min || input > max) {
            printf("Invalid. Integer must be between %d and %d inclusive:\n", min, max);
        } else {
            return input;
        }
    }
}

    while (!(scanf("%d", &input) && getchar() == '\n')) {
        // Clear the scanf buffer.
        while (getchar() != '\n'); 

        printf("Invalid. Must enter an integer:\n");
    }
    return input;


/*
 * Prompts the user for input until a character from the string of valid 
 * choices is supplied. Returns the valid character supplied.
 */
char choose_valid_char(const char valid_choices[]) {
    char choice;
    
    while (1) {
        scanf(" %c", &choice);
        // Make sure the user entered a single character followed by a new line.
        if (getchar() == '\n') {
            int i = 0;
            // Return the character chosen by the user if it is found in the
            // string of valid characters.
            while (valid_choices[i] != '\0') {
                if (choice == valid_choices[i]) {
                    return choice;
                } 
                i++;
            }
        // Otherwise, clear the input buffer and let the loop continue.
        } else {
            while (getchar() != '\n');
        }
        printf("Invalid. Enter one of the specified characters:\n");
    }
}