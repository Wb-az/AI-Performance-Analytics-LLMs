import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


__all__ = ['pie_chart', 'stacked_chart', 'horizontal_stacked', 'grouped_bar_chart',
           'plotly_pareto', 'diverging_plot', 'facet_plots', 'simple_bar']

def pie_chart(data, names='Category', values='count', color='Category', title="",
              fig_name=None,  **kwargs):

    fig = px.pie(data, values=values, names=names, color=color, color_discrete_map=kwargs['colors'],
                    title=title, template=kwargs['template'])
    fig.update_traces(textposition='inside', textinfo=kwargs['textinfo'], # textinfo='percent+label+value'
                         # textinfo='percent+label',
                      showlegend=kwargs['show_legend'])
    fig.update_layout(title_x=0.5, width=kwargs['width'], height=kwargs['height'],
                      font=dict(size=12, family='PT Sans'),
                      legend=dict(orientation="h", yanchor='top', title_text=""))
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")
    return fig.show()


def stacked_chart(data, x=None, y=None, y_title=None, fig_name=None, **kwargs):
    fig = px.bar(data, x=x, y=y, color=kwargs['color'], text_auto=True, color_discrete_sequence=kwargs['colors'],
                 width=kwargs['width'], height=kwargs['height'])
    fig.update_traces(textposition='inside', texttemplate=kwargs['texttemplate'], width=0.8)
    fig.update_layout(showlegend=True, template=kwargs['template'], barmode='stack', xaxis_tickangle=-45,
                      font=dict(size=12, family='PT Sans'), margin=dict(b=40,t=40,l=80,r=50),
                      legend=dict(orientation="h", yanchor='top', y=20, title_text="" ))
    fig.update_yaxes(showgrid=True, title=y_title)
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")
    return fig.show()


def horizontal_stacked(data, x=None, y=None, color=None, text=None, x_title=None, y_title=None,
                       fig_name=None, **kwargs):

    fig = px.bar(data, x=x, y=y, color=color, orientation='h', text=text, color_discrete_map=kwargs['colors'],
                 width=kwargs['width'], height=kwargs['height']
                 )
    fig.update_traces(textposition='inside', texttemplate=kwargs['texttemplate'],
                      showlegend=kwargs['show_legend'], width=kwargs['col_width'])
    fig.update_layout(template=kwargs['template'], barmode='stack',
                     font=dict(size=12, family='PT Sans'),
                      legend=dict(orientation="h", yanchor='top', y=20, title_text=""))

    fig.update_xaxes(showgrid=True, title=x_title)
    fig.update_yaxes(showgrid=False, title=y_title)
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")

    return fig.show()


def grouped_bar_chart(data, x, y, color, text, title="", fig_name=None, **kwargs):
    fig = px.bar(data, x=x, y=y, color=color, text=text, color_discrete_sequence=kwargs['colors'],
                 title=title, template=kwargs['template'], height=kwargs['height'], width=kwargs['width'])
    fig.update_traces(textposition='inside', texttemplate=kwargs['texttemplate'])
    fig.update_layout(barmode='group', xaxis_tickangle=-45, font=dict(size=12, family='PT Sans'),
                       margin=dict(b=40,t=40,l=80,r=50),
                      legend=dict(orientation="h", yanchor='top', y=20, title_text="" ))
    fig.update_yaxes(showgrid=True)
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")
    return fig.show()


def graph_pareto(dataframe, col_01, col_02, col_03, path, fig_name=None):
    df = dataframe.copy()

    data = [
        go.Bar(
          name = "col_01",
          x= df[col_01],
          y= df[col_02],
          marker= {"color": list(np.repeat('rgb(71, 71, 135)', 5)
                                 ) + list(np.repeat('rgb(112, 111, 211)', len(df.index) - 5))}),
        go.Scatter(
          line= {
            "color": "rgb(192, 57, 43)",
            "width": 3
          },
          name= col_02, #percent
          x=  df[col_01],
          y= df[col_03],
          yaxis= "y2",
          mode='lines+markers'
        ),
    ]

    layout = {
      "title": {
        'text': f"{col_01} Pareto",
        'font': dict(size=20)
      },
      # Font
      "font": {
        "size": 14,
        "color": "rgb(44, 44, 84)",
        "family": "PT Sans"
      },

      # Graph Box
      "margin": {
        "b": 20,
        "l": 50,
        "r": 50,
        "t": 10,
      },
      "height": 400,

      # Graph Box

      "plot_bgcolor": "rgb(255, 255, 255)",


      # Settings Legend
      "legend": {
        "x": 0.79,
        "y": 1.2,
        "font": {
          "size": 12,
          "color": "rgb(44, 44, 84)",
          "family": "PT Sans"
        },
        'orientation': 'h',
      },

      # Yaxis 1 position left

      "yaxis": {
        "title": f"Count {col_01}",
        "titlefont": {
        "size": 16,
        "color": "rgb(71, 71, 135)",
        "family": "PT Sans",
       },
           "anchor":"x",
        # overlaying='y',
        "side":'left',
        "position":0
      },


      # Yaxis 2 position right
      "yaxis2": {
        "side": "right",
        # "range": [0, 100],
        "title": f"Percentage {col_01}",
        "titlefont": {
          "size": 16,
          "color": "rgb(71, 71, 135)",
          "family": "PT Sans",
        },
        "overlaying": "y",


        "ticksuffix": " %",
      },

    }

    fig = go.Figure(data=data, layout=layout)
    fig.write_image(f"{path}/{fig_name}.svg", format="svg")

    return fig.show()


