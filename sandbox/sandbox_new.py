import json
import numpy
import param
import pandas as pd
import panel as pn
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.interpolate import griddata
<<<<<<< Updated upstream
from time import sleep
import threading
import gc
from abc import ABCMeta, abstractmethod
=======

>>>>>>> Stashed changes


class Sandbox:
    # TODO Marco: Object as argument required?

    def __init__(self, calibration_file=None, projector_resolution=None):
        self.calibrationdata = CalibrationData(file=calibration_file)
        if projector_resolution is not None:
            self.calibrationdata.p_width = projector_resolution[0]
            self.calibrationdata.p_height = projector_resolution[1]

        self.sensor = DummySensor(self.calibrationdata)
        self.projector = Projector(self.calibrationdata)
        self.module = TopoModule(self.calibrationdata, self.sensor, self.projector)

class CalibrationData:

    def __init__(self, file=None):
        self.p_width = 800
        self.p_height = 600
        self.p_dpi = 100
        self.p_top_margin = 0
        self.p_left_margin = 0
        self.p_area_width = 400
        self.p_area_height = 200
        self.p_area_depth = 200 #deprecated

        self.s_width = 512
        self.s_heigth = 424
        self.s_area_width = 512
        self.s_area_height = 424
        #self.s_left_margin
        #self.s_top_margin

        if file is not None:
            self.load_json(file)

    def load_json(self, file='calibration.json'):
        # TODO: Check for overwriting of existing (new) parameters with older calibration files!
        with open(file) as calibration_json:
            self.__dict__ = json.load(calibration_json)
        print("JSON configuration loaded.")

    def save_json(self, file='calibration.json'):
        with open(file, "w") as calibration_json:
            json.dump(self.__dict__, calibration_json)
        print('JSON configuration file saved:', str(file))


class Projector:

    def __init__(self, calibrationdata):
        self.calib = calibrationdata
        #self.plot = plot

        # panel components (panes)
        self.frame = None
        self.legend = None
        self.panel = None

        self.create_panel() # make explicit?

    def show(self, figure):
        # TODO: Fix that nasty memory leak!
        self.frame.object = figure
        #plt.close()

<<<<<<< Updated upstream
=======
    def show(self):
        self.frame.object = self.plot.render_frame()

    def show_loop(self, iterations=5, sleep_s=0.1):
        for i in numpy.arange(0, iterations):
            self.show()
            sleep(sleep_s)
>>>>>>> Stashed changes

    def create_panel(self):

        css = '''
        body {
          margin:0px;
          background-color: #ffffff;
        }
        .bk.frame {
        }
        .bk.legend {
          background-color: #AAAAAA;
        }
        .panel {
          background-color: #000000;
        }
        '''

        pn.extension(raw_css=[css])
        # Create a panel object and serve it within an external bokeh browser that will be opened in a separate window
        # in this special case, a "tight" layout would actually add again white space to the plt canvas, which was already cropped by specifying limits to the axis


<<<<<<< Updated upstream
        self.frame = pn.pane.Matplotlib(plt.figure(), width=self.calib.p_area_width, height=self.calib.p_area_height,
                                         margin=[self.calib.p_top_margin, 0, 0, self.calib.p_left_margin], tight=False, dpi=self.calib.p_dpi, css_classes=['frame'])
=======
        self.frame = pn.pane.Matplotlib(self.plot.figure, width=self.calib.p_area_width, height=self.calib.p_area_height,
                                         margin=[self.calib.p_top_margin, 0, 0, self.calib.p_left_margin], tight=False, dpi=self.calib.p_dpi, css_classes=['output'])
>>>>>>> Stashed changes

        self.legend = pn.Column("<br>\n# Legend",
                                margin=[self.calib.p_top_margin, 0, 0, 0],
                                css_classes=['legend'])

        # Combine panel and deploy bokeh server
        self.panel = pn.Row(self.frame, self.legend, width=self.calib.p_width, height=self.calib.p_height,
                            sizing_mode='fixed', css_classes=['panel'])

        # TODO: Add specific port? port=4242
        self.panel.show(threaded=False)

    def trigger(self):
        self.frame.param.trigger('object')

    def calibrate_projector(self):

        margin_top = pn.widgets.IntSlider(name='Top margin', value=self.calib.p_top_margin, start=0, end=200)
        def callback_mt(target, event):
            m = target.margin
            n = event.new
            # just changing single indices does not trigger updating of pane
            target.margin = [n, m[1], m[2], m[3]]
            # also update calibration object
            self.calib.p_top_margin = event.new
<<<<<<< Updated upstream
=======
        margin_top.link(self.frame, callbacks={'value': callback_mt})
