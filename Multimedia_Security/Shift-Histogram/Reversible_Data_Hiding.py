import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import Attack

#--------------------------------[Data Embedding]
#-----(1)[data load]
def dataload(path):
	img = cv.imread(path,0)
	h, w = img.shape[:2]  # get the pixel's high and wide
	return img.reshape([h * w, ]), h, w	# turn to 1 row array



#-----(2)[histogram and find the max&min point]
def Get_Histogram(pixelSequence):
	numberBins = [i + 0.5 for i in list(range(0, 256))]  # set the range of bins
	histogram, bins = np.histogram(pixelSequence, bins=numberBins)  # histograming
	return histogram

def MaxMinPoint(histogram):
	max_a = max(histogram)  # max pixel number
	min_b = min(histogram)	# min pixel number
	histogram_list = histogram.tolist()
	Max = histogram_list.index(max(histogram_list))+1  # max gray value
	Min = histogram_list.index(min(histogram_list))+1  # min gray value
	print('the max number:', max_a,
	'\nthe min number:', min_b,
	'\nthe max gray value:', Max,
	'\nthe min gray value:', Min)

	# judge the 0 point
	BookKeeping = []  
	if min_b != 0:
		for i in range(len(pixelSequence)):
			if pixelSequence[i] == MinPoint:
				BookKeeping.append(i)
				pixelSequence[i] = MinPoint - 1

	return Max, Min, BookKeeping, max_a



#-----(3)[shift histogram to left]
def shift(pixelSequence, MaxPoint, MinPoint):
	for i in range(len(pixelSequence)):
		if MinPoint < pixelSequence[i] < MaxPoint:
			pixelSequence[i] -= 1
	return pixelSequence


#-----(4)[embedding data]
def embedding(pixelSequence, MaxPoint, Hidden_Data):
	n = 0
	for i in range(len(pixelSequence)):
		if pixelSequence[i] == MaxPoint:
			if Hidden_Data[n] == 1:
				pixelSequence[i] -= 1
			else:
				pass
			n += 1	
			if n == len(Hidden_Data):
				break
	return pixelSequence, len(Hidden_Data)

#-----(5)[extracting data]
def extracting(pixelSequence, MaxPoint, length):
	Recover_Data = []
	count = 0
	for i in range(len(pixelSequence)):
		if pixelSequence[i] == MaxPoint-1:
			Recover_Data.append(1)
			count += 1
		if pixelSequence[i] == MaxPoint:
			Recover_Data.append(0)
			count += 1
		if count == length:
			break
	return pixelSequence, Recover_Data

#-----（6）[recover image]
def recoverImg(pixelSequence,MaxPoint,MinPoint,BookKeeping):
	for i in range(len(BookKeeping)):
		pixelSequence[BookKeeping[i]] = MinPoint

	for i in range(len(pixelSequence)):
		if MinPoint <= pixelSequence[i] <= MaxPoint-1:
			pixelSequence[i] += 1
	return pixelSequence