def plotly_pareto(data, title="", x="", y1="", y2="", y1_title='Frequency',
                       y2_title='Cumulative percentage (%)', x_axis='Preference',
                       fig_name=None, **kwargs):

    # Create subplot with secondary axis
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Create bar plot and update traces
    bar = px.bar(data, x=x, y=y1, color_discrete_sequence=['#088F8F'])
    bar.update_traces(showlegend=False, width=0.6)

    # Create the line plot and change the axis for line trace
    line = px.line(data , x=x, y=y2, markers=True)
    line.update_traces(yaxis="y2", line_color='red')

    #Add the figures to the subplot figure
    subplot_fig.add_traces(bar.data + line.data)

    # Update subplot
    subplot_fig.update_layout(title=title, yaxis=dict(title=y1_title),
                              yaxis2=dict(title=y2_title), xaxis=dict(title=x_axis))
    subplot_fig.update_layout(margin=dict(b=40,t=40,l=80,r=80), title_x=0.5,
                              width=kwargs['width'], height=kwargs['height'], xaxis_tickangle=-45,
                              font=dict(size=10, family='PT Sans'), template=kwargs['template'])
    subplot_fig.update_yaxes(showgrid=True, secondary_y=True)

    subplot_fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")

    return subplot_fig.show()


def diverging_plot(data, left, right, center, fig_name=None, **kwargs):

    # Creating a figure
    fig = go.Figure()

    # Add left side rating - GPT
    for col in left:
        fig.add_trace(go.Bar(x=-data[col].values,
                                   y=data.index,
                                   orientation='h',
                                   name=col,
                                   hovertemplate="%{y}: %{x}",marker_color=kwargs['colors'][col]))

    # Add neutral rating
    fig.add_trace(go.Bar(x=data[center], y=data.index, orientation='h', name=center,
                         hovertemplate="%{y}: %{x}",
                         marker_color=kwargs['colors'][center]))

    # Add right side rating - GPT
    for col in right:

        fig.add_trace(go.Bar(x=data[col], y=data.index, orientation='h',
                             name=col, hovertemplate="%{y}: %{x}",
                             marker_color=kwargs['colors'][col]))

    # Update the plot layout
    fig.update_layout(barmode='relative', template=kwargs['template'],
                      margin=dict(l=20, r=20, t=20, b=20), height=kwargs['height'],
                      width=kwargs['width'], font=dict(size=12, family='PT Sans'),
                      yaxis_autorange='reversed', bargap=0.5,
                      legend=dict(orientation="h", yanchor='top', y=20))

    fig.update_xaxes(showgrid=True)
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")

    return fig.show()


def facet_plots(data, x, y, color, facet_col, facet_wrap, text, fig_name=None, **kwargs):

    fig = px.bar(data, x=x, y=y, color=color, text=text, facet_col=facet_col, facet_col_wrap=facet_wrap,
    color_discrete_map=kwargs['colors'])
    fig.update_traces(textposition='inside', texttemplate=kwargs['texttemplate'])
    fig.update_layout(template=kwargs['template'], barmode='relative', width=kwargs['width'],
                      height=kwargs['height'], margin=dict(r=20, l=40),
                      font=dict(size=12, family='PT Sans'),
                      legend=dict(orientation="h", title_text=kwargs["legend_text"], yanchor="top",
                                  y=1.1),
                      xaxis_title=kwargs['xtitle'], xaxis2_title=kwargs['xtitle'],)
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")
    fig.update_xaxes(showgrid=True)

    return fig.show()


def simple_bar(data, x, y, title, fig_name,  **kwargs):
    fig = px.bar(data, x=x, y=y, color_discrete_sequence=kwargs['colors'], title=title)
    fig.update_layout(template="simple_white", height=kwargs['height'], width=kwargs['width'], 
                      margin=dict(b=50,t=50,l=80,r=50), xaxis_tickangle=-90, font=dict(size=12),
                      font_family='PT Sans')
    fig.update_yaxes(showgrid=kwargs['grid'])
    fig.write_image(f"{kwargs['path']}/{fig_name}.svg", format="svg")
    return fig.show()












