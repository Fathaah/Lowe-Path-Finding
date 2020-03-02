# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.CORD

def GetCORD():

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	# vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# open the output CSV file for writing and initialize the set of
	# barcodes found thus far
	

	barcodeData = 'a'
	k=1
	# loop over the frames from the video stream
	while (k != 0):
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# find the barcodes in the frame and decode each of the barcodes
		barcodes = pyzbar.decode(frame)

	    	# loop over the detected barcodes
		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
			
			print(barcodeData)
			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			#return (barcodeData)
			# if the barcode text is currently not in our CSV file, write
			# the timestamp + barcode to disk and update the set
			k = k-1
		# show the output frame
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	 	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	
	print("[INFO] cleaning up...")
	
	cv2.destroyAllWindows()
	vs.stop()
	i = barcodeData.index("(")
	j = barcodeData.index(")")
	k = barcodeData.index(",")
	a = barcodeData[i+1:k]
	b = barcodeData[k+1:j]
	#if(barcodeData == 'entry'):
		#barcodeData1 = (60,60)
	return (int(a),int(b))
		


# close the output CSV file do a bit of cleanup
