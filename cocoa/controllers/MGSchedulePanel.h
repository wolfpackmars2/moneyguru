/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGPanel.h"
#import "MGTableView.h"
#import "MGSplitTable.h"
#import "HSPopUpList.h"
#import "PySchedulePanel.h"

@class MGMainWindowController;

@interface MGSchedulePanel : MGPanel <NSTextFieldDelegate> {
    NSTabView *tabView;
    NSTextField *startDateField;
    NSTextField *repeatEveryField;
    NSTextField *repeatEveryDescLabel;
    NSPopUpButton *repeatTypePopUpView;
    NSTextField *stopDateField;
    NSTextField *descriptionField;
    NSTextField *payeeField;
    NSTextField *checknoField;
    NSTextField *notesField;
    MGTableView *splitTableView;
    
    MGSplitTable *splitTable;
    HSPopUpList *repeatTypePopUp;
}

@property (readwrite, retain) NSTabView *tabView;
@property (readwrite, retain) NSTextField *startDateField;
@property (readwrite, retain) NSTextField *repeatEveryField;
@property (readwrite, retain) NSTextField *repeatEveryDescLabel;
@property (readwrite, retain) NSPopUpButton *repeatTypePopUpView;
@property (readwrite, retain) NSTextField *stopDateField;
@property (readwrite, retain) NSTextField *descriptionField;
@property (readwrite, retain) NSTextField *payeeField;
@property (readwrite, retain) NSTextField *checknoField;
@property (readwrite, retain) NSTextField *notesField;
@property (readwrite, retain) MGTableView *splitTableView;

- (id)initWithParent:(MGMainWindowController *)aParent;
- (PySchedulePanel *)model;
/* Actions */
- (void)addSplit;
- (void)deleteSplit;
/* Python --> Cocoa */
- (void)refreshRepeatEvery;
@end
