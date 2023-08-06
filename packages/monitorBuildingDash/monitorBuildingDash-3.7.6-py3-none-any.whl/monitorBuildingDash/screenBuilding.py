#!/bin/python
# #######################
# #   GLOBAL VARIABLES  #
# # COMPUTER DEPENDENT  #
# #######################
import os, time, datetime as dt,importlib,pickle
import pandas as pd,numpy as np
from dorianUtils.utilsD import Utils
import dorianUtils.comUtils as comUtils
importlib.reload(comUtils)
import socket
namePC = socket.gethostname()
DATABASE_SIZE_SECONDS = 60*10
dbParameters = {
    'host'     : "localhost",
    'port'     : "5432",
    'dbname'   : "bigbrother",
    'user'     : "postgres",
    'password' : "sylfenbdd"
    }

if 'sylfen' in os.getenv('HOME'):
    baseFolder   = '/home/sylfen/share/dataScientismProd/MonitoringBatiment/'
    IPCARLOGAVAZZI = "192.168.1.110"
    PORTCG = 502
    IPSMARTLOGGER = "80.11.202.203"
    PORTSL = 502

else:
    baseFolder = '/home/dorian/data/sylfenData/'
    IPCARLOGAVAZZI = 'localhost'
    PORTCG = 4550
    # IPCARLOGAVAZZI = "192.168.1.110"
    # PORTCG = 502

    IPSMARTLOGGER = "localhost"
    PORTSL = 5550

folderpkl = baseFolder + 'monitoringData/'

smartloggerConf={}#add and scale
smartloggerConf["PV00000001-centrale SLS 80kWc-JTW-00"] = [40525,1000]
smartloggerConf["PV00000001-centrale SLS 80kWc-JTWH-00"]= [40560,10]

FileSystem = comUtils.FileSystem
fs = FileSystem()
appdir = os.path.dirname(os.path.realpath(__file__))
parentdir = fs.getParentDir(appdir)
confFolder = parentdir+'monitorBuildingDash/confFiles/'
# ==============================================================================
#                           CONFIGURATIONS
ModeBusConfigMaster = comUtils.ModeBusConfigMaster
SimulatorModeBus = comUtils.SimulatorModeBus
DumpingModeBusClient = comUtils.DumpingModeBusClient
StreamingVisualisationMaster = comUtils.StreamingVisualisationMaster

class ConfigScreenBuilding(ModeBusConfigMaster):
    def __init__(self):
        ModeBusConfigMaster.__init__(self,
        folderpkl,confFolder,dbParameters,
        ipdevice=IPCARLOGAVAZZI,port=PORTCG,
        dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=60*1
        )
        self.compteurs = {k.split('-')[1]:'-'.join(k.split('-')[:3]) for k in self.dfPLC.index if 'sys-JTW' in k}
        units       = {'kW':'JTW','kWh':'JTWH','kVA':'JTVA','kvar':'JTVar','kvarh':'JTVarH','kVAh':'JTVAH'}
        compteurs   = self.dfInstr['point de comptage'].apply(lambda x:self.compteurs[x])
        units       = self.dfInstr['unit'].apply(lambda x:units[x])
        tags        = [c+'-' + d+'-'+u for c,d,u in zip(compteurs,self.dfInstr['description'],units)]
        self.dfInstr.index = tags
        self.validTags = [k for k in self.dfInstr.index if k in self.dfPLC.index]
        self.allTags = self.validTags

class Simulator_SB(ConfigScreenBuilding,SimulatorModeBus):
    def __init__(self):
        ConfigScreenBuilding.__init__(self)
        SimulatorModeBus.__init__(self,speedflowdata=1000,volatilitySimu=1)

class DumpingClient_SB(ConfigScreenBuilding,DumpingModeBusClient):
    def __init__(self):
        ConfigScreenBuilding.__init__(self)
        DumpingModeBusClient.__init__(self)

class StreamingVisualisation_SB(ConfigScreenBuilding,StreamingVisualisationMaster):
    def __init__(self):
        ConfigScreenBuilding.__init__(self)
        StreamingVisualisationMaster.__init__(self)

class EmptyClass():pass

import plotly.express as px
import plotly.graph_objects as go

