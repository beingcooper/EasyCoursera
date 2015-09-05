import os
import time

def get_ctime(file):
    attr_list = []
    fl_stat = os.stat(file)
    attr_list = time.ctime(fl_stat.st_ctime).split()
    return attr_list[2] + "-" + attr_list[3]


def prettify(st_time,path, to_save, week_tags):
        
        int_ind = int(sorted(os.listdir(path))[0][0])
        i = int_ind
        fold_index = 0    
        while(i <= (int_ind + len(week_tags) -1)):
            sub_fold_index = 0
            for file in sorted(os.listdir(path)):         
                 des_path = sorted(os.listdir(to_save+week_tags[fold_index]))
                 if file.endswith(".mp4") and file.startswith(str(i)+" -"):
                     os.rename(path+file,to_save+week_tags[fold_index]+"/"+des_path[sub_fold_index]+"/"+file)
                     sub_fold_index+=1
            i+=1
            fold_index += 1





 
       