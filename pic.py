#coding: utf-8
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics

# ����ѹ���ȣ���ֵԽ��ѹ��ԽС
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


def make_directory(directory):
    """����Ŀ¼"""
    os.makedirs(directory)

def directory_exists(directory):
    """�ж�Ŀ¼�Ƿ����"""
    if os.path.exists(directory):
        return True
    else:
        return False

def list_img_file(directory):
    """�г�Ŀ¼�������ļ�����ɸѡ��ͼƬ�ļ��б���"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
	    # print filename
    # print new_list
    new_list.sort(key= lambda x:(x[2],x[3],x[5],x[6],x[8],x[9]))
    return new_list



def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)

def compress(choose, des_dir, src_dir, file_list):
    """ѹ���㷨��img.thumbnail��ͼƬ����ѹ����
    
    ����
    -----------
    choose: str
            ѡ��ѹ���ı�������4��ѡ�Խ��ѹ�����ͼƬԽС
    """
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        img.save(des_dir + infile)
def compress_photo():
    '''����ѹ��ͼƬ�ĺ���
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list_src = list_img_file(src_dir)
    if directory_exists(des_dir):
        if not directory_exists(des_dir):
            make_directory(des_dir)
        file_list_des = list_img_file(des_dir)
        # print file_list
    '''����Ѿ�ѹ���ˣ��Ͳ���ѹ��'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    compress('4', des_dir, src_dir, file_list_src)

def handle_photo():
    '''����ͼƬ���ļ����������Ҫ��json��ʽ������
    
    -----------
    ���data.json�ļ��浽���͵�source/photos�ļ�����
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    file_list = list_img_file(src_dir)
    list_info = []
    for i in range(len(file_list)):
        filename = file_list[i]
        date_str, info = filename.split("_")
        info, _ = info.split(".")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]            
        if i == 0:  # �����һ���ļ�
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                                   'month': date.month,
                                                                   'link': [filename],
                                                                   'text': [info],
                                                                   'type': ['image']
                                                                   }
                                        } 
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # ��������һ�����ڣ����½�һ��dict
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                   'month': date.month,
                                                   'link': [filename],
                                                   'text': [info],
                                                   'type': ['image']
                                                   }
                        }
            list_info.append(new_dict)
        else:  # ͬһ������
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')
    list_info.reverse()  # ��ת
    final_dict = {"list": list_info}
    with open("./source/photos/data.json","w") as fp:
        json.dump(final_dict, fp)

def cut_photo():
    """�ü��㷨
    
    ----------
    ����Graphics���еĲü��㷨����src_dirĿ¼�µ��ļ����вü�ü�������Σ�
    """
    src_dir = "photos/"
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list = list_img_file(src_dir)
        # print file_list
        if file_list:
            print_help()
            for infile in file_list:
                img = Image.open(src_dir+infile)
                Graphics(infile=src_dir+infile, outfile=src_dir + infile).cut_by_ratio()            
        else:
            pass
    else:
        print("source directory not exist!")     



def git_operation():
    '''
    git �����к��������ֿ��ύ
    
    ----------
    ��Ҫ��װgit�����й��ߣ�������ӵ�����������
    '''
    os.system('git add --all')
    os.system('git commit -m "add photos"')
    os.system('git push origin deploy')

if __name__ == "__main__":
    print sys.getdefaultencoding()
    cut_photo()        # �ü�ͼƬ���ü�������Σ�ȥ�м䲿��
    compress_photo()   # ѹ��ͼƬ�������浽mini_photos�ļ�����
 #   git_operation()    # �ύ��github�ֿ�
    handle_photo()     # ���ļ������json��ʽ���浽���Ͳֿ���
    
    
    
    
