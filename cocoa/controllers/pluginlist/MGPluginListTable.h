/* 
Copyright 2016 Virgil Dupras

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyTable.h"
#import "MGEditableTable.h"

@interface MGPluginListTable : MGEditableTable {}
- (id)initWithPyRef:(PyObject *)aPyRef tableView:(MGTableView *)aTableView;
- (void)initializeColumns;
- (PyTable *)model;
@end