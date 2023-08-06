import h5py as hdf
import numpy as np
import pickle as pickle
import matplotlib.pyplot as plt
import pandas as pd
import DMCpy
import os.path
from DMCpy import InteractiveViewer

import copy
from DMCpy import _tools

scanTypes = ['Old Data','Powder','A3']
class entry:
    """Dummy class for h5py group entries"""
    def __init__(self,**kwargs):
        for item,value in kwargs:
            setattr(self,item,value)

def decode(item):
    """Test and decode item to utf8"""
    if hasattr(item,'__len__'):
        if len(item)>0:
            if hasattr(item[0],'decode'):
                item = item[0].decode('utf8')
            
                    
    return item

class h5pyReader:
    """Custom class used to traverse hdf file and extract all data
    
    This object traverses the HDF file structure and creates a dummy
    entry object for each layer. As H5PY do not traverse links already
    visited, special care is to be taken!"""
    def __init__(self,exclude=None):
        """Initialize a reader with custom exclude
        
        Kwargs: 
            - exclude (str): Exclude this first name (default None)"""
        if exclude is None:
            self.exclude = None
        else:
            self.exclude = exclude

    def __call__(self, name, h5obj):
        """Called by the hdf5 visititmes method"""
        if name == self.exclude:
            return
        
        
        # Split names by '/' and replace - with _
        name = name.replace('-','_').split('/')
        if name[0] == self.exclude:
            name = name[1:]
        if len(name) == 0:
            return 
        
        # Reverse name order to enable the use of pop
        name = name[::-1]
        
        
        # Find correct depth in object
        obj = self
        
        while len(name) != 1: # Go through name and add entries for all missing links
            # I.e: DMC/DMC_BF3_Detector/CounterMod -> 'CounterMode', 'DMC_BF3_Detector', 'DMC'
            # add 'DMC' to obj, then 'DMC_BF3_Detector'
            currentName = name.pop()
            if not hasattr(obj,currentName):
                obj.__dict__[currentName] = entry()
            obj = getattr(obj,currentName) # get one level down object
            
        attributeName = name[0]
        if attributeName == 'lambda':
            attributeName = 'Lambda' # lambda is a key word in python
        if hasattr(h5obj,'dtype'): 
            obj.__dict__[attributeName] = np.array(h5obj)
        
        if not hasattr(obj,attributeName): # Add the group to the data
            obj.__dict__[attributeName] = entry()
        
        for item,value in dict(h5obj.attrs).items():
            try:
                setattr(getattr(obj,attributeName),item,value)
            except AttributeError: # cannot add things to numpy array.... alternatively add it by using _ instead
                setattr(obj,'__'+attributeName+'_'+item,value)
            

@_tools.KwargChecker()
def maskFunction(phi,maxAngle=10.0):
    """Mask all phi angles outside plus/minus maxAngle

    Args:

        - phi (array): Numpy array of phi angles to be masked

    Kwargs:

        - maxAngle (float): Mask points greater than this or less than -maxAngle in degrees (default 10)
    """
    return np.abs(phi)<maxAngle

@_tools.KwargChecker()
def findCalibration(fileName):
    """Find detector calibration for specified file

    Args:

        - fileName (str): Name of file for which calibration is needed

    Returns:

        - calibration (array): Detector efficiency

        - calibrationName (str): Name of calibration file used

    Raises:

        - fileNotFoundError

    """

    # Extract only actual file name if path is provided    
    fileName = os.path.split(fileName)[-1]

    # Split name in 'dmcyyyynxxxxxx.hdf'
    year,fileNo = [int(x) for x in fileName[3:].replace('.hdf','').split('n')]

    calibrationDict = DMCpy.calibrationDict

    # Calibration files do not cover the wanted year
    if not year in calibrationDict.keys():
        raise FileNotFoundError('Calibration files for year {} (extracted from file name "{}") is'.format(year,fileName)+\
            ' not covered in calibration tables. Please update to newest version by invoking "pip install --upgrade DMCpy"')

    yearCalib = calibrationDict[year]
    
    limits = yearCalib['limits']
    
    # Calibration name is index of the last limit below file number
    idx = np.sum([fileNo>limits])-1
    
    idx = np.max([idx,0]) # ensure that idx is not negative
    
    # Calibration is saved in yearCalib with name of calibration file
    calibrationName = yearCalib['names'][idx]
    calibration = yearCalib[calibrationName]
    return calibration,calibrationName

