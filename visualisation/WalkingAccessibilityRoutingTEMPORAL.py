import os
import pandas as pd
import geopandas as gpd
import pandana
import seaborn as sns
import networkx as nx
import osmnx as ox
import fiona
from shapely.geometry import mapping, Point, LineString, Polygon
ox.config(log_console=True, use_cache=True)
ox.__version__


#### FUNCTIONS #####

# FUNCTION 1: Add neareast nodeID as column
def nearestNodeID(df):
    df['x'] = df.geometry.x
    df['y'] = df.geometry.y
    df["node_id"] = network.get_node_ids(df['x'], df['y']).values

    return df

# FUNCTION 2: Get unique nodes
def getUniqueNodes (df):
    nodes_unique_population = df.groupby(['node_id']).first().reset_index()
    nodes_unique_population = nodes_unique_population["node_id"]

    return nodes_unique_population

#FUNCTION 3: Walk time calculator
def calculateWalkingTimes(df):
    speed = 3000
    for i in range(41):
        df["tt_"+str(speed)] = df["distance_17"] / speed * 60
        speed += 100
    return df

def calculateReachableStores(df):
    identifier = 3000
    resultDF = pd.DataFrame(columns=["speed", "count"])
    for i in range(41):
        under15 = df.loc[df["tt_"+str(identifier)]<=15]
        under15Count = under15.groupby(["id_nro"]).count().reset_index()
        resultDF.loc[len(resultDF.index)] = [identifier, under15Count["groceryID"].mean()]
        identifier += 100
    return resultDF

#### MAIN #####

os.chdir() #ADD PATH

#Read road network
nodes = pd.read_csv('Data\\nodes22.csv', index_col=0)
edges = pd.read_csv('Data\\edges22.csv', index_col=[0,1])

#Read population and POIs data
population_Grid_PkSeutu = gpd.read_file('Data\\rttk20_250m_shp\\HKI_Region2020_YKR_population_populatedOnly.shp')
metropAccessGrid_PkSeutu = gpd.read_file('Data\\MetropAccess_YKR_grid\\MetropAccess_YKR_grid_EurefFIN.shp')

population_PkSeutu_2020 = gpd.read_file('Data\\rttk20_250m_shp\\HKI_Region2020_YKR_population_populatedOnlyCENTROIDS.shp')
metropAccessCentroids_PkSeutu = gpd.read_file('Data\\MetropAccess_YKR_grid\\MetropAccess_YKR_grid_EurefFIN_Centroids.shp')

groceries_PKSeutu_2022_17 = gpd.read_file('Data\\Kaupat2022_5pm_WGS84.gpkg')
groceries_PKSeutu_2022_06 = gpd.read_file('Data\\Kaupat2022_6am_WGS84.gpkg')

walkingSpeedMeasurementsDRY = pd.read_csv('Data\\Walking_speed_measurements_EW_CH_Dry.csv', sep=";")
walkingSpeedMeasurementsWINTER= pd.read_csv('Data\\Walking_speed_measurements_EW_CH_Winter.csv', sep=";", encoding='latin-1')

serviceAreaStartPointVALLILA = gpd.read_file("Data\\ServiceAreaStartPointVALLILA_UTM35N.gpkg")

# Reproject population and grocery store data
population_grid_PkSeutu = population_Grid_PkSeutu.to_crs(epsg=4326)
population_PkSeutu_2020 = population_PkSeutu_2020.to_crs(epsg=4326)
metropAccessGrid_PkSeutu = metropAccessGrid_PkSeutu.to_crs(epsg=4326)
metropAccessCentroids_PkSeutu = metropAccessCentroids_PkSeutu.to_crs(epsg=4326)

groceries_PKSeutu_2022_17 = groceries_PKSeutu_2022_17.to_crs(epsg=4326)
groceries_PKSeutu_2022_06 = groceries_PKSeutu_2022_06.to_crs(epsg=4326)

################# PART 1 -  ROUTING  #######################

