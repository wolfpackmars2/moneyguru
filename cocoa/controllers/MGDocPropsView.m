/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGDocPropsView.h"
#import "MGDocPropsView_UI.h"
#import "Utils.h"

@implementation MGDocPropsView

@synthesize currencyComboBoxView;
@synthesize firstWeekdayPopUpView;
@synthesize aheadMonthsPopUpView;
@synthesize yearStartMonthPopUpView;

- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyDocPropsView *m = [[PyDocPropsView alloc] initWithModel:aPyRef];
    self = [super initWithModel:m];
    [m release];
    self.view = createMGDocPropsView_UI(self);
    currencyComboBox = [[HSComboBox alloc] initWithPyRef:[[self model] currencyList] view:currencyComboBoxView];
    firstWeekdayPopUp = [[HSPopUpList alloc] initWithPyRef:[[self model] firstWeekdayList] popupView:firstWeekdayPopUpView];
    aheadMonthsPopUp = [[HSPopUpList alloc] initWithPyRef:[[self model] aheadMonthsList] popupView:aheadMonthsPopUpView];
    yearStartMonthPopUp = [[HSPopUpList alloc] initWithPyRef:[[self model] yearStartMonthList] popupView:yearStartMonthPopUpView];
    return self;
}
        
- (void)dealloc
{
    [currencyComboBox release];
    [firstWeekdayPopUp release];
    [aheadMonthsPopUp release];
    [yearStartMonthPopUp release];
    [super dealloc];
}

- (PyDocPropsView *)model
{
    return (PyDocPropsView *)model;
}

- (NSString *)tabIconName
{
    return @"gledger_16";
}
@end