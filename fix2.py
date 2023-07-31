import serial as ser
import cv2
from time import sleep
import numpy as np 
import time
import csv
import os

# bisa = ser.Serial("COM6", 115200)

# def gerakkan_motor(motor_command):
#     bisa.write(motor_command.encode())

tesmode = 1

# def berhenti():
#     gerakkan_motor('4')
    
# def lurus():
#     gerakkan_motor('a')

# def kanan():
#     #gerakkan_motor('d')
#     #sleep(3)
#     gerakkan_motor('2')
#     # sleep(0.3)
#     # gerakkan_motor('a')
#     # sleep(0.2)

# def kiri():
#     #gerakkan_motor('d')
#     #sleep(3)
#     gerakkan_motor('d')
#     # sleep(0.3)
#     # gerakkan_motor('a')
#     # sleep(0.2)

# def mundur():
#     gerakkan_motor('7')

# def putar_poros_kanan():
#     gerakkan_motor('5')
#     sleep(0.5)
#     gerakkan_motor('a')

# def putar_poros_kiri():
#     gerakkan_motor('6')
#     sleep(0.5)
#     gerakkan_motor('a')

# def stop_sementara():
#     # gerakkan_motor('4') #stoop
#     # sleep(0.5)
#     gerakkan_motor('5') #mutar kanan
#     sleep(0.8)
#     gerakkan_motor('a') # lurus
#     sleep(0.2)
#     # gerakkan_motor('5')
#     # sleep(0.2)
#     # gerakkan_motor('a')

# def stop_sementara_lagi():
#     # gerakkan_motor('4') #stoop
#     # sleep(0.5)
#     gerakkan_motor('6') #mutar kiri
#     sleep(0.8)
#     gerakkan_motor('a') # lurus
#     sleep(0.2)
#     # gerakkan_motor('6')
#     # sleep(0.2)
#     # gerakkan_motor('a')

# def gerak_menghindar_kanan():
#     gerakkan_motor('4')
#     sleep(0.3)
#     gerakkan_motor('8')
#     sleep(0.4)
#     gerakkan_motor('a')
#     sleep(0.3)
#     gerakkan_motor('d')
#     sleep(0.3)
#     gerakkan_motor('a')

# def gerak_menghindar_kiri():
#     gerakkan_motor('4')
#     sleep(0.3)
#     gerakkan_motor('9')
#     sleep(0.4)
#     gerakkan_motor('a')
#     sleep(0.3)
#     gerakkan_motor('2')
#     sleep(0.3)
#     gerakkan_motor('a')

# def gerakan_ke_kiri():
#     gerakkan_motor('d')
#     sleep(0.3)
#     gerakkan_motor('a')

# def gerakan_ke_kanan():
#     gerakkan_motor('2')
#     sleep(0.3)
#     gerakkan_motor('a')


