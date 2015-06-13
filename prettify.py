import os

def prettify(path, to_save, week_tags):
        
        
        int_ind = int(sorted(os.listdir(path))[0][0])
        i = int_ind
        while(i <= (int_ind + len(week_tags) -1)):
            for file in os.listdir(path):         
                 if file.endswith(".mp4") and file.startswith(str(i)+" -"):
                     os.rename(path+file,to_save+week_tags[i-1]+"/"+file)
            i+=1     
