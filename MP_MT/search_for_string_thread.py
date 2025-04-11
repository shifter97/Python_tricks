import threading
import concurrent.futures
import os
import itertools
# from concurrent.futures import ThreadPoolExecutor
# thread_local = threading.local()

to_be_searched = 'Elias'


path = 'MP_MT/files'
files = os.listdir(path)

txtfiles = []
for file in files:
    txtfiles.append(file)

def find_occurence_count(filename, to_be_searched):
    with open(f'MP_MT/files/{filename}', 'r') as text:
        occurence = 0
        all_text = str(text)
        for line in text:
            for word in line.split():
                if word == to_be_searched:
                    occurence +=1
    return occurence
    print(occurence)

# thread1 = threading.Thread(target=find_occurence_count, args=(to_be_searched,))
# thread2 = threading.Thread(target=find_occurence_count, args=("alias",))

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

final_value = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results_iterator = executor.map(find_occurence_count, txtfiles, itertools.repeat(to_be_searched))

    final_value = sum(results_iterator) 


    # for word in all_text: 
    #     print(word)
    #     if word == "c":

    #         occurence +=1
print(final_value)        
# print(occurence)
        

