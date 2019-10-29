import sys, os
import s3_utils

detectPath = os.path.abspath(os.path.join('..', 'darknet-AlexeyAB'))
basedir = os.path.abspath(os.path.dirname(__file__))

def getDetectionResult(filePath):
    fileName = os.path.basename(filePath)
    outputPath = os.path.join(basedir, 'detect/' + fileName)
    print outputPath
    os.chdir(detectPath)
    cmd = "python " + os.path.join(detectPath, "darknet_video.py") + " --video " + filePath + " --output " + outputPath + " --net_config " + os.path.join(detectPath, "cfg/yolov3_416.cfg") + " --net_weights " + os.path.join(detectPath, "weights/yolov3_416_final.weights") + " --metafile " + os.path.join(detectPath, "cfg/sharks.data") + " --output_h 400"  + " --output_w 400" + " --output_bbox " + "true"
    print cmd
    os.system(cmd)
    # upload to s3 and return the path to the result video
    outputVideoPath = s3_utils.upload(outputPath, "detect_" + fileName)   
    # get detect type
    detFileName = os.path.splitext(fileName)[0] + '.det'
    detFilePath = os.path.join(basedir, 'detect/' + detFileName)
    detFile = open(detFilePath, 'r')
    label = detFile.readlines()[1].split('\t')[-1]
    # remove everthing in the detect folder
    os.remove(detFile)
    print "label is " +label
     
    return outputVideoPath, label
