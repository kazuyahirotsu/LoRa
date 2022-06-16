from gps_class import GPSVis

# vis = GPSVis(data_path='data.csv',
#              map_path='map.png',  # Path to map downloaded from the OSM.
#              points=(35.71517, 139.75898, 35.71164, 139.76447)) # Two coordinates of the map (upper left, lower right)

vis = GPSVis(data_path='data.csv',
             map_path='map.png',  # Path to map downloaded from the OSM.
             points=(35.6514, 139.7720, 35.6413, 139.7856)) # Two coordinates of the map (upper left, lower right)

vis.create_image(color=(0, 0, 255), width=3)  # Set the color and the width of the GNSS tracks.
vis.plot_map(output='save')

print()
