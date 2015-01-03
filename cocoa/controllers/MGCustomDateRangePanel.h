/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGDocument.h"
#import "MGPanel.h"
#import "PyCustomDateRangePanel.h"

@class MGMainWindowController;

@interface MGCustomDateRangePanel : MGPanel <NSTextFieldDelegate> {
    NSTextField *startDateField;
    NSTextField *endDateField;
    NSPopUpButton *slotIndexSelector;
    NSTextField *slotNameField;
}

@property (readwrite, retain) NSTextField *startDateField;
@property (readwrite, retain) NSTextField *endDateField;
@property (readwrite, retain) NSPopUpButton *slotIndexSelector;
@property (readwrite, retain) NSTextField *slotNameField;

- (id)initWithParent:(MGMainWindowController *)aParent;
- (PyCustomDateRangePanel *)model;
@end