class DataFile(object):
    @_tools.KwargChecker(include=['radius','data','twoThetaPosition','A3','verticalPosition','Monitor','waveLength'])
    def __init__(self, file=None,**kwargs):
        """DataFile object holding all data from a single DMC powder scan file

        Kwargs:

            - file (string or object): File path or file object (default None)

            - other kwargs will be used to overwrite values otherwise loaded from file. Following are possible to overwrite:

                - radius (float)

                - data (int shaped (n,128,1152))

                - twoThetaPosition (float shaped (1), i.e. np.array([0.0]))

                - A3 (float shaped (n))

                - verticalPosition (float shaped (128))

                - Monitor (float shaped (n))

                - waveLength (float)

        If a file path is given data is loaded into this object. If an existing DataFile object
        is provided, its data is copied into the new object.

        """

        self._debugging = False
        self.kwargs = kwargs

        if not file is None: 
            if isinstance(file,DataFile): # Copy everything from provided file
                # Copy all file settings
                self.updateProperty(file.__dict__)

            elif os.path.exists(file): # load file from disk
                self.loadFile(file)


            else:
                if not file == 'DEBUG': # If testing is activated load a dummy data file
                    raise FileNotFoundError('Provided file path "{}" not found.'.format(file))

                self._debugging = True
                self.folder = None
                self.fileName = None



    @_tools.KwargChecker()
    def loadFile(self,filePath):
        if not os.path.exists(filePath):
            raise FileNotFoundError('Provided file path "{}" not found.'.format(filePath))

        self.folder, self.fileName = os.path.split(filePath)

        # Open file in reading mode
        with hdf.File(filePath,mode='r') as f:
            bulkData = h5pyReader(exclude='entry')
            f.visititems(bulkData) 

            if 'entry/data' in f: # data1 is not included as it only contains soft links
                data1 = h5pyReader()
                f['entry/data'].visititems(data1)
                bulkData.data1 = data1

        self.updateProperty(bulkData.__dict__)

        # copy important paramters to correct position
        self.radius = self.kwargs.get('radius',0.8)
        
        countShape = self.DMC.detector.data.shape
        if len(countShape) == 2:
            self.scanType = 'Powder'
            self.counts = self.kwargs.get('data',self.DMC.detector.data)
            
            self.counts.shape = (1,*self.counts.shape)
            
            try:
                self.twoThetaPosition = self.kwargs.get('twoThetaPosition',self.DMC.detector.detector_position)
            except AttributeError:
                self.twoThetaPosition = np.array([0.0])
            self.twoTheta = np.linspace(0,132,self.counts.shape[2])
            if not np.isnan(self.twoThetaPosition[0]):
                self.twoTheta+=self.twoThetaPosition
            
            try:
                self.A3 = self.kwargs.get('A3',self.sample.rotation_angle)
            except AttributeError:
                pass
        elif len(countShape) == 3: # We have 3D data! Assume A3 scan with shape (step,128*9,height)
            self.counts = self.kwargs.get('data',self.DMC.detector.data)
            self.A3 = self.kwargs.get('A3',self.sample.rotation_angle)

            if not len(self.A3) == countShape[0]:
                self.A3 = self.A3[:-1]

                #raise AttributeError("Scan performed is not an A3 scan... Sorry, I can't work with this....")

            if np.diff(self.A3).mean()>0:
                self.scanType = 'A3'
            else:
                raise AttributeError('Scan is not A3!')

            try:
                self.twoThetaPosition = self.kwargs.get('twoThetaPosition',self.DMC.detector.detector_position)
            except AttributeError:
                self.twoThetaPosition = self.kwargs.get('twoThetaPosition',np.array([0.0]))

            self.twoThetaPosition = self.twoThetaPosition[0]
            self.twoTheta = np.linspace(0,132,self.counts.shape[2])+self.twoThetaPosition
            
            
        else:
            raise AttributeError('Data file format not understood. Size of counts is {}...'.format(self.DMC.detector.data.shape))

        
        repeats = self.counts.shape[1]
        verticalPosition = self.kwargs.get('verticalPosition',np.linspace(-0.1,0.1,repeats,endpoint=True))
        
        
        self.twoTheta, z = np.meshgrid(self.twoTheta.flatten(),verticalPosition,indexing='xy')
        

        
        self.pixelPosition = np.array([self.radius*np.cos(np.deg2rad(self.twoTheta)),
                                    -self.radius*np.sin(np.deg2rad(self.twoTheta)),
                                    z]).reshape(3,*self.counts.shape[1:])
        
        
        self.Monitor = self.kwargs.get('Monitor',self.monitor)
        self.monitor = self.monitor.monitor[0]
        if self.monitor == np.array([0]): # error mode from commissioning
            self.monitor = np.ones(self.counts.shape[0])
        self.waveLength = self.kwargs.get('waveLength',self.DMC.monochromator.wavelength[0])
        #self.correctedTwoTheta = np.rad2deg(np.arccos(self.pixelPosition[0]/(np.linalg.norm(self.pixelPosition,axis=0))))
        self.alpha = np.rad2deg(np.arctan2(self.pixelPosition[2],self.radius))

        Ki = 2*np.pi/self.waveLength # length of ki
        self.ki = np.array([Ki,0.0,0.0]) # along ki with x
        self.ki.shape = (3,1,1)

        self.kf = Ki * np.array([np.cos(np.deg2rad(self.twoTheta))*np.cos(np.deg2rad(self.alpha)),
                                    -np.sin(np.deg2rad(self.twoTheta))*np.cos(np.deg2rad(self.alpha)),
                                    np.sin(np.deg2rad(self.alpha))])
        self.q = self.ki-self.kf   
        
        if len(self.DMC.detector.data.shape) == 3: # A3 Scan
            # rotate kf to correct for A3
            zero = np.zeros_like(self.A3)
            ones = np.ones_like(self.A3)
            rotMat = np.array([[np.cos(np.deg2rad(self.A3)),np.sin(np.deg2rad(self.A3)),zero],[-np.sin(np.deg2rad(self.A3)),np.cos(np.deg2rad(self.A3)),zero],[zero,zero,ones]])
            q_temp = self.ki-self.kf

            self.q = np.einsum('jki,k...->ji...',rotMat,q_temp)
            
        

        self.Q = np.linalg.norm(self.q,axis=0)
        

        self.correctedTwoTheta = 2.0*np.rad2deg(np.arcsin(self.waveLength*self.Q[0]/(4*np.pi)))[np.newaxis].repeat(self.Q.shape[0],axis=0)
        
        self.phi = np.rad2deg(np.arctan2(self.q[2],np.linalg.norm(self.q[:2],axis=0)))

        

        self.generateMask(maskingFunction=None)
            # Create a mask only containing False as to signify all points are allowed

        # Load calibration
        try:
            self.normalization, self.normalizationFile = findCalibration(self.fileName)
        except ValueError:
            self.normalizationFile = 'None'

        if self.normalizationFile == 'None':
            self.normalization = np.ones_like(self.counts,dtype=float)
        else:
            
            if self.scanType == "A3": # A3 scan
                self.normalization = np.repeat(self.normalization[np.newaxis],self.counts.shape[0],axis=0)
                self.normalization = self.normalization.transpose(0,2,1)
            else:
                self.normalization.shape = self.counts.shape

        if hasattr(self,'sample'):
            # If no temperature is saved in sample.sample_temperature
            if not hasattr(self.sample,'sample_temperature'):
                #print('No temperature... Adding zero then')
                self.sample.sample_temperature = np.array([0])
            if not hasattr(self.sample,'sample_name'):
                self.sample.sample_name = 'UNKNONW'
            #else:
            #    print('Well all is good?')
        self.time = self.Monitor.time
    #else:
    #    raise NotImplementedError("Expected data file to originate from DMC...")

    def generateMask(self,maskingFunction = maskFunction, **pars):
        """Generate maks to applied to data in data file
        
        Kwargs:

            - maskingFunction (function): Function called on self.phi to generate mask (default maskFunction)

        All other arguments are passed to the masking function.

        """

        # check if counts attribute is available

        if not hasattr(self,'counts'):
            raise RuntimeError('DataFile does not contain any counts. Look for self.counts but found nothing.')

        if maskingFunction is None:
            self.mask = np.ones_like(self.counts,dtype=bool)
        else:
            self.mask = maskingFunction(self.phi,**pars)
        
        

    def updateProperty(self,dictionary):
        """Update self with key and values from provided dictionary. Overwrites any properties already present."""
        if isinstance(dictionary,dict):
            for key,item in dictionary.items():
                if key == 'exclude': continue
                if key == 'kwargs': # copy kwargs directly and continue
                    self.kwargs = item
                    continue
                if isinstance(item,entry):
                    for key2,item2 in item.__dict__.items():
                        item.__dict__[key2] = decode(item2)
                else:
                    item = decode(item)
                    
                self.__setattr__(key,copy.deepcopy(item))
        else:
            raise AttributeError('Provided argument is not of type dictionary. Received instance of type {}'.format(type(dictionary)))


    def __eq__(self,other):
        return len(self.difference(other))==0


    def difference(self,other,keys = set(['fileName','folder'])):
        """Return the difference between two data files by keys"""
        dif = []
        if not set(self.__dict__.keys()) == set(other.__dict__.keys()): # Check if same generation and type (hdf or nxs)
            return list(set(self.__dict__.keys())-set(other.__dict__.keys()))

        comparisonKeys = keys
        for key in comparisonKeys:
            skey = self.__dict__[key]
            okey = other.__dict__[key]
            if isinstance(skey,np.ndarray):
                try:
                    if not np.all(np.isclose(skey,okey)):
                        if not np.all(np.isnan(skey),np.isnan(okey)):
                            dif.append(key)
                except (TypeError, AttributeError,ValueError):
                    if np.all(skey!=okey):
                        dif.append(key)
            elif not np.all(self.__dict__[key]==other.__dict__[key]):
                dif.append(key)
        return dif


    @_tools.KwargChecker(function=plt.errorbar,include=_tools.MPLKwargs)
    def plotDetector(self,ax=None,applyNormalization=True,**kwargs):
        """Plot intensity as function of twoTheta (and vertical position of pixel in 2D)

        Kwargs:

            - ax (axis): Matplotlib axis into which data is plotted (default None - generates new)

            - applyNormalization (bool): If true, take detector efficiency into account (default True)

            - All other key word arguments are passed on to plotting routine

        """

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.get_figure()

        
        intensity = self.counts/self.monitor.reshape(-1,1,1)
        if applyNormalization:
            intensity*=1.0/self.normalization

        count_err = np.sqrt(self.counts)
        intensity_err = count_err/self.monitor.reshape(-1,1,1)
        if applyNormalization:
            intensity_err*=1.0/self.normalization
 


        # If data is one dimensional
        if self.twoTheta.shape[1] == 1:
            if not 'fmt' in kwargs:
                kwargs['fmt'] = '.-'

            ax._err = ax.errorbar(self.twoTheta[self.mask],intensity[self.mask],intensity_err[self.mask],**kwargs)
            ax.set_xlabel(r'$2\theta$ [deg]')
            ax.set_ylabel(r'Counts/mon [arb]')

            def format_coord(ax,xdata,ydata):
                if not hasattr(ax,'xfmt'):
                    ax.mean_x_power = _tools.roundPower(np.mean(np.diff(ax._err.get_children()[0].get_data()[0])))
                    ax.xfmt = r'$2\theta$ = {:3.'+str(ax.mean_x_power)+'f} Deg'
                if not hasattr(ax,'yfmt'):
                    ymin,ymax,ystep = [f(ax._err.get_children()[0].get_data()[1]) for f in [np.min,np.max,len]]
                    
                    ax.mean_y_power = _tools.roundPower((ymax-ymin)/ystep)
                    ax.yfmt = r'Int = {:.'+str(ax.mean_y_power)+'f} cts'

                return ', '.join([ax.xfmt.format(xdata),ax.yfmt.format(ydata)])

            ax.format_coord = lambda format_xdata,format_ydata:format_coord(ax,format_xdata,format_ydata)
        else: # plot a 2D image with twoTheta vs z
            # Set all masked out points to Nan
            intensity[np.logical_not(self.mask)] = np.nan

            if 'colorbar' in kwargs:
                colorbar = kwargs['colorbar']
                del kwargs['colorbar']
            else:
                colorbar = False
            
            ax._pcolormesh = ax.pcolormesh(self.twoTheta,self.pixelPosition[2],np.sum(intensity,axis=0),shading='auto')

            if colorbar:
                ax._col = fig.colorbar(ax._pcolormesh)
                ax._col.set_label('Intensity [cts/Monitor]')
                

            ax.set_xlabel(r'$2\theta$ [deg]')
            ax.set_ylabel(r'z [m]')

        return ax

    @_tools.KwargChecker()
    def save(self,filePath):
        """Save data file in hdf format.
        
        Args:

            - filePath (path): Path into which file is to be saved

        """
        if os.path.exists(filePath):
            raise AttributeError('File already exists! ({})'.format(filePath))


    @property
    def intensity(self):
        return np.divide(self.counts,self.normalization)

    def InteractiveViewer(self,**kwargs):
        if not self.scanType.lower() in ['a3','powder'] :
            raise AttributeError('Interactive Viewer can only be used for the new data files. Either for powder or for a single crystal A3 scan')
        return InteractiveViewer.InteractiveViewer(self.intensity,self.twoTheta,self.pixelPosition,self.A3,scanParameter = 'A3',scanValueUnit='deg',colorbar=True,**kwargs)