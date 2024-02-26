# Generic Commands

| Command      | Implemented | Tested | Status |                                      Comment |
|--------------|:-----------:|-------:|-------:|---------------------------------------------:|
| icl_info     |      ✅      |      ✅ |      ✅ |                                              |
| icl_shutdown |      ✅      |      ✅ |     ⚠️ | Shutdown frame not always received by client |
| icl_binMode  |      ✅      |      ✅ |      ✅ |                                              |

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

| Command                    | Implemented | Tested | Status |                                                             Comment |
|----------------------------|:-----------:|-------:|-------:|--------------------------------------------------------------------:|
| ccd_list                   |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_listCount              |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_open                   |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_close                  |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_isOpen                 |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_restart                |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getConfig              |      ✅      |      ✅ |      ⛔ |                              Does not return anything at the moment |
| ccd_getChipSize            |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getChipTemperature     |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getNumberOfAvgs        |      ✅      |      ⛔ |      ⛔ |                             [E];-315;CCD does not support averaging |
| ccd_setNumberOfAvgs        |      ✅      |      ⛔ |      ⛔ |                             [E];-315;CCD does not support averaging |
| ccd_getGain                |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setGain                |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getSpeed               |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setSpeed               |      ✅      |      ✅ |     ⚠️ |   I have a camera with 45kHz, 1MHz, 1MHz Ultra, what else is there? |
| ccd_getFitParams           |      ✅      |      ✅ |      ✅ |                                     results":{"params":"0,1,0,0,0"} |
| ccd_setFitParams           |      ✅      |      ✅ |     ⚠️ |                There is no documentation what these parameters mean |
| ccd_getExposureTime        |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setExposureTime        |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getTimerResolution     |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setTimerResolution     |      ✅      |      ✅ |      ⛔ | I can set timer resolution to 0 or 1 as "resolution", but no effect |
| ccd_setAcqFormat           |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setRoi                 |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getXAxisConversionType |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setXAxisConversionType |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getDataRetrievalMethod |      ⛔      |     ✖️ |     ✖️ |       "[E];-2;ccd_getDataRetrievalMethod;Command handler not found" |
| ccd_setDataRetrievalMethod |      ⛔      |     ✖️ |     ✖️ |       "[E];-2;ccd_getDataRetrievalMethod;Command handler not found" |
| ccd_getAcqCount            |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setAcqCount            |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getCleanCount          |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setCleanCount          |      ✅      |      ✅ |     ⚠️ |                             No documentation what the "mode" 238 is |
| ccd_getDataSize            |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getTriggerIn           |      ⛔      |     ✖️ |     ✖️ |                                          needs documentation about: |
| ccd_setTriggerIn           |      ⛔      |     ✖️ |     ✖️ |                    "addressWhere":-1,"eventWhen":-1,"sigTypeHow":-1 |
| ccd_getSignalOut           |      ⛔      |     ✖️ |     ✖️ |                                            "errors":["[E];-729;on"] |
| ccd_setSignalOut           |      ⛔      |     ✖️ |     ✖️ |                                                                     |
| ccd_getAcquisitionReady    |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setAcquisitionStart    |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_getAcquisitionBusy     |      ✅      |      ✅ |      ✅ |                                                                     |
| ccd_setAcquisitionAbort    |      ✅      |     ✖️ |     ✖️ |                                                                     |
| ccd_getAcquisitionData     |      ✅      |      ✅ |      ✅ |                                                                     |

# Single Chanel Detector Commands

| Command       | Implemented | Tested | Status | Comment |
|---------------|:-----------:|-------:|-------:|--------:|
| scd_discover  |     ✖️      |     ✖️ |     ✖️ |         |
| scd_list      |     ✖️      |     ✖️ |     ✖️ |         |
| scd_listCount |     ✖️      |     ✖️ |     ✖️ |         |
| scd_open      |     ✖️      |     ✖️ |     ✖️ |         |
| scd_close     |     ✖️      |     ✖️ |     ✖️ |         |
| scd_isOpen    |     ✖️      |     ✖️ |     ✖️ |         |
