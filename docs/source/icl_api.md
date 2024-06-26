# ICL API Programmers Manual

revision: **0.1**  
date: **12/13/2023**

This document describes the remote command and data API provided by the ICL.

## Table of Contents

- [ICL API Programmers Manual](#icl-api-programmers-manual)
  - [Table of Contents](#table-of-contents)
  - [Execute](#execute)
  - [Connecting to ICL](#connecting-to-icl)
  - [Command and Control API](#command-and-control-api)
    - [Overview](#overview)
    - [Command Format](#command-format)
  - [General Commands](#general-commands)
    - [icl\_info](#icl_info)
    - [icl\_shutdown](#icl_shutdown)
    - [icl\_binMode](#icl_binmode)
  - [Monochromator Module Commands](#monochromator-module-commands)
    - [mono\_discover](#mono_discover)
    - [mono\_list](#mono_list)
    - [mono\_listCount](#mono_listcount)
    - [mono\_open](#mono_open)
    - [mono\_close](#mono_close)
    - [mono\_isOpen](#mono_isopen)
    - [mono\_isBusy](#mono_isbusy)
    - [mono\_init](#mono_init)
    - [mono\_isInitialized](#mono_isinitialized)
    - [mono\_getConfig](#mono_getconfig)
    - [mono\_getPosition](#mono_getposition)
    - [mono\_setPosition](#mono_setposition)
    - [mono\_moveToPosition](#mono_movetoposition)
    - [mono\_getGratingPosition](#mono_getgratingposition)
    - [mono\_moveGrating](#mono_movegrating)
    - [mono\_getFilterWheelPosition](#mono_getfilterwheelposition)
    - [mono\_moveFilterWheel](#mono_movefilterwheel)
    - [mono\_getMirrorPosition](#mono_getmirrorposition)
    - [mono\_moveMirror](#mono_movemirror)
    - [mono\_getSlitPositionInMM](#mono_getslitpositioninmm)
    - [mono\_moveSlitMM](#mono_moveslitmm)
    - [mono\_shutterOpen](#mono_shutteropen)
    - [mono\_shutterClose](#mono_shutterclose)
    - [mono\_getShutterStatus](#mono_getshutterstatus)
  - [CCD Module Commands](#ccd-module-commands)
    - [ccd\_discover](#ccd_discover)
    - [ccd\_list](#ccd_list)
    - [ccd\_listCount](#ccd_listcount)
    - [ccd\_open](#ccd_open)
    - [ccd\_close](#ccd_close)
    - [ccd\_isOpen](#ccd_isopen)
    - [ccd\_restart](#ccd_restart)
    - [ccd\_getConfig](#ccd_getconfig)
    - [ccd\_getChipSize](#ccd_getchipsize)
    - [ccd\_getChipTemperature](#ccd_getchiptemperature)
    - [ccd\_getGain](#ccd_getgain)
    - [ccd\_setGain](#ccd_setgain)
    - [ccd\_getSpeed](#ccd_getspeed)
    - [ccd\_setSpeed](#ccd_setspeed)
    - [ccd\_getFitParams](#ccd_getfitparams)
    - [ccd\_getExposureTime](#ccd_getexposuretime)
    - [ccd\_setExposureTime](#ccd_setexposuretime)
    - [ccd\_getTimerResolution](#ccd_gettimerresolution)
    - [ccd\_setTimerResolution](#ccd_settimerresolution)
    - [ccd\_setAcqFormat](#ccd_setacqformat)
    - [ccd\_setRoi](#ccd_setroi)
    - [ccd\_getXAxisConversionType](#ccd_getxaxisconversiontype)
    - [ccd\_setXAxisConversionType](#ccd_setxaxisconversiontype)
    - [ccd\_getAcqCount](#ccd_getacqcount)
    - [ccd\_setAcqCount](#ccd_setacqcount)
    - [ccd\_getCleanCount](#ccd_getcleancount)
    - [ccd\_setCleanCount](#ccd_setcleancount)
    - [ccd\_getDataSize](#ccd_getdatasize)
    - [ccd\_getTriggerIn](#ccd_gettriggerin)
    - [ccd\_setTriggerIn](#ccd_settriggerin)
    - [ccd\_getSignalOut](#ccd_getsignalout)
    - [ccd\_setSignalOut](#ccd_setsignalout)
    - [ccd\_getAcquisitionReady](#ccd_getacquisitionready)
    - [ccd\_setAcquisitionStart](#ccd_setacquisitionstart)
    - [ccd\_getAcquisitionBusy](#ccd_getacquisitionbusy)
    - [ccd\_getAcquisitionData](#ccd_getacquisitiondata)
    - [ccd\_setCenterWavelength](#ccd_setcenterwavelength)

  - [SpectrAcq3 - Single Channel Detector Interface](#spectracq3---single-channel-detector-interface)
    - [scd\_discover](#scd_discover)
    - [scd\_list](#scd_list)
    - [scd\_listCount](#scd_listcount)
    - [scd\_open](#scd_open)
    - [scd\_close](#scd_close)
    - [scd\_isOpen](#scd_isopen)
  - [Binary Events](#binary-events)
  - [Error Codes](#error-codes)

<div style="page-break-before:always">&nbsp;</div>
<p></p>

## Execute

The ICL is a Windows console application that can be executed:

1. From the command line in a terminal.
2. From the Windows Explorer by double clicking the icl.exe file.
3. Automatically started by adding a shortcut to the Windows startup folder.
4. ...

## Connecting to ICL

URL to connecting to a locally running ICL:
> ws://localhost:25010

When connecting to a remote running ICL replace the _localhost_ with the remote ICL's network address.

Currently, a secure websocket connection (wss:) is not yet implemented.

## Command and Control API

### Overview

...

### Command Format

The text based payload of a websocket message uses JSON formatting.

**Command Payload:**

```json
{
    "id": number
    "command": string
    "parameters": {

    }
}
```

**id** optional field. An integer number that can be used to line-up/sync-up outgoing commands with incoming asynchronous response.  _May remove._  
**command** is a string indicating the command to execute.  
**parameters**: optional - depends on command.  Can be used to pass in 1 or more parameters.  The key/value parameters (JSON object(s)) can be strings, number (int or float) booleans (true or false) and array - as described in the individual commands.  

_Note 1:_ All commands have a prefix xxx_ to indicate the target module in the ICL.  
_Note 2:_ Currently all commands are case sensitive.

**Reply Payload:**

```json
{
    "id": number
    "command": string
    "results": {}
    "errors": [
        string_1,
        string_2,
        string_n
        ]
}
```

**id** is the integer number that was sent with the command. If no **id** was sent with the command this field will have a value of 0 (currently – may change this so it is not present if it wasn’t present in the command).  
**command** is a string indicating the command that was executed.  
**results** Optional - depends on command. A collection of key/value pairs where value can be a string, number or Boolean.  
**errors** Optional - only if error(s). Report zero (0) or more errors.  And array of strings. Currently format of an error string is:

```c++
"[E];<error code>;<error string>"
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

## General Commands

This section describes general ICL commands.


### <a id="icl_info"></a>icl_info

Gets detailed information about the connected to ICL.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|nodeAlias|The name of the node.|
>|nodeApiVersion|An integer number indicating the API version|
>|nodeBuilt|Built date|
>|nodeDescription|Text description of the ICL|
>|nodeId|An integer number indicating this ICL's id|
>|nodeVersion|String describing the detailed version number|

**Example command:**

```json
{
    "id": 1234,
    "command": "icl_info"
}
```

**Example response:**

```json
{
  "command": "icl_info",
  "errors": [],
  "id": 1234,
  "results": {
    "nodeAlias": "ICL",
    "nodeApiVersion": 300,
    "nodeBuilt": "Dec  5 2023-13:17:00",
    "nodeDescription": "Instrument Control Library",
    "nodeId": 1,
    "nodeVersion": "2.0.0.108.d762232a"
  }
}
```
<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="icl_shutdown"></a>icl_shutdown

Command to start a safe shutdown of the connected to ICL.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|state|Text message indicating action taken. Normally _Shutting down_|

**Example command:**

```json
{
    "id": 1234,
    "command": "icl_shutdown"
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "icl_shutdown",
    "results": {
        "state": "Shutting down"
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="icl_binmode"></a>icl_binMode

Command to control if binary messages are to be sent to this client. Binary message types include: \"logs\", \"information\" and \"data\".  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|mode|String. Possible values: \"none\", \"all\". all = receive all binary message types|

**Response results:**
>| results | description |
>|---|---|
>|state|Text message indicating action taken. Normally "_Shutting down_"|

**Example command:**

```json
{
    "id": 1234,
    "command": "icl_binMode",
    "parameters": {
        "mode": "none"
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "icl_binMode"
    "results": {
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

## Monochromator Module Commands

### <a id="mono_discover"></a>mono_discover

Attempts to find supported monos connected and powered on the USB bus.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer value indicating number of monochromators discovered|

**Example command:**

```json
{  
    "id": 1234,
    "command": "mono_discover"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_discover",
    "results": {
        "count": 1
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_list"></a>mono_list

Returns a formatted list of discovered mono devices.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>| devices | Array of discovered mono devices. Each discovered mono consists of the following details: <br> deviceType - Mono device description <br> index - Index of the discovered device <br> serialNumber - Mono device serial number|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_list"
}
```

**Example response:**

```json
{
    "command": "mono_list",
    "errors": [],
    "id": 1234,
    "results": {
        "devices": [
            {
                "deviceType": "HORIBA Scientific iHR",
                "index": 0,
                "serialNumber": "1745A-2017-iHR320"
            }
        ]
    }
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_listcount"></a>mono_listCount

Returns the number of monochromators found on the USB bus.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer. Indicates the number of monochromators found|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_listCount"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_listCount",
    "results": {
        "count": 2
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_open"></a>mono_open

Opens communications with the monochromator indicated by the index command parameter.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Open first mono in the list of monos discoverd.

```json
{  
    "id": 1234,
    "command": "mono_open",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_open",
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_close"></a>mono_close

Closes communications with the monochromator indicated by the index.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See [mono_list](#mono_list) command|

**Response Results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_close",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_close",
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_isopen"></a>mono_isOpen

Returns _true_ if selected monochromator is open.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See [mono_list](#mono_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| open | Boolean. True = open |

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_isOpen",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_isOpen",
    "results":{
        "open": true
    }
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_isbusy"></a>mono_isBusy

Returns _true_ if selected monochromator is busy.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>| busy | Boolean. True = busy |

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_isBusy",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_isBusy",
    "results":{
        "busy": true
    }
    "errors": [
    ]
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_init"></a>mono_init

Starts the monochromator initialization process (homing...). This is a "long-running" asynchronous command. Use the [mono_isBusy](#mono_isbusy) command to know when initialization has completed.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>| force | Boolean. Force starts the initialization process.

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Start the initialization process of the first mono.  

```json
{
    "id": 1234,
    "command": "mono_init",
    "parameters":{
        "index": 0,
        "force": false
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_init",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_isinitialized"></a>mono_isInitialized

This command returns _true_ when the mono is initialized. Otherwise it returns _false_.

_Note:_ This command may also return false when the mono is busy with another command.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command |

**Response results:**
>| results | description |
>|---|---|
>|initialized | Boolean. True when the mono is initialized, otherwise false |

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_isInitialized",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "mono_isInitialized",
    "errors": [],
    "id": 1234,
    "results": {
        "initialized": true
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getconfig"></a>mono_getConfig

This command returns the monochromator configuration.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|configuration| String. Mono device configuration.|

**Port Descriptions:**
>| parameter | description |
>|---|---|
>| locationId | Integer. Used to identify the slit location. <br> 1 = Front entrance (axial) <br> 2 = Side entrance (lateral) <br> 3 = Front exit (axial) <br> 4 = Side exit (lateral) |
>| slitType | Integer. Used to identify the slit size. <br> 1 = 2mm slit <br> 2 = 7mm slit |

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getConfig",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "mono_getConfig",
    "errors": [],
    "id": 1234,
    "results": {
        "configuration": {
            "filterWheels": [
                {
                    "locationId": 1
                },
                {
                    "locationId": 2
                }
            ],
            "gratings": [
                {
                    "blaze": 0,
                    "grooveDensity": 600,
                    "positionIndex": 0
                },
                {
                    "blaze": 0,
                    "grooveDensity": 300,
                    "positionIndex": 1
                },
                {
                    "blaze": 0,
                    "grooveDensity": 150,
                    "positionIndex": 2
                }
            ],
            "mirrors": [
                {
                    "locationId": 1
                },
                {
                    "locationId": 2
                }
            ],
            "model": "iHR320",
            "ports": [
                {
                    "locationId": 1,
                    "slitType": 1
                },
                {
                    "locationId": 2,
                    "slitType": 1
                },
                {
                    "locationId": 4,
                    "slitType": 1
                }
            ],
            "productId": "257",
            "serialNumber": ""
        }
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getposition"></a>mono_getPosition

Returns the wavelength value, in nm, of the monochromator's current position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|wavelength|Float. Position in nm.|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getPosition",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_getPosition",
    "results":{
        "wavelength": 320.0
    }  
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_setposition"></a>mono_setPosition

This command sets the wavelength value of the current grating position of the monochromator. This could potentially un-calibrate the monochromator and report an incorrect wavelength compared to the actual output wavelength.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>|wavelength| Float. Set the wavelength of the mono at the current position.|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Sets the position wavelength value to 320nm.  

```json
{
    "id": 1234,
    "command": "mono_setPosition",
    "parameters":{
        "index": 0
        "wavelength": 320
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_setPosition",
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_movetoposition"></a>mono_moveToPosition

This command starts the monochromator moving to the requested wavelength in nm. This is an asynchronous command. Use the [mono_isBusy](#mono_isbusy) command to know when the move has completed.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>|wavelength| Float. Move to wavelength.|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Sets the position wavelength value to 320nm.  

```json
{
    "id": 1234,
    "command": "mono_moveToPosition",
    "parameters":{
        "index": 0,
        "wavelength": 320
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "mono_moveToPosition",
    "errors": [
    ]
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getgratingposition"></a>mono_getGratingPosition

Returns the current grating turret position.

_Note:_ Prior to the initialization of the grating turret, this value may not reflect the actual position of the turret. To read the current position of the grating turret, please run [mono_init](#mono_init) prior to running this command.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|position|Integer. Current position of the grating turret.|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getGratingPosition",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_getGratingPosition",
    "results":{
        "position": 1
    }  
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_movegrating"></a>mono_moveGrating

Moves the grating turret to the specified position.

_Note:_ The turret sensor does not re-read the position each time it is moved, therefore the position may not be accurate prior to initialization. See note for [mono_getGratingPosition](#mono_getgratingposition).

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>|position| Integer. Position to move the grating turret.|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Move grating turret to position 1.

```json
{
    "id": 1234,
    "command": "mono_moveGrating",
    "parameters":{
        "index": 0,
        "position": 1
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_moveGrating",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getfilterwheelposition"></a>mono_getFilterWheelPosition

Returns the current filter wheel position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>| locationId | Integer. Specifies the filter wheel location. <br> 0 = Filter wheel 1 (Internal) <br> 1 = Filter wheel 2 (External) |

**Response results:**
>| results | description |
>|---|---|
>|position|Integer. Current filter wheel position|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getFilterWheelPosition",
    "parameters":{
        "index": 0,
        "locationId": 0
    }
}
```

**Example response:**

```json
{
    "command": "mono_getFilterWheelPosition",
    "errors": [],
    "id": 1234,
    "results": {
        "position": 2
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_movefilterwheel"></a>mono_moveFilterWheel

Move the filter wheel to a position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command |
>| locationId | Integer. Specifies which filter wheel to move. <br> 0 = Filter wheel 1 (Internal) <br> 1 = Filter wheel 2 (External) |
>|position| Integer. Position to move the filter wheel. |

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Move the internal filter wheel to position 2.

```json
{
    "id": 1234,
    "command": "mono_moveFilterWheel",
    "parameters": {
        "index": 0,
        "locationId": 0,
        "position": 2
    }
}
```

**Example response:**

```json
{
    "command": "mono_moveFilterWheel",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getmirrorposition"></a>mono_getMirrorPosition

Returns the position of the specified mirror.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command |
>| locationId | Integer. Identifies which mirror to get the position from. <br> 0 = Mirror 1 (Entrance) <br> 1 = Mirror 2 (Exit) |

**Response results:**
>| results | description |
>|---|---|
>|position|Integer. Position of the specified mirror. <br> 0 = Axial <br> 1 = Lateral |

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getMirrorPosition",
    "parameters": {
        "index": 0,
        "locationId": 1
    }
}
```

**Example response:**

```json
{
    "command": "mono_getMirrorPosition",
    "errors": [],
    "id": 1234,
    "results": {
        "position": 0
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_movemirror"></a>mono_moveMirror

Moves the specified mirror to a position.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>| locationId | Integer. Identifies which mirror to move (zero-based). <br> 0 = Mirror 1 (Entrance) <br> 1 = Mirror 2 (Exit) |
>| position | Integer. Position to move to. <br> 0 = Axial <br> 1 = Lateral |

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Move mirror 2 to position 1.

```json
{
    "id": 1234,
    "command": "mono_moveMirror",
    "parameters":{
        "index": 0,
        "locationId": 1,
        "position": 1
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_moveMirror",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getslitpositioninmm"></a>mono_getSlitPositionInMM

Returns the position of the specified slit in millimeters. The location id of each configured slit can be found under the ports section of the mono configuration. See [mono_getConfig](#mono_getconfig) for additional information.

**For example:**
```json
"ports": [
    {
        "locationId": 1,
        "slitType": 1
    },
    {
        "locationId": 2,
        "slitType": 1
    },
    {
        "locationId": 4,
        "slitType": 1
    }
]
```

_Note:_ The "locationId" parameter found in the mono configuration is 1-based. However, the mono_getSlitPositionInMM command uses a 0-based "locationId".

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>| locationId | Integer. Slit location (zero-based) |

**Response results:**
>| results | description |
>|---|---|
>| position | Float. Slit position in millimeters|

**Example command:** Get position of slit in port 4

```json
{
    "id": 1234,
    "command": "mono_getSlitPositionInMM",
    "parameters":{
        "index": 0,
        "locationId": 3
    }
}
```

**Example response:**

```json
{  
    "command": "mono_getSlitPositionInMM",
    "errors": [],
    "id": 1234,
    "results": {
        "position": 0.5
    }  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_moveslitmm"></a>mono_moveSlitMM

Moves the specified slit to the position in millimeters. The location id of each configured slit can be found under the ports section of the mono configuration. See [mono_getConfig](#mono_getconfig) for additional information.

**For example:**
```json
"ports": [
    {
        "locationId": 1,
        "slitType": 1
    },
    {
        "locationId": 2,
        "slitType": 1
    },
    {
        "locationId": 4,
        "slitType": 1
    }
]
```

_Note:_ The "locationId" parameter found in the mono configuration is 1-based. However, the mono_moveSlitMM command uses a 0-based "locationId".

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|
>| locationId | Integer. Slit location (zero-based) |
>| position | Float. Position in millimeters |

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:** Move slit in port 2 to 1.5mm position

```json
{
    "id": 1234,
    "command": "mono_moveSlitMM",
    "parameters":{
        "index": 0,
        "locationId": 1,
        "position": 1.5
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_moveSlitMM",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_shutteropen"></a>mono_shutterOpen

Activates the currently selected shutter solenoid.

_Note:_ The device must be configured for internal shutter mode. The shutter solenoid will not respond in External (Bypass) mode.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_shutterOpen",
    "parameters":{
        "index": 0,
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_shutterOpen",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_shutterclose"></a>mono_shutterClose

Deactivates the currently selected shutter solenoid.

_Note:_ The device must be configured for internal shutter mode. The shutter solenoid will not respond in External (Bypass) mode.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_shutterClose",
    "parameters":{
        "index": 0,
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_shutterClose",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getshutterstatus"></a>mono_getShutterStatus

Returns the status of the currently selected shutter.

_Note:_ To view the status of the shutter solenoid the device must be configured for internal shutter mode.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See [mono_list](#mono_list) command|

**Response results:**
>| results | description |
>|---|---|
>| shutterIndex | Integer. Index of the currently selected shutter.
>| shutterStatus | Integer. Shutter position status. <br> 0 = Closed <br> 1 = Open

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getShutterStatus",
    "parameters":{
        "index": 0,
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_getShutterStatus",
    "errors": [],
    "results": {
        "shutterIndex": 1,
        "shutterPosition": 0
    }  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


## CCD Module Commands

### <a id="ccd_discover"></a>ccd_discover

This command searches for all supported CCD devices that are connected to the computer system via their USB interface. When this command occurs, references to previously discovered CCDs are cleared and a new search is made.  

If this command does not discover a particular CCD, please insure that the device’s power supply is turned on and its USB cable is connected to the computer.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer value indicating number of CCD's discovered|

**Example command:**

```json
{  
    "id": 1234,
    "command": "ccd_discover"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "ccd_discover",
    "results": {
        "count": 1
    }
  "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_list"></a>ccd_list

This command returns a list of the CCD devices that were discovered in the computer system.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|devices| Array of discovered CCD devices. Each discovered CCD consists of the following details: <br> deviceType - CCD device description <br> index - Index of the discovered device <br> productId - CCD USB product id (PID) <br> serialNumber - CCD device serial number|


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_list"
}
```

**Example response:**

```json
{
    "command": "ccd_list",
    "errors": [],
    "id": 1234,
    "results": {
        "devices": [
            {
                "deviceType": "HORIBA Scientific Syncerity",
                "index": 0,
                "productId": 13,
                "serialNumber": "Camera SN:  5128"
            },
            {
                "deviceType": "HORIBA Compact CCD",
                "index": 1,
                "productId": 8,
                "serialNumber": "Camera SN:  934"
            }
        ]
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_listcount"></a>ccd_listCount

This command returns the number of CCD devices discovered on the USB bus.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer. Indicates the number of CCD's found|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_listCount"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "ccd_listCount",
    "results": {
        "count": 2
    }
  "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_open"></a>ccd_open

This command initializes the CCD and gets it’s the CCD configuration from the device. The device is also connected to the API. Since a CCD hardware initialization occurs, all CCD parameters, including any previously set parameters, will be reset to their default values.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Open first (index 0) CCD in the list of monos discoverd.

```json
{  
    "id": 1234,
    "command": "ccd_open",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "ccd_open",
    "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_close"></a>ccd_close

Closes communications with the CCD indicated by the index.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Response Results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_close",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "ccd_close",
    "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_isopen"></a>ccd_isOpen

Returns _true_ if selected CCD is open.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>|open|boolean. true = open|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_isOpen",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "ccd_isOpen",
    "results":{
        "open": true
    }
    "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_restart"></a>ccd_restart

Performs a restart on the CCD.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>|_none_| |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_restart",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_restart",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getconfig"></a>ccd_getConfig

Returns the CCD device configuration.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| configuration | JSON. CCD device configuration. |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getConfig",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getConfig",
    "errors": [],
    "id": 1234,
    "results": {
        "configuration": {
            "centerWavelength": 0,
            "chipHSpacing": "140",
            "chipHeight": "70",
            "chipName": "S10420",
            "chipSerialNumber": "FAH23 098",
            "chipVSpacing": "140",
            "chipWidth": "2048",
            "deviceType": "HORIBA Scientific Syncerity",
            "fitParameters": [
                0,
                1,
                0,
                0,
                0
            ],
            "gains": [
                {
                    "info": "Best Dynamic Range",
                    "token": 1
                },
                {
                    "info": "High Sensitivity",
                    "token": 2
                },
                {
                    "info": "High Light",
                    "token": 0
                }
            ],
            "hardwareAvgAvailable": false,
            "lineScan": false,
            "productId": "13",
            "serialNumber": "Camera SN:  5128",
            "signals": [
                {
                    "events": [
                        {
                            "name": "Ready For Trigger",
                            "token": 1,
                            "types": [
                                {
                                    "name": "TTL Active Low",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Active High",
                                    "token": 0
                                }
                            ]
                        },
                        {
                            "name": "Not Readout",
                            "token": 2,
                            "types": [
                                {
                                    "name": "TTL Active Low",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Active High",
                                    "token": 0
                                }
                            ]
                        },
                        {
                            "name": "Shutter Open",
                            "token": 3,
                            "types": [
                                {
                                    "name": "TTL Active Low",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Active High",
                                    "token": 0
                                }
                            ]
                        },
                        {
                            "name": "Start Experiment",
                            "token": 0,
                            "types": [
                                {
                                    "name": "TTL Active Low",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Active High",
                                    "token": 0
                                }
                            ]
                        }
                    ],
                    "name": "Signal Output",
                    "token": 0
                }
            ],
            "speeds": [
                {
                    "info": "500 kHz ",
                    "token": 1
                },
                {
                    "info": "500 kHz Ultra",
                    "token": 2
                },
                {
                    "info": "500 kHz Wrap",
                    "token": 127
                },
                {
                    "info": " 45 kHz ",
                    "token": 0
                }
            ],
            "supportedFeatures": {
                "cf_3PositionSlit": false,
                "cf_CMOSOffsetCorrection": false,
                "cf_Cleaning": true,
                "cf_DSP": false,
                "cf_DSPBin2X": false,
                "cf_DelayAfterTrigger": false,
                "cf_Delays": false,
                "cf_EMCCD": false,
                "cf_EShutter": false,
                "cf_HDR": false,
                "cf_Image": true,
                "cf_MemorySlots": true,
                "cf_Metadata": false,
                "cf_MultipleExposeTimes": false,
                "cf_MultipleSensors": false,
                "cf_PulseSummation": false,
                "cf_ROIs": true,
                "cf_Signals": true,
                "cf_Spectra": true,
                "cf_TriggerQualifier": false,
                "cf_Triggers": true"
            },
            "triggers": [
                {
                    "events": [
                        {
                            "name": "Each - For Each Acq",
                            "token": 1,
                            "types": [
                                {
                                    "name": "TTL Rising  Edge",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Falling Edge",
                                    "token": 0
                                }
                            ]
                        },
                        {
                            "name": "Once - Start All",
                            "token": 0,
                            "types": [
                                {
                                    "name": "TTL Rising  Edge",
                                    "token": 1
                                },
                                {
                                    "name": "TTL Falling Edge",
                                    "token": 0
                                }
                            ]
                        }
                    ],
                    "name": "Trigger Input",
                    "token": 0
                }
            ],
            "version": "Syncerity Ver 1.002.9"
        }
    }
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_getchipsize"></a>ccd_getChipSize

Returns the chip sensor’s pixel width and height size.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| x | Integer. Chip sensor's x size in pixels (width)|
>| y | Integer. Chip sensor's y size in pixels (height)|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getChipSize",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "ccd_getChipSize",
    "results":{
        "x": 1600
        "y": 200
    }
    "errors": []
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getchiptemperature"></a>ccd_getChipTemperature

Returns the temperature of the chip sensor in degrees C.


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| temperature | Float. Chip sensor temperature in degrees C. |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getChipTemperature",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getChipTemperature",
    "errors": [],
    "id": 1234,
    "results": {
        "temperature": -50.15999984741211
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getgain"></a>ccd_getGain

Gets the current gain token and the associated description information for the gain token. Gain tokens and their descriptions are part of the CCD configuration information. See [ccd_getConfig](#ccd_getconfig) command. <br> **For example:** <br>
```json
"gains": [
            {
                "info": "Best Dynamic Range",
                "token": 1
            },
            {
                "info": "High Sensitivity",
                "token": 2
            },
            {
                "info": "High Light",
                "token": 0
            }
]
```


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| info | String. Description of the current gain token. |
>| token | Integer. Current gain token. |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getGain",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getGain",
    "errors": [],
    "id": 1234,
    "results": {
        "info": "Best Dynamic Range",
        "token": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setgain"></a>ccd_setGain

Sets the CCD gain token. A list of supported gain tokens can be found in the CCD configuration. See [ccd_getConfig](#ccd_getconfig) command. <br> **For example:** <br>
```json
"gains": [
            {
                "info": "Best Dynamic Range",
                "token": 1
            },
            {
                "info": "High Sensitivity",
                "token": 2
            },
            {
                "info": "High Light",
                "token": 0
            }
]
```


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| token | Integer. Gain token from CCD config. |


**Return Results:**
>| results | description |
>|---|---|
>| _none_ | |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setGain",
    "parameters": {
        "index": 0,
        "token": 1
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setGain",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getspeed"></a>ccd_getSpeed

Gets the current speed token and the associated description information for the speed token. Speed tokens and their descriptions are part of the CCD configuration information. See [ccd_getConfig](#ccd_getconfig) command. <br> **For example:** <br>
```json
"speeds": [
            {
                "info": "500 kHz ",
                "token": 1
            },
            {
                "info": "500 kHz Ultra",
                "token": 2
            },
            {
                "info": "500 kHz Wrap",
                "token": 127
            },
            {
                "info": " 45 kHz ",
                "token": 0
            }
]
```


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| info | String. Description of the current speed token. |
>| token | Integer. Current speed token. |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getSpeed",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getSpeed",
    "errors": [],
    "id": 1234,
    "results": {
        "info": "500 kHz ",
        "token": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setspeed"></a>ccd_setSpeed

Sets the CCD speed token. A list of supported speed tokens can be found in the CCD configuration. See [ccd_getConfig](#ccd_getconfig) command. <br> **For example:** <br>
```json
"speeds": [
            {
                "info": "500 kHz ",
                "token": 1
            },
            {
                "info": "500 kHz Ultra",
                "token": 2
            },
            {
                "info": "500 kHz Wrap",
                "token": 127
            },
            {
                "info": " 45 kHz ",
                "token": 0
            }
]
```


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| token | Integer. Speed token from CCD config. |


**Return Results:**
>| results | description |
>|---|---|
>| _none_ | |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setSpeed",
    "parameters": {
        "index": 0,
        "token": 1
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setSpeed",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getfitparams"></a>ccd_getFitParams

Gets the FIT parameters contained in the CCD configuration.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| fitParameters | Array. CCD FIT parameters. |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getFitParams",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getFitParams",
    "errors": [],
    "id": 1234,
    "results": {
        "fitParameters": [
            0,
            1,
            0,
            0,
            0
        ]
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getexposuretime"></a>ccd_getExposureTime

Gets the exposure time (expressed in Timer Resolution units).

_Note:_ To check the current Timer Resolution value see [ccd_getTimerResolution](#ccd_gettimerresolution). Alternatively the Timer Resolution value can be set using [ccd_setTimerResolution](#ccd_settimerresolution).

**Example:** <br>
If _Exposure Time_ is set to 50, and the _Timer Resolution_ value is 1000, the CCD exposure time (integration time) = 50 milliseconds. <br>

If _Exposure Time_ is set to 50, and the _Timer Resolution_ value is 1, the CCD exposure time (integration time) = 50 microseconds.


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| time | Integer. Exposure time (expressed in Timer Resolution units).

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getExposureTime",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getExposureTime",
    "errors": [],
    "id": 1234,
    "results": {
        "time": 10
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setexposuretime"></a>ccd_setExposureTime

Sets the exposure time (expressed in Timer Resolution units).

_Note:_ To check the current Timer Resolution value see [ccd_getTimerResolution](#ccd_gettimerresolution). Alternatively the Timer Resolution value can be set using [ccd_setTimerResolution](#ccd_settimerresolution).

**Example:** <br>
If _Exposure Time_ is set to 50, and the _Timer Resolution_ value is 1000, the CCD exposure time (integration time) = 50 milliseconds. <br>

If _Exposure Time_ is set to 50, and the _Timer Resolution_ value is 1, the CCD exposure time (integration time) = 50 microseconds.


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| time | Integer. Exposure time (expressed in Timer Resolution units).

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setExposureTime",
    "parameters": {
        "index": 0,
        "time": 50
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setExposureTime",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_gettimerresolution"></a>ccd_getTimerResolution

Gets the current timer resolution token.


**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| resolutionToken | Integer. Timer resolution token. <br> 0 - Timer resolution is set to 1000 microseconds <br> 1 - Timer resolution is set to 1 microsecond

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getTimerResolution",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getTimerResolution",
    "errors": [],
    "id": 1234,
    "results": {
        "resolutionToken": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_settimerresolution"></a>ccd_setTimerResolution

Sets the current timer resolution token.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| resolutionToken | Integer. Timer resolution token. <br> 0 - Sets the timer resolution to 1000 microseconds <br> 1 - Sets the timer resolution to 1 microsecond\*

_\*Note:_ The timer resolution value of 1 microsecond is not supported by every CCD.

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setTimerResolution",
    "parameters": {
        "index": 0,
        "resolutionToken": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setTimerResolution",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setacqformat"></a>ccd_setAcqFormat

Sets the acquisition format and the number of ROIs (Regions of Interest) or areas. After using this command to set the number of ROIs and format, the [ccd_setRoi](#ccd_setroi) command should be used to define each ROI.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| numberOfRois | Integer. Number of ROIs (Regions of Interest / areas)
>| format | Integer. The acquisition format. <br> 0 = Spectra <br> 1 = Image <br> 2 = Crop\* <br> 3 = Fast Kinetics\*

_\* Note:_ The Crop (2) and Fast Kinetics (3) acquisition formats are not supported by every CCD.

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setAcqFormat",
    "parameters":{
        "index": 0,
        "numberOfRois": 1,
        "format": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setAcqFormat",
    "errors": [],
    "id": 1234,
    "results":{}
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_setroi"></a>ccd_setRoi

Sets a single (_roiIndex_) ROI (Region of Interest) or area as defined by the X and Y origin, size, and bin parameters. The number of ROIs may be set using the [ccd_setAcqFormat](#ccd_setacqformat) command. For Spectral acquisition format set yBin = ySize.

_Note:_ All values must fall within the _x_ and _y_ limits of the chip sensor, see [ccd_getChipSize](#ccd_getchipsize). If the ROI is not valid, the device will not be properly setup for acquisition.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| roiIndex | Integer. The region of interest’s index (one-based)
>| xOrigin | Integer. The starting pixel in the x direction (zero-based)
>| yOrigin | Integer. The starting pixel in the y direction (zero-based)
>| xSize | Integer. The number of pixels in the x direction (one-based)
>| ySize | Integer. The number of pixels in the y direction (one-based)
>| xBin | Integer. The number of pixels to “bin” (x pixels summed to 1 value)
>| yBin | Integer. The number of pixels to “bin” (y pixels summed to 1 value)
**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setRoi",
    "parameters":{
        "index": 0,
        "roiIndex": 1,
        "xOrigin": 0,
        "yOrigin": 0,
        "xSize": 5,
        "ySize": 5,
        "xBin": 5,
        "yBin": 5
    }
}
```

**Example response:**

```json
{
    "command": "ccd_Roi",
    "errors": [],
    "id": 1234,
    "results":{}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getxaxisconversiontype"></a>ccd_getXAxisConversionType

Gets the X axis pixel conversion type to be used when retrieving the acquisition data with the [ccd_getAcquisitionData](#ccd_getacquisitiondata) command. 

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| type | Integer. The X-axis pixel conversion type to be used. <br> 0 = None (default) <br> 1 = CCD FIT parameters contained in the CCD firmware <br> 2 = Mono Wavelength parameters contained in the icl_settings.ini file


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getXAxisConversionType",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getXAxisConversionType",
    "errors": [],
    "id": 1234,
    "results": {
        "type": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setxaxisconversiontype"></a>ccd_setXAxisConversionType

Sets the X-axis pixel conversion type to be used when retrieving the acquisition data with the [ccd_getAcquisitionData](#ccd_getacquisitiondata) command.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| type | Integer. The X-axis pixel conversion type to be used. <br> 0 = None (default) <br> 1 = CCD FIT parameters contained in the CCD firmware <br> 2 = Mono Wavelength parameters contained in the icl_settings.ini file

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setXAxisConversionType",
    "parameters":{
        "index": 0,
        "type": 2
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setXAxisConversionType",
    "errors": [],
    "id": 1234,
    "results":{}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getacqcount"></a>ccd_getAcqCount

Gets the number of acquisition measurements to be perform sequentially by the hardware.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| count | Integer. The number of acquisition measurements to be performed.

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getAcqCount",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getAcqCount",
    "errors": [],
    "id": 1234,
    "results": {
        "count": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setacqcount"></a>ccd_setAcqCount

Sets the number of acquisition measurements to be performed sequentially by the hardware. A count > 1 is commonly referred to as "MultiAcq".

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| count | Integer. The number of acquisition measurements.

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setAcqCount",
    "parameters": {
        "index": 0,
        "count": 1
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setAcqCount",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getcleancount"></a>ccd_getCleanCount

Gets the number of cleans to be performed prior to measurement.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| count | Integer. Number of cleans. |
>| mode | Integer. Specifies how the cleans will be performed. <br> 0 = Never <br> 1 = First Only <br> 2 = Between Only <br> 3 = Each |


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getCleanCount",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getCleanCount",
    "errors": [],
    "id": 1234,
    "results": {
        "count": 1,
        "mode": 2
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setcleancount"></a>ccd_setCleanCount

Sets the number of cleans to be performed according to the specified mode setting.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| count | Integer. Number of cleans. |
>| mode | Integer. Specifies how the cleans will be performed. <br> 0 = Never <br> 1 = First Only <br> 2 = Between Only <br> 3 = Each |

**Return Results:**
>| results | description |
>|---|---|
>| _none_ | |


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setCleanCount",
    "parameters": {
        "index": 0,
        "count": 1,
        "mode": 1
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setCleanCount",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getdatasize"></a>ccd_getDataSize

Gets the number of pixels to be returned based on the current settings.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| size | Integer. Byte data size for all ROIs and acquisitions. |


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getDataSize",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getDataSize",
    "errors": [],
    "id": 1234,
    "results": {
        "size": 2048
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_gettriggerin"></a>ccd_getTriggerIn

This command is used to get the current setting of the input trigger. The _address_, _event_, and _signalType_ parameters are used to define the input trigger based on the supported options of that particular CCD. <br>
The supported trigger options are retrieved using the [ccd_getConfig](#ccd_getconfig) command, and begin with the "Triggers" string contained in the configuration. <br> **For example:** <br>
```json
"triggers": [
    {
        "events": [
            {
                "name": "Each - For Each Acq",
                "token": 1,
                "types": [
                    {
                        "name": "TTL Rising Edge",
                        "token": 1
                    },
                    {
                        "name": "TTL Falling Edge",
                        "token": 0
                    }
                ]
            },
            {
                "name": "Once - Start All",
                "token": 0,
                "types": [
                    {
                        "name": "TTL Rising Edge",
                        "token": 1
                    },
                    {
                        "name": "TTL Falling Edge",
                        "token": 0
                    }
                ]
            }
        ],
        "name": "Trigger Input",
        "token": 0
    }
]
```

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| address | Integer. Token used to specify _where_ the trigger is located. <br> (e.g. 0 = Trigger Input) <br> <br> _Note:_ Trigger name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the input trigger is disabled |
>| event | Integer. Token used to specify _when_ the trigger event should occur. <br> (e.g. 0 = Once - Start All) <br> <br> _Note:_ Event name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the input trigger is disabled |
>| signalType | Integer. Token used to specify _how_ the signal will cause the input trigger. <br> (e.g. 0 = TTL Falling Edge) <br> <br> _Note:_ Signal type and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the input trigger is disabled |


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getTriggerIn",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getTriggerIn",
    "errors": [],
    "id": 1234,
    "results": {
        "address": 0,
        "event": 0,
        "signalType": 0
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_settriggerin"></a>ccd_setTriggerIn

This command is used to enable or disable the trigger input. When enabling the trigger input, the _address_, _event_, and _signalType_ parameters are used to define the input trigger based on the supported options of that particular CCD. <br>
The supported trigger options are retrieved using the [ccd_getConfig](#ccd_getconfig) command, and begin with the "Triggers" string contained in the configuration. <br> **For example:** <br>
```json
"triggers": [
    {
        "events": [
            {
                "name": "Each - For Each Acq",
                "token": 1,
                "types": [
                    {
                        "name": "TTL Rising Edge",
                        "token": 1
                    },
                    {
                        "name": "TTL Falling Edge",
                        "token": 0
                    }
                ]
            },
            {
                "name": "Once - Start All",
                "token": 0,
                "types": [
                    {
                        "name": "TTL Rising Edge",
                        "token": 1
                    },
                    {
                        "name": "TTL Falling Edge",
                        "token": 0
                    }
                ]
            }
        ],
        "name": "Trigger Input",
        "token": 0
    }
]
```

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| enable | Boolean. Enables or disables the input trigger. <br> true = enable <br> false = disable <br> <br> _Note:_ When disabling the input trigger, the _address_, _event_, and _signalType_ parameters are ignored.|
>| address | Integer. Token used to specify _where_ the trigger is located. <br> (e.g. 0 = Trigger Input) <br> <br> _Note:_ Trigger name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |
>| event | Integer. Token used to specify _when_ the trigger event should occur. <br> (e.g. 0 = Once - Start All) <br> <br> _Note:_ Event name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |
>| signalType | Integer. Token used to specify _how_ the signal will cause the input trigger. <br> (e.g. 0 = TTL Falling Edge) <br> <br> _Note:_ Signal type and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setTriggerIn",
    "parameters": {
        "index": 0,
        "enable": true,
        "address": 0,
        "event": 0,
        "signalType": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setTriggerIn",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getsignalout"></a>ccd_getSignalOut

This command is used to get the current setting of the signal output. The _address_, _event_, and _signalType_ parameters are used to define the signal based on the supported options of that particular CCD. <br>
The supported signal options are retrieved using the [ccd_getConfig](#ccd_getconfig) command, and begin with the "Signals" string contained in the configuration. <br> **For example:** <br>
```json
"signals": [
    {
        "events": [
            {
                "name": "Shutter Open",
                "token": 3,
                "types": [
                    {
                        "name": "TTL Active Low",
                        "token": 1
                    },
                    {
                        "name": "TTL Active High",
                        "token": 0
                    }
                ]
            },
            {
                "name": "Start Experiment",
                "token": 0,
                "types": [
                    {
                        "name": "TTL Active Low",
                        "token": 1
                    },
                    {
                        "name": "TTL Active High",
                        "token": 0
                    }
                ]
            }
        ],
        "name": "Signal Output",
        "token": 0
    }
]
```

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| address | Integer. Token setting used to specify _where_ the signal is located. <br> (e.g. 0 = Signal Output) <br> <br> _Note:_ Signal name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the signal output is disabled |
>| event | Integer. Token setting used to specify _when_ the signal event should occur. <br> (e.g. 3 = Shutter Open) <br> <br> _Note:_ Event name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the signal output is disabled |
>| signalType | Integer. Token setting used to specify _how_ the signal will cause the event. <br> (e.g. 0 = TTL Active High) <br> <br> _Note:_ Signal type and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) <br> Value of -1 indicates that the signal output is disabled |

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getSignalOut",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getSignalOut",
    "errors": [],
    "id": 1234,
    "results": {
        "address": 0,
        "event": 2,
        "signalType": 1
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setsignalout"></a>ccd_setSignalOut

This command is used to enable or disable the signal output. When enabling the signal output, the _address_, _event_, and _signalType_ parameters are used to define the signal based on the supported options of that particular CCD. <br>
The supported signal options are retrieved using the [ccd_getConfig](#ccd_getconfig) command, and begin with the "Signals" string contained in the configuration. <br> **For example:** <br>
```json
"signals": [
    {
        "events": [
            {
                "name": "Shutter Open",
                "token": 3,
                "types": [
                    {
                        "name": "TTL Active Low",
                        "token": 1
                    },
                    {
                        "name": "TTL Active High",
                        "token": 0
                    }
                ]
            },
            {
                "name": "Start Experiment",
                "token": 0,
                "types": [
                    {
                        "name": "TTL Active Low",
                        "token": 1
                    },
                    {
                        "name": "TTL Active High",
                        "token": 0
                    }
                ]
            }
        ],
        "name": "Signal Output",
        "token": 0
    }
]
```

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| enable | Boolean. Enables or disables the signal. <br> true = enable <br> false = disable <br> <br> _Note:_ When disabling the signal output, the _address_, _event_, and _signalType_ parameters are ignored.|
>| address | Integer. Token used to specify _where_ the signal is located. <br> (e.g. 0 = Signal Output) <br> <br> _Note:_ Signal name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |
>| event | Integer. Token used to specify _when_ the signal event should occur. <br> (e.g. 3 = Shutter Open) <br> <br> _Note:_ Event name and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |
>| signalType | Integer. Token used to specify _how_ the signal will cause the event. <br> (e.g. 0 = TTL Active High) <br> <br> _Note:_ Signal type and token can be found in the CCD config, see [ccd_getConfig](#ccd_getconfig) |

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setSignalOut",
    "parameters": {
        "index": 0,
        "enable": 1,
        "address": 0,
        "event": 3,
        "signalType": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setSignalOut",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getacquisitionready"></a>ccd_getAcquisitionReady

This command is used to get the Acquisition Ready state. The Acquisition Ready state indicates whether the CCD has a sufficient number of parameters specified, and has been properly setup for acquiring data.

_Note:_ To specify the acquisition parameters please see [ccd_setROI](#ccd_setroi) and [ccd_setXAxisConversionType](#ccd_setxaxisconversiontype). If there are no acquisition parameters set at the time of acquisition it may result in no data being generated.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|


**Return Results:**
>| results | description |
>|---|---|
>| ready | Boolean. Acquisition Ready state. <br> false = Not Ready <br> true = Ready

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getAcquisitionReady",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getAcquisitionReady",
    "errors": [],
    "id": 1234,
    "results": {
        "ready": true
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setacquisitionstart"></a>ccd_setAcquisitionStart

Starts an acquisition that has been set up according to the previously defined acquisition parameters.

_Note:_ To specify the acquisition parameters please see [ccd_setROI](#ccd_setroi) and [ccd_setXAxisConversionType](#ccd_setxaxisconversiontype). If there are no acquisition parameters set at the time of acquisition it may result in no data being generated.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| open shutter | Boolean. Sets the state of the shutter during the acquisition. <br> True = open <br> False = close

**Return Results:**
>| results | description |
>|---|---|
>|_none_|

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setAcquisitionStart",
    "parameters":{
        "index": 0,
        "openShutter": true
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setAcquisitionStart",
    "errors": [],
    "id": 1234,
    "results":{}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getacquisitionbusy"></a>ccd_getAcquisitionBusy

Gets the current busy-state of an acquisition.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| isBusy | Boolean. Acquisition busy state. <br> False = Not busy <br> True = Busy


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getAcquisitionBusy",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getAcquisitionBusy",
    "errors": [],
    "id": 1234,
    "results": {
        "isBusy": false
    }
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_getacquisitiondata"></a>ccd_getAcquisitionData

Retrieves data from the last acquisition.

The acquisition description string consists of the following information:
- acqIndex: Acquisition number
- roiIndex: Region of Interest number
- xOrigin: ROI’s X Origin
- yOrigin: ROI’s Y Origin
- xSize: ROI’s X Size
- ySize: ROI’s Y Size
- xBinning: ROI’s X Bin
- yBinning: ROI’s Y Bin
- Timestamp: This is a timestamp that relates to the time when the all the programmed acquisitions have completed. The data from all programmed acquisitions are retrieved from the CCD after all acquisitions have completed, therefore the same timestamp is used for all acquisitions.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|

**Return Results:**
>| results | description |
>|---|---|
>| acquisition | String. Acquisition data. 

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getAcquisitionData",
    "parameters": {
        "index": 0
    }
}
```

**Example response:**

```json
{
    "command": "ccd_getAcquisitionData",
    "errors": [],
    "id": 1234,
    "results": {
        "acquisition": [
                {
                "acqIndex": 1,
                "roi":
                    [
                        {
                        "roiIndex": 1,
                        "xBinning": 1,
                        "xOrigin": 1,
                        "xSize": 8,
                        "xyData": [
                            [
                                885.6389770507812,
                                976
                            ],
                            [
                                885.2899780273438,
                                975
                            ],
                            [
                                884.9409790039062,
                                979
                            ],
                            [
                                884.593017578125,
                                976
                            ],
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="ccd_setcenterwavelength"></a>ccd_setCenterWavelength

Sets the center wavelength value to be used in the grating equation.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See [ccd_list](#ccd_list) command|
>| wavelength | Float. Center wavelength. |

**Return Results:**
>| results | description |
>|---|---|
>| _none_ |


**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_setCenterWavelength",
    "parameters": {
        "index": 0,
        "wavelength": 200.00
    }
}
```

**Example response:**

```json
{
    "command": "ccd_setCenterWavelength",
    "errors": [],
    "id": 1234,
    "results": {}
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


## SpectrAcq3 - Single Channel Detector Interface

### <a id="scd_discover"></a>scd_discover

Attempts to find SpectrAcq3 hardware connected and powered on the USB bus.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer value indicating number of SpectrAcq3's discovered|

**Example command:**

```json
{  
    "id": 1234,
    "command": "scd_discover"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "scd_discover",
    "results": {
        "count": 1
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="scd_list"></a>scd_list

Returns a formatted list of strings identifying each unit found.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|list|Array of strings each describing a SpectrAcq3 that was found. See below for format.|

String format per CCD found:

```c++
<index>;<SpectrAcq3 name>;<SpectrAcq3 serialnumber>
```

*index* - Integer index to use in SpectrAcq3 commands to indicate which SpectrAcq3 to target.  
*SpectrAcq3 name* - TBD  
*SpectrAcq3 serialnumber* - SpectrAcq3 reported serial number.  

**Example command:**

```json
{
    "id": 1234,
    "command": "scd_list"
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "scd_list",
    "results": {
        "list": [
            "0;iHR550;sn12345",
            "1;iHR320;snabscde",
        ]
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="scd_listcount"></a>scd_listCount

Returns the number of SpectrAcq3's found on the USB bus.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|count|Integer. Indicates the number of SpectrAcq3's found|

**Example command:**

```json
{
    "id": 1234,
    "command": "scd_listCount"
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "scd_listCount",
    "results": {
        "count": 1
    }
  "errors": []
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="scd_open"></a>scd_open

Opens communications with the SpectrAcq3 indicated by the index command parameter.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which SpectrAcq3 to target. See _scd_list_ command|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Open first (index 0) SpectrAcq3 in the list of monos discoverd.

```json
{  
    "id": 1234,
    "command": "scd_open",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "scd_open",
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="scd_close"></a>scd_close

Closes communications with the CCD indicated by the index.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which SpectrAcq3 to target. See _scd_list_ command|

**Response Results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**

```json
{
    "id": 1234,
    "command": "scd_close",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "scd_close",
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="scd_isopen"></a>scd_isOpen

Returns _true_ if selected SpectrAcq3 is open.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which SpectrAcq3 to target. See _scd_list_ command|

**Return Results:**
>| results | description |
>|---|---|
>|open|boolean. true = open|

**Example command:**

```json
{
    "id": 1234,
    "command": "scd_isOpen",
    "parameters":{
        "index": 0
    }
}
```

**Example response:**

```json
{
    "id": 1234,
    "command": "scd_isOpen",
    "results":{
        "open": true
    }
    "errors": [
    ]
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

## Binary Events

## Error Codes

```c++
ERR_NO_ERROR                     0

ERR_ICL_NOPARSERFOUND            -1
ERR_ICL_UNKNOWNCOMMAND           -2
ERR_ICL_INVALIDBINMODE           -3

ERR_CCD_ALREADY_INIT            -300
ERR_CCD_ALREADY_OPEN            -301
ERR_CCD_ALREADY_CLOSED          -302
ERR_CCD_ALREADY_UNINIT          -303
ERR_CCD_NOT_INITIALIZED         -304
ERR_CCD_NOT_OPEN                -305
ERR_CCD_NOT_FOUND               -306
ERR_CCD_INVALID_DEV_INDEX       -307
ERR_CCD_INITIALIZE_FAILURE      -308
ERR_CCD_ACQUIRING               -309
ERR_CCD_ACQPREP_FAILED          -310
ERR_CCD_NOT_READY_FOR_ACQ       -311
ERR_CCD_GETSPECTRA_FAILED       -312
ERR_CCD_GO_FAILED               -313
ERR_CCD_NO_FREE_PACKET          -314
ERR_CCD_CMD_NOT_SUPPORTED       -315
ERR_CCD_CMD_FAILED              -316
ERR_CCD_INVALID_TOKEN           -317
ERR_CCD_INVALID_VALUE           -318
ERR_CCD_CAPS_READ_ERROR         -319
ERR_CCD_ACQ_ALREADY_RUNNING     -320
ERR_CCD_ACQ_DATA_FORMAT_ERROR   -321
ERR_CCD_UNSUPPORTED_ACQ_FORMAT  -322
ERR_CCD_CMD_EXECUTION_EXCEPTION -323
ERR_CCD_MISSING_PARAMETER       -324

ERR_MONO_ALREADY_INIT           -500
ERR_MONO_ALREADY_OPEN           -501
ERR_MONO_ALREADY_OPENING        -502
ERR_MONO_ALREADY_CLOSED         -503
ERR_MONO_ALREADY_UNINIT         -504
ERR_MONO_NOT_INIT               -505
ERR_MONO_NOT_OPEN               -506
ERR_MONO_NOT_FOUND              -507
ERR_MONO_INVALID_DEV_INDEX      -508
ERR_MONO_INITIALIZE_FAILURE     -509
ERR_MONO_CMD_NOT_SUPPORTED      -510
ERR_MONO_DISCOVERY              -511
ERR_MONO_COMM_ERROR             -512
ERR_MONO_INVALID_PARAMETER      -513
ERR_MONO_LOST_USB_CONNECTION    -514
ERR_MONO_OPEN_ERROR             -515
ERR_MONO_ERROR_LOG              -516
ERR_MONO_INIT_ERROR             -517
ERR_MONO_GET_CONFIGURATION      -518
ERR_MONO_COMMAND_ERROR          -519
ERR_MONO_COMM_FAILED            -520
ERR_MONO_MISSING_PARAMETER      -521

ERR_SCD_CMD_NOT_SUPPORTED       -600

```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


## Production Commands

- [Monochromator Module Commands](#monochromator-module-commands-prod)
    - [mono\_moveSlit](#mono_moveslit)
    - [mono\_getSlitStepPosition](#mono_getslitstepposition)



<div style="page-break-before:always">&nbsp;</div>
<p></p>


## <a id="monochromator-module-commands-prod"></a>Monochromator Module Commands

### <a id="mono_moveslit"></a>mono_moveSlit

Moves the specified slit to the position in steps. The location id of each configured slit can be found under the ports section of the mono configuration. See [mono_getConfig](#mono_getconfig) for additional information.

**For example:**
```json
"ports": [
    {
        "locationId": 1,
        "slitType": 1
    },
    {
        "locationId": 2,
        "slitType": 1
    },
    {
        "locationId": 4,
        "slitType": 1
    }
]
```

_Note:_ The "locationId" parameter found in the mono configuration is 1-based. However, the mono_moveSlit command uses a 0-based "locationId".

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|
>| locationId | Integer. Slit location (zero-based) |
>| position | Integer. Position in steps |

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:** Move slit in port 2 to step position 250

```json
{
    "id": 1234,
    "command": "mono_moveSlit",
    "parameters":{
        "index": 0,
        "locationId": 1,
        "position": 250
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_moveSlit",
    "errors": [
    ]  
}
```


<div style="page-break-before:always">&nbsp;</div>
<p></p>


### <a id="mono_getslitstepposition"></a>mono_getSlitStepPosition

Returns the position of the specified slit in steps. The location id of each configured slit can be found under the ports section of the mono configuration. See [mono_getConfig](#mono_getconfig) for additional information.

**For example:**
```json
"ports": [
    {
        "locationId": 1,
        "slitType": 1
    },
    {
        "locationId": 2,
        "slitType": 1
    },
    {
        "locationId": 4,
        "slitType": 1
    }
]
```

_Note:_ The "locationId" parameter found in the mono configuration is 1-based. However, the mono_getSlitStepPosition command uses a 0-based "locationId".

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|
>| locationId | Integer. Slit location (zero-based) |

**Response results:**
>| results | description |
>|---|---|
>| position | Integer. Slit position in steps.|

**Example command:** Get step position of slit in port 4

```json
{
    "id": 1234,
    "command": "mono_getSlitStepPosition",
    "parameters":{
        "index": 0,
        "locationId": 3
    }
}
```

**Example response:**

```json
{  
    "command": "mono_getSlitStepPosition",
    "errors": [],
    "id": 1234,
    "results": {
        "position": 250
    }  
}
```
