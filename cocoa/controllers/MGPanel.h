/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGDateFieldEditor.h"
#import "MGFieldEditor.h"
#import "PyPanel.h"

@interface MGPanel : NSWindowController <NSWindowDelegate> {
    PyPanel *model;
    NSWindow *parentWindow;
    MGFieldEditor *customFieldEditor;
    MGDateFieldEditor *customDateFieldEditor;
}
- (id)initWithNibName:(NSString *)aNibName model:(PyPanel *)aModel parent:(NSWindowController *)aParent;
- (id)initWithModel:(PyPanel *)aModel parent:(NSWindowController *)aParent;
- (PyPanel *)model;
/* Virtual */
- (NSString *)completionAttrForField:(id)aField;
- (BOOL)isFieldDateField:(id)aField;
- (NSResponder *)firstField;
- (void)loadFields;
- (void)saveFields;
/* Public */
- (void)save;
/* Actions */
- (void)cancel:(id)sender;
- (void)save:(id)sender;
@end
