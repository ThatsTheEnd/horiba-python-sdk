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
  - [Monochromater Module Commands](#monochromater-module-commands)
    - [mono\_discover](#mono_discover)
    - [mono\_list](#mono_list)
    - [mono\_listCount](#mono_listcount)
    - [mono\_open](#mono_open)
    - [mono\_close](#mono_close)
    - [mono\_isOpen](#mono_isopen)
    - [mono\_isBusy](#mono_isbusy)
    - [mono\_init](#mono_init)
    - [mono\_getConfig](#mono_getconfig)
    - [mono\_setConfig](#mono_setconfig)
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
    - [mono\_getSlitStepPosition](#mono_getslitstepposition)
    - [mono\_moveSlit](#mono_moveslit)
    - [mono\_enableLaser](#mono_enablelaser)
    - [mono\_getLaserStatus](#mono_getlaserstatus)
    - [mono\_setLaserPower](#mono_setlaserpower)
    - [mono\_getLaserPower](#mono_getlaserpower)
    - [mono\_getLidStatus](#mono_getlidstatus)
    - [mono\_getSwitchStatus](#mono_getswitchstatus)
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
    - [ccd\_getNumberOfAvgs](#ccd_getnumberofavgs)
    - [ccd\_setNumberOfAvgs](#ccd_setnumberofavgs)
    - [ccd\_getGain](#ccd_getgain)
    - [ccd\_setGain](#ccd_setgain)
    - [ccd\_getSpeed](#ccd_getspeed)
    - [ccd\_setSpeed](#ccd_setspeed)
    - [ccd\_getFitParams](#ccd_getfitparams)
    - [ccd\_setFitParams](#ccd_setfitparams)
    - [ccd\_getExposureTime](#ccd_getexposuretime)
    - [ccd\_setExposureTime](#ccd_setexposuretime)
    - [ccd\_getTimerResolution](#ccd_gettimerresolution)
    - [ccd\_setTimerResolution](#ccd_settimerresolution)
    - [ccd\_setAcqFormat](#ccd_setacqformat)
    - [ccd\_setRoi](#ccd_setroi)
    - [ccd\_getXAxisConversionType](#ccd_getxaxisconversiontype)
    - [ccd\_setXAxisConversionType](#ccd_setxaxisconversiontype)
    - [ccd\_getDataRetrievalMethod](#ccd_getdataretrievalmethod)
    - [ccd\_setDataRetrievalMethod](#ccd_setdataretrievalmethod)
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
    - [ccd\_setAcquisitionAbort](#ccd_setacquisitionabort)
    - [ccd\_getAcquisitionData](#ccd_getacquisitiondata)
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
3. Automaticaly started by adding a shortcut to the Windows startup folder.
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

**id** optional field. An integer number that can be used to line-up/sync-up outgoing commands with incoming asyncrounous response.  _May remove._  
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

## Monochromater Module Commands

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

Returns a formated list of strings.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|list|Array of strings each describing a monochromator that was found. See below for format.|

String format per monochromator found:

```c++
<index>;<mono name>;<mono serialnumber>
```

*index* - Integer index to use in monochromator commands to indicate which monochomator to target.  
*mono name* - ??  
*mono serialnumber* - Monochromator reported serial number.  

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
    "id": 1234,
    "command": "mono_list",
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
>| index | Integer. Used to identify which mono to target. See _mono_list_ command|

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
>| index | Integer. Used to identify which mono to target. See _mono_list_ command|

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

Returns _true_ if selected monochromater is open.  

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See _mono_list_ command|

**Return Results:**
>| results | description |
>|---|---|
>|open|boolean. true = open|

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

Returns _true_ if selected monochromater is busy.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to target. See _mono_list_ command|

**Response results:**
>| results | description |
>|---|---|
>|busy|boolean. true = busy|

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

Starts the monochromator initialization process (homing...). This is a "long-running" asynchronous command. Use the _mono_isBusy_ command to know when initialization has completed.

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|

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
        "index": 0
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

### <a id="mono_getconfig"></a>mono_getConfig

This command returns the monochromator configuration.

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### mono_getPosition

Returns the wavelength value, in nm, of the monochromator's current position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|

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

This command sets the wavelength value of the current grating position of the monochromator. This could potentially uncalibrate the monochromator and report an incorrect wavelength compared to the actual output wavelength.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|
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

This command starts the monochromater moving to the requested wavelength in nm. This is an asynchronous command. Use the _mono_isBusy_ command to know when the move has completed.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|
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
    "command": "mono_setPosition",
    "parameters":{
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

### <a id="mono_getgratingposition"></a>mono_getGratingPosition

Returns the current grating turret position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|

**Response results:**
>| results | description |
>|---|---|
>|position|Integer.|

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

Move the grating turret.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which mono to control. See _mono_list_ command|
>|position| Integer.|

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

Returns the current filterwheel position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| type | Integer. Identifies which filterwheel. TODO possible values.|

**Response results:**
>| results | description |
>|---|---|
>|position|Integer. TODO - possible positions|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getFilterWheelPosition",
    "parameters":{
        "type": 1
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_getFilterWheelPosition",
    "results":{
        "position": 1
    }  
    "errors": [
    ]  
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_movefilterwheel"></a>mono_moveFilterWheel

Move the filterwheel to a position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|type| Integer. Identifies which filterwheel.|
>|position| Integer. Position to move to.|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Move filterwheel to position 1.

```json
{
    "id": 1234,
    "command": "mono_moveFilterWheel",
    "parameters":{
        "type": 0,
        "position": 1
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_moveFilterWheel",
    "errors": [
    ]  
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_getmirrorposition"></a>mono_getMirrorPosition

Returns the position of the mirror.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>| type | Integer. Identifies which mirror. TODO possible values.|

**Response results:**
>| results | description |
>|---|---|
>|position|Integer. TODO - possible positions|

**Example command:**

```json
{
    "id": 1234,
    "command": "mono_getMirrorPosition",
    "parameters":{
        "type": 1
    }
}
```

**Example response:**

```json
{  
    "id": 1234,
    "command": "mono_getMirrorPosition",
    "results":{
        "position": 1
    }  
    "errors": [
    ]  
}
```

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="mono_movemirror"></a>mono_moveMirror

Move the mirror to a position.  

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|type| Integer. Identifies which mirror.|
>|position| Integer. Position to move to.|

**Response results:**
>| results | description |
>|---|---|
>|_none_||

**Example command:**
Move mirror to position 1.

```json
{
    "id": 1234,
    "command": "mono_moveMirror",
    "parameters":{
        "type": 0,
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

### mono_getSlitPositionInMM

### mono_moveSlitMM

### mono_shutterOpen

### mono_shutterClose

### mono_getShutterStatus

### mono_getSlitStepPosition

### mono_moveSlit

### mono_enableLaser

### mono_getLaserStatus

### mono_setLaserPower

### mono_getLaserPower

### mono_getLidStatus

### mono_getSwitchStatus

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
A typical return result for a system containing two CCDs might appear similar to the following:  

0;7;HORIBA Scientific Synapse / Symphony II;Camera SN: 439  
1;8;HORIBA Scientific Compact CCD;Camera SN: 1026

Each discovered CCD item in the list consists of four details separated by a semicolon character (‘;’). These details are:  

- ccd index: Index of the discovered CCD
- ccd product id: CCD HORIBA USB product id (PID)
- ccd description: CCD HORIBA device description
- ccd serial number: CCD HORIBA serial number

**Command parameters:**
>| parameter  | description   |
>|---|---|
>|_none_||

**Response results:**
>| results | description |
>|---|---|
>|list|Array of strings each describing a CCD that was found. See below for format.|

String format per CCD found:

```c++
<index>;<CCD name>;<CCD serialnumber>
```

*index* - Integer index to use in CCD commands to indicate which CCD to target.  
*CCD name* - TBD  
*CCD serialnumber* - CCD reported serial number.  

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
    "id": 1234,
    "command": "ccd_list",
    "results": {
        "list": [
            "0;7;HORIBA Scientific Synapse / Symphony II;Camera SN: 439",
            "1;8;HORIBA Scientific Compact CCD;Camera SN: 1026",
        ]
    }
  "errors": []
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
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|

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
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|

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
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|

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

### <a id="ccd_getconfig"></a>ccd_getConfig

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_getchipsize"></a>ccd_getChipSize

Returns the chip sensor’s pixel width and height size.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|

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

### ccd_getChipTemperature

### ccd_getNumberOfAvgs

### ccd_setNumberOfAvgs

### ccd_getGain

### ccd_setGain

### ccd_getSpeed

### ccd_setSpeed

### ccd_getFitParams

### ccd_setFitParams

### ccd_getExposureTime

### ccd_setExposureTime

### ccd_getTimerResolution

### ccd_setTimerResolution

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_setacqformat"></a>ccd_setAcqFormat

Sets the acquisition format and the number of ROIs (Regions of Interest) or areas. After using this command to set the number of ROIs and format, the [ccd_setRoi](#ccd_setroi) command should be used to define each ROI.

_\* Note: The Crop (2) and Fast Kinetics (3) acquisition formats are not supported by every CCD._

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|
>| numberOfRois | Integer. Number of ROIs (Regions of Interest / areas)
>| format | Integer. The acquisition format. <br> 0 = Spectra <br> 1 = Image <br> 2 = Crop\* <br> 3 = Fast Kinetics\*

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

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|
>| roiIndex | Integer. The region of interest’s index (one-based index)
>| xOrigin | Integer. The one-based starting pixel in the x direction
>| yOrigin | Integer. The one-based starting pixel in the y direction
>| xSize | Integer. The Number of pixels in the x direction
>| ySize | Integer. The Number of pixels in the y direction
>| xBin | Integer. The Number of pixels to “bin” (x pixels summed to 1 value)
>| yBin | Integer. The Number of pixels to “bin” (y pixels summed to 1 value)
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
        "xOrigin": 1,
        "yOrigin": 1,
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

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_setxaxisconversiontype"></a>ccd_setXAxisConversionType

Sets the X-axis pixel conversion type to be used when retrieving the acquisition data with the [ccd_getAcquisitionData](#ccd_getacquisitiondata) command.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|
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

### ccd_getDataRetrievalMethod

### ccd_setDataRetrievalMethod

### ccd_getAcqCount

### ccd_setAcqCount

### ccd_getCleanCount

### ccd_setCleanCount

### ccd_getDataSize

### ccd_getTriggerIn

### ccd_setTriggerIn

### ccd_getSignalOut

### ccd_setSignalOut

### ccd_getAcquisitionReady

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_setacquisitionstart"></a>ccd_setAcquisitionStart

Starts an acquisition that has been set up according to the previously defined acquisition parameters.

Note: To specify the acquisiton parameters please see [ccd_setROI](#ccd_setroi) and [ccd_setXAxisConversionType](#ccd_setxaxisconversiontype). If there are no acquisition parameters set at the time of acquisition it may result in no data being generated.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|
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

### ccd_getAcquisitionBusy

### ccd_setAcquisitionAbort

<div style="page-break-before:always">&nbsp;</div>
<p></p>

### <a id="ccd_getacquisitiondata"></a>ccd_getAcquisitionData

Retrieves data from the last acquisition. The acquisition data is returned in ASCII text format as comma-separated XY values. The XY values for each acquisition and Region of Interest (ROI) are preceded by a header description string.  

The acquisition header description string consists of the following information
- Acq. #: Acquisition number  
- ROI #: Region of Interest number  
- xOrigin-#: ROI’s X Origin  
- yOrigin-#: ROI’s Y Origin  
- xSize-#: ROI’s X Size  
- ySize-#: ROI’s Y Size  
- xBin-#: ROI’s X Bin  
- yBin-#: ROI’s Y Bin  
- @ ###: Timestamp. This is a timestamp that relates to the time when the all the programmed acquisitions have completed. The data from all programmed acquisitions are retrieve from the CCD after all acquisitions have completed, therefore the same header timestamp is used for all acquisitions.

**Command Parameters:**
>| parameter  | description   |
>|---|---|
>| index | Integer. Used to identify which CCD to target. See _ccd_list_ command|

**Return Results:**
>| results | description |
>|---|---|
>| data | String. Acquisition data. 

**Example command:**

```json
{
    "id": 1234,
    "command": "ccd_getAcquisitionData",
    "parameters":{
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
    "results":{
        "data": "Acq. 1 - ROI 1: xOrigin-1; yOrigin-1; xSize-1; ySize-1; xBin-1; yBin-1; @ 2024.02.01
        10:35:46.937 
        823.527,0"
    }
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

Returns a formated list of strings identifying each unit found.

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

ERR_MONO_ALLREADY_INIT          -500
ERR_MONO_ALLREADY_OPEN          -501
ERR_MONO_ALLREADY_OPENING       -502
ERR_MONO_ALLREADY_CLOSED        -503
ERR_MONO_ALLREADY_UNINIT        -504
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
