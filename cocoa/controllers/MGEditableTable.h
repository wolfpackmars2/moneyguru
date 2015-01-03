/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGTableView.h"
#import "MGTable.h"
#import "MGFieldEditor.h"
#import "MGDateFieldEditor.h"

@interface MGEditableTable : MGTable
{
    MGFieldEditor *customFieldEditor;
    MGDateFieldEditor *customDateFieldEditor;
}
- (id)initWithModel:(PyTable *)aPy tableView:(NSTableView *)aTableView;
- (id)initWithPyRef:(PyObject *)aPyRef tableView:(NSTableView *)aTableView;
/* Virtual */
- (NSArray *)dateColumns;
- (NSArray *)completableColumns;
/* Public */
- (void)startEditing;
- (void)stopEditing;
- (NSString *)editedFieldname;
- (id)fieldEditorForObject:(id)asker;
@end
