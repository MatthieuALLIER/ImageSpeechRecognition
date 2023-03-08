import cv2

def pretrained_age():

    ageProto = "./video/model/age_deploy.prototxt"
    ageModel = "./video/model/age_net.caffemodel"

    genderProto = "./video/model/gender_deploy.prototxt"
    genderModel = "./video/model/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    ageNet = cv2.dnn.readNet(ageModel,ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    return ageNet,genderNet,ageList,genderList,MODEL_MEAN_VALUES