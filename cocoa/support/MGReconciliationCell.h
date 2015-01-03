/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>

@interface MGReconciliationCell : NSButtonCell 
{
    BOOL canReconcile;
    BOOL recurrent;
    BOOL isBudget;
    BOOL isInFuture;
    BOOL isInPast;
}

- (void)setCanReconcile:(BOOL)aCanReconcile;
- (void)setReconciled:(BOOL)aReconciled;
- (void)setRecurrent:(BOOL)aRecurrent;
- (void)setIsBudget:(BOOL)aIsBudget;
- (void)setIsInFuture:(BOOL)aIsInFuture;
- (void)setIsInPast:(BOOL)aIsInPast;
@end