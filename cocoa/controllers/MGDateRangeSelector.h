/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "HSGUIController.h"
#import "PyDateRangeSelector.h"

@interface MGDateRangeSelector : HSGUIController <NSAnimationDelegate>
{
    NSPopUpButton *dateRangePopUp;
    NSSegmentedControl *segmentedControl;
    
    NSArray *customRangeItems;
}

@property (readwrite, retain) NSPopUpButton *dateRangePopUp;
@property (readwrite, retain) NSSegmentedControl *segmentedControl;

- (id)initWithPyRef:(PyObject *)aPyRef;

/* Virtual */
- (PyDateRangeSelector *)model;

/* Public */
- (void)animate:(BOOL)forward;

/* Actions */
- (void)segmentClicked;
- (void)selectSavedCustomRange:(id)sender;
@end