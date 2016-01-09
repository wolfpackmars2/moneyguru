/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGDocumentController.h"
#import "MGDocument.h"
#import "MGMainWindowController.h"

@implementation MGDocumentController
- (void)openDocumentWithContentsOfURL:(NSURL *)url
                              display:(BOOL)displayDocument
                    completionHandler:(void (^)(NSDocument *document,
                                                BOOL documentWasAlreadyOpen,
                                                NSError *error))completionHandler
{
    /* What we want to do here is to add special handling for importable documents. In Info.plist,
       all importable documents are listed so that it's possible to import them by double-clicking.
       However, we don't want to create a new document, we want to take the current document and tell
       it to import the URL. In Info.plist, we added importable documents with a NSDocumentClass
       attribute that doesn't exist (MGImport), so the way to recognize them is to check if
       typeForContentsOfURL:error: is not nil, and then if documentClassForType: is nil.
    */
    NSString *urlType = [self typeForContentsOfURL:url error:nil];
    if ((urlType != nil) && ([self documentClassForType:urlType] == nil)) {
        MGDocument *doc = (MGDocument *)[self currentDocument];
        if (doc == nil) {
            if ([[self documents] count] > 0) {
                doc = [[self documents] objectAtIndex:0];
            }
        }
        if (doc != nil) {
            MGMainWindowController *mw = [[doc windowControllers] objectAtIndex:0];
            [[mw model] import:[url path]];
        }
        else {
            // We opened moneyGuru by dragging an importable file into it. This doesn't make much
            // sense, so we ignore thath file. However, if we don't call completionHandler, we
            // end up in a state where we can't drag anything into the application, so that is why
            // we have that line below.
            completionHandler(nil, NO, nil);
        }
    }
    else {
        [super openDocumentWithContentsOfURL:url
                                     display:displayDocument
                           completionHandler:completionHandler];
    }
}

- (void)openFirstDocument
{
    /* Try opening the most recently opened document if possible, or open a new document.
    */
    if ([[self documents] count] > 0) {
        return;
    }
    NSArray *recentURLs = [self recentDocumentURLs];
    if ([recentURLs count] > 0) {
        NSError *error;
        NSURL *url = [recentURLs objectAtIndex:0];
        [self openDocumentWithContentsOfURL:url
                                    display:YES
                          completionHandler:^(NSDocument *document,
                                              BOOL documentWasAlreadyOpen,
                                              NSError *error)
                                            {}];
    }
    else {
        NSError *error;
        [self openUntitledDocumentAndDisplay:YES error:&error];
    }
}
@end