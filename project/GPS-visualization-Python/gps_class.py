import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


class GPSVis(object):
    """
        Class for GPS data visualization using pre-downloaded OSM map in image format.
    """
    def __init__(self, data_path, map_path, points):
        """
        :param data_path: Path to file containing GPS records.
        :param map_path: Path to pre-downloaded OSM map in image format.
        :param points: Upper-left, and lower-right GPS points of the map (lat1, lon1, lat2, lon2).
        """
        self.data_path = data_path
        self.points = points
        self.map_path = map_path

        self.result_image = Image
        self.x_ticks = []
        self.y_ticks = []
        self.x = []
        self.y = []
        self.z = []

    def plot_map(self, output='save', save_as='resultMap.png'):
        """
        Method for plotting the map. You can choose to save it in file or to plot it.
        :param output: Type 'plot' to show the map or 'save' to save it.
        :param save_as: Name and type of the resulting image.
        :return:
        """
        self.get_ticks()
        cm = plt.cm.get_cmap('PiYG')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        mappable = ax.scatter(self.x, self.y, c=self.z, s=10, cmap=cm)
        fig.colorbar(mappable, ax=ax)
        ax.imshow(self.result_image)
        ax.plot(218, 28, color="red", marker='*', markersize=10) 
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(width=0)
        # ax.set_title("RSSI value of the signal from the star mark")
        # ax.set_xticklabels(self.x_ticks)
        # ax.set_yticklabels(self.y_ticks)

        # self.get_ticks()
        # fig, axis1 = plt.subplots(figsize=(10, 10))
        # axis1.imshow(self.result_image)
        # axis1.set_xlabel('Longitude')
        # axis1.set_ylabel('Latitude')
        # axis1.set_xticklabels(self.x_ticks)
        # axis1.set_yticklabels(self.y_ticks)
        # axis1.grid()
        if output == 'save':
            plt.savefig(save_as)
        else:
            plt.show()

    def create_image(self, color, width=2):
        """
        Create the image that contains the original map and the GPS records.
        :param color: Color of the GPS records.
        :param width: Width of the drawn GPS records.
        :return:
        """
        data = pd.read_csv(self.data_path, names=['RSSI','LATITUDE', 'LONGITUDE'], sep=',')

        self.result_image = Image.open(self.map_path, 'r')
        img_points = []
        gps_data = tuple(zip(data['LATITUDE'].values, data['LONGITUDE'].values))
        gps_rssi_data = tuple(zip(data['RSSI'].values, data['LATITUDE'].values, data['LONGITUDE'].values))
        for i in range(len(gps_data)):
            x1, y1 = self.scale_to_img(gps_data[i], (self.result_image.size[0], self.result_image.size[1]))
        #    img_points.append((x1, y1))
            img_points.append([x1,y1,gps_rssi_data[i][0]])

        #draw = ImageDraw.Draw(self.result_image)
        # draw.line(img_points, fill=color, width=width)
        for i in range(len(img_points)):
            # rgb=self.rgb(90,130,-1*img_points[i][2])
            #rgb=self.rgb(min([-1*j[2] for j in img_points]),max([-1*j[2] for j in img_points]),-1*img_points[i][2])
            self.x.append(img_points[i][0])
            self.y.append(img_points[i][1])
            self.z.append(img_points[i][2])
            #draw.ellipse(img_points[i][:2], fill=rgb, width=1)

    def scale_to_img(self, lat_lon, h_w):
        """
        Conversion from latitude and longitude to the image pixels.
        It is used for drawing the GPS records on the map image.
        :param lat_lon: GPS record to draw (lat1, lon1).
        :param h_w: Size of the map image (w, h).
        :return: Tuple containing x and y coordinates to draw on map image.
        """
        # https://gamedev.stackexchange.com/questions/33441/how-to-convert-a-number-from-one-min-max-set-to-another-min-max-set/33445
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        old = (self.points[1], self.points[3])
        new = (0, h_w[0])
        x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        # y must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        return int(x), h_w[1] - int(y)

    def get_ticks(self):
        """
        Generates custom ticks based on the GPS coordinates of the map for the matplotlib output.
        :return:
        """
        self.x_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[1], self.points[3], num=9))
        y_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[2], self.points[0], num=8))
        # Ticks must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        self.y_ticks = sorted(y_ticks, reverse=True)
    def rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        ratio = 2 * (value-minimum) / (maximum - minimum)
        b = int(max(0, 255*(1 - ratio)))
        r = int(max(0, 255*(ratio - 1)))
        g = 255 - b - r
        return r, g, b