#Read walking network from OSM
'''
network = osm.pdna_network_from_bbox(60.0, 24.0, 60.5, 25.3, network_type='walk')  # Helsinki region
network.nodes_df.to_csv('nodes.csv')
network.edges_df.to_csv('edges.csv')
'''
#Remove unconnected edges
nodes = nodes.loc[nodes.index != 1503720022] #Unconnected node
nodes = nodes.loc[nodes.index != 1732975079] #Unconnected node
nodes = nodes.loc[nodes.index != 4210318680] #Unconnected node
nodes = nodes.loc[nodes.index != 4209636546] #Unconnected node
nodes = nodes.loc[nodes.index != 1366882580] #Unconnected node
nodes = nodes.loc[nodes.index != 1366882584] #Unconnected node
nodes = nodes.loc[nodes.index != 618337110] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893747] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893748] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893757] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893752] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893755] #Unconnected node
nodes = nodes.loc[nodes.index != 6138893750] #Unconnected node
nodes = nodes.loc[nodes.index != 4574848710] #Unconnected node
nodes = nodes.loc[nodes.index != 4574848712] #Unconnected node
nodes = nodes.loc[nodes.index != 3635805273] #Unconnected node
nodes = nodes.loc[nodes.index != 4574848479] #Unconnected node
nodes = nodes.loc[nodes.index != 4574848478] #Unconnected node
nodes = nodes.loc[nodes.index != 4574848480] #Unconnected node
nodes = nodes.loc[nodes.index != 3639506569] #Unconnected node
nodes = nodes.loc[nodes.index != 3639506573] #Unconnected node

edges = edges.loc[(edges["from"] != 1503720022) & (edges["to"] != 1732975079)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4210318680) & (edges["to"] != 4209636546)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 1366882580) & (edges["to"] != 1366882584)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 1366882584) & (edges["to"] != 1366882580)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 1366882580) & (edges["to"] != 618337110)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 618337110) & (edges["to"] != 1366882584)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 6138893755) & (edges["to"] != 6138893750)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 6138893752) & (edges["to"] != 6138893755)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 6138893757) & (edges["to"] != 6138893752)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 6138893757) & (edges["to"] != 6138893748)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 6138893748) & (edges["to"] != 6138893747)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 3639506573) & (edges["to"] != 4574848479)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4574848479) & (edges["to"] != 4574848478)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4574848478) & (edges["to"] != 4574848480)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 3639506569) & (edges["to"] != 4574848480)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4574848712) & (edges["to"] != 4574848478)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4574848712) & (edges["to"] != 3635805273)] #Connecting edge between unconnected nodes
edges = edges.loc[(edges["from"] != 4574848710) & (edges["to"] != 4574848712)] #Connecting edge between unconnected nodes

'''
# IF NEEDED Make Geodataframes both from edges and nodes using the x and y coordinate columns. Write as csv
nodes_gdf = gpd.GeoDataFrame(nodes, geometry=gpd.points_from_xy(nodes.x, nodes.y))
nodes_gdf.reset_index(inplace=True)
edges_gdf = edges.merge(nodes_gdf[["id", "geometry"]], how='left', left_on="from", right_on="id")
edges_gdf = edges_gdf.merge(nodes_gdf[["id", "geometry"]], how='left', left_on="to", right_on="id")
edges_gdf['geom'] =edges_gdf.apply(lambda row: LineString([row['geometry_x'], row['geometry_y']]), axis=1) #Create a linestring column
edges_gdf.drop(["id_x", "id_y", "geometry_x", "geometry_y"], 1, inplace=True)

outfp_nodes_gdf = "nodes_gdf.csv"
outfp_edges_gdf = "edges_gdf.csv"

nodes_gdf.to_csv(outfp_nodes_gdf, sep=";")
edges_gdf.to_csv(outfp_edges_gdf, sep=";")
'''
#Make the graph (network) file
network = pandana.Network(nodes['x'], nodes['y'], edges['from'], edges['to'], edges[['distance']])

