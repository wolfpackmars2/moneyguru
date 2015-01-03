/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGCSVLayoutNameDialog.h"
#import "MGCSVLayoutNameDialog_UI.h"
#import "MGConst.h"

@implementation MGCSVLayoutNameDialog

@synthesize nameTextField;

+ (NSString *)askForLayoutName
{
    return [MGCSVLayoutNameDialog askForLayoutNameBasedOnOldName:@""];
}

+ (NSString *)askForLayoutNameBasedOnOldName:(NSString *)oldName
{
    MGCSVLayoutNameDialog *dialog = [[MGCSVLayoutNameDialog alloc] initWithWindow:nil];
    [dialog setWindow:createMGCSVLayoutNameDialog_UI(dialog)];
    [dialog setLayoutName:oldName];
    NSString *result = [NSApp runModalForWindow:[dialog window]] == NSRunStoppedResponse ? [dialog layoutName] : nil;
    [[dialog window] close];
    [dialog release];
    return result;
}

- (void)ok
{
    [NSApp stopModal];
}

- (void)cancel
{
    [NSApp abortModal];
}

- (NSString *)layoutName
{
    return [nameTextField stringValue];
}

- (void)setLayoutName:(NSString *)name
{
    [nameTextField setStringValue:name];
}

@end