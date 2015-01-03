/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

@interface MGCSVLayoutNameDialog : NSWindowController
{
    NSTextField *nameTextField;
}

@property (readwrite, retain) NSTextField *nameTextField;

+ (NSString *)askForLayoutName;
+ (NSString *)askForLayoutNameBasedOnOldName:(NSString *)oldName;

- (void)ok;
- (void)cancel;

- (NSString *)layoutName;
- (void)setLayoutName:(NSString *)name;
@end