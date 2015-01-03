/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGPanel.h"
#import "HSPopUpList.h"
#import "PyBudgetPanel.h"

@class MGMainWindowController;

@interface MGBudgetPanel : MGPanel <NSTextFieldDelegate> {
    NSTextField *startDateField;
    NSTextField *repeatEveryField;
    NSTextField *repeatEveryDescLabel;
    NSPopUpButton *repeatTypePopUpView;
    NSTextField *stopDateField;
    NSPopUpButton *accountSelector;
    NSPopUpButton *targetSelector;
    NSTextField *amountField;
    NSTextField *notesField;
    
    HSPopUpList *repeatTypePopUp;
    HSPopUpList *accountPopUp;
    HSPopUpList *targetPopUp;
}

@property (readwrite, retain) NSTextField *startDateField;
@property (readwrite, retain) NSTextField *repeatEveryField;
@property (readwrite, retain) NSTextField *repeatEveryDescLabel;
@property (readwrite, retain) NSPopUpButton *repeatTypePopUpView;
@property (readwrite, retain) NSTextField *stopDateField;
@property (readwrite, retain) NSPopUpButton *accountSelector;
@property (readwrite, retain) NSPopUpButton *targetSelector;
@property (readwrite, retain) NSTextField *amountField;
@property (readwrite, retain) NSTextField *notesField;

- (id)initWithParent:(MGMainWindowController *)aParent;
- (PyBudgetPanel *)model;
/* Python --> Cocoa */
- (void)refreshRepeatEvery;
@end
