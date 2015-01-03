/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGImportBindingCell.h"

@implementation MGImportBindingCell
- (void)drawInteriorWithFrame:(NSRect)cellFrame inView:(NSView *)controlView
{
    if ([self intValue])
    {
        NSImage *i = [NSImage imageNamed:@"lock_12"];
        NSSize s = [i size];
        CGFloat w = s.width;
        CGFloat h = s.height;
        CGFloat fx = cellFrame.origin.x;
        CGFloat fy = cellFrame.origin.y;
        CGFloat fw = cellFrame.size.width;
        CGFloat fh = cellFrame.size.height;
        NSRect destRect = NSMakeRect(fx + (fw - w) / 2, fy + (fh - h) / 2, w, h);
        [i drawInRect:destRect
             fromRect:NSZeroRect
            operation:NSCompositeSourceOver
             fraction:1
       respectFlipped:YES
                hints:nil];
    }    
}
@end
