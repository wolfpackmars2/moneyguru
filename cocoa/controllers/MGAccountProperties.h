/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGPanel.h"
#import "HSPopUpList.h"
#import "HSComboBox.h"
#import "PyAccountPanel.h"

@class MGMainWindowController;

@interface MGAccountProperties : MGPanel {
    NSTextField *nameTextField;
    NSPopUpButton *typeSelector;
    NSComboBox *currencySelector;
    NSTextField *accountNumberTextField;
    NSTextField *notesTextField;
    
    HSPopUpList *typePopUp;
    HSComboBox *currencyComboBox;
}

@property (readwrite, retain) NSTextField *nameTextField;
@property (readwrite, retain) NSPopUpButton *typeSelector;
@property (readwrite, retain) NSComboBox *currencySelector;
@property (readwrite, retain) NSTextField *accountNumberTextField;
@property (readwrite, retain) NSTextField *notesTextField;

- (id)initWithParent:(MGMainWindowController *)aParent;
- (PyAccountPanel *)model;
@end