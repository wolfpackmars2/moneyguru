/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

@interface MGTextFieldCell : NSTextFieldCell {
    BOOL hasArrow;
    BOOL hasDarkBackground;
    NSInteger indent;
    id arrowTarget;
    SEL arrowAction;
    NSString *buttonImageName;
    id buttonTarget;
    SEL buttonAction;
}
- (void)setHasDarkBackground:(BOOL)value;
- (void)setIndent:(NSInteger)value;
- (void)setHasArrow:(BOOL)value;
- (void)setArrowTarget:(id)value;
- (void)setArrowAction:(SEL)value;
// the cell's button is a little image showing at the right of the cell (but at the left of the arrow)
// set it to nil to not show anything
- (void)setButtonImageName:(NSString *)aImageName;
- (void)setButtonTarget:(id)value;
- (void)setButtonAction:(SEL)value;
@end
