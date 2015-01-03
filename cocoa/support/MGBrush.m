/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGBrush.h"

@implementation MGBrush
@synthesize color;
@synthesize gradient;

+ (id)brushWithColor:(NSColor *)aColor isGradient:(BOOL)aIsGradient
{
    return [[[MGBrush alloc] initWithColor:aColor isGradient:aIsGradient] autorelease];
}

+ (id)nullBrush
{
    return [MGBrush brushWithColor:nil isGradient:NO];
}

- (id)initWithColor:(NSColor *)aColor isGradient:(BOOL)aIsGradient
{
    self = [super init];
    self.color = aColor;
    if (aIsGradient) {
        NSColor *light = [aColor blendedColorWithFraction:0.5 ofColor:[NSColor whiteColor]];
        self.gradient = [[[NSGradient alloc] initWithStartingColor:aColor endingColor:light] autorelease];
    }
    else {
        self.gradient = nil;
    }
    return self;
}

- (void)fill:(NSBezierPath *)aPath
{
    if (self.color == nil) {
        return;
    }
    if (self.gradient != nil) {
        [NSGraphicsContext saveGraphicsState];
        [aPath addClip];
        [self.gradient drawInRect:[aPath bounds] angle:90];
        [NSGraphicsContext restoreGraphicsState];        
    }
    else {
        [self.color setFill];
        [aPath fill];
    }
}
@end
