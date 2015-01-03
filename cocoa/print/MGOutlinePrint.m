/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGOutlinePrint.h"

@implementation MGOutlinePrint
- (id)objectValueForTableColumn:(NSTableColumn *)aColumn row:(NSInteger)aRow
{
    NSOutlineView *o = (NSOutlineView *)tableView;
    id d = [o delegate];
    id item = [o itemAtRow:aRow];
    return [d outlineView:o objectValueForTableColumn:aColumn byItem:item];
}

- (void)willDisplayCell:(NSCell *)aCell forTableColumn:(NSTableColumn *)aColumn row:(NSInteger)aRow
{
    NSOutlineView *o = (NSOutlineView *)tableView;
    id d = [o delegate];
    id item = [o itemAtRow:aRow];
    [d outlineView:o willDisplayCell:aCell forTableColumn:aColumn item:item];
}

- (CGFloat)indentForTableColumn:(NSTableColumn *)aColumn row:(NSInteger)aRow
{
    NSOutlineView *o = (NSOutlineView *)tableView;
    if ([[o tableColumns] indexOfObject:aColumn] == 0)
    {
        NSInteger level = [o levelForRow:aRow];
        return level * [o indentationPerLevel];
    }
    else
        return 0;
}

@end