# Menghitung jarak
def kal_jarak(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    jarak = np.sqrt((x2 - x1)**2 + (y2-y1)**2)
    return jarak

# Buat tiga cabang dalam satu frame
def buat_Cabang(EdgeArray, ukuran_cabang):
    Cabang = []
    for i in range(0, len(EdgeArray), ukuran_cabang):
        Cabang.append(EdgeArray[i:i + ukuran_cabang])
    return Cabang

# Memunculkan kamera
cap = cv2.VideoCapture(0)
StepSize = 5
currentFrame = 0
fps = 0 
frame_count = 0
fps_start_time = time.time()

csv_file = 'percobaan_barulagi.csv'
header = ['edgearray', 'cabang', 'x_vals', 'y_vals', 'avg_x', 'avg_y', 'avg_of_chunck', 'forward_edge', 'forward_edge[0]', 'farthest_point', 'farthest_point[1]', 'arah', 'jarak']
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
# if tesmode == 1:
#     F = open("")

try:
   if not os.path.exists('data'):
      os.makedirs('data')
except OSError:
   print ('Error: Creating directory of data')

StepSize = 5
currentFrame = 0

if tesmode == 1:
   F = open("./data/imagedetails.txt",'a')
   F.write("\n\nNew Test \n")

while (1):
    _, frame = cap.read()
    name = './data/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)

    frame_asli = frame.copy() # Sebagai perbandingan gambar asli dengan lainnya
    img_edgerepresentation = frame.copy() # Untuk menampilkan edge representation
    img_contour = frame.copy() #untuk menampilkan hasil deteksi kontur
    img_navigasi = frame.copy() # untuk menunjukkan arah

    gray = cv2.cvtColor(img_contour, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 9, 40, 40) # teknik blur gambar untuk menghilangkan noise
    print("blur: ",blur)
    edges = cv2. Canny(blur, 50, 100)# Mendapatkan tepi yang jelas menggunakan canny edge detection

    
    # Menyimpan tinggi pada Gambar jika akan digunakan dalam kondisi loop
    img_edgerepresentation_h = img_edgerepresentation.shape[0] - 1 
    print("h:", img_edgerepresentation_h)
    # Menyimpan lebar pada Gambar jika akan digunakan dalam kondisi loop
    img_edgerepresentation_w = img_edgerepresentation.shape[1] - 1
    print("w:", img_edgerepresentation_w)


    if _:
        # Hitung FPS
        frame_count += 1
        if (time.time() - fps_start_time) > 1:
            fps = frame_count / (time.time() - fps_start_time)
            fps_start_time = time.time()
            frame_count = 0

    # Initilisasi array untuk menyimpan tepi yang bersangkutan untuk representasi tepi.
    EdgeArray = []
    # print("edge:", EdgeArray)

    # Untuk loop sepanjang lebar gambar dengan stepize yang diberikan.
    for j in range(0, img_edgerepresentation_w, StepSize):
        # jika tepi tidak ditemukan dalam kolom, nilai akan disimpan didalam edgearray
        pixel = (j, 0) 
        # untuk loopin
        # g height pada gambar
        for i in range(img_edgerepresentation_h - 5, 0, -1):
            # mengecheck untuk tepi
            if edges.item(i, j) == 255:
                pixel = (j, i)
                break
        EdgeArray.append(pixel)


    # # Mengukuti setiap tepi untuk perbedaan frame menjadi ruang kosong dan ruang yang dikonjustifikasi (dengan objek)
    # hijau = untuk pemetaan yg menunjukkan penandaan di luar (membedakan ruang kosong dengan obstacle di dalam frame)
    for x in range(len(EdgeArray) - 1):
        cv2.line(img_edgerepresentation, EdgeArray[x], EdgeArray[x + 1], (0,255,0), 1)   
    # print("Tepi:", EdgeArray[x])
    # print("edge:", EdgeArray[x + 1])    
    
    # # Mengukuti setiap tepi untuk perbedaan frame menjadi ruang kosong dan ruang yang dikonjustifikasi (dengan objek)
    # biru = untuk pemetaan yg menunjukkan penandaan di dalam (mengisi penanda di ruang kosong)
    for x in range(len(EdgeArray)):
        cv2.line(img_edgerepresentation, (x * StepSize, img_edgerepresentation_h), EdgeArray[x], (0,255,0),1)
    # print("xam:", EdgeArray)
    # print('exel:', len(EdgeArray)-1)
    # print('varensia', len(EdgeArray))
    # print('x:', x)
    # print("hasil: ", x * StepSize)
    # print("img:", img_edgerepresentation_h)
    # print("coba :", img_edgerepresentation)

    # Program untuk deteksi kontur
    
    
    blurin_frame = cv2.bilateralFilter(gray, 9, 75, 75)
    ret, thresh = cv2.threshold(blurin_frame, 106, 255, 1)
    brightness = cv2.mean(gray)[0]
    print("Intensitas cahaya:", brightness)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_edgerepresentation, contours, -1, (0, 0, 255), 3)

    #Program untuk membuat keputusan arah kanan, kiri dan lurus
    banyak_cabang = 3
    panjang_cabang = int(len(EdgeArray) / banyak_cabang)
    cabang = buat_Cabang(EdgeArray, panjang_cabang)
    # print("cabang:", cabang)
    rata_pada_cabang = []

    for i in range(len(cabang) -1):
        x_vals = []
        y_vals = []
        # Simpan nilai x dan y yang dipisahkan untuk menemukan rata - rata
        for (x, y) in cabang[i]:
            x_vals.append(x)
            y_vals.append(y)
        avg_x = int(np.average(x_vals))
        avg_y = int(np.average(y_vals))
        rata_pada_cabang.append([avg_y, avg_x])
        #bentuk 3 garis arah cabang
        cv2.line(frame, (int(img_edgerepresentation_w / 2), img_edgerepresentation_h), (avg_x, avg_y), (255, 0, 0), 2)
        print("www:", img_edgerepresentation_w / 2) 
    
    arah_lurus = rata_pada_cabang[1]
    # print("yaaa:",len(cabang))
    #print(arah_lurus)
    # cv2.line(frame, (int(img_edgerepresentation_w / 2), img_edgerepresentation_h), (arah_lurus[1], arah_lurus[0]), (0, 255, 0), 3)
    titik_terjauh = (min(rata_pada_cabang))
    #print(titik_terjauh)

    # Check pada objek didepan yang terdekat pada robot
    # print(arah_lurus[0])
    
    # Diluar dari dua kondisi tersebut adalah arah lurus
    # if arah_lurus[0] > 330:
    #330
    #310
    if arah_lurus[0] > 330:
        if titik_terjauh[1] < 310:
            # kiri()
            arah = "Kiri"
            print(arah)
        else:
            # kanan()
            arah = "Kanan"
            print(arah)
    
    elif arah_lurus[0] > 166 and arah_lurus[0] < 330:
        # lurus()
        arah = "Lurus"
        print(arah)
    
    else:
        # berhenti()
        arah = "berhenti"
        print(arah)
    
    
    # if titik_terjauh[1] ==  102:  
    #     kiri()
    #     #kiri()
    #     arah = "Kiri "
    #     print(arah)
    # elif titik_terjauh [1] == 312:
    #     lurus() 
    #     #kanan()
    #     arah = "lurus"
    #     print(arah)

    # elif titik_terjauh[1] == 522:
    #     kanan()
    #     arah = "kanan"
    #     print(arah)


    # if arah_lurus[0] < 8:
    #     berhenti()
    #      # time.sleep(0.1)
    #      # lurus()
    #     arah = "berhenti"
    #     print(berhenti)
    # elif arah_lurus[0] > 0 and arah_lurus[0] < 155:
    #     if titik_terjauh[1] < 320:
    #         kiri()
    #         arah = "Bergerak ke arah kiri"
    #         print(arah)
    #     else:
    #         kanan()
    #         arah = " Bergerak ke arah kanan"
    #         print(arah)
    
    # # elif arah_lurus[0] == 154 or arah_lurus[0] == 155: 
    # #     if titik_terjauh[1] < 320:
    # #         kiri()
    # #         arah = "Bergerak ke arah kiri"
    # #         print(arah)
    # #     else:
    # #         kanan()
    # #         arah = " Bergerak ke arah kanan"
    # #         print(arah)
    
    # elif arah_lurus[0] > 156 and arah_lurus[0] < 280:
    #     lurus()
    #     arah = "bergerak lurus"
    #     print(arah)
    
    # elif arah_lurus[0] >  280: 
    #     if titik_terjauh[1] < 320:
    #         kiri()
    #         arah = "Bergerak ke Kiri"
    #         print(arah)
    #     # lebih kecil 310 menunjukkan arah kanan
    #     else:
    #         kanan()
    #         #gerak_menghindar_kanan()
    #         arah = "Bergerak ke Kanan"
    #         print(arah)

    # output0 = EdgeArray[x]
    # output = EdgeArray[x + 1]
    output0 = EdgeArray
    output1 = cabang
    output2 = x_vals
    output3 = y_vals
    output4 = avg_x
    output5 = avg_y
    output6 = rata_pada_cabang
    output7 = arah_lurus
    output8 = arah_lurus[0]
    output9 = titik_terjauh
    output10 = titik_terjauh[1]
    output11 = arah
    output12 = fps
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([output0, output1, output2, output3, output4, output5, output6, output7, output8, output9, output10, output11, output12])

        
    # output = arah_lurus[0]
    # with open(csv_file, 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([output])
    #     time.sleep(5)
    
    # Program untuk menunjukan hasil
    # if tesmode == 1:
    #    F.write ("frame"+str(currentFrame)+".jpg" +" | " + str(EdgeArray[0]) + " | " + str(EdgeArray[1]) + " | " +str(EdgeArray[2])  + " | " + arah + "\n") 
    #    currentFrame +=1 
    
    if tesmode == 1:
        cv2.imshow("frame_asli", frame_asli)
        cv2.imshow("grayscale", gray)
        cv2.imshow("Canny", edges)
        cv2.imshow("blur", blurin_frame)
     
        cv2.imshow("Threshold", thresh)
        cv2.imshow("intensitas cahaya", brightness)
        cv2.imshow("Edge_seperation", img_edgerepresentation)
        font = cv2.FONT_HERSHEY_SIMPLEX
        navigasi = cv2.putText(frame, arah, (275, 50), font, 1, (0,0, 255), 2, cv2.LINE_AA)
        cv2.imshow("Navigasi", navigasi)
        FPS = cv2.putText(frame, "FPS: {}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("FPS:", FPS)
    
    
    k = cv2.waitKey(5) & 0XFF
    if k == 27:
        break

cv2.destroyAllWindows
cap.release()
