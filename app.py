import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # this package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req

# use the built in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# names the page
ui.page_opts(title="Alvaro's King Penguin data", fillable=True)

# creates sidebar for user interaction
with ui.sidebar(open="open"):
    
    ui.h2("Sidebar")
    
    # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],)

    # Creates a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 50)
    
    # Creates a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 200, 100)
    
    # Creates a checkbox group input
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,)

      # Adds a horizontal rule to the sidebar
    ui.hr()
    
    # Adds a hyperlink to GitHub Repo
    ui.a(
        "GitHub",
         href="https://github.com/alvaroquintero28/cintel-02-data/blob/main/app.py",
         target="_blank",
         )

# Creates a DataTable showing all data

with ui.layout_columns(col_widths=(5, 10)):        
    with ui.card():
        "DataTable"

    ui.h2("Penguins Table")

    @render.data_frame
    def render_penguins_table():
        return render. DataTable(filtered_data())

# Creates a DataGrid showing all data

with ui.layout_columns(col_widths=(5, 10)):        
    with ui.card():
        "DataGrid"

    ui.h2("Penguins DataGrid")


@render.data_frame
def penguins_data():
    return render. DataTable(filtered_data()) 

# Creates a Plotly Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Histogram")
    
    @render_plotly
    def plotly_histogram():
        return px.histogram(
            filtered_data(), x=input.selected_attribute(), nbins=input.plotly_bin_count()
        )

# Creates a Seaborn Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Seaborn Histogram")

    @render.plot(alt="Seaborn Histogram")
    def seaborn_histogram():
        histplot = sns.histplot(data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count())
        histplot.set_title("Palmer penguins")
        histplot.set_xlabel("Mass")
        histplot.set_ylabel("Count")
        return histplot

# Creates a Plotly Scatterplot showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(filtered_data(),
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=10,)

@reactive.calc
def filtered_data():
    return penguins_df
