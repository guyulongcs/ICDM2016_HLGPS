from Tool.Plot.Plotbar import *
from Tool.Plot.Plotcdf import *
from os.path import join
from Config import *
from AnalyseResult import *
from matplotlib.backends.backend_pdf import PdfPages
from HomeLocIdentify import *
from Tool.GeoPlot.gmplot.gmplot import *


class PlotExpRes():
    def __init__(self):
        self.folder = join(Config.folderData, Config.folderDataParsed, Config.folderExp, Config.folderPic)
        pass

    def start(self):
        self.plot_acc()
        #self.plot_errcdf()
        #self.plot_loc_res()

    def plot_acc(self):
        self.plot_acc_checkin()
        self.plot_acc_all()
        self.plot_acc_errdis()



        pass

    def plot_errcdf(self):
        self.plot_errdis()

    def plot_acc_checkin(self):
        plotBar = Plotbar()
        plotBar.xlabels = ["Maxvote", "ClusterHier", "Avg", "HLGPS"]
        plotBar.xcolor = ['green','blue','orange','red']
        plotBar.xwidth = 0.5
        plotBar.y = [ 91.9, 91.6, 88.8, 92.3]
        plotBar.yaxis = [86, 93.5, 1]
        plotBar.ylabel = "ACC"
        plotBar.title = "Performance of methods for Home Location Identfication on U$_{-H} \cap U^C$(rh=0.8)"
        plotBar.alpha=0.6
        plotBar.grid = False


        fileName =  "acc_checkin.pdf"
        plotBar.file = join(self.folder, fileName)

        plotBar.plot_bar()

    def plot_acc_all(self):
        plotBar = Plotbar()
        plotBar.xlabels = ["UDI", "HLGPS${tj}$", "HLGPS${-r}$", "HLGPS${uc}$", "HLGPS"]
        plotBar.xcolor = ['green','blue','orange', 'purple', 'red']
        plotBar.xwidth = 0.5
        plotBar.y = [59, 65.2, 65.6, 64.5, 67.7]
        plotBar.yaxis = [55, 69, 1]
        plotBar.ylabel = "ACC"
        plotBar.title = "Performance of methods for Home Location Identfication on U$_{-H}$(rh=0.8)"
        plotBar.alpha=0.6
        plotBar.grid = False


        fileName =  "acc_all.pdf"
        plotBar.file = join(self.folder, fileName)

        plotBar.plot_bar()

    def plot_acc_errdis(self):
        plotBar = Plotbar()
        plotBar.xlabels = ["UDI",  "HLGPS"]
        plotBar.xcolor = ['green','red']
        plotBar.xwidth = 0.5
        plotBar.y = [32.6, 55.9]
        plotBar.yaxis = [30, 61, 2]
        plotBar.ylabel = "ACC"
        plotBar.title = "Performance of methods for Home Location Identfication on U$_{-H}$(rh=0.2)"
        plotBar.alpha=0.6
        plotBar.grid = False


        fileName =  "acc_errdis.pdf"
        plotBar.file = join(self.folder, fileName)

        plotBar.plot_bar()

    def plot_errdis(self):
        #err_dis = AnalyseResult.load_errdis_method(Config.methodTrust)
        cpTrust = AnalyseResult.load_err_dis_cp_method(Config.methodTrust)
        cpUDI = AnalyseResult.load_err_dis_cp_method(Config.methodInfluenceGlobal)
        cpAvg = AnalyseResult.load_err_dis_cp_method(Config.methodAvg)
        cpVote = AnalyseResult.load_err_dis_cp_method(Config.methodVote)
        cpHierar = AnalyseResult.load_err_dis_cp_method(Config.clustering_Hierarchical)

        fileName = Config.file_exp_result_errcdf


        #plot
        file = join(self.folder, fileName)
        pp = PdfPages(file)
        plt.figure(1)

        plt.plot(cpTrust[0], cpTrust[1])
        plt.plot(cpUDI[0], cpUDI[1])
        plt.plot(cpAvg[0], cpAvg[1])
        plt.plot(cpVote[0], cpVote[1])
        plt.plot(cpHierar[0], cpHierar[1])



        pp.savefig()
        pp.close()
        plt.close()


    def plot_loc_res(self):

        hli = HomeLocIdentify()
        hli.load_data_home_loc()
        dictUserTrue = hli.homeLocTrue
        dictUserTrust = hli.homeLocTrust


        fileName =  "map_res.html"
        file = join(self.folder, fileName)

        sampleRatio = 0.02
        userList = dictUserTrue.keys()
        userList = ProcessTool.sampleListByRatio(userList, sampleRatio)
        userSet = set(userList)

        #1:true, blue
        (checkLatList1, checkLonList1) = self.get_check_in_plot_list(dictUserTrue, userSet)
        (checkLatList2, checkLonList2) = self.get_check_in_plot_list(dictUserTrust, userSet)

        #GoogleMapPlotter.demo(file)
        #return

        mymap = GoogleMapPlotter(37.428, -110.145, 4.5)
        #mymap = GoogleMapPlotter.from_geocode("America", 4.5)

        #
        # latList = []
        # lonList = []
        # for cityId in self.dictCity:
        #     city = self.dictCity[cityId]
        #     lat = city.lat
        #     lon = city.lon
        #     latList.append(lat)
        #     lonList.append(lon)
        #
        #     #mymap.marker(lat, lon, "green")
        #     mymap.circle(lat, lon, 20000, "b", ew=2)
            #mymap.polygon(path3[0], path3[1], edge_color="cyan", edge_width=5, face_color="blue", face_alpha=0.1)

        #mymap.heatmap(latList, lonList, threshold=10, radius=20)
        gradient = [
'rgba(255, 0, 0, 0)',
'rgba(255, 255, 0, 0.9)',
'rgba(0, 255, 0, 0.7)',
'rgba(173, 255, 47, 0.5)',
'rgba(152, 251, 152, 0)',
'rgba(152, 251, 152, 0)',
'rgba(0, 0, 238, 0.5)',
'rgba(186, 85, 211, 0.7)',
'rgba(255, 0, 255, 0.9)',
'rgba(255, 0, 0, 1)']

            #Blue
        gradient1 = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 225, 255, 1)',
    'rgba(0, 200, 255, 1)',
    'rgba(0, 175, 255, 1)',
    'rgba(0, 160, 255, 1)',
    'rgba(0, 145, 223, 1)',
    'rgba(0, 125, 191, 1)',
    'rgba(0, 110, 255, 1)',
    'rgba(0, 100, 255, 1)',
    'rgba(0, 75, 255, 1)',
    'rgba(0, 50, 255, 1)',
    'rgba(0, 25, 255, 1)',
    'rgba(0, 0, 255, 1)'
        ]