#Search the nearest node id for every population centroid and grocery store
population_PkSeutu_2020 = nearestNodeID(population_PkSeutu_2020)
metropAccessCentroids_PkSeutu = nearestNodeID(metropAccessCentroids_PkSeutu)

groceries_PKSeutu_2022_17 = nearestNodeID(groceries_PKSeutu_2022_17)
groceries_PKSeutu_2022_06 = nearestNodeID(groceries_PKSeutu_2022_06)

# Create two new dataframes with unique population and grocery store node ids
nodes_unique_population2020 = getUniqueNodes(population_PkSeutu_2020)
nodes_unique_metropAccessCentroids = getUniqueNodes(metropAccessCentroids_PkSeutu)

nodes_unique_groceries_2022_17 = getUniqueNodes(groceries_PKSeutu_2022_17)
nodes_unique_groceries_2022_06 = getUniqueNodes(groceries_PKSeutu_2022_06)

'''
# Create a list of origin node ids and destination node ids
origsGrocery_2022_17 = [o for o in nodes_unique_population2020 for d in nodes_unique_groceries_2022_17]
destsGrocery_2022_17 = [d for o in nodes_unique_population2020 for d in nodes_unique_groceries_2022_17]

origsGrocery_2022_06 = [o for o in nodes_unique_population2020 for d in nodes_unique_groceries_2022_06]
destsGrocery_2022_06 = [d for o in nodes_unique_population2020 for d in nodes_unique_groceries_2022_06]
'''
# Create a list of origin node ids and destination node ids
origsGrocery_2022_17 = [o for o in nodes_unique_metropAccessCentroids for d in nodes_unique_groceries_2022_17]
destsGrocery_2022_17 = [d for o in nodes_unique_metropAccessCentroids for d in nodes_unique_groceries_2022_17]

origsGrocery_2022_06 = [o for o in nodes_unique_metropAccessCentroids for d in nodes_unique_groceries_2022_06]
destsGrocery_2022_06 = [d for o in nodes_unique_metropAccessCentroids for d in nodes_unique_groceries_2022_06]

# Find the shortest distance between all the population centroids and all different grocery locations. Make origin-destaination dataframe of the result
routesGrocery_2022_17 = network.shortest_path_lengths(origsGrocery_2022_17, destsGrocery_2022_17)
routesDF_Grocery_2022_17 = pd.DataFrame(list(zip(origsGrocery_2022_17, destsGrocery_2022_17, routesGrocery_2022_17)))
routesDF_Grocery_2022_17.rename(columns={0: "from_id", 1:"to_id", 2:"distance_17"},inplace=True)

routesGrocery_2022_06 = network.shortest_path_lengths(origsGrocery_2022_06, destsGrocery_2022_06)
routesDF_Grocery_2022_06 = pd.DataFrame(list(zip(origsGrocery_2022_06, destsGrocery_2022_06, routesGrocery_2022_06)))
routesDF_Grocery_2022_06.rename(columns={0: "from_id", 1:"to_id", 2:"distance_06"},inplace=True)

'''
# Join the population data, grocery and accessibility data  to the origin-destination dataframe. Filter and rename columns
routesDF_Grocery_2022_17_joined = population_PkSeutu_2020.merge(routesDF_Grocery_2022_17, how='outer', left_on="node_id", right_on="from_id")
routesDF_Grocery_2022_17_joined = routesDF_Grocery_2022_17_joined.merge(groceries_PKSeutu_2022_17, how='left', left_on="to_id", right_on="node_id")
routesDF_Grocery_2022_17_joined = routesDF_Grocery_2022_17_joined[["id_nro", "id",  'name', 'shop',"distance_17"]]
routesDF_Grocery_2022_17_joined.rename(columns={"id":"groceryID","name":"shopName", "shop":"shopType"}, inplace=True)

routesDF_Grocery_2022_06_joined = population_PkSeutu_2020.merge(routesDF_Grocery_2022_06, how='outer', left_on="node_id", right_on="from_id")
routesDF_Grocery_2022_06_joined = routesDF_Grocery_2022_06_joined.merge(groceries_PKSeutu_2022_06, how='left', left_on="to_id", right_on="node_id")
routesDF_Grocery_2022_06_joined = routesDF_Grocery_2022_06_joined[["id_nro", "id",  'name', 'shop',"distance_06"]]
routesDF_Grocery_2022_06_joined.rename(columns={"id":"groceryID","name":"shopName", "shop":"shopType"}, inplace=True)
'''