>>>>>>> Stashed changes

        margin_top.link(self.frame, callbacks={'value': callback_mt})

        margin_left = pn.widgets.IntSlider(name='Left margin', value=self.calib.p_left_margin, start=0, end=200)
        def callback_ml(target, event):
            m = target.margin
            n = event.new
            # just changing single indices does not trigger updating of pane
            target.margin = [m[0], m[1], m[2], n]
            # also update calibration object
            self.calib.p_left_margin = event.new
        margin_left.link(self.frame, callbacks={'value': callback_ml})

        width = pn.widgets.IntSlider(name='Map width', value=self.calib.p_area_width, start=self.calib.p_area_width - 400, end=self.calib.p_area_width + 400)
        def callback_width(target, event):
            target.width = event.new
            target.param.trigger('object')
            # also update calibration object
            self.calib.p_area_width = event.new
        width.link(self.frame, callbacks={'value': callback_width})

        height = pn.widgets.IntSlider(name='Map height', value=self.calib.p_area_height, start=self.calib.p_area_height - 400, end=self.calib.p_area_height + 400)
        def callback_height(target, event):
            target.height = event.new
            target.param.trigger('object')
            # also update calibration object
            self.calib.p_area_height = event.new
            #self.plot.redraw_plot()
        height.link(self.frame, callbacks={'value': callback_height})

        widgets = pn.Column("### Map positioning", margin_top, margin_left, width, height)
        return widgets

class Sensor:
    pass


class Kinect2:
    # will be child class of Sensor

    def __init__(self, calibration):
        self.calib = calibration

    # TODO: Daniel: access and update calibration data program wide with self.calib.s_width = 451 or similar


class DummySensor:

    def __init__(self, calibrationdata, width=512, height=424, depth_limits=(80, 100), points_n=5, points_distance=20,
                 alteration_strength=0.1, random_seed=None):

        # alteration_strength: 0 to 1 (maximum 1 equals numpy.pi/2 on depth range)

        self.calib = calibrationdata # use in the future from calibration file

        self.width = width
        self.height = height
        self.depth_lim = depth_limits
        self.n = points_n
        self.distance = points_distance
        self.strength = alteration_strength
        self.seed = random_seed

        # create grid, init values, and init interpolation
        self.grid = self.create_grid()
        self.positions = self.pick_positions()

        self.os_values = None
        self.values = None
        self.pick_values()

        self.interpolation = None
        self.interpolate()

    ## Methods

    def get_frame(self):
        # TODO: Add time check for 1/30sec
        self.alter_values()
        self.interpolate()
        return self.interpolation

    def get_filtered_frame(self):
        return self.get_frame()

    ## Private functions
    # TODO: Make private

    def oscillating_depth(self, random):
        r = (self.depth_lim[1] - self.depth_lim[0]) / 2
        return numpy.sin(random) * r + r + self.depth_lim[0]

    def create_grid(self):
        # creates 2D grid for given resolution
        x, y = numpy.meshgrid(numpy.arange(0, self.width, 1), numpy.arange(0, self.height, 1))
        return numpy.stack((x.ravel(), y.ravel())).T

    def pick_positions(self, corners=True, seed=None):
        '''
        grid: Set of possible points to pick from
        n: desired number of points, not guaranteed to be reached
        distance: distance or range, pilot points should be away from dat points
        '''

        numpy.random.seed(seed=seed)

        gl = self.grid.shape[0]
        gw = self.grid.shape[1]
        points = numpy.zeros((self.n, gw))

        # randomly pick initial point
        ipos = numpy.random.randint(0, gl)
        points[0, :2] = self.grid[ipos, :2]

        i = 1  # counter
        while i < self.n:

            # calculate all distances between remaining candidates and sim points
            dist = cdist(points[:i, :2], self.grid[:, :2])
            # choose candidates which are out of range
            mm = numpy.min(dist, axis=0)
            candidates = self.grid[mm > self.distance]
            # count candidates
            cl = candidates.shape[0]
            if cl < 1: break
            # randomly pick candidate and set next pilot point
            pos = numpy.random.randint(0, cl)
            points[i, :2] = candidates[pos, :2]

            i += 1

        # just return valid points if early break occured
        points = points[:i]

        if corners:
            c = numpy.zeros((4, gw))
            c[1, 0] = self.grid[:, 0].max()
            c[2, 1] = self.grid[:, 1].max()
            c[3, 0] = self.grid[:, 0].max()
            c[3, 1] = self.grid[:, 1].max()
            points = numpy.vstack((c, points))

        return points

    def pick_values(self):
        numpy.random.seed(seed=self.seed)
        n = self.positions.shape[0]
        self.os_values = numpy.random.uniform(-numpy.pi, numpy.pi, n)
        self.values = self.oscillating_depth(self.os_values)

    def alter_values(self):
        # maximum range in both directions the values should be altered
        # TODO: replace by some kind of oscillation :)
        numpy.random.seed(seed=self.seed)
        os_range = self.strength * (numpy.pi / 2)
        for i, value in enumerate(self.os_values):
            self.os_values[i] = value + numpy.random.uniform(-os_range, os_range)
        self.values = self.oscillating_depth(self.os_values)

    def interpolate(self):
        inter = griddata(self.positions[:, :2], self.values, self.grid[:, :2], method='cubic', fill_value=0)
        self.interpolation = inter.reshape(self.height, self.width)