#// Red - negative
        gradient2 = [
            'rgba(255, 255, 0, 0)',
            'rgba(255, 255, 0, 1)',
            'rgba(255, 225, 0, 1)',
            'rgba(255, 200, 0, 1)',
            'rgba(255, 175, 0, 1)',
            'rgba(255, 160, 0, 1)',
            'rgba(255, 145, 0, 1)',
            'rgba(255, 125, 0, 1)',
            'rgba(255, 110, 0, 1)',
            'rgba(255, 100, 0, 1)',
            'rgba(255, 75, 0, 1)',
            'rgba(255, 50, 0, 1)',
            'rgba(255, 25, 0, 1)',
            'rgba(255, 0, 0, 1)'
        ]

        g1 = [
            'rgba(255, 255, 0, 0)',
        ]
        g2=[
            'rgba(255, 255, 0, 1)'
        ]


        mymap.heatmap(checkLatList1, checkLonList1, threshold=10, radius=40, gradient = gradient1, opacity=0.7)
        mymap.heatmap(checkLatList2, checkLonList2, threshold=10, radius=40,gradient = gradient2, opacity=0.4)

        for i in xrange(len(checkLatList1)):
            lat = checkLatList1[i]
            lon = checkLonList1[i]
            #mymap.marker(lat, lon, "green")
            mymap.circle(lat, lon, 10000, "b", ew=2)

        for i in xrange(len(checkLatList2)):
            lat = checkLatList2[i]
            lon = checkLonList2[i]
            #mymap.marker(lat, lon, "red")
            mymap.circle(lat, lon, 6000, "r", ew=2)



        #mymap.heatmap(latList, lonList, threshold=10, radius=20)
        #mymap.scatter(checkLatList1, checkLonList1, c='b', marker=True)
        #mymap.scatter(checkLatList2, checkLonList2, c='r', marker=True)





        #mymap.marker(37.427, -122.145, "yellow")

        mymap.draw(file)
        pass

    def get_check_in_plot_list(self, dictUser, userSet):
        InOut.console_func_begin("get_check_in_plot_list")

        latList = []
        lonList = []

        list  = []

        for user_id in userSet:
            if user_id not in dictUser:
                continue

            user = dictUser[user_id]
            lat = user.latitude
            lon = user.longitude

            latList.append(lat)
            lonList.append(lon)
        print "len:", len(latList), len(lonList)
        return (latList, lonList)






