/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import <Python.h>
#import "PyImportTable.h"
#import "PyImportWindow.h"
#import "MGEditableTable.h"
#import "MGTableView.h"

@interface MGImportTable : MGEditableTable {}
- (id)initWithPyRef:(PyObject *)aPyRef view:(MGTableView *)aTableView;
- (void)initializeColumns;
- (PyImportTable *)model;

- (void)updateOneOrTwoSided;
- (void)bindLockClick:(id)sender;
@end