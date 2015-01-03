/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGBudgetView.h"
#import "MGBudgetPrint.h"
#import "Utils.h"

@implementation MGBudgetView
- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyBudgetView *m = [[PyBudgetView alloc] initWithModel:aPyRef];
    self = [super initWithModel:m];
    [m release];
    tableView = [[MGTableView alloc] initWithFrame:NSMakeRect(0, 0, 100, 100)];
    [self setupTableView:tableView];
    mainResponder = tableView;
    self.view = [tableView wrapInScrollView];
    budgetTable = [[MGBudgetTable alloc] initWithPyRef:[[self model] table] tableView:tableView];
    [tableView release];
    return self;
}
        
- (void)dealloc
{
    [budgetTable release];
    [super dealloc];
}

- (PyBudgetView *)model
{
    return (PyBudgetView *)model;
}

- (MGPrintView *)viewToPrint
{
    return [[[MGBudgetPrint alloc] initWithPyParent:[self model] tableView:[budgetTable tableView]] autorelease];
}

- (NSString *)tabIconName
{
    return @"budget_16";
}
@end