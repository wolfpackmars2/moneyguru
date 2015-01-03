/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "NSTableViewAdditions.h"
#import "HSTableView.h"

@class MGTableView;

@protocol MGTableViewDelegate <HSTableViewDelegate>
- (NSString *)autoCompletionForColumn:(NSTableColumn *)column partialWord:(NSString *)partialWord;
- (NSString *)currentValueForColumn:(NSTableColumn *)column;
- (NSString *)prevValueForColumn:(NSTableColumn *)column;
- (NSString *)nextValueForColumn:(NSTableColumn *)column;
- (NSString *)dataForCopyToPasteboard;
@end

@interface MGTableView : HSTableView {}
- (id <MGTableViewDelegate>)delegate;
- (void)setDelegate:(id <MGTableViewDelegate>)aDelegate;
- (void)copy:(id)sender;
@end

