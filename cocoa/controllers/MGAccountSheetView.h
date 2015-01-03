/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "PyAccountSheetView.h"
#import "MGBaseView.h"
#import "HSOutlineView.h"
#import "MGBalanceSheet.h"
#import "MGBalanceGraph.h"
#import "MGPieChartView.h"
#import "MGChart.h"

/* This base class is to share the pie/graph visibility logic between netwroth and profit views
*/
@interface MGAccountSheetView : MGBaseView <NSSplitViewDelegate>
{
    NSSplitView *mainSplitView;
    NSSplitView *subSplitView;
    HSOutlineView *outlineView;
    MGPieChartView *pieChartsView;
    
    /* Set this during initialization */
    NSView *graphView;
    MGChart *pieChart;
    MGChart *graph;
    
    BOOL graphCollapsed;
    BOOL pieCollapsed;
    CGFloat graphCollapseHeight;
    CGFloat pieCollapseWidth;
}

@property (readwrite, retain) NSSplitView *mainSplitView;
@property (readwrite, retain) NSSplitView *subSplitView;
@property (readwrite, retain) HSOutlineView *outlineView;
@property (readwrite, retain) MGPieChartView *pieChartsView;

- (id)initWithPyRef:(PyObject *)aPyRef;
- (PyAccountSheetView *)model;
@end