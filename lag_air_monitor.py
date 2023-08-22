import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Function to retrieve data from Astra
def get_data_from_astra():
    try:
        # Load secrets from token file
        with open("DCBDMS_LAG-token.json") as f:
            secrets = json.load(f)
        CLIENT_ID = secrets["clientId"]
        CLIENT_SECRET = secrets["secret"]
        
        # Load Cassandra secure connect bundle
        cloud_config = {'secure_connect_bundle': 'secure-connect-dcbdms-lag.zip'}
        auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()
        
        # Update keyspace and table name
        keyspace = 'dcbdms_keyspace'
        table_name = 'lagairdf'
        
        # Build and execute the query
        query = f"SELECT * FROM {keyspace}.{table_name}"
        rows = session.execute(query)
        
        # Convert rows to a list of dictionaries
        data = [row._asdict() for row in rows]
        
        # Convert list of dictionaries to a pandas DataFrame
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"Error retrieving data from Astra: {e}")
        return None
    finally:
        if 'session' in locals():
            session.shutdown()
        if 'cluster' in locals():
            cluster.shutdown()

# Attempt to get data from Astra
df = get_data_from_astra()

# If df is None, fallback activated
if df is None:
    print("Retrieving data from local host...")
    data_path = 'lagairdf.csv'
    df = pd.read_csv(data_path)
    df['startdate'] = pd.to_datetime(df['startdate'])
    df['enddate'] = pd.to_datetime(df['enddate'])


df = df.sort_values(by=['startdate'], ascending=False)

#df.head()


# GUI Creation
root = Tk()
root.title('LAGOS AIR QUALITY MONITORING SYSTEM')


# Updating Plot Function

def update_plot():
    selected_year = int(year_var.get())
    selected_attribute = attribute_var.get()
    selected_plot_type = plot_type_var.get()
    
    df_selected = df[df['startdate'].dt.year == selected_year]
    
    plt.clf()  
    
    if selected_plot_type == "Time Series":
        plt.plot(df_selected['startdate'], df_selected[selected_attribute], marker='o')
        plt.xlabel('Date')
        plt.ylabel(selected_attribute)
        plt.title(f'{selected_attribute} in {selected_year}')
        plt.xticks(rotation=45)
    
    elif selected_plot_type == "Scatter Plot":
        plt.scatter(df_selected[selected_attribute], df_selected['startdate'], marker='o', color='blue')
        plt.ylabel('Date')
        plt.xlabel(selected_attribute)
        plt.title(f'Scatter Plot of {selected_attribute} for {selected_year}')
    
    elif selected_plot_type == "Box Plot":
        df_selected.boxplot(column=selected_attribute)
        plt.title(f'Box Plot of {selected_attribute} for {selected_year}')
    
    plt.tight_layout()

    # Update Summary Statistics 
    stats_table = df_selected[selected_attribute].describe()
    stats_label.config(text=stats_table)

    plot_canvas.draw()  


# Year selection
year_label = Label(root, text='Select Year:')
year_label.pack()

year_var = StringVar()
year_var.set("2023")  

year_options = [str(year) for year in df['startdate'].dt.year.unique()]
year_menu = OptionMenu(root, year_var, *year_options)
year_menu.pack()

# Attribute selection
attribute_label = Label(root, text='Select Attribute:')
attribute_label.pack()

attribute_var = StringVar()
attribute_var.set(df.columns[2])  

attribute_options = list(df.columns[2:])
attribute_menu = OptionMenu(root, attribute_var, *attribute_options)
attribute_menu.pack()

# Plot type selection
plot_type_label = Label(root, text='Select Plot Type:')
plot_type_label.pack()

plot_type_var = StringVar()
plot_type_var.set("Time Series")  

plot_type_options = ["Time Series", "Scatter Plot", "Box Plot"]
plot_type_menu = OptionMenu(root, plot_type_var, *plot_type_options)
plot_type_menu.pack()


button_plot_frame = Frame(root)
button_plot_frame.pack(padx=10, pady=10)

plot_button = Button(button_plot_frame, text="Plot Data", command=update_plot, bg='green', fg='white', font=('Helvetica', 12, 'bold'))
plot_button.pack(side=LEFT, padx=10)

# Plot canvas
plot_canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 6)), master=root)
plot_canvas.get_tk_widget().pack(side=LEFT, padx=10, pady=10)


stats_label = Label(root, text='', font=('Helvetica', 12, 'bold'))
stats_label.pack(side=LEFT, padx=10, pady=10)

# Run the GUI
root.mainloop()