# Join the metropAccess data, grocery and accessibility data  to the origin-destination dataframe. Filter and rename columns
routesDF_Grocery_2022_17_joined = metropAccessCentroids_PkSeutu.merge(routesDF_Grocery_2022_17, how='outer', left_on="node_id", right_on="from_id")
routesDF_Grocery_2022_17_joined = routesDF_Grocery_2022_17_joined.merge(groceries_PKSeutu_2022_17, how='left', left_on="to_id", right_on="node_id")
routesDF_Grocery_2022_17_joined = routesDF_Grocery_2022_17_joined[["YKR_ID", "id",  'name', 'shop',"distance_17"]]
routesDF_Grocery_2022_17_joined.rename(columns={"id":"groceryID","name":"shopName", "shop":"shopType"}, inplace=True)

routesDF_Grocery_2022_06_joined = metropAccessCentroids_PkSeutu.merge(routesDF_Grocery_2022_06, how='outer', left_on="node_id", right_on="from_id")
routesDF_Grocery_2022_06_joined = routesDF_Grocery_2022_06_joined.merge(groceries_PKSeutu_2022_06, how='left', left_on="to_id", right_on="node_id")
routesDF_Grocery_2022_06_joined = routesDF_Grocery_2022_06_joined[["YKR_ID", "id",  'name', 'shop',"distance_06"]]
routesDF_Grocery_2022_06_joined.rename(columns={"id":"groceryID","name":"shopName", "shop":"shopType"}, inplace=True)

'''

#See if the results are correct
minDistPop_Grocery_17 = routesDF_Grocery_2022_17_joined.groupby(["id_nro"]).min().reset_index()
minDistPop_Grocery_06 = routesDF_Grocery_2022_06_joined.groupby(["id_nro"]).min().reset_index()
'''

#See if the results are correct
minDistPop_Grocery_17 = routesDF_Grocery_2022_17_joined.groupby(["YKR_ID"]).min().reset_index()
minDistPop_Grocery_06 = routesDF_Grocery_2022_06_joined.groupby(["YKR_ID"]).min().reset_index()

# See if there's outliers
outliers_Grocery_17 = routesDF_Grocery_2022_17_joined.loc[routesDF_Grocery_2022_17_joined["distance_17"] >100000]
outliers_Grocery_06 = routesDF_Grocery_2022_06_joined.loc[routesDF_Grocery_2022_06_joined["distance_06"] >100000]

'''
# Walking speed tests
walkingSpeedMeasurementsDRY["Speed (km/h)"].loc[walkingSpeedMeasurementsDRY["Age"]== "Adult"].median()
walkingSpeedMeasurementsDRY["Speed (km/h)"].loc[walkingSpeedMeasurementsDRY["Age"]== "Elderly"].median()
walkingSpeedMeasurementsWINTER["Speed (km/h)"].loc[walkingSpeedMeasurementsWINTER["Age"]== "Adult"].median()
walkingSpeedMeasurementsWINTER["Speed (km/h)"].loc[(walkingSpeedMeasurementsWINTER["Age"]== "Elderly") & (walkingSpeedMeasurementsWINTER["Condition"]== "Gritted ice")].median()

walkingSpeedMeasurementsWINTER["Speed (km/h)"].loc[(walkingSpeedMeasurementsWINTER["Age"]== "Elderly") & (walkingSpeedMeasurementsWINTER["Condition"]== "Gritted ice")].hist()

walkingSpeedMeasurementsDRY["Speed (km/h)"].loc[walkingSpeedMeasurementsDRY["Age"]== "Elderly"].hist()
walkingSpeedMeasurementsDRY["Speed (km/h)"].loc[walkingSpeedMeasurementsDRY["Age"]== "Adult"].hist()
'''

