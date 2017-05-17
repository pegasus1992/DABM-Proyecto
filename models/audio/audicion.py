from PyQt5 import QtCore
import threading
import speech_recognition as sr


class AudioThread(QtCore.QThread):
    sig = QtCore.pyqtSignal(str)

    def __init__(self, ui):
        QtCore.QThread.__init__(self)
        self.r = sr.Recognizer()
        self.sig.connect(ui.acciones)
        return

    def run(self):
        while True:
            # Record Audio
            with sr.Microphone() as source:
                audio = self.r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = self.r.listen(source)
            # Speech recognition using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                language = "es-CO"
                orden = self.r.recognize_google(audio, language=language)
                print("You said: " + orden)
                self.sig.emit(orden)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return
