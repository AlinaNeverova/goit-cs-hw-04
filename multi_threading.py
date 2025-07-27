import threading
import timeit
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords, results, lock):
    try:                                            # додано обробку помилок за допомогою try-except
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:
                        results[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")



def thread_task(files, keywords, results, lock):
    for file in files:
        search_in_file(file, keywords, results, lock)


def main_threading(file_paths, keywords):
    start = timeit.default_timer()                      # додано вимір часу виконання

    num_threads = min(4, len(file_paths))          # обмеження кількості потоків до 4 або кількості файлів
    threads = []
    results = defaultdict(list)
    lock = threading.Lock()                        # додано блокування для захисту доступу до спільних ресурсів

    chunk_size = (len(file_paths) + num_threads - 1) // num_threads # рівномірно розподіляємо файли між потоками
    for i in range(num_threads):
        chunk = file_paths[i*chunk_size:(i+1)*chunk_size]
        thread = threading.Thread(target=thread_task, args=(chunk, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = timeit.default_timer()              # додано обчислення часу виконання
    print(f"Execution time: {end - start:.5f} seconds")
    return dict(results)


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"File paths: {file_paths}\n")
    keywords = ["thread", "import", "TODO"]          # ключові слова для пошуку
    results = main_threading(file_paths, keywords)
    print(results)                                   # Execution time: 0.00265 seconds