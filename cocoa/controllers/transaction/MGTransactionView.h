/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyTransactionView.h"
#import "MGBaseView.h"
#import "MGTableView.h"
#import "AMButtonBar.h"
#import "MGTransactionTable.h"
#import "MGFilterBar.h"

@interface MGTransactionView : MGBaseView
{
    MGTableView *tableView;
    AMButtonBar *filterBarView;
    
    MGTransactionTable *transactionTable;
    MGFilterBar *filterBar;
}

@property (readwrite, retain) MGTableView *tableView;
@property (readwrite, retain) AMButtonBar *filterBarView;

- (id)initWithPyRef:(PyObject *)aPyRef;

- (PyTransactionView *)model;

- (id)fieldEditorForObject:(id)asker;
@end