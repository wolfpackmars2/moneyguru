/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

@interface MGPen : NSObject
{
    NSColor *color;
    CGFloat width;
}
+ (id)penWithColor:(NSColor *)aColor width:(CGFloat)aWidth;
+ (id)nullPen;
- (id)initWithColor:(NSColor *)aColor width:(CGFloat)aWidth;
- (void)stroke:(NSBezierPath *)aPath;
@property (readwrite, retain) NSColor *color;
@property (readwrite) CGFloat width;
@end
