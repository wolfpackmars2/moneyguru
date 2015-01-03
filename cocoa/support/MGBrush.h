/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

@interface MGBrush : NSObject
{
    NSColor *color;
    NSGradient *gradient;
}
+ (id)brushWithColor:(NSColor *)aColor isGradient:(BOOL)aIsGradient;
+ (id)nullBrush;
- (id)initWithColor:(NSColor *)aColor isGradient:(BOOL)aIsGradient;
- (void)fill:(NSBezierPath *)aPath;
@property (readwrite, retain) NSColor *color;
@property (readwrite, retain) NSGradient *gradient; 
@end