class ScreenBuildingMaster():
    def __init__(self):
        self.listComputation = ['power enveloppe','consumed energy','energyPeriodBarPlot']
        # self.listCompteurs  = pd.read_csv(self.confFolder+'/compteurs.csv')
        # self.listVars       = self._readVariables()
        # self.dfPLCMonitoring = self._buildDescriptionDFplcMonitoring()
        # self.dfMeteoPLC     = self._loadPLCMeteo()
        # self.dfPLC          = self._mergeMeteoMonitoringPLC()
        # self.listUnits      = list(self.dfPLC.UNITE.unique())
        # self.listCalculatedVars = None
        # self.listFilesMeteo = self.utils.get_listFilesPklV2(self.pklMeteo)
        # self.dfPLC= self.dfPLC.set_index('TAG')

    def _readVariables(self):
        x1=pd.ExcelFile(self.confFolder+'/variables.ods')
        return {s:pd.read_excel(self.confFolder+'/variables.ods',sheet_name=s) for s in x1.sheet_names}

    def exportToxcel(self,df):
        df.index = [t.astimezone(pytz.timezone('Etc/GMT-2')).replace(tzinfo=None) for t in df.index]
        df.to_excel(dt.date.today().strftime('%Y-%m-%d')+'.xlsx')

    def getListVarsFromPLC(self):
        def getListCompteursFromPLC(self,regExpTagCompteur='[a-zA-Z][0-9]+-\w+'):
            return list(np.unique([re.findall(regExpTagCompteur,k)[0] for k in self.dfPLC.TAG]))
        listVars = self.getTagsTU(getListCompteursFromPLC()[0])
        listVars = [re.split('(h-)| ',k)[2] for k in listVars]
        return listVars

    def _loadPLCMeteo(self):
        dfPLC       = pd.read_csv(self.appDir + '/confFiles/configurationMeteo.csv')
        dfPLC.TAG = dfPLC.TAG.apply(lambda x: x.replace('SIS','SIS-02'))
        return dfPLC

    def _buildDescriptionDFplcMonitoring(self):
        self.confFile = 'build from listVars.csv and listCompteurs.csv'
        tagDess,tagIds,unites=[],[],[]
        for c in self.listCompteurs.iterrows():
            compteurName = c[1][1]
            compteurId = c[1][0]
            if compteurId[0]=='C':
                listVars=self.listVars['triphase']
            elif compteurId[:2]=='PV':
                listVars=self.listVars['PV']
            elif compteurId[0]=='M':
                listVars=self.listVars['monophase']

            for v in listVars.iterrows():
                varName = v[1][1]
                varId = v[1][0]
                tagDess.append(compteurName + ' ' + varName)
                tagIds.append(compteurId + '-' + varId)
                # print(compteurId + '-' + varId)
                unites.append(v[1][2])
        dfPLC =  pd.DataFrame(data={'TAG':tagIds,'UNITE':unites,'DESCRIPTION':tagDess})
        # dfPLC['MIN']  = 0
        # dfPLC['MAX']  = 0
        # dfPLC['TYPE'] = 'float'
        return dfPLC

    def _mergeMeteoMonitoringPLC(self):
        tagToday    = self._getListMeteoTags()
        dfMeteoPLC  = self.dfMeteoPLC[self.dfMeteoPLC.TAG.isin(tagToday)]#keep only measured data not predictions
        dfPLC=pd.concat([self.dfPLCMonitoring,dfMeteoPLC])
        dfPLC.to_csv(self.confFolder+'/screenBuilding-10001-001-ConfigurationPLC.csv')
        return dfPLC

    def _getListMeteoTags(self):
        return list(self.dfMeteoPLC[self.dfMeteoPLC.TAG.str.contains('-[A-Z]{2}-01-')].TAG)

    def _getListMeteoTagsDF(self,df):
        return list(df[df.tag.str.contains('-[A-Z]{2}-01-')].tag.unique())

    # ==============================================================================
    #                   functions filter on dataFrame
    # ==============================================================================
    def loadFileMeteo(self,filename):
        if '*' in filename :
            filenames=self.utils.get_listFilesPklV2(self.pklMeteo,filename)
            if len(filenames)>0 : filename=filenames[0]
            else : return pd.DataFrame()
        df = pickle.load(open(filename, "rb" ))
        df.tag   = df.tag.apply(lambda x:x.replace('@',''))#problem with tag remove @
        df.tag   = df.tag.apply(lambda x:x.replace('_','-'))#
        tagToday = self._getListMeteoTagsDF(df)
        # tagToday = self._getListMeteoTags()
        # print(tagToday)
        # print(df.tag.unique())
        df       = df[df.tag.isin(tagToday)]#keep only measured data not predictions
        df.timestampUTC = pd.to_datetime(df.timestampUTC,utc=True)# convert datetime to utc
        return df

    def loadFileMonitoring(self,filename):
        return self.loadFile(filename)

    def _DF_fromTagList(self,df,tagList,rs):
        df = df.drop_duplicates(subset=['timestampUTC', 'tag'], keep='last')
        if not isinstance(tagList,list):tagList =[tagList]
        df = df[df.tag.isin(tagList)]
        if not rs=='raw':df = df.pivot(index="timestampUTC", columns="tag", values="value")
        else : df = df.sort_values(by=['tag','timestampUTC']).set_index('timestampUTC')
        return df

    def _loadDFTagsDayMeteoBuilding(self,datum,listTags,rs):
        realDatum = self.utils.datesBetween2Dates([datum,datum],offset=+1)[0][0]
        dfMonitoring  = self.loadFileMonitoring('*'+realDatum+'*')
        dfMeteo       = self.loadFileMeteo('*'+realDatum+'*')
        if not dfMonitoring.empty : dfMonitoring = self._DF_fromTagList(dfMonitoring,listTags,rs)
        if not dfMeteo.empty : dfMeteo = self._DF_fromTagList(dfMeteo,listTags,rs)
        if rs=='raw':
            df = pd.concat([dfMonitoring,dfMeteo],axis=1)
            # tmp = list(df.columns);tmp.sort();df=df[tmp]
        df = pd.concat([dfMonitoring,dfMeteo],axis=0)
        return df
        # return dfMonitoring

    # ==========================================================================
    #                       COMPUTATIONS FUNCTIONS
    # ==========================================================================
    def computePowerEnveloppe(self,timeRange,compteur = 'EM_VIRTUAL',rs='auto'):
        listTags = self.getTagsTU(compteur+'.+[0-9]-JTW','kW')
        df = self.df_loadTimeRangeTags(timeRange,listTags,rs='5s')
        L123min = df.min(axis=1)
        L123max = df.max(axis=1)
        L123moy = df.mean(axis=1)
        L123sum = df.sum(axis=1)
        df = pd.concat([df,L123min,L123max,L123moy,L123sum],axis=1)

        from dateutil import parser
        ts=[parser.parse(t) for t in timeRange]
        deltaseconds=(ts[1]-ts[0]).total_seconds()
        if rs=='auto':rs = '{:.0f}'.format(max(1,deltaseconds/1000)) + 's'
        df = df.resample(rs).apply(np.mean)
        dfmin = L123min.resample(rs).apply(np.min)
        dfmax = L123max.resample(rs).apply(np.max)
        df = pd.concat([df,dfmin,dfmax],axis=1)
        df.columns=['L1_mean','L2_mean','L3_mean','PminL123_mean','PmaxL123_mean',
                    'PmoyL123_mean','PsumL123_mean','PminL123_min','PmaxL123_max']
        return df

    def _integratePowerCol(self,df,tag,pool):
        print(tag)
        x1=df[df.tag==tag]
        if not x1.empty:
            timestamp=x1.index
            x1['totalSecs']=x1.index.to_series().apply(lambda x: (x-x1.index[0]).total_seconds())/3600
            x1=pd.DataFrame(integrate.cumulative_trapezoid(x1.value,x=x1.totalSecs))
            x1.index=timestamp[1:]
            x1.columns=[tag]
        return x1

    def compute_kWhFromPower(self,timeRange,compteurs=['B001'],rs='raw'):
        generalPat='('+'|'.join(['(' + c + ')' for c in compteurs])+')'
        listTags = self.getTagsTU(generalPat+'.*sys-JTW')

        df = self.df_loadTimeRangeTags(timeRange,listTags,rs=rs,applyMethod='mean',pool=True)
        dfs=[]
        for tag in listTags:
            dftmp = self._integratePowerCol(df,tag,True)
            if not dftmp.empty:dfs.append(dftmp)

        try : df=pd.concat(dfs,axis=1)
        except : df = pd.DataFrame()
        return df.ffill().bfill()

    def compute_kWhFromCompteur(self,timeRange,compteurs=['B001']):
        generalPat='('+'|'.join(['(' + c + ')' for c in compteurs])+')'
        listTags = self.getTagsTU(generalPat+'.+kWh-JTWH')
        df = self.df_loadTimeRangeTags(timeRange,listTags,rs='raw',applyMethod='mean')
        df = df.drop_duplicates()
        dfs=[]
        for tag in listTags:
            x1=df[df.tag==tag]
            dfs.append(x1['value'].diff().cumsum()[1:])
        try :
            df = pd.concat(dfs,axis=1)
            df.columns = listTags
        except : df = pd.DataFrame()
        return df.ffill().bfill()

    def plot_compare_kwhCompteurvsPower(self,timeRange,compteurs=['B001'],rs='600s'):
        dfCompteur = self.compute_kWhFromCompteur(timeRange,compteurs)
        dfPower = self.compute_kWhFromPower(timeRange,compteurs)
        df = self.utils.prepareDFsforComparison([dfCompteur,dfPower],
                            ['energy from compteur','enery from Power'],
                            group1='groupPower',group2='compteur',
                            regexpVar='\w+-\w+',rs=rs)

        fig=px.line(df,x='timestamp',y='value',color='compteur',line_dash='groupPower',)
        fig=self.utils.quickLayout(fig,'energy consumed from integrated power and from energy counter',ylab='kWh')
        fig.update_layout(yaxis_title='energy consommée en kWh')
        return fig

    def energyPeriodBarPlot(self,timeRange,period='1d',compteurs = ['A003','B001']):
        dfCompteur   = self.compute_kWhFromCompteur(timeRange,compteurs)
        df = dfCompteur.resample(period).first().diff()[1:]
        fig = px.bar(df,title='répartition des énergies consommées par compteur')
        fig.update_layout(yaxis_title='énergie en kWh')
        fig.update_layout(bargap=0.5)
        return fig
    # ==========================================================================
    #                       for website monitoring
    # ==========================================================================
    def generateFilename(self,proprietaire='MJ',client='*',batiment='*',local='*'):
        return '-'.join([proprietaire,client,batiment,local])

    def getListTagsAutoConso(self,compteurs):
        pTotal = [self.getTagsTU(k + '.*sys-JTW')[0] for k in compteurs]
        pvPower = self.getTagsTU('PV.*-JTW-00')[0]
        listTagsPower = pTotal + [pvPower]
        energieTotale = [self.getTagsTU(k + '.*kWh-JTWH')[0] for k in compteurs]
        pvEnergie = self.getTagsTU('PV.*-JTWH-00')[0]
        listTagsEnergy = energieTotale + [pvEnergie]
        return pTotal,pvPower,listTagsPower,energieTotale,pvEnergie,listTagsEnergy

    def computeAutoConso(self,timeRange,compteurs,formula='g+f-e+pv'):
        pTotal,pvPower,listTagsPower,energieTotale,pvEnergie,listTagsEnergy = self.getListTagsAutoConso(compteurs)
        # df = self.df_loadTimeRangeTags(timeRange,listTagsPower,'600s','mean')
        df = self.df_loadTimeRangeTags(timeRange,listTagsPower,'600s','mean')
        if formula=='g+f-e+pv':
            g,e,f = [self.getTagsTU(k+'.*sys-JTW')[0] for k in ['GENERAL','E001','F001',]]
            df['puissance totale'] = df[g] + df[f] - df[e] + df[pvPower]
        elif formula=='sum-pv':
            df['puissance totale'] = df[pTotal].sum(axis=1) - df[pvPower]
        elif formula=='sum':
            df['puissance totale'] = df[pTotal].sum(axis=1)

        df['diffPV']=df[pvPower]-df['puissance totale']
        dfAutoConso = pd.DataFrame()
        df['zero'] = 0
        dfAutoConso['part rSoc']     = 0
        dfAutoConso['part batterie'] = 0
        dfAutoConso['part Grid']     = -df[['diffPV','zero']].min(axis=1)
        dfAutoConso['Consommation du site']      = df['puissance totale']
        dfAutoConso['surplus PV']    = df[['diffPV','zero']].max(axis=1)
        dfAutoConso['part PV']       = df[pvPower]-dfAutoConso['surplus PV']
        # dfAutoConso['Autoconsommation'] = df[pvPower]-dfAutoConso['PV surplus']
        return dfAutoConso

    def consoPowerWeek(self,timeRange,compteurs,formula='g+f-e+pv'):
        pTotal,pvPower,listTagsPower,energieTotale,pvEnergie,listTagsEnergy = self.getListTagsAutoConso(compteurs)
        # df = self.df_loadTimeRangeTags(timeRange,listTagsPower,'1H','mean')
        df = self.df_loadTimeRangeTags(timeRange,listTagsPower,'1H','mean')

        if formula=='g+f-e+pv':
            g,e,f = [self.getTagsTU(k+'.*sys-JTW')[0] for k in ['GENERAL','E001','F001',]]
            df['puissance totale'] = df[g] + df[f] - df[e] + df[pvPower]
        elif formula=='sum-pv':
            df['puissance totale'] = df[pTotal].sum(axis=1) - df[pvPower]
        elif formula=='sum':
            df['puissance totale'] = df[pTotal].sum(axis=1)

        df = df[['puissance totale',pvPower]]
        df.columns = ['consommation bâtiment','production PV']
        return df

    def compute_EnergieMonth(self,timeRange,compteurs,formula='g+f-e+pv'):
        pTotal,pvPower,listTagsPower,energieTotale,pvEnergie,listTagsEnergy = self.getListTagsAutoConso(compteurs)
        # df = self.df_loadTimeRangeTags(timeRange,listTagsEnergy,rs='raw',applyMethod='mean')
        df = self.df_loadTimeRangeTags(timeRange,listTagsEnergy,rs='raw',applyMethod='mean')
        df = df.drop_duplicates()

        df=df.pivot(columns='tag',values='value').resample('1d').first().ffill().bfill()
        newdf=df.diff().iloc[1:,:]
        newdf.index = df.index[:-1]
        if formula=='g+f-e+pv':
            g,e,f = [self.getTagsTU(k + '.*kWh-JTWH')[0] for k in ['GENERAL','E001','F001',]]
            newdf['energie totale'] = newdf[g] + newdf[f] - newdf[e] + newdf[pvEnergie]
        elif formula=='sum-pv':
            newdf['energie totale'] = newdf[pTotal].sum(axis=1) - newdf[pvEnergie]
        elif formula=='sum':
            newdf['energie totale'] = newdf[energieTotale].sum(axis=1)

        newdf = newdf[['energie totale',pvEnergie]]
        newdf.columns = ['kWh consommés','kWh produits']
        return newdf

    def get_compteur(self,timeDate,compteurs,formula='g+f-e+pv'):
        timeRange = [k.isoformat() for k in [timeDate - dt.timedelta(seconds=600),timeDate]]
        pTotal,pvPower,listTagsPower,energieTotale,pvEnergie,listTagsEnergy = self.getListTagsAutoConso(compteurs)
        df = self.df_loadTimeRangeTags(timeRange,listTagsEnergy,rs='20s',applyMethod='mean')
        g,e,f = [self.getTagsTU(k + '.*kWh-JTWH')[0] for k in ['GENERAL','E001','F001',]]
        if formula=='g+f-e+pv':
            df['energie totale'] = df[g] + df[f] - df[e] + df[pvEnergie]
        elif formula=='sum':
            df['energie totale'] = df[energieTotale].sum(axis=1)
        return df.iloc[-1,:]
    # ==============================================================================
    #                   graphic functions
    # ==============================================================================
    def update_lineshape_fig(self,fig,style='default'):
        if style=='default':
            fig.update_traces(line_shape="linear",mode='lines+markers')
        elif style in ['markers','lines','lines+markers']:
            fig.update_traces(line_shape="linear",mode=style)
        elif style =='stairs':
            fig.update_traces(line_shape="hv",mode='lines')


class ScreenBuildingComputer(ScreenBuildingMaster,StreamingVisualisation_SB):
    def __init__(self,*args,**kwargs):
        StreamingVisualisation_SB.__init__(self,*args,**kwargs)
        ScreenBuildingMaster.__init__(self)
