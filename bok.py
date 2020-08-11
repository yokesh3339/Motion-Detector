from a import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool,ColumnDataSource
df['st']=df['start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['ed']=df['end'].dt.strftime("%Y-%m-%d %H:%M:%S")
cds=ColumnDataSource(df)
output_file('time.html')
f=figure(x_axis_type='datetime',height=500,width=1000,title="graph")
f.yaxis.minor_tick_line_color=None
f.ygrid[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[('start','@st'),('end','@ed')])
f.add_tools(hover)

f.quad(left='start',right='end',top=1,bottom=0,color='green',source=cds)


show(f)