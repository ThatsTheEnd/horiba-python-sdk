# ICL Command Status

## ICL Version

2.0.0.126.226ac9f0

## Generic Commands

| Command      | Implemented | Tested | Status | Comment |
|--------------|:-----------:|-------:|-------:|--------:|
| icl_info     |      ✅     |     ✅ |     ✅ |         |
| icl_shutdown |      ✅     |     ✅ |     ✅ |         |
| icl_binMode  |      ✅     |     ✅ |     ✅ |         |

## Monochromator Commands

| Command                     | Implemented | Tested | Status |                                                                Comment |
|-----------------------------|:-----------:|-------:|-------:|-----------------------------------------------------------------------:|
| mono_discover               |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_list                   |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_listCount              |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_open                   |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_close                  |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_isOpen                 |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_isBusy                 |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_init                   |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_getConfig              |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_getPosition            |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_setPosition            |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_moveToPosition         |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_getGratingPosition     |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_moveGrating            |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_getFilterWheelPosition |      ✅     |     ⛔ |      ⚠️ |                more info needed about all possible filter wheel setups |
| mono_moveFilterWheel        |      ✅     |     ⛔ |      ⚠️ |                more info needed about all possible filter wheel setups |
| mono_getMirrorPosition      |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_moveMirror             |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_getSlitPositionInMM    |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_moveSlitMM             |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_shutterSelect          |      ✖️      |      ⚠️ |      ⚠️ |                          Still open if it should be implemented or not |
| mono_shutterOpen            |      ✅     |      ⚠️ |      ⚠️ |   cannot test and implemenation will depend on future of shutterSelect |
| mono_shutterClose           |      ✅     |      ⚠️ |      ⚠️ |   cannot test and implemenation will depend on future of shutterSelect |
| mono_getShutterStatus       |      ✅     |      ⚠️ |      ⚠️ | cannot test and returns the status of all shutters instead of just one |
| mono_getSlitStepPosition    |      ✅     |     ✅ |     ✅ |                                                                        |
| mono_moveSlit               |      ✅     |     ✅ |     ✅ |                                                                        |

## CCD Commands

| Command                    | Implemented | Tested | Status |                                                                                                                                                       Comment |
|----------------------------|:-----------:|-------:|-------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| ccd_list                   |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_listCount              |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_open                   |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_close                  |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_isOpen                 |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_restart                |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getConfig              |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getChipSize            |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getChipTemperature     |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getGain                |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setGain                |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getSpeed               |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setSpeed               |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getFitParams           |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setFitParams           |      ✅     |     ✅ |     ⛔ |                                                                                                                      setting new fit parameters does not work |
| ccd_getExposureTime        |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setExposureTime        |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getTimerResolution     |      ✅     |     ✅ |      ⚠️ |                                                                      setTimerResolution arguments are 0&1 but getTimerResolution return value is 1000 or 1(?) |
| ccd_setTimerResolution     |      ✅     |     ✅ |     ⛔ | does not set a new timer resolution:{"command":"ccd_setTimerResolution","parameters":{"index":0, "resolution":1}}, even if not supported should return error? |
| ccd_setAcqFormat           |      ✅     |     ✅ |     ❓ |                                                                                                                                  how can we test this method? |
| ccd_setRoi                 |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getXAxisConversionType |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setXAxisConversionType |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getDataRetrievalMethod |      ⛔     |      ✖️ |      ✖️ |                                                                                                 "[E];-2;ccd_getDataRetrievalMethod;Command handler not found" |
| ccd_setDataRetrievalMethod |      ⛔     |      ✖️ |      ✖️ |                                                                                                 "[E];-2;ccd_getDataRetrievalMethod;Command handler not found" |
| ccd_getAcqCount            |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setAcqCount            |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getCleanCount          |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setCleanCount          |      ✅     |     ✅ |      ⚠️ |                                                                                                                       No documentation what the "mode" 238 is |
| ccd_getDataSize            |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getTriggerIn           |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setTriggerIn           |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getSignalOut           |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setSignalOut           |      ✅     |     ✅ |     ⛔ |                                                                                                                              does not set a new signal output |
| ccd_getAcquisitionReady    |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setAcquisitionStart    |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getAcquisitionBusy     |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_setAcquisitionAbort    |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |
| ccd_getAcquisitionData     |      ✅     |     ✅ |     ✅ |                                                                                                                                                               |

## Single Chanel Detector Commands

| Command       | Implemented | Tested | Status | Comment |
|---------------|:-----------:|-------:|-------:|--------:|
| scd_discover  |      ✖️      |      ✖️ |      ✖️ |         |
| scd_list      |      ✖️      |      ✖️ |      ✖️ |         |
| scd_listCount |      ✖️      |      ✖️ |      ✖️ |         |
| scd_open      |      ✖️      |      ✖️ |      ✖️ |         |
| scd_close     |      ✖️      |      ✖️ |      ✖️ |         |
| scd_isOpen    |      ✖️      |      ✖️ |      ✖️ |         |
