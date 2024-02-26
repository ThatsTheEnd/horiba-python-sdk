# Generic Commands
| Command                     | Implemented | Tested | Status |                                                                 Comment |
|-----------------------------|:-----------:|-------:|-------:|------------------------------------------------------------------------:|
| icl_info                    |      ✅      |      ✅ |      ✅ |                                                                         |
| icl_shutdown                |      ✅      |      ✅ |     ⚠️ |                            Showtdown frame not alwys received by client |
| icl_binMode                 |      ✅      |      ✅ |      ✅ |                                                                         |

# Monochromator Commands
| Command                     | Implemented | Tested | Status |                                                                 Comment |
|-----------------------------|:-----------:|-------:|-------:|------------------------------------------------------------------------:|
| mono_discover               |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_list                   |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_listCount              |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_open                   |      ✅      |      ✅ |      ⛔ |     Opening the mono does not work atm if a CCD is attached to the mono |
| mono_close                  |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_isOpen                 |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_isBusy                 |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_init                   |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getConfig              |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getPosition            |      ✅      |      ✅ |      ✅ |                                                                         |
| mono_setPosition            |      ✅      |     ✖️ |     ⚠️ |                                      Should this be available to users? |
| mono_moveToPosition         |      ✅      |      ✅ |      ⛔ | Mono not working as expected yet, does not move to position as expected |
| mono_getGratingPosition     |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_moveGrating            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getFilterWheelPosition |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_moveFilterWheel        |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getMirrorPosition      |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_moveMirror             |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getSlitPositionInMM    |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_moveSlitMM             |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_shutterOpen            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_shutterClose           |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getShutterStatus       |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getSlitStepPosition    |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_moveSlit               |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_enableLaser            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getLaserStatus         |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_setLaserPower          |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getLaserPower          |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getLidStatus           |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| mono_getSwitchStatus        |     ✖️      |     ✖️ |     ✖️ |                                                                         |

# CCD Commands
| Command                     | Implemented | Tested | Status |                                                                 Comment |
|-----------------------------|:-----------:|-------:|-------:|------------------------------------------------------------------------:|
| ccd_list                    |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_listCount               |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_open                    |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_close                   |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_isOpen                  |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_restart                 |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getConfig               |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getChipSize             |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_getChipTemperature      |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_getNumberOfAvgs         |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setNumberOfAvgs         |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getGain                 |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setGain                 |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getSpeed                |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setSpeed                |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getFitParams            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setFitParams            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getExposureTime         |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_setExposureTime         |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_getTimerResolution      |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setTimerResolution      |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setAcqFormat            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setRoi                  |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_getXAxisConversionType  |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setXAxisConversionType  |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getDataRetrievalMethod  |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setDataRetrievalMethod  |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getAcqCount             |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setAcqCount             |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getCleanCount           |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setCleanCount           |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getDataSize             |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getTriggerIn            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setTriggerIn            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getSignalOut            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_setSignalOut            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getAcquisitionReady     |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_setAcquisitionStart     |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_getAcquisitionBusy      |      ✅      |      ✅ |      ✅ |                                                                         |
| ccd_setAcquisitionAbort     |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| ccd_getAcquisitionData      |      ✅      |      ✅ |     ⚠️ |                  Data is being retrieved but still formatted for telnet |

# Single Chanel Detector Commands
| Command                     | Implemented | Tested | Status |                                                                 Comment |
|-----------------------------|:-----------:|-------:|-------:|------------------------------------------------------------------------:|
| scd_discover            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_list            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_list            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_listCount            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_open            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_close            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
| scd_isOpen            |     ✖️      |     ✖️ |     ✖️ |                                                                         |
