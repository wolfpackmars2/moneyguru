/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import "MGTransactionPrint.h"
#import "MGConst.h"

@implementation MGTransactionPrint
+ (Class)pyClass
{
    return [PyTransactionPrint class];
}

- (PyTransactionPrint *)py
{
    return (PyTransactionPrint *)py;
}

- (NSArray *)unresizableColumns
{
    return [NSArray arrayWithObjects:@"status",@"date",@"amount",nil];
}

- (NSArray *)accountColumnNames
{
    return [NSArray arrayWithObjects:@"from",@"to",nil];
}

- (NSInteger)splitCountThreshold
{
    return 3;
}
@end