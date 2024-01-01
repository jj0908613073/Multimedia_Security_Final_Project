# Multimedia_Security_Final_Project
## LSB-Steganography
使用最低有效位（LSB）在數字數據的二進制表示中嵌入額外的信息，這樣的技術可以用來隱藏訊息，而不引起人眼或人耳的感知變化。<br>
直接跑Lsb.py即可
<p>
請選擇功能：<br>
1.隱寫<br>
使用Key("txt\secret.txt")加密明文("image\lena.bmp")，生成密文("image\res_encode.png")<br>

2.攻擊<br>
attacks = ['gaussian_noise', 'salt_and_pepper_noise', 'mean_filter', 'median_filter', 'high_pass_filter', 'rotate_image']<br>
利用以上攻擊方法，攻擊"image\res_encode.png"，<br>
並產生統計圖("result\all_results.png")及數據("result\attack_results.txt")及攻擊後的個別圖片("result\attacks_name.png")<br>
![all_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/2482891b-c2cb-4dda-b2c4-550e478a38f7)

3.提取<br>
解出明文("image\res_encode.png")，並存Key("txt\secret_out.txt")<br>
![secret](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/2992d843-85c0-4295-8e9c-4229e81c598e)

4.退出<br>
結束應用<br>
![end](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/18779d0a-c85b-4b55-8479-e68331f18f2b)
</p>

## Shift-Histogram
使用直方圖的位移中嵌入額外的信息，這樣的技術可以用來隱藏訊息，而不引起人眼或人耳的感知變化。<br>
直接跑Reversible_Data_Hiding.py即可
<p>

請選擇功能：<br>
1.隱寫<br>
使用Key(random)加密明文("image\lena.bmp")，生成密文("image\Marked_Image.png")<br>
![all_image_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/3ed5e015-516f-4a44-a21b-b7c2f9cf9b81)

2.攻擊<br>
attacks = ['gaussian_noise', 'salt_and_pepper_noise', 'mean_filter', 'median_filter', 'high_pass_filter', 'rotate_image']<br>
利用以上攻擊方法，攻擊"image\Marked_Image.png"，<br>
並產生統計圖("result\all_attack_results.png")及數據("result\attack_results.txt")及攻擊後的個別圖片("result\attacks_name.png")<br>
![all_attack_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/cd3156cf-ee6b-4eac-b1f2-76a928fcf2cf)

3.提取<br>
解出明文("image\Recovered_Image.png")，並存Key("txt\secret_out.txt")<br>
![secret](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/013fa2d2-83ea-445c-bbbb-b77076fe0b59)

4.退出<br>
結束應用<br>
![end](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/b2082429-6257-4f95-af83-c924c6f4094b)
</p>

## 攻擊過後數據
<p>
  
![image](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/60953120-c01b-40bb-bd54-4197123516b4)
</p>
