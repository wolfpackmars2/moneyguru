/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

// This used to subclass NSActionCell, and it worked alright, but since I've started tarketing
// 10.5, no action would be triggered on click. I had to subclass NSButtonCell
@interface MGImportBindingCell : NSButtonCell {}
@end