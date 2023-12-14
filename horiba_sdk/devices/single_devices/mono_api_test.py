"""
Created on Mon May 23 20:56:23 2016

@author: jdv12
"""


# class MonoApiTest:
#     def __init__(self, icl):
#         if icl is None:
#             raise RuntimeError('ICL is None')
#         self._icl = icl

#     def home(self, mononum):
#         icl_if.runCmd(self._icl, 'lmb_monoInit ' + str(mononum))
#         print('Homing mono')
#         while self.is_mono_busy(mononum):
#             print('Mono busy')
#             time.sleep(0.5)
#         print('Mono homed')

#     def wavelength_limits(self, mononum):
#         ret = icl_if.runCmd(self._icl, 'lmb_monoWaveLim ' + str(mononum))
#         rc = icl_if.returnCode(ret)
#         if rc < 0:
#             raise RuntimeError('ILC Communications error! Error: ' + str(rc))
#         return ret[0].strip(), ret[1].strip()

#     def setWavelength(self, mononum, wavelength):
#         icl_if.runCmd(self._icl, 'lmb_monoSetWave ' + str(mononum) + ' ' + str(wavelength))

#     def moveToNoWait(self, mononum, wavelength):
#         # print ('Mono position: ' + self._mono_current_position(mononum))
#         while self.is_mono_busy(mononum):
#             print('Mono position: ' + self.mono_current_position(mononum))
#             time.sleep(0.5)
#         icl_if.runCmd(self._icl, 'lmb_monoMoveTo ' + str(mononum) + ' ' + str(wavelength))
#         # print ('Mono position: ' + self._mono_current_position(mononum))

#     def moveTo(self, mononum, wavelength):
#         # print ('Mono position: ' + self._mono_current_position(mononum))
#         # icl_if.runCmd(self._icl, 'lmb_monoMoveTo ' + str(mononum) + ' ' + str(wavelength))
#         icl_if.runCmd(self._icl, 'lmb_monoMoveTo ' + str(mononum) + ' ' + str(wavelength))
#         while self.is_mono_busy(mononum):
#             # print ('Mono position: ' + self._mono_current_position(mononum))
#             time.sleep(0.5)
#         print('Mono position: ' + self.mono_current_position(mononum))

#     def is_mono_busy(self, mononum):
#         ret = icl_if.runCmd(self._icl, 'lmb_monoBusy ' + str(mononum))
#         rc = icl_if.returnCode(ret)
#         if rc < 0:
#             raise RuntimeError('ILC Communications error! Error: ' + str(rc))
#         return ret[0].startswith('1')

#     def stop(self, mononum):  # no such command
#         ret = icl_if.runCmd(self._icl, 'lmb_monoStop ' + str(mononum))
#         rc = icl_if.returnCode(ret)
#         if rc < 0:
#             raise RuntimeError('ILC Communications error! Error: ' + str(rc))
#         return ret[0].startswith('1')

#     def mono_current_position(self, mononum):
#         ret = icl_if.runCmd(self._icl, 'lmb_monoPosition ' + str(mononum))
#         rc = icl_if.returnCode(ret)
#         if rc < 0:
#             raise RuntimeError('ILC Communications error! Error: ' + str(rc))
#         return ret[0].strip()

#     def mono_status(self, mononum):
#         ret = icl_if.runCmd(self._icl, 'lmb_monoStatus ' + str(mononum))
#         rc = icl_if.returnCode(ret)
#         if rc < 0:
#             raise RuntimeError('ILC Communications error! Error: ' + str(rc))
#         return ret[0].strip()

#     def SetWave(self, mononum, wavelength):
#         print('Mono position: ' + self.mono_current_position(mononum))
#         icl_if.runCmd(self._icl, 'lmb_monoSetWave ' + str(mononum) + ' ' + str(wavelength))
#         while self.is_mono_busy(mononum):
#             print('Mono position: ' + self.mono_current_position(mononum))
#             time.sleep(0.5)
#         print('Mono position: ' + self.mono_current_position(mononum))

#     def getGratingInfo(self, mononum):
#         ret = icl_if.runCmd(self._icl, 'lmb_monoGrateInfo ' + str(mononum))
#         print(str(ret))
#         return str(ret[0].strip())
#         # retcount = len(ret)
#         # print ('retcount: ' + str(retcount))
#         # i = 0
#         # while (i < retcount-1):
#         #    print ('Mono Grating Information: ' + str(i) + ' value: ' + str(ret[i].strip()))
#         #    i = i + 1
