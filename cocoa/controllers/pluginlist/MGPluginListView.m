/* 
Copyright 2016 Virgil Dupras

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGPluginListView.h"
#import "HSPyUtil.h"
#import "Utils.h"

@implementation MGPluginListView
- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyPluginListView *m = [[PyPluginListView alloc] initWithModel:aPyRef];
    self = [super initWithModel:m];
    [m bindCallback:createCallback(@"BaseViewView", self)];
    [m release];
    tableView = [[MGTableView alloc] initWithFrame:NSMakeRect(0, 0, 100, 100)];
    [self setupTableView:tableView];
    mainResponder = tableView;
    self.view = [tableView wrapInScrollView];
    pluginListTable = [[MGPluginListTable alloc] initWithPyRef:[[self model] table] tableView:tableView];
    [tableView release];
    return self;
}
        
- (void)dealloc
{
    [pluginListTable release];
    [super dealloc];
}

- (PyPluginListView *)model
{
    return (PyPluginListView *)model;
}
@end