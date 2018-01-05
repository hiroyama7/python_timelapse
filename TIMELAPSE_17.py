#########################################################
#TIMELAPSE SCRIPT (XPERIA X COMPACT, GOOGLE PHOTO UPLOAD)
#(c)2017 Hiroyuki Yamada<hiroyama@env.agr.hokudai.ac.jp>
#
#CONSOLE:
#QPYTHON3<https://play.google.com/store/apps/details?id=org.qpython.qpy3&hl=ja>
#SL4A<https://github.com/damonkohler/sl4a>
#REFERENCE: 
#<http://docs.solab.jp/sl4a/api/dialog/>
#<http://www.submergedspaceman.com/blog/?p=154>
#<http://www.linux-magazine.com/Issues/2015/176/Workspace-Python-Scripting#article_l2>
#<http://stackoverflow.com/questions/40305725/kivy-android-how-to-create-and-read-a-file>
#<http://qiita.com/wasnot/items/ae1e6282d2c33626b604>
# INSTALL: 
# ScanMediaPlease<https://play.google.com/store/apps/details?id=net.zhuoweizhang.scanmediaplz&hl=ja>
#########################################################
import android, time, datetime, os
droid = android.Android()

#****************************************************
title = "TIMELAPSE"
message = "Hello!"
droid.dialogCreateAlert(title, message)
droid.dialogSetPositiveButtonText("Continue")
droid.dialogSetNegativeButtonText("Cancel")
droid.dialogShow()
response = droid.dialogGetResponse()
if response.result["which"] == "negative":
   droid.makeToast("Cancelled. Bye!")
   time.sleep(2)
   droid.dialogDismiss()
   exit()
time.sleep(1)
#****************************************************
title = 'Choose or enter interval'
droid.dialogCreateAlert(title)
items =["2 sec", "10 sec", "10 min","60 min","24 hr","Custom"]
droid.dialogSetItems(items)
droid.dialogShow()
response = droid.dialogGetResponse().result["item"]
#droid.makeToast(str(response))
#droid.makeToast(items[response])
#droid.dialogDismiss()
if response == 0:
 timer = 2
elif response == 1:
 timer = 10
elif response == 2:
 timer = 10 * 60
elif response == 3:
 timer = 60 * 60
elif response == 4:
 timer = 24 * 60 * 60
elif response == 5:
 timer = droid.dialogGetInput('Custom', 'Please enter interval in second').result
interval = int(timer)
droid.makeToast("Interval: " + str(timer) + " (sec)")
droid.dialogDismiss()
print("Interval: " + str(timer) + " (sec)")
time.sleep(1)

#****************************************************
title = "START TIME SETTING"
droid.dialogCreateAlert(title)
droid.dialogSetPositiveButtonText("From now")
droid.dialogSetNegativeButtonText("Custom")
droid.dialogShow()
response = droid.dialogGetResponse()
if response.result["which"] == "negative":
 ##DATE PICKER
 y = time.strftime("%Y", time.localtime())
 m = time.strftime("%m", time.localtime())
 d = time.strftime("%d", time.localtime())
 droid.dialogCreateDatePicker(int(y), int(m), int(d))
 droid.dialogShow()
 response = droid.dialogGetResponse()
 if response.result["which"] == "positive":
    dates = "%d-%02d-%02d" % (response.result["year"], response.result["month"], response.result["day"])
    droid.makeToast(dates)
 droid.dialogDismiss()
 time.sleep(1)

 ##TIME PICKER
 droid.dialogCreateTimePicker(00, 00)
 droid.dialogShow()
 response = droid.dialogGetResponse()
 if response.result["which"] == "positive":
    times = "%02d:%02d" % (response.result["hour"], response.result["minute"])
    timess = times + ":00"
    droid.makeToast(timess)
 droid.dialogDismiss()
 time.sleep(1)

 ##START TIME SETTING
 st = dates + " " + timess
 droid.makeToast(st)
 droid.dialogDismiss()
 stdt = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
 epocst = time.mktime(stdt.timetuple())
 sleeptime = epocst - time.time()
 if sleeptime <= 0.0:
   droid.makeToast("Woops, you missed start time!")
   droid.dialogDismiss()
   exit()
 time.sleep(1)

 #****************************************************
 title = "RECORDING"
 message = "Ready? Press START!"
 droid.dialogCreateAlert(title, message)
 droid.dialogSetPositiveButtonText("START")
 droid.dialogSetNegativeButtonText("Cancel")
 droid.dialogShow()
 response = droid.dialogGetResponse()
 if response.result["which"] == "negative":
   droid.makeToast("Cancelled. Bye!")
   time.sleep(2)
   droid.dialogDismiss()
   exit()
 print("Start time: " + st)
 print("Please wait until start time.")
 #droid.ttsSpeak("Please wait until start time")
 print("You can stop the recording using the back button.")
 #****************************************************

 sleeptime = epocst - time.time()
 droid.makeToast(str(sleeptime))
 droid.makeToast("Please wait until start time...")
 droid.dialogDismiss()
 droid.makeToast("You can stop the recording using the back button.")
 time.sleep(3)
 droid.dialogDismiss()

 time.sleep(sleeptime)
 #****************************************************

#****************************************************
#folder = os.path.dirname(os.path.abspath(__file__))
folder = "/storage/emulated/0/DCIM/TLP"
print("Path: " + folder)
if not os.path.exists(folder):
    os.makedirs(folder)
droid.makeToast("PATH: " + folder)
droid.dialogDismiss()
stTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
print(stTime)
#****************************************************
while True:
 ##NIGHT to MORNING SLEEP SETTING
 now =  datetime.datetime.now()
 epocnow = int(time.mktime(now.timetuple()))
 print("Now    : " + str(epocnow))

 nt = now.strftime("%Y/%m/%d") +" "+ "19:00"
 ntt = datetime.datetime.strptime(nt, "%Y/%m/%d %H:%M")
 epocntt = int(time.mktime(ntt.timetuple()))
 print("Night  : " + str(epocntt))

 mt = now.strftime("%Y/%m/%d") +" "+ "5:00"
 mtt = datetime.datetime.strptime(mt, "%Y/%m/%d %H:%M")
 epocmtt = int(time.mktime(mtt.timetuple()))
 print("Morning: " + str(epocmtt))
 ##
 
 if epocnow > epocntt or epocnow < epocmtt:
    print("Please wait until the next moring...")
    time.sleep(60)
    continue

 captureTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
 captureLocation = folder+"/"+str(captureTime)+".jpg"
 #droid.makeToast("Store: " + captureLocation)
 #droid.dialogDismiss()
 #droid.cameraCapturePicture(captureLocation) # autofocus
 droid.cameraCapturePicture(captureLocation,False)
 #droid.makeToast("Captured")
 #droid.dialogDismiss()
 #droid.makeToast("Please wait until next capture...")
 #droid.dialogDismiss()
 print(captureLocation)
 print("Please wait until next capture...")
 #
 droid.launch("net.zhuoweizhang.scanmediaplz.ScanMediaPlzActivity")
 #droid.forceStopPackage("net.zhuoweizhang.scanmediaplz.ScanMediaPlzActivity")
 #
 time.sleep(interval)
#****************************************************

