/* 
Copyright 2015 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.gnu.org/licenses/gpl-3.0.html
*/

#import <Cocoa/Cocoa.h>
#import "MGChartView.h"

#define GRAPH_LINE_WIDTH 2.0
#define GRAPH_AXIS_OVERLAY_WIDTH 0.2
#define GRAPH_LABEL_FONT_SIZE 10.0
#define GRAPH_TITLE_FONT_SIZE 15.0

@interface MGGraphView : MGChartView 
{
    NSColor *axisColor;
    NSGradient *fillGradient;
    NSGradient *futureGradient;
}
@end

