/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyCSVImportOptions.h"

@interface MGCSVImportOptions : NSWindowController <NSTableViewDelegate, NSTableViewDataSource>
{
    NSTableView *csvDataTable;
    NSMenu *columnMenu;
    NSPopUpButton *layoutSelector;
    NSPopUpButton *encodingSelector;
    NSPopUpButton *targetSelector;
    NSTextField *delimiterTextField;
    
    NSInteger lastClickedColumnIndex;
    PyCSVImportOptions *model;
}

@property (readwrite, retain) NSTableView *csvDataTable;
@property (readwrite, retain) NSMenu *columnMenu;
@property (readwrite, retain) NSPopUpButton *layoutSelector;
@property (readwrite, retain) NSPopUpButton *encodingSelector;
@property (readwrite, retain) NSPopUpButton *targetSelector;
@property (readwrite, retain) NSTextField *delimiterTextField;

- (id)initWithPyRef:(PyObject *)aPyRef;

/* Actions */
- (void)cancel;
- (void)continueImport;
- (void)deleteSelectedLayout;
- (void)newLayout;
- (void)renameSelectedLayout;
- (void)rescan;
- (void)selectLayout:(id)sender;
- (void)selectTarget;
- (void)setColumnField:(id)sender;
- (void)toggleLineExclusion;

/* Public */
- (BOOL)canDeleteLayout;
@end