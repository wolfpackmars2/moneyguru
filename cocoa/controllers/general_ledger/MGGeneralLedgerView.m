/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGGeneralLedgerView.h"
#import "MGGeneralLedgerPrint.h"
#import "MGTransactionInspector.h"
#import "MGMassEditionPanel.h"
#import "HSPyUtil.h"
#import "Utils.h"

@implementation MGGeneralLedgerView
- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyGeneralLedgerView *m = [[PyGeneralLedgerView alloc] initWithModel:aPyRef];
    self = [super initWithModel:m];
    [m bindCallback:createCallback(@"BaseViewView", self)];
    [m release];
    tableView = [[MGGeneralLedgerTableView alloc] initWithFrame:NSMakeRect(0, 0, 100, 100)];
    [self setupTableView:tableView];
    mainResponder = tableView;
    self.view = [tableView wrapInScrollView];
    ledgerTable = [[MGGeneralLedgerTable alloc] initWithPyRef:[[self model] table] tableView:tableView];
    [tableView release];
    return self;
}
        
- (void)dealloc
{
    [ledgerTable release];
    [super dealloc];
}

- (PyGeneralLedgerView *)model
{
    return (PyGeneralLedgerView *)model;
}

- (MGPrintView *)viewToPrint
{
    return [[[MGGeneralLedgerPrint alloc] initWithPyParent:[self model] tableView:[ledgerTable tableView]] autorelease];
}

- (NSString *)tabIconName
{
    return @"gledger_16";
}

- (id)fieldEditorForObject:(id)asker
{
    return [ledgerTable fieldEditorForObject:asker];
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