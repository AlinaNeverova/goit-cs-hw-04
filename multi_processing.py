import multiprocessing
from collections import defaultdict
from pathlib import Path
import timeit


def search_in_file(file_path, keywords, results_queue):
    try:                                            # додано обробку помилок за допомогою try-except
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results_queue.put((keyword, str(file_path)))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def process_task(files, keywords, results_queue):
    for file in files:
        search_in_file(file, keywords, results_queue)


def main_multiprocessing(file_paths, keywords):
    start = timeit.default_timer()             # вимір часу виконання
    num_processes = min(4, len(file_paths))    # залишила таке ж обмеження як для threading
    processes = []
    results_queue = multiprocessing.Queue()
    results = defaultdict(list)

    chunk_size = (len(file_paths) + num_processes - 1) // num_processes # рівномірний розподіл файлів між процесами
    for i in range(num_processes):
        chunk = file_paths[i*chunk_size:(i+1)*chunk_size]
        process = multiprocessing.Process(target=process_task, args=(chunk, keywords, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        results[keyword].append(file_path)

    end = timeit.default_timer()
    print(f"Multiprocessing execution time: {end - start:.5f} seconds")
    return dict(results)


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"File paths: {file_paths}\n")
    keywords = ["thread", "import", "TODO"]    # ті самі ключові слова, що й у threading
    results = main_multiprocessing(file_paths, keywords)
    print(results)                             # Multiprocessing execution time: 1.21717 seconds