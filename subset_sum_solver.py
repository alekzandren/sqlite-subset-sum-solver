import sqlite3
import random
import time
import os

class CoreEngine:
    def __init__(self, db_name="storage_v1.db"):
        if os.path.exists(db_name):
            os.remove(db_name)
            
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=OFF;")
        self.conn.execute("PRAGMA cache_size=-2000000;")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data_points 
                               (s_val TEXT PRIMARY KEY, n_val TEXT)''')
        self.conn.commit()

    def run_solve(self, numbers, target):
        self.cursor.execute("INSERT INTO data_points VALUES (?, ?)", ("0", "BASE"))
        self.conn.commit()

        print(f"[*] СТАРТ. Чисел в наборе: {len(numbers)}")
        print(f"[*] Цель: {str(target)[:60]}...")

        for i, num in enumerate(numbers):
            self.cursor.execute("SELECT s_val FROM data_points")
            current_sums = self.cursor.fetchall()

            batch = []
            for (s_text,) in current_sums:
                new_s = int(s_text) + num
                if abs(new_s) > 10**1000:
                    continue
                
                new_s_text = str(new_s)
                
                if new_s == target:
                    self.cursor.execute("INSERT OR REPLACE INTO data_points VALUES (?, ?)", (new_s_text, str(num)))
                    self.conn.commit()
                    return self.get_path(target)
                
                batch.append((new_s_text, str(num)))

            self.cursor.executemany("INSERT OR IGNORE INTO data_points VALUES (?, ?)", batch)
            
            if i % 10 == 0:
                self.conn.commit()
                print(f"[i] Прогресс: {i}/{len(numbers)} | Сумм в базе: {len(current_sums)}")

        return None

    def get_path(self, target):
        path = []
        curr = target
        while curr != 0:
            self.cursor.execute("SELECT n_val FROM data_points WHERE s_val=?", (str(curr),))
            res = self.cursor.fetchone()
            if not res or res[0] == "BASE": 
                break
            val = int(res[0])
            path.append(val)
            curr -= val
        return path

def execute_task():
    engine = CoreEngine()
    
    print("[1/4] Генерация 5000 сверхбольших чисел...")
    data_set = [random.randint(-1099, 1099) for _ in range(5000)]
    
    with open("my_numbers.txt", "w", encoding="utf-8") as f:
        for n in data_set:
            f.write(str(n) + "\n")
            
    
    goal = sum(random.sample(data_set, 12))
    print(f"[2/4] Цель установлена. Длина цели: {len(str(goal))} знаков.")
    
    print("[3/4] Запуск CoreEngine (может занять время)...")
    start_time = time.time()
    result = engine.run_solve(data_set, goal)
    
    if result:
        print(f"\n[!] НАЙДЕНО за {time.time() - start_time:.2f} сек.")
        with open("solution.txt", "w", encoding="utf-8") as f:
            f.write(f"Target: {goal}\n")
            f.write(f"Solution: {result}\n")
            f.write(f"Check sum: {sum(result) == goal}")
        print("[4/4] Результат сохранен в 'solution.txt'")
    else:
        print("\n[-] Решение не найдено. Попробуйте увеличить выборку.")

if __name__ == "__main__":
    execute_task()
