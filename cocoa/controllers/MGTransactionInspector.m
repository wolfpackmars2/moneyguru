/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "MGTransactionInspector.h"
#import "Utils.h"
#import "MGFieldEditor.h"
#import "MGDateFieldEditor.h"
#import "NSEventAdditions.h"

@implementation MGTransactionInspector
- (id)initWithDocument:(MGDocument *)aDocument
{
    self = [super initWithNibName:@"TransactionInspector" pyClassName:@"PyTransactionPanel" document:aDocument];
    [self window]; // Initialize the window
    customFieldEditor = [[MGFieldEditor alloc] init];
    customDateFieldEditor = [[MGDateFieldEditor alloc] init];
    splitTable = [[MGSplitTable alloc] initWithTransactionPanel:[self py] view:splitTableView];
    [splitTable connect];
    return self;
}

- (void)dealloc
{
    [customDateFieldEditor release];
    [customFieldEditor release];
    [splitTable release];
    [super dealloc];
}

- (PyTransactionPanel *)py
{
    return (PyTransactionPanel *)py;
}

- (NSString *)fieldOfTextField:(NSTextField *)textField
{
    if (textField == descriptionField)
    {
        return @"description";
    }
    else if (textField == payeeField)
    {
        return @"payee";
    }
    return nil;
}

- (NSResponder *)firstField
{
    return dateField;
}

- (void)loadFields
{
    [tabView selectFirstTabViewItem:self];
    [descriptionField setStringValue:[[self py] description]];
    [payeeField setStringValue:[[self py] payee]];
    [checknoField setStringValue:[[self py] checkno]];
    [notesField setStringValue:[[self py] notes]];
    [amountField setStringValue:[[self py] amount]];
    [amountField2 setStringValue:[[self py] amount]];
    [splitTable refresh];
}

- (void)saveFields
{
    [[self py] setDescription:[descriptionField stringValue]];
    [[self py] setPayee:[payeeField stringValue]];
    [[self py] setCheckno:[checknoField stringValue]];
    [[self py] setNotes:[notesField stringValue]];
    [[self py] setAmount:[amountField stringValue]];
}

/* Python --> Cocoa */
- (void)refreshAmount
{
    [amountField setStringValue:[[self py] amount]];
    [amountField2 setStringValue:[[self py] amount]];
}

- (void)refreshForMultiCurrency
{
    BOOL mct = [[self py] isMultiCurrency];
    [mctBalanceButton setEnabled:mct];
    [amountField setEnabled:!mct];
    [amountField2 setEnabled:!mct];
    [mctNotice setHidden:!mct];
    [mctNotice2 setHidden:!mct];
}

/* Actions */
- (IBAction)addSplit:(id)sender
{
    [[splitTable py] add];
}

- (IBAction)deleteSplit:(id)sender
{
    [[splitTable py] deleteSelectedRows];
}

- (IBAction)mctBalance:(id)sender
{
    [[self py] mctBalance];
}

/* Delegate */
- (void)controlTextDidEndEditing:(NSNotification *)aNotification
{
    id control = [aNotification object];
    if ((control == amountField) || (control == amountField2)) {
        // must be edited right away to refresh the split table
        [[self py] setAmount:[(NSTextField *)control stringValue]];
    }
}

- (id)windowWillReturnFieldEditor:(NSWindow *)window toObject:(id)asker
{
    if (asker == dateField)
    {
        return customDateFieldEditor;
    }
    return customFieldEditor;
}
@end
