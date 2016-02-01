/* 
Copyright 2016 Virgil Dupras

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGPluginListTable.h"
#import "MGTableView.h"
#import "HSPyUtil.h"

@implementation MGPluginListTable
- (id)initWithPyRef:(PyObject *)aPyRef tableView:(MGTableView *)aTableView
{
    PyTable *m = [[PyTable alloc] initWithModel:aPyRef];
    self = [super initWithModel:m tableView:aTableView];
    [m bindCallback:createCallback(@"TableView", self)];
    [m release];
    [self initializeColumns];
    [aTableView setSortDescriptors:[NSArray array]];
    return self;
}

- (void)initializeColumns
{
    HSColumnDef defs[] = {
        {@"enabled", 60, 60, 60, NO, [NSButtonCell class]},
        {@"name", 300, 60, 0, NO, nil},
        {@"type", 150, 60, 0, NO, nil},
        {@"author", 120, 60, 0, NO, nil},
        nil
    };
    [[self columns] initializeColumns:defs];
    NSTableColumn *c = [[self tableView] tableColumnWithIdentifier:@"enabled"];
    [[c dataCell] setButtonType:NSSwitchButton];
    [[c dataCell] setControlSize:NSSmallControlSize];
    [[self columns] restoreColumns];
}

/* Overrides */
- (PyTable *)model
{
    return (PyTable *)model;
}
@end