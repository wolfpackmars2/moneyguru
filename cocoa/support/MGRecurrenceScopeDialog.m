/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGRecurrenceScopeDialog.h"
#import "MGConst.h"
#import "MGRecurrenceScopeDialog_UI.h"

@implementation MGRecurrenceScopeDialog

@synthesize showDialogNextTime;

- (id)init
{
    self = [super initWithWindow:nil];
    self.showDialogNextTime = YES; // If we're showing this, it means that our pref is set to true
    [self setWindow:createMGRecurrenceScopeDialog_UI(self)];
    return self;
}

- (ScheduleScope)run
{
    ScheduleScope result = [NSApp runModalForWindow:[self window]];
    [[self window] close];
    return result;
}

- (void)cancel
{
    [NSApp stopModalWithCode:ScheduleScopeCancel];
}

- (void)chooseGlobalScope
{
    [NSApp stopModalWithCode:ScheduleScopeGlobal];
}

- (void)chooseLocalScope
{
    [NSApp stopModalWithCode:ScheduleScopeLocal];
}

@end