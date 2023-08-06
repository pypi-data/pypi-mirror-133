# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 17:28:37 2021

@author: Sebastian Menze, sebastian.menze@gmail.com
"""

def start():
    
    import sys
    import matplotlib
    # matplotlib.use('Qt5Agg')
    
    from PyQt5 import QtCore, QtGui, QtWidgets
    
    # from PyQt5.QtWidgets import QShortcut
    # from PyQt5.QtGui import QKeySequence
    
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    
    import scipy.io.wavfile as wav
    
    import soundfile as sf
    
    
    from scipy import signal
    import numpy as np
    from matplotlib import pyplot as plt
    import pandas as pd
    import datetime as dt
    import time
    import os
    
    from matplotlib.widgets import RectangleSelector
    
    
    # from pydub import AudioSegment
    # from pydub.playback import play
    # import threading
    
    import simpleaudio as sa
    
    
    class MplCanvas(FigureCanvasQTAgg ):
    
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.fig.add_subplot(111)
            super(MplCanvas, self).__init__(self.fig)
    
    
    
    class MainWindow(QtWidgets.QMainWindow):
    
        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)
    
            self.canvas =  MplCanvas(self, width=5, height=4, dpi=150)
                    
            # self.call_time=pd.Series()
            # self.call_frec=pd.Series()
            
            self.f_min = QtWidgets.QLineEdit(self)
            self.f_min.setText('10')
            self.f_max = QtWidgets.QLineEdit(self)
            self.f_max.setText('16000')
            self.t_length = QtWidgets.QLineEdit(self)
            self.t_length.setText('120')
            self.db_saturation=QtWidgets.QLineEdit(self)
            self.db_saturation.setText('155')
            self.db_vmin=QtWidgets.QLineEdit(self)
            self.db_vmin.setText('30')
            self.db_vmax=QtWidgets.QLineEdit(self)
            self.db_vmax.setText('')       
            # self.fft_size = QtWidgets.QLineEdit(self)
            # self.fft_size.setText('32768')
            self.fft_size = QtWidgets.QComboBox(self)
            self.fft_size.addItem('1024')        
            self.fft_size.addItem('2048')        
            self.fft_size.addItem('4096')        
            self.fft_size.addItem('8192')        
            self.fft_size.addItem('16384')        
            self.fft_size.addItem('32768')        
            self.fft_size.addItem('65536')    
            self.fft_size.addItem('131072')    
            self.fft_size.setCurrentIndex(4)
            
            
            self.colormap_plot = QtWidgets.QComboBox(self)
            self.colormap_plot.addItem('plasma')        
            self.colormap_plot.addItem('viridis')        
            self.colormap_plot.addItem('inferno')        
            self.colormap_plot.addItem('gist_gray')           
            self.colormap_plot.addItem('gist_yarg')           
            self.colormap_plot.setCurrentIndex(2)
            
            self.checkbox_logscale=QtWidgets.QCheckBox('log scale')
            self.checkbox_logscale.setChecked(True)
            self.checkbox_background=QtWidgets.QCheckBox('Remove background')
            self.checkbox_background.setChecked(False)
            
            self.fft_overlap = QtWidgets.QLineEdit(self)
            self.fft_overlap.setText('0.9')
     
            self.filename_timekey = QtWidgets.QLineEdit(self)
            self.filename_timekey.setText('aural_%Y_%m_%d_%H_%M_%S.wav')       
     
            self.playbackspeed = QtWidgets.QComboBox(self)
            self.playbackspeed.addItem('0.5')        
            self.playbackspeed.addItem('1')        
            self.playbackspeed.addItem('2')        
            self.playbackspeed.addItem('5')        
            self.playbackspeed.addItem('10')        
            self.playbackspeed.setCurrentIndex(1)
            
            
            self.time= dt.datetime.now()
            self.f=None
            self.t=[-1,-1]
            self.Sxx=None
            self.draw_x=pd.Series(dtype='float')
            self.draw_y=pd.Series(dtype='float')
            self.cid1=None
            self.cid2=None
            
            self.plotwindow_startsecond=0
            # self.plotwindow_length=120
            self.filecounter=-1
            self.filenames=np.array( [] )
            self.current_audiopath=None
    
            
            openfilebutton=QtWidgets.QPushButton('Open files')
            def openfilefunc():
                self.filecounter=-1         
                self.annotation= pd.DataFrame({'t1': pd.Series(dtype='datetime64[ns]'),
                       't2': pd.Series(dtype='datetime64[ns]'),
                       'f1': pd.Series(dtype='float'),
                       'f2': pd.Series(dtype='float'),
                       'label': pd.Series(dtype='object')   })
                
                # self.annotation=pd.DataFrame(columns=['t1','t2','f1','f2','label'],dtype=[("t1", "datetime64[ns]"), ("t2", "datetime64[ns]"), ("f1", "float"), ("f2", "float"), ("label", "object")] )
                
                # annotation=pd.DataFrame(dtype=[("t1", "datetime64[ns]"), ("t2", "datetime64[ns]"), ("f1", "float"), ("f2", "float"), ("label", "object")] )
    
                # ,dtype=('datetime64[ns]','datetime64[ns]','float','float','object'))
                # self.call_t_1=pd.Series(dtype='datetime64[ns]')
                # self.call_f_1=pd.Series(dtype='float')            
                # self.call_t_2=pd.Series(dtype='datetime64[ns]')
                # self.call_f_2=pd.Series(dtype='float') 
                # self.call_label=pd.Series(dtype='object')            
    
                options = QtWidgets.QFileDialog.Options()
                # options |= QtWidgets.QFileDialog.DontUseNativeDialog
                self.filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", r"C:\Users\a5278\Documents\passive_acoustics\detector_delevopment\detector_validation_subset","Audio Files (*.wav *.aif *.aiff *.aifc *.ogg *.flac)", options=options)
                self.filenames = np.array( self.filenames )
                print(self.filenames)
            openfilebutton.clicked.connect(openfilefunc)
            
            
            def read_wav():
              if self.filecounter>=0:        
                self.current_audiopath=self.filenames[self.filecounter]
                
                # if self.filename_timekey.text()=='':
                #     self.time= dt.datetime(1,1,1,0,0,0)
                # else:     
                #     self.time= dt.datetime.strptime( audiopath.split('/')[-1], self.filename_timekey.text() )
               
                if self.filename_timekey.text()=='':
                    # self.time= dt.datetime(1,1,1,0,0,0)
                    self.time= dt.datetime.now()
                else:     
                    try:
                        self.time= dt.datetime.strptime( self.current_audiopath.split('/')[-1], self.filename_timekey.text() )
                    except: 
                        print('wrongfilename')
                
                # if audiopath[-4:]=='.wav':
                    
                    
                self.x,self.fs  =  sf.read(self.current_audiopath,dtype='int16')
    
                # if audiopath[-4:]=='.aif' | audiopath[-4:]=='.aiff' | audiopath[-4:]=='.aifc':
                #     obj = aifc.open(audiopath,'r')
                #     self.fs, self.x = wav.read(audiopath)     
                print('open new file: '+self.current_audiopath)
                print('FS: '+str(self.fs) +' x: '+str(np.shape(self.x)))
                if len(self.x.shape)>1:
                    if np.shape(self.x)[1]>1:
                        self.x=self.x[:,0]
    
                # factor=60
                # x=signal.decimate(x,factor,ftype='fir')
                
                db_saturation=float( self.db_saturation.text() )
                x=self.x/32767 
                p =np.power(10,(db_saturation/20))*x #convert data.signal to uPa    
                
                fft_size=int( self.fft_size.currentText() )
                fft_overlap=float(  self.fft_overlap.text() )
                self.f, self.t, self.Sxx = signal.spectrogram(p, self.fs, window='hamming',nperseg=fft_size,noverlap=int(fft_size*fft_overlap))
                # self.t=self.time +  pd.to_timedelta( t  , unit='s')           
            
            def plot_annotation_box(annotation_row):
                print('row:')
                # print(annotation_row.dtypes)
                x1=annotation_row.iloc[0,0]
                x2=annotation_row.iloc[0,1]
                
                xt=pd.Series([x1,x2])
                print(xt)
                print(xt.dtype)
    
                # print(np.dtype(np.array(self.time).astype('datetime64[ns]') ))
                tt=xt - np.array(self.time).astype('datetime64[ns]')  
                xt=tt.dt.seconds + tt.dt.microseconds/10**6
                x1=xt[0]
                x2=xt[1]
                
                # tt=x1 - np.array(self.time).astype('datetime64[ns]')  
                # x1=tt.dt.seconds + tt.dt.microseconds/10**6
                # tt=x2 - np.array(self.time).astype('datetime64[ns]')  
                # x2=tt.dt.seconds + tt.dt.microseconds/10**6
       
                y1=annotation_row.iloc[0,2]
                y2=annotation_row.iloc[0,3]
                c_label=annotation_row.iloc[0,4]
                
                line_x=[x2,x1,x1,x2,x2]
                line_y=[y1,y1,y2,y2,y1]
                
                xmin=np.min([x1,x2])
                ymax=np.max([y1,y2])
                
                self.canvas.axes.plot(line_x,line_y,'-b',linewidth=.75)
                self.canvas.axes.text(xmin,ymax,c_label,size=5)
                  
                
                
            def plot_spectrogram():
             if self.filecounter>=0:
                # self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
                # self.setCentralWidget(self.canvas)
                self.canvas.fig.clf() 
                self.canvas.axes = self.canvas.fig.add_subplot(111)
                # self.canvas.axes.cla()
                
                if self.t_length.text()=='':
                    self.plotwindow_length= self.t[-1] 
                    self.plotwindow_startsecond=0
                else:    
                    self.plotwindow_length=float( self.t_length.text() )
                    if self.t[-1]<self.plotwindow_length:
                        self.plotwindow_startsecond=0
                        self.plotwindow_length=self.t[-1]
                        
                y1=int(self.f_min.text())    
                y2=int(self.f_max.text())    
                if y2>(self.fs/2):
                    y2=(self.fs/2)
                t1=self.plotwindow_startsecond
                t2=self.plotwindow_startsecond+self.plotwindow_length
                
                # if self.t_length.text=='':
                #     t2=self.t[-1]
                # else:    
                #     if self.t[-1]<float(self.t_length.text()):
                #         t2=self.t[-1]
                #     else:    
                #         t2=self.plotwindow_startsecond+self.plotwindow_length
                        
                # tt,ff=np.meshgrid(self.t,self.f)
                # ix_time=(tt>=self.plotwindow_startsecond) & (tt<(self.plotwindow_startsecond+self.plotwindow_length))
                # ix_f=(ff>=y1) & (ff<y2)
                # plotsxx=self.Sxx[ ix_f & ix_time]
                ix_time=np.where( (self.t>=t1) & (self.t<t2 ))[0]
                ix_f=np.where((self.f>=y1) & (self.f<y2))[0]
                # print(ix_time.shape)
                # print(ix_f.shape)
                plotsxx= self.Sxx[ int(ix_f[0]):int(ix_f[-1]),int(ix_time[0]):int(ix_time[-1]) ] 
                plotsxx_db=10*np.log10(plotsxx)
                
                if self.checkbox_background.isChecked():
                   spec_mean=np.median(plotsxx_db,axis=1) 
                   sxx_background=np.transpose(np.broadcast_to(spec_mean,np.transpose(plotsxx_db).shape))
                   plotsxx_db = plotsxx_db - sxx_background
                   plotsxx_db=plotsxx_db - np.min(plotsxx_db.flatten())
                # print(plotsxx.shape)
      
                # img=self.canvas.axes.pcolormesh(self.t, self.f, 10*np.log10(self.Sxx) ,cmap='plasma')
                colormap_plot=self.colormap_plot.currentText()
                img=self.canvas.axes.imshow( plotsxx_db , aspect='auto',cmap=colormap_plot,origin = 'lower',extent = [t1, t2, y1, y2])
              
                # img=self.canvas.axes.pcolormesh(self.t[ int(ix_time[0]):int(ix_time[-1])], self.f[int(ix_f[0]):int(ix_f[-1])], 10*np.log10(plotsxx) , shading='flat',cmap='plasma')
    
                
                self.canvas.axes.set_ylabel('Frequency [Hz]')
                self.canvas.axes.set_xlabel('Time [sec]')
                if self.checkbox_logscale.isChecked():
                    self.canvas.axes.set_yscale('log')
                else:
                    self.canvas.axes.set_yscale('linear')        
                    
     
    
                
                if self.filename_timekey.text()=='':
                    # audiopath=self.filenames[self.filecounter]
                    self.canvas.axes.set_title(self.current_audiopath.split('/')[-1])
                else:     
                    self.canvas.axes.set_title(self.time)
    
                # img.set_clim([ 40 ,10*np.log10( np.max(np.array(plotsxx).ravel() )) ] )
                clims=img.get_clim()
                if (self.db_vmin.text()=='') & (self.db_vmax.text()!=''):
                    img.set_clim([ clims[0] , float(self.db_vmax.text())] )
                if (self.db_vmin.text()!='') & (self.db_vmax.text()==''):
                    img.set_clim([ float(self.db_vmin.text()) ,clims[1]] )
                if (self.db_vmin.text()!='') & (self.db_vmax.text()!=''):
                    img.set_clim([ float(self.db_vmin.text()) ,float(self.db_vmax.text()) ] )        
                    
                self.canvas.fig.colorbar(img,label='PSD [dB re $1 \ \mu Pa \ Hz^{-1}$]')
                
                # print(self.time)        
                # print(self.call_time)
    
            # plot annotations
                if self.annotation.shape[0]>0:
                     ix=(self.annotation['t1'] > (np.array(self.time).astype('datetime64[ns]')+pd.Timedelta(self.plotwindow_startsecond, unit="s") )  ) & (self.annotation['t1'] < (np.array(self.time).astype('datetime64[ns]')+pd.Timedelta(self.plotwindow_startsecond+self.plotwindow_length, unit="s") )  )          
                     if np.sum(ix)>0:
                         ix=np.where(ix)[0]
                         print('ix is')
                         print(ix)
                         for ix_x in ix:
                           a= pd.DataFrame([self.annotation.iloc[ix_x,:] ])
                           print(a)
                           plot_annotation_box(a)
              
       
                  
                self.canvas.axes.set_ylim([y1,y2])
                self.canvas.axes.set_xlim([t1,t2])
                          
                    
                self.canvas.fig.tight_layout()
                toggle_selector.RS=RectangleSelector(self.canvas.axes, box_select_callback,
                                           drawtype='box', useblit=False,
                                           button=[1],  # disable middle button                                  
                                           interactive=False,rectprops=dict(facecolor="blue", edgecolor="black", alpha=0.1, fill=True))
    
    
                self.canvas.draw()
                self.cid1=self.canvas.fig.canvas.mpl_connect('button_press_event', onclick)
        
            def box_select_callback(eclick, erelease):
    
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
    
                x1 =self.time +  pd.to_timedelta( x1 , unit='s') 
                x2 =self.time +  pd.to_timedelta( x2 , unit='s') 
                
                # sort to increasing values
                t1=np.min([x1,x2])
                t2=np.max([x1,x2])
                f1=np.min([y1,y2])
                f2=np.max([y1,y2])
                
                if self.bg.checkedId()==-1:
                    c_label=''
                else:
                    c_label=eval( 'self.an_'+str(self.bg.checkedId())+'.text()' )
                
                # a=pd.DataFrame(columns=['t1','t2','f1','f2','label'])
                # a.iloc[0,:]=np.array([x1,x2,y1,y2,c_label ])
                a=pd.DataFrame({'t1': pd.Series(t1,dtype='datetime64[ns]'),
                       't2': pd.Series(t2,dtype='datetime64[ns]'),
                       'f1': pd.Series(f1,dtype='float'),
                       'f2': pd.Series(f2,dtype='float'),
                       'label': pd.Series(c_label,dtype='object')   })
                
                # a=pd.DataFrame(data=[ [x1,x2,y1,y2,c_label ] ],columns=['t1','t2','f1','f2','label'])
                # print('a:')
                # print(a.dtypes)
                # self.annotation.append(a, ignore_index = True)
                self.annotation=pd.concat([ self.annotation ,a ] , ignore_index = True)
    
                # print(self.annotation.dtypes)  
                plot_annotation_box(a)
    
            def toggle_selector(event):
                # toggle_selector.RS.set_active(True)
                print('select')
                # if event.key == 't':
                #     if toggle_selector.RS.active:
                #         print(' RectangleSelector deactivated.')
                #         toggle_selector.RS.set_active(False)
                #     else:
                #         print(' RectangleSelector activated.')
                #         toggle_selector.RS.set_active(True)
            
    
    
            def onclick(event):
                if event.button==3:
                    self.annotation=self.annotation.head(-1)
                    # print(self.annotation)            
                    plot_spectrogram()              
            
            def end_of_filelist_warning(): 
                msg_listend = QtWidgets.QMessageBox()
                msg_listend.setIcon(QtWidgets.QMessageBox.Information)
                msg_listend.setText("End of file list reached!")
                msg_listend.exec_()
    
            def plot_next_spectro():
             if len(self.filenames)>0:
                print('old filecounter is: '+str(self.filecounter))
               
                if self.t_length.text()=='' or self.t[-1]<float(self.t_length.text()):
                    self.filecounter=self.filecounter+1
                    if self.filecounter>self.filenames.shape[0]-1:
                        self.filecounter=self.filenames.shape[0]-1
                        print('That was it')
                        end_of_filelist_warning()  
                    self.plotwindow_length= self.t[-1] 
                    self.plotwindow_startsecond=0
                    # new file    
                    # self.filecounter=self.filecounter+1
                    read_wav()
                    plot_spectrogram()
                        
                else:    
                    self.plotwindow_length=float( self.t_length.text() )       
                    self.plotwindow_startsecond=self.plotwindow_startsecond + self.plotwindow_length
                    
                print( [self.plotwindow_startsecond,  self.t[-1] ] )
                
                if self.plotwindow_startsecond > self.t[-1]:              
                    #save log
                    if checkbox_log.isChecked():
                        
                        tt= self.annotation['t1'] - self.time             
                        t_in_seconds=np.array( tt.values*1e-9 ,dtype='float16')
                        reclength=np.array( self.t[-1] ,dtype='float16')
        
                        ix=(t_in_seconds>0) & (t_in_seconds<reclength)
                        
                        calldata=self.annotation.iloc[ix,:]
                        print(calldata)
                        savename=self.current_audiopath
                        calldata.to_csv(savename[:-4]+'_log.csv')                  
                        print('writing log: '+savename[:-4]+'_log.csv')
                    # new file    
                    self.filecounter=self.filecounter+1
                    if self.filecounter>=self.filenames.shape[0]-1:
                        self.filecounter=self.filenames.shape[0]-1
                        print('That was it')
                        end_of_filelist_warning()  
                    read_wav()
                    self.plotwindow_startsecond=0
                    plot_spectrogram()
                else:
                    plot_spectrogram()
             
    
                        
            def plot_previous_spectro():
             if len(self.filenames)>0:   
                print('old filecounter is: '+str(self.filecounter))
             
                if self.t_length.text()=='' or self.t[-1]<float(self.t_length.text()):
                    self.filecounter=self.filecounter-1
                    if self.filecounter<0:
                        self.filecounter=0
                        print('That was it')
                        end_of_filelist_warning()  
                    self.plotwindow_length= self.t[-1] 
                    self.plotwindow_startsecond=0
                    # new file    
                    # self.filecounter=self.filecounter+1
                    read_wav()
                    plot_spectrogram()
                    
                else:                
                    self.plotwindow_startsecond=self.plotwindow_startsecond -self.plotwindow_length
                    print( [self.plotwindow_startsecond,  self.t[-1] ] )      
                    if self.plotwindow_startsecond < 0: 
                        self.plotwindow_startsecond = self.t[-1] + self.plotwindow_startsecond                
                        # old file    
                        self.filecounter=self.filecounter-1
                        if self.filecounter<0:
                            self.filecounter=0
                            print('That was it')
                            end_of_filelist_warning()  
                        
                        # if self.filecounter<0:
                        #     print('That was it')
                        #     self.canvas.fig.clf() 
                        #     self.canvas.axes = self.canvas.fig.add_subplot(111)
                        #     self.canvas.axes.set_title('That was it')
                        #     self.canvas.draw()                 
                        # elif self.filecounter>=self.filenames.shape[0]-1:
                        #     print('That was it')
                        #     self.canvas.fig.clf() 
                        #     self.canvas.axes = self.canvas.fig.add_subplot(111)
                        #     self.canvas.axes.set_title('That was it')
                        #     self.canvas.draw()
       
                        read_wav()
                        # self.plotwindow_startsecond=0
                        plot_spectrogram()
                    else:
                        plot_spectrogram()
             
                    
             
            def new_fft_size_selected():
                 read_wav()
                 plot_spectrogram()
            self.fft_size.currentIndexChanged.connect(new_fft_size_selected)
    
            self.colormap_plot.currentIndexChanged.connect( plot_spectrogram)
            self.checkbox_background.stateChanged.connect(plot_spectrogram  )      
            self.checkbox_logscale.stateChanged.connect(plot_spectrogram   )         
             
                            
            # self.canvas.fig.canvas.mpl_connect('button_press_event', onclick)
            # self.canvas.fig.canvas.mpl_connect('key_press_event', toggle_selector)
    
    
            
            # QtGui.QShortcut(QtCore.Qt.Key_Right, MainWindow, plot_next_spectro())
            # self.msgSc = QShortcut(QKeySequence(u"\u2192"), self)
            # self.msgSc.activated.connect(plot_next_spectro)
            button_plot_spectro=QtWidgets.QPushButton('Next spectrogram-->')
            button_plot_spectro.clicked.connect(plot_next_spectro)
            
            button_plot_prevspectro=QtWidgets.QPushButton('<--Previous spectrogram')
            button_plot_prevspectro.clicked.connect(plot_previous_spectro)
        
            button_save=QtWidgets.QPushButton('Save annotation csv')
            def func_savecsv():         
                options = QtWidgets.QFileDialog.Options()
                savename = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", r"C:\Users\a5278\Documents\passive_acoustics\detector_delevopment\detector_validation_subset", "csv files (*.csv)",options=options)
                print('location is:' + savename[0])
                if len(savename[0])>0:
                    self.annotation.to_csv(savename[0])         
            button_save.clicked.connect(func_savecsv)
            
            button_quit=QtWidgets.QPushButton('Quit')
            button_quit.clicked.connect(QtWidgets.QApplication.instance().quit)
            
            
            
            def func_logging():    
                if checkbox_log.isChecked():
                    print('logging')
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)   
                    msg.setText("Overwrite existing log files?")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    returnValue = msg.exec()
                    if returnValue == QtWidgets.QMessageBox.No:
                                     
                        ix_delete=[]
                        i=0
                        for fn in self.filenames:
                            logpath=fn[:-4]+'_log.csv'
                            # print(logpath)
                            if os.path.isfile( logpath):
                                ix_delete.append(i)    
                            i=i+1
                        # print(ix_delete)
            
                        self.filenames=np.delete(self.filenames,ix_delete)
                        print('Updated filelist:')
                        print(self.filenames)
                    
    
    
            checkbox_log=QtWidgets.QCheckBox('Real-time Logging')
            checkbox_log.toggled.connect(func_logging)
            
            button_plot_all_spectrograms=QtWidgets.QPushButton('Plot all spectrograms')
            def plot_all_spectrograms():         
                
               msg = QtWidgets.QMessageBox()
               msg.setIcon(QtWidgets.QMessageBox.Information)   
               msg.setText("Are you sure you want to plot "+ str(self.filenames.shape[0]) +" spectrograms?")
               msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
               returnValue = msg.exec()
    
               if returnValue == QtWidgets.QMessageBox.Yes:
                    for audiopath in self.filenames:
                                        
                        if self.filename_timekey.text()=='':
                            self.time= dt.datetime.now()
                        else:  
                            try:
                                self.time= dt.datetime.strptime( audiopath.split('/')[-1], self.filename_timekey.text() )
                            except:
                                self.time= dt.datetime.now()
                                
                        self.x,self.fs  =  sf.read(audiopath,dtype='int16')
                        print('open new file: '+audiopath)
                        
                        db_saturation=float( self.db_saturation.text() )
                        x=self.x/32767 
                        p =np.power(10,(db_saturation/20))*x #convert data.signal to uPa    
                        
                        fft_size=int( self.fft_size.currentText() )
                        fft_overlap=float(  self.fft_overlap.text() )
                        
                        
                        self.f, self.t, self.Sxx = signal.spectrogram(p, self.fs, window='hamming',nperseg=fft_size,noverlap=fft_size*fft_overlap)
                        
                        self.plotwindow_startsecond=0
                        
                        plot_spectrogram()
                        self.canvas.axes.set_title(audiopath.split('/')[-1])
                        self.canvas.fig.savefig( audiopath[:-4]+'.jpg',dpi=150 )    
                
                
            button_plot_all_spectrograms.clicked.connect(plot_all_spectrograms)        
    
            button_draw_shape=QtWidgets.QPushButton('Draw shape')
            def func_draw_shape_plot(): 
                   if self.filecounter>=0:
                        self.canvas.fig.clf() 
                        self.canvas.axes = self.canvas.fig.add_subplot(111)                    
                        if self.t_length.text()=='':
                            self.plotwindow_length= self.t[-1] 
                            self.plotwindow_startsecond=0
                        else:    
                            self.plotwindow_length=float( self.t_length.text() )
                            if self.t[-1]<self.plotwindow_length:
                                self.plotwindow_startsecond=0
                                self.plotwindow_length=self.t[-1]
                                
                        y1=int(self.f_min.text())    
                        y2=int(self.f_max.text())    
                        if y2>(self.fs/2):
                            y2=(self.fs/2)
                        t1=self.plotwindow_startsecond
                        t2=self.plotwindow_startsecond+self.plotwindow_length
                    
                        ix_time=np.where( (self.t>=t1) & (self.t<t2 ))[0]
                        ix_f=np.where((self.f>=y1) & (self.f<y2))[0]
    
                        plotsxx= self.Sxx[ int(ix_f[0]):int(ix_f[-1]),int(ix_time[0]):int(ix_time[-1]) ] 
                        plotsxx_db=10*np.log10(plotsxx)
                        
                        if self.checkbox_background.isChecked():
                           spec_mean=np.median(plotsxx_db,axis=1) 
                           sxx_background=np.transpose(np.broadcast_to(spec_mean,np.transpose(plotsxx_db).shape))
                           plotsxx_db = plotsxx_db - sxx_background
                           plotsxx_db=plotsxx_db - np.min(plotsxx_db.flatten())
              
                        colormap_plot=self.colormap_plot.currentText()
                        img=self.canvas.axes.imshow( plotsxx_db , aspect='auto',cmap=colormap_plot,origin = 'lower',extent = [t1, t2, y1, y2])
                                            
                        self.canvas.axes.set_ylabel('Frequency [Hz]')
                        self.canvas.axes.set_xlabel('Time [sec]')
                        if self.checkbox_logscale.isChecked():
                            self.canvas.axes.set_yscale('log')
                        else:
                            self.canvas.axes.set_yscale('linear')        
                            
                        if self.filename_timekey.text()=='':
                            self.canvas.axes.set_title(self.current_audiopath.split('/')[-1])
                        else:     
                            self.canvas.axes.set_title(self.time)
            
                        clims=img.get_clim()
                        if (self.db_vmin.text()=='') & (self.db_vmax.text()!=''):
                            img.set_clim([ clims[0] , float(self.db_vmax.text())] )
                        if (self.db_vmin.text()!='') & (self.db_vmax.text()==''):
                            img.set_clim([ float(self.db_vmin.text()) ,clims[1]] )
                        if (self.db_vmin.text()!='') & (self.db_vmax.text()!=''):
                            img.set_clim([ float(self.db_vmin.text()) ,float(self.db_vmax.text()) ] )        
                            
                        self.canvas.fig.colorbar(img,label='PSD [dB re $1 \ \mu Pa \ Hz^{-1}$]')
                        
                    # plot annotations
                        if self.annotation.shape[0]>0:
                             ix=(self.annotation['t1'] > (np.array(self.time).astype('datetime64[ns]')+pd.Timedelta(self.plotwindow_startsecond, unit="s") )  ) & (self.annotation['t1'] < (np.array(self.time).astype('datetime64[ns]')+pd.Timedelta(self.plotwindow_startsecond+self.plotwindow_length, unit="s") )  )          
                             if np.sum(ix)>0:
                                 ix=np.where(ix)[0]
                                 print('ix is')
                                 print(ix)
                                 for ix_x in ix:
                                   a= pd.DataFrame([self.annotation.iloc[ix_x,:] ])
                                   print(a)
                                   plot_annotation_box(a)
                                   
                        if self.t_limits==None:           
                            self.canvas.axes.set_ylim([y1,y2])
                            self.canvas.axes.set_xlim([t1,t2])
                        else:
                          self.canvas.axes.set_ylim(self.f_limits)
                          self.canvas.axes.set_xlim(self.t_limits)
                     
     
                                                      
                        self.canvas.fig.tight_layout()
                    
                        self.canvas.axes.plot(self.draw_x,self.draw_y,'.-g')
      
                        self.canvas.draw()    
                        self.cid2=self.canvas.fig.canvas.mpl_connect('button_press_event', onclick_draw)
                        
            def onclick_draw(event):
                    # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                    #       ('double' if event.dblclick else 'single', event.button,
                    #        event.x, event.y, event.xdata, event.ydata))
                    if event.button==1 & event.dblclick:
                        self.draw_x=self.draw_x.append( pd.Series(event.xdata) ,ignore_index=True )
                        self.draw_y=self.draw_y.append( pd.Series(event.ydata) ,ignore_index=True )
                        self.f_limits=self.canvas.axes.get_ylim()
                        self.t_limits=self.canvas.axes.get_xlim()                              
                        func_draw_shape_plot()   
                      
                    if event.button==3:
                        self.draw_x=self.draw_x.head(-1)
                        self.draw_y=self.draw_y.head(-1)
                        self.f_limits=self.canvas.axes.get_ylim()
                        self.t_limits=self.canvas.axes.get_xlim()
                        func_draw_shape_plot()              
     
            def func_draw_shape_exit():
                print('save shape' + str(self.draw_x.shape))
                self.canvas.fig.canvas.mpl_disconnect(self.cid2)
                plot_spectrogram()
                print('back to boxes')
                if self.draw_x.shape[0]>0:
                    options = QtWidgets.QFileDialog.Options()
                    savename = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "csv files (*.csv)",options=options)
                    if len(savename[0])>0:     
                        if savename[:-4]!='.csv':
                            savename=savename[0]+'.csv'
                        # drawcsv=pd.concat([self.draw_x,self.draw_y],axis=1)
                        drawcsv=pd.DataFrame(columns=['Time_in_s','Frequency_in_Hz'])
                        drawcsv['Time_in_s']=self.draw_x
                        drawcsv['Frequency_in_Hz']=self.draw_y
                        drawcsv.to_csv(savename)   
                        
            self.drawexitm = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
            self.drawexitm.activated.connect(func_draw_shape_exit)  
    
            def func_draw_shape():                  
               msg = QtWidgets.QMessageBox()
               msg.setIcon(QtWidgets.QMessageBox.Information)   
               msg.setText("Add points with double left click.\nRemove latest point with single right click. \nExit draw mode and save CSV by pushing enter")
               msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
               returnValue = msg.exec()    
               if returnValue == QtWidgets.QMessageBox.Ok:
                   print('drawing')  
                   self.draw_x=pd.Series(dtype='float')
                   self.draw_y=pd.Series(dtype='float')
                   self.f_limits=self.canvas.axes.get_ylim()
                   self.t_limits=self.canvas.axes.get_xlim()
                   self.canvas.fig.canvas.mpl_disconnect(self.cid1)
                   func_draw_shape_plot()                                                                           
            button_draw_shape.clicked.connect(func_draw_shape)
            
            ####### play audio
            button_play_audio=QtWidgets.QPushButton('Play/Stop [spacebar]')
            def func_playaudio():
                if self.filecounter>=0:
                    if not hasattr(self, "play_obj"):
                        new_rate = 32000          
        
                        t_limits=self.canvas.axes.get_xlim()
                        f_limits=list(self.canvas.axes.get_ylim())
                        if f_limits[1]>=(self.fs/2):
                            f_limits[1]= self.fs/2-10
                        print(t_limits)
                        print(f_limits)
    
                        x_select=self.x[int(t_limits[0]*self.fs) : int(t_limits[1]*self.fs) ]     
                        
                        sos=signal.butter(8, f_limits, 'bandpass', fs=self.fs, output='sos')
                        x_select = signal.sosfilt(sos, x_select)
                        
                        number_of_samples = round(len(x_select) * (float(new_rate)/ float(self.playbackspeed.currentText())) / self.fs)
                        x_resampled = np.array(signal.resample(x_select, number_of_samples)).astype('int')            
                       
                        #normalize sound level
                        maximum_x=32767*0.8
                        old_max=np.max(np.abs([x_resampled.min(),x_resampled.max()]))
                        x_resampled=x_resampled * (maximum_x/old_max)
                        x_resampled = x_resampled.astype(np.int16)
    
                        print( [x_resampled.min(),x_resampled.max()]  )                   
                        wave_obj = sa.WaveObject(x_resampled, 1, 2, new_rate)
                        self.play_obj = wave_obj.play()   
                    else:    
                        if self.play_obj.is_playing():
                            sa.stop_all()
                        else:    
                            new_rate = 32000          
                            t_limits=self.canvas.axes.get_xlim()
                            f_limits=list(self.canvas.axes.get_ylim())
                            if f_limits[1]>=(self.fs/2):
                                f_limits[1]= self.fs/2-10
                            print(t_limits)
                            print(f_limits)
                        
                            x_select=self.x[int(t_limits[0]*self.fs) : int(t_limits[1]*self.fs) ]    
                            sos=signal.butter(8, f_limits, 'bandpass', fs=self.fs, output='sos')
                            x_select = signal.sosfilt(sos, x_select)
                        
                            # number_of_samples = round(len(x_select) * float(new_rate) / self.fs)
                            number_of_samples = round(len(x_select) * (float(new_rate)/ float(self.playbackspeed.currentText())) / self.fs)
    
                            x_resampled = np.array(signal.resample(x_select, number_of_samples)).astype('int')            
                             #normalize sound level
                            maximum_x=32767*0.8
                            old_max=np.max(np.abs([x_resampled.min(),x_resampled.max()]))
                            x_resampled=x_resampled * (maximum_x/old_max)
                            x_resampled = x_resampled.astype(np.int16)
                            print( [x_resampled.min(),x_resampled.max()]  )
                            wave_obj = sa.WaveObject(x_resampled, 1, 2, new_rate)
                            self.play_obj = wave_obj.play()
                
            button_play_audio.clicked.connect(func_playaudio)        
            
            button_save_audio=QtWidgets.QPushButton('Export selected audio')         
            def func_saveaudio():
                if self.filecounter>=0:
                    options = QtWidgets.QFileDialog.Options()
                    savename = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "wav files (*.wav)",options=options)
                    if len(savename[0])>0:     
                        savename=savename[0]
                        new_rate = 32000          
        
                        t_limits=self.canvas.axes.get_xlim()
                        f_limits=list(self.canvas.axes.get_ylim())
                        if f_limits[1]>=(self.fs/2):
                            f_limits[1]= self.fs/2-10
                        print(t_limits)
                        print(f_limits)
                        x_select=self.x[int(t_limits[0]*self.fs) : int(t_limits[1]*self.fs) ]     
                        
                        sos=signal.butter(8, f_limits, 'bandpass', fs=self.fs, output='sos')
                        x_select = signal.sosfilt(sos, x_select)
                                           
                        number_of_samples = round(len(x_select) * (float(new_rate)/ float(self.playbackspeed.currentText())) / self.fs)
                        x_resampled = np.array(signal.resample(x_select, number_of_samples)).astype('int') 
                                            #normalize sound level
                        maximum_x=32767*0.8
                        old_max=np.max(np.abs([x_resampled.min(),x_resampled.max()]))
                        x_resampled=x_resampled * (maximum_x/old_max)
                        x_resampled = x_resampled.astype(np.int16)
                        
                        if savename[:-4]!='.wav':
                            savename=savename+'.wav'
                        wav.write(savename, new_rate, x_resampled)
            button_save_audio.clicked.connect(func_saveaudio)        
              
            ######## layout
            outer_layout = QtWidgets.QVBoxLayout()
            
            top_layout = QtWidgets.QHBoxLayout()       
            
            top_layout.addWidget(openfilebutton)
            top_layout.addWidget(checkbox_log)
            top_layout.addWidget(button_plot_prevspectro)
            top_layout.addWidget(button_plot_spectro)
            top_layout.addWidget(button_plot_all_spectrograms)
            top_layout.addWidget(button_play_audio)
            top_layout.addWidget(QtWidgets.QLabel('Playback speed:'))        
            top_layout.addWidget(self.playbackspeed)
            top_layout.addWidget(button_save_audio)            
            top_layout.addWidget(button_draw_shape)            
    
            top_layout.addWidget(button_save)            
            top_layout.addWidget(button_quit)
    
            top2_layout = QtWidgets.QHBoxLayout()   
            
            # self.f_min = QtWidgets.QLineEdit(self)
            # self.f_max = QtWidgets.QLineEdit(self)
            # self.t_start = QtWidgets.QLineEdit(self)
            # self.t_end = QtWidgets.QLineEdit(self)
            # self.fft_size = QtWidgets.QLineEdit(self)
            top2_layout.addWidget(QtWidgets.QLabel('filename key:'))        
            top2_layout.addWidget(self.filename_timekey)
            top2_layout.addWidget(QtWidgets.QLabel('f_min[Hz]:'))
            top2_layout.addWidget(self.f_min)     
            top2_layout.addWidget(QtWidgets.QLabel('f_max[Hz]:'))
            top2_layout.addWidget(self.f_max)
            top2_layout.addWidget(QtWidgets.QLabel('Spectrogram length [sec]:'))
            top2_layout.addWidget(self.t_length)
     
            top2_layout.addWidget(QtWidgets.QLabel('fft_size[bits]:'))
            top2_layout.addWidget(self.fft_size) 
            top2_layout.addWidget(QtWidgets.QLabel('fft_overlap[0-1]:'))
            top2_layout.addWidget(self.fft_overlap) 
            
    
            top2_layout.addWidget(self.checkbox_logscale)
            
            top2_layout.addWidget(QtWidgets.QLabel('colormap:'))
            top2_layout.addWidget( self.colormap_plot)        
            
            
            top2_layout.addWidget(QtWidgets.QLabel('Saturation dB:'))
            top2_layout.addWidget(self.db_saturation)
            
            top2_layout.addWidget(QtWidgets.QLabel('dB min:'))
            top2_layout.addWidget(self.db_vmin)
            top2_layout.addWidget(QtWidgets.QLabel('dB max:'))
            top2_layout.addWidget(self.db_vmax)
            
    
            top2_layout.addWidget(self.checkbox_background)
            
            # annotation label area
            top3_layout = QtWidgets.QHBoxLayout()   
            top3_layout.addWidget(QtWidgets.QLabel('Annotation labels:'))
    
    
            self.checkbox_an_1=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_1)
            self.an_1 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_1) 
            self.an_1.setText('FW_20_Hz')
            
            self.checkbox_an_2=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_2)
            self.an_2 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_2) 
            self.an_2.setText('FW_40_Hz')
            
            self.checkbox_an_3=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_3)
            self.an_3 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_3) 
            self.an_3.setText('BW_D_call')
            
            self.checkbox_an_4=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_4)
            self.an_4 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_4) 
            self.an_4.setText('BW_Z_call')
            
            self.checkbox_an_5=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_5)
            self.an_5 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_5) 
            self.an_5.setText('US_100-200')
    
            self.checkbox_an_6=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_6)
            self.an_6 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_6) 
            self.an_6.setText('')
            
            self.checkbox_an_7=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_7)
            self.an_7 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_7) 
            self.an_7.setText('')
    
            self.checkbox_an_8=QtWidgets.QCheckBox()
            top3_layout.addWidget(self.checkbox_an_8)
            self.an_8 = QtWidgets.QLineEdit(self)
            top3_layout.addWidget(self.an_8) 
            self.an_8.setText('')
               
            self.bg = QtWidgets.QButtonGroup()
            self.bg.addButton(self.checkbox_an_1,1)
            self.bg.addButton(self.checkbox_an_2,2)
            self.bg.addButton(self.checkbox_an_3,3)
            self.bg.addButton(self.checkbox_an_4,4)
            self.bg.addButton(self.checkbox_an_5,5)
            self.bg.addButton(self.checkbox_an_6,6)
            self.bg.addButton(self.checkbox_an_7,7)
            self.bg.addButton(self.checkbox_an_8,8)
            
    
    
            
            # combine layouts together
            
            plot_layout = QtWidgets.QVBoxLayout()
            toolbar = NavigationToolbar( self.canvas, self)
            plot_layout.addWidget(toolbar)
            plot_layout.addWidget(self.canvas)
            
            outer_layout.addLayout(top_layout)
            outer_layout.addLayout(top2_layout)
            outer_layout.addLayout(top3_layout)
    
            outer_layout.addLayout(plot_layout)
            
            # self.setLayout(outer_layout)
            
            # Create a placeholder widget to hold our toolbar and canvas.
            widget = QtWidgets.QWidget()
            widget.setLayout(outer_layout)
            self.setCentralWidget(widget)
            
            #### hotkeys
            self.msgSc1 = QtWidgets.QShortcut(QtCore.Qt.Key_Right, self)
            self.msgSc1.activated.connect(plot_next_spectro)
            self.msgSc2 = QtWidgets.QShortcut(QtCore.Qt.Key_Left, self)
            self.msgSc2.activated.connect(plot_previous_spectro)        
            self.msgSc3 = QtWidgets.QShortcut(QtCore.Qt.Key_Space, self)
            self.msgSc3.activated.connect(func_playaudio)     
                
            ####
            # layout = QtWidgets.QVBoxLayout()
            # layout.addWidget(openfilebutton)
            # layout.addWidget(button_plot_spectro)
            # layout.addWidget(button_save)            
            # layout.addWidget(button_quit)
    
    
            # layout.addWidget(toolbar)
            # layout.addWidget(self.canvas)
    
            # # Create a placeholder widget to hold our toolbar and canvas.
            # widget = QtWidgets.QWidget()
            # widget.setLayout(layout)
            # self.setCentralWidget(widget)
    
            self.show()
            
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Python Audio Spectrogram Explorer")      
    w = MainWindow()
    sys.exit(app.exec_())