'''
#Join distances to population centroids
population_Grid_PkSeutu_17 = population_grid_PkSeutu.merge(minDistPop_Grocery_17[["id_nro", "distance_17"]], how='left', left_on="id_nro", right_on="id_nro")
population_Grid_PkSeutu_06 = population_grid_PkSeutu.merge(minDistPop_Grocery_06[["id_nro", "distance_06"]], how='left', left_on="id_nro", right_on="id_nro")

#Calculate travel times for certain walking speeds
population_Grid_PkSeutu_17["Adult_speed_dry"] = population_Grid_PkSeutu_17["distance_17"] / 5150 *60
population_Grid_PkSeutu_17["Old_speed_dry"] = population_Grid_PkSeutu_17["distance_17"] / 4260*60
population_Grid_PkSeutu_17["Adult_speed_winter"] = population_Grid_PkSeutu_17["distance_17"] / 4810*60
population_Grid_PkSeutu_17["Old_speed_winter"] = population_Grid_PkSeutu_17["distance_17"] / 3890*60

population_Grid_PkSeutu_06["Adult_speed_dry"] = population_Grid_PkSeutu_06["distance_06"] / 5150 *60
population_Grid_PkSeutu_06["Old_speed_dry"] = population_Grid_PkSeutu_06["distance_06"] / 4260*60
population_Grid_PkSeutu_06["Adult_speed_winter"] = population_Grid_PkSeutu_06["distance_06"] / 4810*60
population_Grid_PkSeutu_06["Old_speed_winter"] = population_Grid_PkSeutu_06["distance_06"] / 3890*60
'''

#Join distances to population centroids
metropAccessGrid_PkSeutu_17 = metropAccessGrid_PkSeutu.merge(minDistPop_Grocery_17[["YKR_ID", "distance_17"]], how='left', left_on="YKR_ID", right_on="YKR_ID")
metropAccessGrid_PkSeutu_06 = metropAccessGrid_PkSeutu.merge(minDistPop_Grocery_06[["YKR_ID", "distance_06"]], how='left', left_on="YKR_ID", right_on="YKR_ID")

#Calculate travel times for certain walking speeds
metropAccessGrid_PkSeutu_17["Adult_speed_dry"] = metropAccessGrid_PkSeutu_17["distance_17"] / 5150 *60
metropAccessGrid_PkSeutu_17["Old_speed_dry"] = metropAccessGrid_PkSeutu_17["distance_17"] / 4260*60
metropAccessGrid_PkSeutu_17["Adult_speed_winter"] = metropAccessGrid_PkSeutu_17["distance_17"] / 4810*60
metropAccessGrid_PkSeutu_17["Old_speed_winter"] = metropAccessGrid_PkSeutu_17["distance_17"] / 3890*60

metropAccessGrid_PkSeutu_06["Adult_speed_dry"] = metropAccessGrid_PkSeutu_06["distance_06"] / 5150 *60
metropAccessGrid_PkSeutu_06["Old_speed_dry"] = metropAccessGrid_PkSeutu_06["distance_06"] / 4260*60
metropAccessGrid_PkSeutu_06["Adult_speed_winter"] = metropAccessGrid_PkSeutu_06["distance_06"] / 4810*60
metropAccessGrid_PkSeutu_06["Old_speed_winter"] = metropAccessGrid_PkSeutu_06["distance_06"] / 3890*60

#Calculate travel times for  walking speeds ranging nfrom 3.0 to 7.0 at 0.1 interval
calculateWalkingTimes(routesDF_Grocery_2022_17_joined)
calculateWalkingTimes(routesDF_Grocery_2022_06_joined)

reachableUnder15_17 = calculateReachableStores(routesDF_Grocery_2022_17_joined)
reachableUnder15_06 = calculateReachableStores(routesDF_Grocery_2022_06_joined)

