import concurrent.futures 
import os
import itertools

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


def main():
    final_value = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results_iterator = executor.map(find_occurence_count, txtfiles, itertools.repeat(to_be_searched))

        final_value = sum(results_iterator)

    print(final_value)       

# def main():
#     start_time = time.perf_counter()
#     with ProcessPoolExecutor() as executor:
#         executor.map(fib, [35] * 20)
#     duration = time.perf_counter() - start_time
#     print(f"Computed in {duration} seconds")

# def fib(n):
#     return n if n < 2 else fib(n - 2) + fib(n - 1)

if __name__ == "__main__":
    main()
