const std = @import("std");
const rand = std.rand;

const debug = std.log.debug;

const stdout = std.io.getStdOut().writer();
const stdin = std.io.getStdIn().reader();


/// Remove leading and trailing whitespace from a string.
fn strStrip(output: []u8, ascii_string: []const u8) []u8 {
    std.debug.assert(output.len >= ascii_string.len);

    var start: usize = 0;
    for (ascii_string) |c, i| {
        if (!std.ascii.isWhitespace(c)) {
            start = i;
            break;
        }
    }
    var end: usize = start;
    for (ascii_string[start..]) |c, i| {
        if (!std.ascii.isWhitespace(c)) {
            end = i + start + 1;
        }
    }

    std.mem.copy(u8, output, ascii_string[start..end]);

    return output[0..(end - start)];
}

test "strStrip1" {
    var buf: [64]u8 = undefined;
    var result = strStrip(&buf, " \t\t \n hello world\n  \t \n ");
    try std.testing.expectEqualStrings("hello world", result);
}

test "strStrip2" {
    var buf: [64]u8 = undefined;
    var result = strStrip(&buf, "");
    try std.testing.expectEqualStrings("", result);
}

test "strStrip3" {
    var buf: [64]u8 = undefined;
    var result = strStrip(&buf, " \n\t    \n    ");
    try std.testing.expectEqualStrings("", result);
}

/// Prompt the user for a u32. Invalid input will be ignored and the user will
/// be prompted again.
/// Returns: A valid u32 entered by the user, or null if EOF is entered.
fn getNumber(prompt: []const u8) !?u32 {
    while (true) {
        var buf: [32]u8 = undefined;

        try stdout.print("{s}", .{prompt});
        const buf_read = stdin.readUntilDelimiterOrEof(&buf, '\n') catch |err| switch(err) {
            error.StreamTooLong => {
                try stdout.print("Error: Input too long\n", .{});
                try stdin.skipUntilDelimiterOrEof('\n');
                continue;
            },
            else => return err
        } orelse return null;
            
        return std.fmt.parseInt(u32, buf_read, 10) catch |err| {
            switch(err) {
                error.InvalidCharacter => try stdout.print("Error: Invalid input\n", .{}),
                error.Overflow => try stdout.print("Error: Number too large\n", .{}),
            }
            continue;
        };
    }
}

/// Prompt the user for yes or no input ('y' or 'n'). Case is ignored, as well as
/// leading or trailing whitespace. User input exceeding 32 characters will be 
/// ignored and the user will be prompted again. 
/// Returns: true for yes, false for no, or null if EOF is entered.
fn getYesNo(prompt: []const u8) !?bool {
    var buf: [32]u8 = undefined;

    try stdout.print("{s}", .{prompt});
    while (true) {
        const buf_read = stdin.readUntilDelimiterOrEof(&buf, '\n') catch |err| switch(err) {
            error.StreamTooLong => {
                try stdout.print("Error: Input too long\n", .{});
                try stdin.skipUntilDelimiterOrEof('\n');
                continue;
            },
            else => return err,
        } orelse return null;

        const buf_stripped = strStrip(&buf, buf_read);
        
        if (std.ascii.eqlIgnoreCase(buf_stripped, "y")) {
            return true;
        } else if (std.ascii.eqlIgnoreCase(buf_stripped, "n")) {
            return false;
        }

        try stdout.print("Invalid Input: Enter y or n: ", .{});
    }
}

pub fn main() !void {
    debug("Start", .{});
    
    try stdout.print("Welcome to Guess the Number!\n", .{});

    var rng = rand.DefaultPrng.init(0);

    game: while (true) {
        const target = rng.random().intRangeAtMost(u32, 1, 100);
        for ([_]u32 {1, 2, 3, 4, 5, 6}) |round| {
            try stdout.print("\nRound {d} of 6\n", .{round});
            const num = try getNumber("Enter a number from 1 to 100: ") orelse {
                break :game;
            };
            if (num > 100) {
                try stdout.print("Silly goose, {d} is bigger than 100!\n", .{num});
            } else if (num == target) {
                try stdout.print("You guessed it!\n", .{});
                break;
            } else if (num < target) {
                try stdout.print("Guess higher!\n", .{});
            } else {
                try stdout.print("Guess lower!\n", .{});
            }
        }

        try stdout.print("The number was {d}\n", .{target});

        if (try getYesNo("\nWould you like to play again? [y/n]: ")) |is_yes| {
            if (!is_yes) {
                break;
            }
        } else {
            break;
        }
    }

    try stdout.print("\nThanks for playing!\n", .{});
}