<<<<<<< Updated upstream
=======



>>>>>>> Stashed changes
class Plot:

    def __init__(self, calibration):

        self.calib = calibration
        #self.sensor = sensor

        # switches
        self.colormap = True
        self.contours = True
        self.points = True

        self.figure = None
        self.ax = None # current plot composition

        self.create_empty_frame() # initial figure for starting projector


<<<<<<< Updated upstream
    def render_frame(self, data):
        # clear axes to draw new ones on figure
        self.ax.cla()

=======
    def render_frame(self):
        # reset old figure
        plt.close(self.figure)
        self.create_empty_frame()
>>>>>>> Stashed changes
        if self.colormap:
            self.add_colormap(data)
        if self.contours:
            self.add_contours(data)
        if self.points:
            #self.add_points(data)
            pass

        # crop axis (!!!input dimensions of calibrated sensor!!!)
        self.ax.axis([0, self.calib.s_area_width, 0, self.calib.s_area_height])
        self.ax.set_axis_off()

        # return final figure
        #return self.figure
        return True


    def create_empty_frame(self):
        self.figure = plt.figure(figsize=(self.calib.p_area_width / self.calib.p_dpi, self.calib.p_area_height / self.calib.p_dpi),
                                 dpi=self.calib.p_dpi)  # , frameon=False) # curent figure
        self.ax = None
        self.ax = self.figure.add_axes([0., 0., 1., 1.])

        # 1) make patch invisible / like 'frameon=False', buggy
        # fig.patch.set_visible(False)
        # 2) Set whitespace to 0
        # fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
        # 3) Turn off axes and set axes limits
        # ax.axis('off')
        self.ax.set_axis_off()

    def add_colormap(self, data):
        c = self.ax.pcolormesh(data, cmap='gist_earth')

    #def add_points(self, data):
     #   p = self.ax.scatter(self.sensor.positions[:, 0], self.sensor.positions[:, 1], color='k', marker='x')

    def add_contours(self, data):
        co = self.ax.contour(data, colors='k')


class Module:

    __metaclass__ = ABCMeta

    def __init__(self, calibrationdata, sensor, projector):
        self.calib = calibrationdata
        self.sensor = sensor
        self.projector = projector
        self.plot = Plot(self.calib)

        # threading
        self._lock = threading.Lock()
        self.thread = None
        self.thread_running = False

    @abstractmethod
    def setup(self):
        """"Wildcard: Everything necessary to set up before an model update can be performed."""
        pass

    @abstractmethod
    def update(self):
        """"Wildcard: Single model update operation that can be looped in a thread."""
        pass

    def thread_loop(self):
        while self.thread_running:
            self.update()

    def run(self):
        if not self.thread_running:
            self.thread_running = True
            self.thread = threading.Thread(target=self.thread_loop, daemon=True, )
            self.thread.start()
            print('Thread started...')
        else:
            print('Thread already running. First stop with stop().')

    def stop(self):
        self.thread_running = False  # set flag to end thread loop
        self.thread.join()  # wait for the thread to finish
        print('Thread stopped.')


class TopoModule(Module):

    def setup(self):
        self.plot.render_frame(self.sensor.get_frame())
        self.projector.frame.object = self.plot.figure

    def update(self):
        with self._lock:
            self.plot.render_frame(self.sensor.get_frame())
            #self.projector.show(fig)
        self.projector.trigger()



class Module:
    def __init__(self, kinect, projector, calibrationdata):
        self.kinect = kinect
        self.projector = projector
        self.calibrationData = calibrationdata

    def setup(self):
        pass

    def run(self):
        pass

<<<<<<< Updated upstream

class BlockModule(Module):
    # child class of Model
    pass

class GemPyModel(Module):
=======
class BlockModule(Module):
    # child class of Model
    pass

class TopoModule(Module):
    # child class of Model
    pass

class GemPyModule(Module):
>>>>>>> Stashed changes
    # child class of Model
    pass