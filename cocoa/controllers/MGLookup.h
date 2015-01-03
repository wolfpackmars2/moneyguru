/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyLookup.h"

@interface MGLookup : NSWindowController <NSTableViewDataSource, NSTableViewDelegate, NSTextFieldDelegate>
{
    NSSearchField *searchField;
    NSTableView *namesTable;
    
    PyLookup *model;
    NSArray *currentNames;
}

@property (readwrite, retain) NSSearchField *searchField;
@property (readwrite, retain) NSTableView *namesTable;

- (id)initWithPyRef:(PyObject *)aPyRef;

- (void)go;
- (void)updateQuery;
@end