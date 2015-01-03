/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGTableView.h"
#import "NSEventAdditions.h"

@implementation MGTableView
- (id <MGTableViewDelegate>)delegate
{
    return (id <MGTableViewDelegate>)[super delegate];
}

- (void)setDelegate:(id <MGTableViewDelegate>)aDelegate
{
    [super setDelegate:aDelegate];
}

/* Actions */
- (void)copy:(id)sender
{
    NSString *data = [[self delegate] dataForCopyToPasteboard];
    NSPasteboard *p = [NSPasteboard generalPasteboard];
    [p declareTypes:[NSArray arrayWithObjects:NSStringPboardType, nil] owner:nil];
    [p setString:data forType:NSStringPboardType];
}
@end
