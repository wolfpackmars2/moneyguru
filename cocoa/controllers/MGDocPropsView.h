/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyDocPropsView.h"
#import "MGBaseView.h"
#import "HSPopUpList.h"
#import "HSComboBox.h"

@interface MGDocPropsView : MGBaseView
{
    NSComboBox *currencyComboBoxView;
    NSPopUpButton *firstWeekdayPopUpView;
    NSPopUpButton *aheadMonthsPopUpView;
    NSPopUpButton *yearStartMonthPopUpView;
    
    HSComboBox *currencyComboBox;
    HSPopUpList *firstWeekdayPopUp;
    HSPopUpList *aheadMonthsPopUp;
    HSPopUpList *yearStartMonthPopUp;
}

@property (readwrite, retain) NSComboBox *currencyComboBoxView;
@property (readwrite, retain) NSPopUpButton *firstWeekdayPopUpView;
@property (readwrite, retain) NSPopUpButton *aheadMonthsPopUpView;
@property (readwrite, retain) NSPopUpButton *yearStartMonthPopUpView;

- (id)initWithPyRef:(PyObject *)aPyRef;
- (PyDocPropsView *)model;
@end