#----------[main]
if __name__ == '__main__':
	# 調整顯示大小
	while True:
		choice = input("請選擇功能：1.隱寫 2.攻擊 3.提取 4.退出 ：")
		if choice=='1':
			#----------[part.1 embed data]
			# 請將原圖像放在和.py同一個資料夾中！
			pixelSequence, h, w = dataload("Shift-Histogram/image/lena.bmp")  # 獲取一维數組
			originpixel = pixelSequence.copy()
			histogram = Get_Histogram(pixelSequence)	# 獲取並繪製圖像直方圖
			MaxPoint, MinPoint, BookKeeping, max_a = MaxMinPoint(histogram)	# 獲取直方圖中的最大值點和最小值點
			pixelSequence = shift(pixelSequence,MaxPoint,MinPoint)		# 移動直方圖
			Hidden_Data = np.random.randint(0,2,int(max_a))	# 產生嵌入數據
			np.savetxt('Shift-Histogram/txt/secret.txt', Hidden_Data, fmt='%d')	#儲存數據
			pixelSequence, data_length = embedding(pixelSequence, MaxPoint, Hidden_Data)	# 數據嵌入
			cv.imwrite('Shift-Histogram/image/Marked_Image.png', pixelSequence.reshape(h, w), [cv.IMWRITE_PNG_COMPRESSION, 0]) # 生成處理圖片
			print("在image中已生成Marked_Image.png")
		elif choice=='2':
			Attack.main()
			print('已攻擊並保存到image中')
		elif choice=='3':
			#----------[part.2 recover data]
			pixelSequence, h, w = dataload("Shift-Histogram/image/Marked_Image.png")  # 獲取一维數組
			pixelSequence, Recover_Data = extracting(pixelSequence, MaxPoint, data_length)  # 提取隐藏數據
			pixelSequence = recoverImg(pixelSequence,MaxPoint,MinPoint,BookKeeping)  # 恢復原圖像信息
			np.savetxt('Shift-Histogram/txt/secret_out.txt', Recover_Data, fmt='%d')	#儲存數據
			recoverpixel = pixelSequence
			cv.imwrite('Shift-Histogram/image/Recover_Image.png', pixelSequence.reshape(h,w), [cv.IMWRITE_PNG_COMPRESSION, 0])

			# 調整顯示大小
			plt.figure(figsize=(8, 4))
			# 顯示原圖
			plt.subplot(1, 3, 1)
			plt.imshow(originpixel.reshape(h, w), cmap='gray')
			plt.title('Original Image')

			# 顯示嵌入後圖片
			plt.subplot(1, 3, 2)
			marked_image = plt.imread('Shift-Histogram/image/Marked_Image.png')
			plt.imshow(marked_image, cmap='gray')
			plt.title('Marked Image')

			# 顯示復原圖像
			plt.subplot(1, 3, 3)
			recover_image = plt.imread('Shift-Histogram/image/Recover_Image.png')
			plt.imshow(recover_image, cmap='gray')
			plt.title('Recovered Image')

			plt.tight_layout()  # 調整子圖之間的間距
			plt.savefig(os.path.join('Shift-Histogram/result', 'all_image_results.png'))
			plt.show()

			#----------[part.3 Validation]
			# 驗證隐藏數據與提取數據一致性
			Flag = 0
			for i in range(len(Hidden_Data)):
				if Hidden_Data[i] != Recover_Data[i]:
					Flag = 1
					break
			if Flag == 0 :
				print('數據提取成功')
			else:
				print('數據提取失敗')

			# 驗證原圖像與復原圖像像素一致性
			Flag = 0
			for i in range(len(originpixel)):
				if originpixel[i] != pixelSequence[i]:
					Flag = 1
					break
			if Flag == 0 :
				print('圖像復原成功')
			else:
				print('圖像復原失敗')

			# 調整顯示大小
			plt.figure(figsize=(10, 4))

			# 顯示原圖直方圖
			plt.subplot(1, 3, 1)
			plt.hist(originpixel, bins=256, color='blue', alpha=0.7)
			plt.title('Original Histogram')

			# 顯示嵌入後圖直方圖
			plt.subplot(1, 3, 2)
			marked_image = plt.imread('Shift-Histogram/image/Marked_Image.png')
			plt.hist(marked_image.flatten(), bins=256, color='red', alpha=0.7)
			plt.title('Marked Image Histogram')

			# 顯示提取後圖直方圖
			plt.subplot(1, 3, 3)
			recover_image = plt.imread('Shift-Histogram/image/Recover_Image.png')
			plt.hist(recover_image.flatten(), bins=256, color='green', alpha=0.7)
			plt.title('Recovered Image Histogram')

			plt.tight_layout()  # 調整子圖之間的間距
			plt.savefig(os.path.join('Shift-Histogram/result', 'all_histogram_results.png'))
			plt.show()
		else:
			print("請查看資料夾! bye~")
			break


