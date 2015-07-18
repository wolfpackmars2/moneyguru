/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGTransactionView.h"
#import "MGTransactionView_UI.h"
#import "MGTransactionPrint.h"
#import "MGTransactionInspector.h"
#import "MGMassEditionPanel.h"
#import "HSPyUtil.h"
#import "Utils.h"

@implementation MGTransactionView

@synthesize tableView;
@synthesize filterBarView;

- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyTransactionView *m = [[PyTransactionView alloc] initWithModel:aPyRef];
    self = [super initWithModel:m];
    [m bindCallback:createCallback(@"BaseViewView", self)];
    [m release];
    self.view = createMGTransactionView_UI(self);
    transactionTable = [[MGTransactionTable alloc] initWithPyRef:[[self model] table] tableView:tableView];
    filterBar = [[MGFilterBar alloc] initWithPyRef:[[self model] filterBar] view:filterBarView forEntryTable:NO];
    return self;
}
        
- (void)dealloc
{
    [transactionTable release];
    [filterBar release];
    [super dealloc];
}

- (PyTransactionView *)model
{
    return (PyTransactionView *)model;
}

- (MGPrintView *)viewToPrint
{
    return [[[MGTransactionPrint alloc] initWithPyParent:[self model] 
        tableView:[transactionTable tableView]] autorelease];
}

- (NSString *)tabIconName
{
    return @"transaction_table_16";
}

- (id)fieldEditorForObject:(id)asker
{
    return [transactionTable fieldEditorForObject:asker];
}

- (PyObject *)createPanelWithModelRef:(PyObject *)aPyRef name:(NSString *)name
{
    MGPanel *panel;
    if ([name isEqual:@"MassEditionPanel"]) {
        panel = [[MGMassEditionPanel alloc] initWithPyRef:aPyRef parentWindow:[[self view] window]];
    }
    else {
        panel = [[MGTransactionInspector alloc] initWithPyRef:aPyRef parentWindow:[[self view] window]];
    }
    panel.releaseOnEndSheet = YES;
    return [[panel model] pyRef];
}
@end