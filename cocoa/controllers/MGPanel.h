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
    BOOL releaseOnEndSheet;
}

/* The releaseOnEndSheet property makes the MGPanel release *itself* after a the sheet is done
   showing itself. It's a bit hackish, but the best way I found to properly release a panel
   in situations where its reference is not held anywhere in the UI layer.
 */
@property (readwrite) BOOL releaseOnEndSheet;

- (id)initWithModel:(PyPanel *)aModel parentWindow:(NSWindow *)aParentWindow;
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
