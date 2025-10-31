import panel as pn
import hvplot.pandas
import sankey as sk
from makeupapi import BeautyProductAPI


pn.extension()
api = BeautyProductAPI()
api.load_data('data/most_used_beauty_cosmetics_products_extended.csv')

# filtering
brand = pn.widgets.Select(name='Brand', options=api.get_options('Brand'))
category = pn.widgets.Select(name='Category', options=api.get_options('Category'))
skin_type = pn.widgets.Select(name='Skin Type', options=api.get_options('Skin_Type'))
gender = pn.widgets.Select(name='Gender', options=api.get_options('Gender_Target'))


width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)

# CALLBACK FUNCTIONS

def get_catalog(brand, category, skin_type, gender):
    """Display sankey"""
    local = api.make_sankey(brand, category, skin_type, gender)
    return pn.widgets.Tabulator(local, selectable=False)

def get_sankey(brand, category, skin_type, gender, width, height):
    """Sankey diagram w/ Gender to Skin Type to Category to Brand"""
    local = api.make_sankey(brand, category, skin_type, gender)
    return sk.make_sankey(local, "source", "target", vals="count", width=width, height=height)

def get_scatter(brand, category, skin_type, gender):
    """Generate scatter plot of Price vs Rating"""
    df = api.filter_data(brand, category, skin_type, gender)
    return df.hvplot.scatter(
        x='Price_USD', y='Rating',
        hover_cols=['Product_Name', 'Brand', 'Category'],
        title=f'Price vs Rating ({len(df)} products)',
        width=800, height=500
    )

def get_top_brands(brand, category, skin_type, gender):
    """ bar plot of top 10 brands by rating"""
    df = api.get_top_brands_by_rating(brand, category, skin_type, gender, top_n=10)
    return df.hvplot.barh(
        x='Brand', y='Rating',
        title='Top 10 Brands by Average Rating',
        width=800, height=500,
        color='#ffd1dc'
    )

def get_price_by_category(brand, category, skin_type, gender):
    """bar chart of average price by category"""
    df = api.get_avg_price_by_category(brand, category, skin_type, gender)
    return df.hvplot.bar(
        x='Category', y='Price_USD',
        title='Average Price by Category',
        width=800, height=500,
        rot=45,
        color='#ffd1dc'
    )

# Connect widgets to functions
catalog = pn.bind(get_catalog, brand, category, skin_type, gender)
sankey = pn.bind(get_sankey, brand, category, skin_type, gender, width, height)
scatter = pn.bind(get_scatter, brand, category, skin_type, gender)
top_brands = pn.bind(get_top_brands, brand, category, skin_type, gender)
price_category = pn.bind(get_price_by_category, brand, category, skin_type, gender)

card_width = 320

# Create sidebar cards
filter_card = pn.Card(
    pn.Column(brand, category, skin_type, gender),
    title="Filters",
    width=card_width,
    collapsed=False
)

plot_settings_card = pn.Card( pn.Column(width, height),title="Plot Settings",width=card_width, collapsed=True
)

# Create dashboard layout
layout = pn.template.FastListTemplate(
    title="Beauty Products Dashboard",
    sidebar=[filter_card, plot_settings_card],
    main=[
        pn.Tabs(
            ("Data", catalog),
            ("Sankey", sankey),
            ("Scatter Plot", scatter),
            ("Top Brands", top_brands),
            ("Price by Category", price_category),
            active=1  # Start on sankey tab
        )
    ],
    header_background='#ffd1dc'
).servable()

layout.show()