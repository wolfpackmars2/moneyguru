/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "HSOutline.h"
#import "PyReport.h"
#import "HSColumns.h"

@interface MGReport : HSOutline {
    HSColumns *columns;
    BOOL toggleExcludedIsEnabled;
}
- (id)initWithPyRef:(PyObject *)aPyRef view:(HSOutlineView *)aOutlineView;
- (PyReport *)model;

- (void)showSelectedAccount;
- (void)toggleExcluded;
- (BOOL)canShowSelectedAccount;
- (HSColumns *)columns;
@end
