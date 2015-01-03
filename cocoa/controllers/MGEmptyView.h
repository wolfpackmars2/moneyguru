/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyEmptyView.h"
#import "MGBaseView.h"
#import "HSSelectableList.h"

@interface MGEmptyView : MGBaseView
{
    NSTableView *pluginTableView;
    
    HSSelectableList *pluginList;
}

@property (readwrite, retain) NSTableView *pluginTableView;

- (id)initWithPyRef:(PyObject *)aPyRef;
- (PyEmptyView *)model;

/* Actions */
- (void)selectNetWorthView;
- (void)selectProfitView;
- (void)selectTransactionView;
- (void)selectScheduleView;
- (void)selectBudgetView;
- (void)selectGeneralLedgerView;
- (void)selectDocPropsView;
- (void)selectPluginView;
@end