/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGAccountSheetView.h"
#import "HSOutlineView.h"
#import "MGBalanceSheet.h"
#import "MGBalanceGraph.h"

@interface MGNetWorthView : MGAccountSheetView
{
    MGBalanceSheet *balanceSheet;
}
/* Public */
- (BOOL)canShowSelectedAccount;
- (void)toggleExcluded;
@end