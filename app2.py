import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import os
from datetime import datetime

def load_image(image_file):
    img=Image.open(image_file)
    return img


def save_uploaded_file(directory, img):
    # 1. 디렉토리가 있는지 확인하여, 없으면 만든다.
    if not os.path.exists(directory):
        os.mkdir(directory)
    # 2. 이제는 디렉토리가 있으니깐, 이미지를 저장.
    filename = datetime.now().isoformat().replace(':','-').replace('.','-')
    img.save(directory+'/'+ filename +'.jpg')

    return st.success('Saved file : {} in {}'.format(filename +'.jpg', directory))


def main():
    


    st.subheader('이미지파일 업로드')
    image_files = st.file_uploader('Upload Image', accept_multiple_files=True, #파일업로드 
    type= ['png', 'jpg','jpeg']) #업로드 될 수 있는 이미지 파일 



    # if image_file is  None :

    #     st.text('이미지를 넣어주세요')


    if image_files is not None :
        
        #2. 각 파일을 이미지로 바꿔야한다.
        image_list =[]
    
        #2-1 모든 파일이 리스트에 이미지로 저장
        for image_file in image_files :
            img = load_image(image_file)
            image_list.append(img)
        # #3. 화면에 확인해 본다.
        # for img in image_list:
        #     st.image(img)

        option_list =['Show Image', 'Rotate Image', 'Create Thumbnail', 'Crop Image','Merge Image'
        ,'Flip Image', 'Change Color', 'Filters-Sharpen', 'Filters - Edge Enhance','Contrast Image']


        option = st.selectbox('옵션을 선택하세요.', option_list)

    #--------------show image-----------------------------------------
        if option == 'Show Image' :
            
            for img in image_list:
                st.image(img)

            directory =st.text_input('파일 경로 입력')
            if st.button('SAVE'):
                #3.파일 저장
                for img in image_list:
                    save_uploaded_file(directory, img)
    
    #--------------Rotate image-----------------------------------------
        elif option == 'Rotate Image' :
            #1. 유저 입력
            degree=st.slider('회전 각도를 입력하세요',0,360 )
            #2. 모든 이미지를 돌려보자 
            rotated_list =[]
            for img in image_list:
                rotated_img = img.rotate(degree)
                st.image(rotated_img)
                rotated_list.append(rotated_img)

            directory =st.text_input('파일 경로 입력')
            if st.button('SAVE'):
                #3.파일 저장
                for img in rotated_list:
                    save_uploaded_file(directory, img)

                # file_name =st.text_input('파일 이름 입력')
                # img.save(directory+'/'+file_name +'.png')

    #--------------create thumbmail-----------------------------------------
        elif option == 'Create Thumbnail' :
            #이미지의 사이즈를 알아야겠다.
            # 가장 작은 사이즈  
            width_max, height_max=img.size

            width =st.number_input('가로크기를 입력하세요',1,width_max) #범위 지정
            height =st.number_input('세로크기를 입력하세요',1,height_max)

            st.text('{}X{}'.format(width, height))
            size = (width,height)

            thumbnailed_list = []
            for img in image_list :
                img.thumbnail(size)
                st.image(img)
                thumbnailed_list.append(img)

            directory =st.text_input('파일 경로 입력')
            if st.button('SAVE'):
                #3.파일 저장
                for img in thumbnailed_list:
                    save_uploaded_file(directory, img)
            
    #--------------crop image-----------------------------------------
        elif option == 'Crop Image' :
            # 왼쪽 위(50,100) 부분 부터 시작해서 좌표 만큼 (200,200)만큼 잘라라

            start_x = st.number_input('시작 x 좌표 입력', 0, img.size[0]-1)
            start_y = st.number_input('시작 y 좌표 입력', 0, img.size[1]-1)
            max_width =  img.size[0] - start_x
            max_height = img.size[1] - start_y

            width = st.number_input('width 입력', 1, max_width)
            height = st.number_input('height 입력', 1, max_height)

            box = (start_x, start_y, start_x + width, start_y + height)
            
            cropped_img=img.crop(box)
            st.image(cropped_img)

    #--------------merge image-----------------------------------------
        elif option == 'Merge Image':

            merge_file=st.file_uploader('Upload Image', #파일업로드 
                                type= ['png', 'jpg','jpeg'], key = 'merge')

            if merge_file is not None :

                merge_img = load_image(merge_file)

                start_x = st.number_input('시작 x 좌표 입력', 0, img.size[0] - merge_img.size[0])
                start_y = st.number_input('시작 y 좌표 입력', 0, img.size[1] - merge_img.size[1])
                position = (start_x, start_y)
            
                img.paste(merge_img, position)
                st.image(img)

    #--------------flip image-----------------------------------------
        elif option == 'Flip Image':
            status = st.radio('원하는 옵션을 선택하세요',['LEFT_RIGHT', 'TOP_BOTTEM', 'LEFT_RIGHT_TOP_BOTTEM'])
            transformed_img_list = []
            if status == 'LEFT_RIGHT' :
                for img in image_list:
                    flipped_LR_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    st.image(flipped_LR_img)
                    transformed_img_list.append(flipped_LR_img)

            if status == 'TOP_BOTTEM':
                for img in image_list:
                    flipped_TB_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_TB_img)
                    transformed_img_list.append(flipped_TB_img)

            elif status == 'LEFT_RIGHT_TOP_BOTTEM':
                for img in image_list:
                    flipped_LRTB_img = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_LRTB_img) 
                    transformed_img_list.append(flipped_LRTB_img)

            
            directory =st.text_input('파일 경로 입력')
            if st.button('SAVE'):
                #3.파일 저장
                for img in transformed_img_list:
                    save_uploaded_file(directory, img)
            
            

    #--------------Change Color-----------------------------------------
        elif option == 'Change Color' :
            status = st.radio('색상을 선택하세요',['Color', 'Gray scale', 'Black & White'])
            print(status)
            if status  == 'Color':
                bw = img.convert('RGB')
            elif status == 'Gray scale':
                bw = img.convert('L')
            elif status == 'Black & White':
                bw = img.convert('1')
            
            st.image(bw)

            
    #--------------Filters-Sharpen-----------------------------------------
        elif option == 'Filters-Sharpen':
            sharp_img = img.filter(ImageFilter.SHARPEN)
            st.image(sharp_img)

    #--------------Filters - Edge Enhance-----------------------------------------
        elif option == 'Filters - Edge Enhance':
            edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
            st.image(edge_img)

    #--------------contrast image-----------------------------------------
        elif option == 'Contrast Image':
            number=st.slider('원하는 선명도를 선택하세요',1,10 )
            contrast_img = ImageEnhance.Contrast(img).enhance(number)#단계
            st.image(contrast_img)
# 1.이미지를 내가 마음대로 올릴수 있어야 한다. 
# 이미지는 1장

#  2.userinteraction 할 수 있어야 한다. 


if __name__=='__main__' :
    main()