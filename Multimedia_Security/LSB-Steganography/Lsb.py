import os
import numpy as np
import PIL.Image as Image
import Attack


def lsb_embed(pic_src,file_src):
    # 讀取圖片的像素訊息
    picture = Image.open('{}'.format(pic_src))
    pic_data = np.array(picture)

    # 讀取要隱寫的文件
    with open('{}'.format(file_src), encoding="utf-8") as file:
        secrets = file.read()

    # 將圖片copy一份，作為最终的圖片數據
    im_data = np.array(picture.copy()).ravel().tolist()

    def cover_lsb(bin_index, data):
        '''
        :param bin_index:  當前字符的ascii的二進制
        :param data: 取出數组像素的八個數值
        :return: LSB隱寫后的字符
        '''
        res = []
        for i in range(8):
            data_i_bin = bin(data[i])[2:].zfill(8)
            if bin_index[i] == '0':
                data_i_bin = data_i_bin[0:7] + '0'
            elif bin_index[i] == '1':
                data_i_bin = data_i_bin[0:7] + '1'
            res.append(int(data_i_bin, 2))
        return res

    pic_idx = 0
    # 採用LSB隱寫技術，横向取數據，每次取9個數據，改變8個像素最低位
    res_data = []
    for i in range(len(secrets)):
        # 拿到隱寫文件的字符ascii數值, 並轉換為二進制,填充成八位
        index = ord(secrets[i])
        bin_index = bin(index)[2:].zfill(8)
        # 對數據進行LSB隱寫，替換操作
        res = cover_lsb(bin_index, im_data[pic_idx * 8: (pic_idx + 1) * 8])
        pic_idx += 1
        res_data += res
    # 對剩餘未填充的數據進行補充填充，防止圖像無法復原
    res_data += im_data[pic_idx * 8:]

    # 將新生成的文件進行格式轉換並保存，此處一定保存為壓縮的png文件
    new_im_data = np.array(res_data).astype(np.uint8).reshape((pic_data.shape))
    res_im = Image.fromarray(new_im_data)
    res_im.save('LSB-Steganography/image/res_encode.png')
    print("在image中已生成res_encode.png")

def lsb_extract(pic_src,file_src):
    # 打开隱寫文件
    picture = Image.open('{}'.format(pic_src))
    pic_datas = np.array(picture).ravel().tolist()

    with open('{}'.format(file_src), encoding="utf-8") as file:
        secrets = file.read()

    str_len = len(secrets)

    # 將圖片copy一份，作為最终的圖片數據
    im_data = np.array(picture.copy()).ravel().tolist()

    def lsb_decode(data):
        '''
        :param bin_index:  當前字符的ascii的二進制
        :param data: 取出數组像素的八個數值
        :return: LSB隱寫后的字符
        '''
        str = ''
        for i in range(len(data)):
            # print(bin(data[i])[2:])
            data_i_bin = bin(data[i])[2:][-1]
            str += data_i_bin
        return str

    # 採用LSB隱寫技術，横向取數據，每次取9個數據，改變8個像素最低位
    res_data = []

    for i in range(str_len):
        # 拿到第i個數據,轉換成二進制
        data = im_data[i * 8: (i + 1) * 8]
        data_int = lsb_decode(data)
        # 找到最低位
        res_data.append(int(data_int, 2))

    # 將二進制數據轉換成ASCII
    str_data = ''
    for i in res_data:
        temp = chr(i)
        str_data += temp
    print("提取成功，輸出下列解密结果")
    print(str_data)
    with open('LSB-Steganography/txt/secret_out.txt', 'w',encoding="utf-8") as file:
        file.write(str_data)
    print('已保存在txt/secret_out.txt中')


if __name__ == '__main__':
    # print("當前目錄下image資料夾中存放圖片，txt資料夾存放待加密訊息和解密訊息")
    while True:
        choice = input("請選擇功能：1.隱寫 2.攻擊 3.提取 4.退出 ：")
        if choice=='1':
            img_src = 'LSB-Steganography/image/lena.bmp'
            file_src = 'LSB-Steganography/txt/secret.txt'
            lsb_embed(img_src,file_src)
        elif choice=='2':
            Attack.main()
            print('已攻擊並保存到image中')
        elif choice=='3':
            img_src = 'LSB-Steganography/image/res_encode.png'
            file_src = 'LSB-Steganography/txt/secret.txt'
            lsb_embed(img_src,file_src)
            lsb_extract(img_src,file_src)
        else:
            print("請查看資料夾! bye~")
            break

