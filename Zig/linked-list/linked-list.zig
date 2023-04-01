const std = @import("std");
const stdout = std.io.getStdOut().writer();

var gpa = std.heap.GeneralPurposeAllocator(.{}){};

pub fn LinkedList(comptime T: type) type {
    return struct {
        pub const Node = struct {
            data: T,
            next: ?*Node,
        };

        allocator: std.mem.Allocator,
        first: ?*Node = null,
        last: ?*Node = null,
        len: usize = 0,

        pub fn init(allocator: std.mem.Allocator) @This() {
            return @This(){.allocator=allocator};
        }

        pub fn push_right(self: *@This(), data: T) !void {
            var new_node = try self.allocator.create(Node);
            new_node.data = data;
            new_node.next = null;
            if (self.last) |last| {
                last.next = new_node;
            } else {
                self.first = new_node;
            }
            self.last = new_node;
            self.len += 1;
        }

        pub fn push_left(self: *@This(), data: T) !void {
            var new_node = try self.allocator.create(Node);
            new_node.data = data;
            new_node.next = self.first;
            self.first = new_node;
            self.len += 1;
        } 

        pub fn pop_left(self: *@This()) ?T {
            if (self.first) |first| {
                var new_first = first.next;
                var retval = first.data;
                self.allocator.destroy(first);
                self.first = new_first;
                self.len -= 1;
                return retval;
            } else {
                return null;
            }
        }

        pub fn print(self: *@This()) !void {
            var node_ptr = self.first;
            while (node_ptr) |node| {
                try stdout.print("{any}, ", .{node.data});
                node_ptr = node.next;
            }
        }
    };
}

test "LinkedList_pushpop" {
    var list = LinkedList(u32).init(gpa.allocator());

    std.debug.assert(list.pop_left() == null);

    try list.push_right(2);
    try list.push_right(69);
    try list.push_right(420);

    std.debug.assert(list.len == 3);

    std.debug.assert(list.pop_left().? == 2);
    std.debug.assert(list.len == 2);
    
    try list.push_left(1867);
    
    std.debug.assert(list.pop_left().? == 1867);
    std.debug.assert(list.pop_left().? == 69);
    std.debug.assert(list.pop_left().? == 420);
    std.debug.assert(list.pop_left() == null);
    std.debug.assert(list.len == 0);
}

pub fn main() !void {
    var list = LinkedList(u32).init(gpa.allocator());
    try list.push_right(2);
    try list.push_right(69);
    try list.push_right(420);
    try list.push_left(69);
    try list.push_left(420);
    try stdout.print("size: {d}\n", .{list.len});
    try list.print();

    try stdout.print("\n", .{});
}