#Convert coordinate system back to original
'''
population_Grid_PkSeutu_17 = population_Grid_PkSeutu_17.to_crs(epsg=3067)
population_Grid_PkSeutu_06 = population_Grid_PkSeutu_06.to_crs(epsg=3067)
'''
metropAccessGrid_PkSeutu_17 = metropAccessGrid_PkSeutu_17.to_crs(epsg=3067)
metropAccessGrid_PkSeutu_06 = metropAccessGrid_PkSeutu_06.to_crs(epsg=3067)

# Write Oot
'''
population_Grid_PkSeutu_17.to_file("Data\\rttk2020_grocery_22_17.gpkg", driver="GPKG")
population_Grid_PkSeutu_06.to_file("Data\\rttk2020_grocery_22_06.gpkg", driver="GPKG")
'''
metropAccessGrid_PkSeutu_17.to_file("Data\\metropAccessGrid_grocery_22_17.gpkg", driver="GPKG")
metropAccessGrid_PkSeutu_06.to_file("Data\\metropAccessGrid_grocery_22_06.gpkg", driver="GPKG")


#### Service area analysis with osmnx and networkx ####
# From here
    place = 'Helsinki, Finland'
    network_type = 'all'
    trip_times =  [15] #in minutes
    travel_speed_Adult_20_summer = 4.50 #walking speed in km/hour
    travel_speed_Adult_40_summer = 4.97
    travel_speed_Adult_60_summer = 5.33
    travel_speed_Adult_80_summer = 5.85
    travel_speed_Old_20_winter = 3.43
    travel_speed_Old_40_winter = 4.00
    travel_speed_Old_60_winter =4.24
    travel_speed_Old_80_winter = 4.74

    # download the street network
    G = ox.graph_from_place(place, network_type=network_type)

    # find the centermost node and then project the graph to UTM
    gdf_nodes = ox.graph_to_gdfs(G, edges=False)
    x, y = gdf_nodes['geometry'].unary_union.centroid.xy
    startNode = ox.get_nearest_node(G, (serviceAreaStartPointVALLILA.iloc[0].geometry.y, serviceAreaStartPointVALLILA.iloc[0].geometry.x))
    G = ox.project_graph(G)

    # add an edge attribute for time in minutes required to traverse each edge
    meters_per_minute = travel_speed_Old_80_winter * 1000 / 60 #km per hour to m per minute
    for u, v, k, data in G.edges(data=True, keys=True):
        data['time'] = data['length'] / meters_per_minute

    def make_iso_polys(G, edge_buff=25, node_buff=50, infill=False):
        isochrone_polys = []
        for trip_time in sorted(trip_times, reverse=True):
            subgraph = nx.ego_graph(G, startNode, radius=trip_time, distance='time')

            node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
            nodes_gdf = gpd.GeoDataFrame({'id': subgraph.nodes()}, geometry=node_points)
            nodes_gdf = nodes_gdf.set_index('id')

            edge_lines = []
            for n_fr, n_to in subgraph.edges():
                f = nodes_gdf.loc[n_fr].geometry
                t = nodes_gdf.loc[n_to].geometry
                edge_lookup = G.get_edge_data(n_fr, n_to)[0].get('geometry', LineString([f, t]))
                edge_lines.append(edge_lookup)

            n = nodes_gdf.buffer(node_buff).geometry
            e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
            all_gs = list(n) + list(e)
            new_iso = gpd.GeoSeries(all_gs).unary_union

            # try to fill in surrounded areas so shapes will appear solid and blocks without white space inside them
            if infill:
                new_iso = Polygon(new_iso.exterior)
            isochrone_polys.append(new_iso)
        return isochrone_polys

    isochrone_polys = make_iso_polys(G, edge_buff=25, node_buff=0, infill=True)

    for polygon in isochrone_polys:
        gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:32635', geometry=[polygon])
        gdf.to_file("Data\\ServiceAreaVALLILA_"+str(travel_speed_Old_80_winter)+".gpkg", driver="GPKG")


#If need to create a geopackage of the graph
ox.io.save_graph_geopackage(G, filepath="Data\\OSMNX_graph.gpkg", encoding='utf-8', directed=False) 
