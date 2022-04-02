from re import T
from telnetlib import Telnet
import cv2
import imutils
import time
from imutils.video.videostream import VideoStream

WEBCAM = 0

#Inicializando video
print("[INFO] inicializando streaming de video")
vs = VideoStream(src=WEBCAM).start()
time.sleep(2.0)

imagem = cv2.imread('naMerda.png', cv2.IMREAD_UNCHANGED)

#Classificador
classificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectando todos os rostos presentes no frame
    rosto = classificador.detectMultiScale(frame, 1.3, 5)

    for(x, y, w, h) in rosto:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255, 0), 2)

        # Redimensionando filtro
        redimensionando_imagem = imutils.resize(imagem, width=w)
        filas_imagem = redimensionando_imagem.shape[0]
        coluna_imagem = w

        dif = 0

        posicao_filtro = filas_imagem // 3

        # condição para que a imagem do filtro não desapareça se "faltar tela".
        if y - filas_imagem + posicao_filtro >= 0:
            n_frame = frame[y - filas_imagem + posicao_filtro: y + posicao_filtro, x: x + w] 
        else:
            dif = abs(y - filas_imagem + posicao_filtro)
            n_frame = frame[0: y + posicao_filtro, x: x + w]

        mask = redimensionando_imagem[:, :, 3]
        mask_inv = cv2.bitwise_not(mask)

        # Tratando a imagem do filtro para que fique com o fundo "transparente".
        bg_black = cv2.bitwise_and(redimensionando_imagem, redimensionando_imagem, mask=mask)
        bg_black = bg_black[dif:, :, 0:3]
        bg_frame = cv2.bitwise_and(n_frame, n_frame, mask=mask_inv[dif:, :])

        result = cv2.add(bg_black, bg_frame)
        if y - filas_imagem + posicao_filtro >= 0:
            frame[y - filas_imagem + posicao_filtro: y + posicao_filtro, x: x + w] = result
        else:
            frame[0: y + posicao_filtro, x: x + w] = result
            
            

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()

'''Trabalho da disciplina "FUNDAMENTOS DE REALIDADE VIRTUAL E AUMENTADA"

Nome: Willian de Oliveira Damas  RA: D92672-1
Nome: Matheus Aparecido Luccas   RA: N39948-1

'''

