import pandas as pd


class BeautyProductAPI:

    def load_data(self, filename):
        '''Load and store beauty products data'''
        self.data = pd.read_csv(filename)

    def get_options(self, column):
        '''filtering unique features'''
        values = self.data[column].unique().tolist()
        return ['All'] + sorted(values)

    def filter_data(self, brand='All', category='All', skin_type='All', gender='All'):
        '''Apply filters to dataset and return filtered dataframe'''
        df = self.data.copy()

        if brand != 'All':
            df = df[df['Brand'] == brand]
        if category != 'All':
            df = df[df['Category'] == category]
        if skin_type != 'All':
            df = df[df['Skin_Type'] == skin_type]
        if gender != 'All':
            df = df[df['Gender_Target'] == gender]

        return df

    def make_sankey(self, brand='All', category='All', skin_type='All', gender='All'):
        '''
        sankey flows:Gender to Skin Type to Category to Brand
        '''
        df = self.filter_data(brand, category, skin_type, gender)

        # Create flows for sankey
        flows = []

        #  Gender to Skin Type
        flow1 = df.groupby(['Gender_Target', 'Skin_Type']).size().reset_index(name='count')
        flow1.columns = ['source', 'target', 'count']
        flows.append(flow1)

        # Skin Type to Category
        flow2 = df.groupby(['Skin_Type', 'Category']).size().reset_index(name='count')
        flow2.columns = ['source', 'target', 'count']
        flows.append(flow2)

        # Category to Brand
        flow3 = df.groupby(['Category', 'Brand']).size().reset_index(name='count')
        flow3.columns = ['source', 'target', 'count']
        flows.append(flow3)

        # Combine all of them
        sankey_data = pd.concat(flows, ignore_index=True)

        return sankey_data
#bar charts
    def get_top_brands_by_rating(self, brand='All', category='All', skin_type='All', gender='All', top_n=10):
        '''top 10 brands by average rating'''
        df = self.filter_data(brand, category, skin_type, gender)
        top_brands = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False).head(top_n)
        return top_brands.reset_index()

    def get_avg_price_by_category(self, brand='All', category='All', skin_type='All', gender='All'):
        '''average price by category'''
        df = self.filter_data(brand, category, skin_type, gender)
        avg_price = df.groupby('Category')['Price_USD'].mean().sort_values(ascending=False)
        return avg_price.reset_index()