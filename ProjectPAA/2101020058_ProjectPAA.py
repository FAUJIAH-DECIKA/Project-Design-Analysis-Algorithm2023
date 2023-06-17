import tkinter as tk
import random
import heapq

# Konstanta dan variabel yang digunakan
CELL_SIZE = 30 
ROWS = 20
COLS = 30
WALL_COLOR = "black"
PATH_COLOR = "white"
RED_COLOR = "red"
GREEN_COLOR = "green"

# Kelas untuk mengatur permainan dan melakukan interaksi antara pemain dan objek-objek dalam permainan
class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Design Analysis Algorithm 2023")

        self.canvas = tk.Canvas(self.root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
        self.canvas.pack()

        self.map_data = self.generate_map()
        self.red_droid = self.place_droid(RED_COLOR)
        self.green_droid = self.place_droid(GREEN_COLOR)

        self.paused = True

        self.create_buttons()
        self.root.after(500, self.game_loop)
        self.root.mainloop()

    # mengatur logika permainannya
    def game_loop(self):
        # Melakukan perulangan game secara terus-menerus
        # sampai permainan dijeda atau berakhir

        if not self.paused:
            # Jika permainan tidak dijeda, lanjutkan pergerakan droid
            self.move_red_droid()
            self.move_green_droid()
            self.draw_map()
            self.draw_droids()

            if self.check_game_over():
                # Periksa apakah permainan berakhir
                # Jika iya, tampilkan pesan "GAME OVER" dan jeda permainan
                self.show_game_over()
                self.paused = True

        # Memanggil metode game_loop() secara berulang setiap 500 milidetik
        self.root.after(500, self.game_loop)

    # untuk menghasilkan peta permainan
    def generate_map(self):
        # Inisialisasi peta dengan dinding
        map_data = [[1 for _ in range(ROWS)] for _ in range(COLS)]

        # Buat jalur menggunakan algoritma Recursive Backtracking
        stack = [(0, 0)] # Mulai dengan koordinat (0, 0)
        visited = set()  # Set untuk melacak sel yang sudah dikunjungi

        while stack:
            x, y = stack[-1]  # Koordinat saat ini
            visited.add((x, y))  # Tandai sel saat ini sebagai sudah dikunjungi
            neighbors = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]  # Tandai sel saat ini sebagai sudah dikunjungi
            
            # Filter tetangga yang belum dikunjungi dan berada dalam batas peta
            unvisited_neighbors = [neighbor for neighbor in neighbors if
                                   neighbor not in visited and 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS]

            if unvisited_neighbors:
                # Jika masih ada tetangga yang belum dikunjungi
                nx, ny = random.choice(unvisited_neighbors) # Pilih tetangga secara acak
                map_data[nx][ny] = 0  # Jadikan tetangga tersebut sebagai jalur
                map_data[x + (nx - x) // 2][y + (ny - y) // 2] = 0  # Buat dinding di antara tetangga dan posisi saat ini
                stack.append((nx, ny))  # Pindah ke tetangga yang dipilih
            else:
                stack.pop() # Jika tidak ada tetangga yang belum dikunjungi, mundur ke posisi sebelumnya

        return map_data

    # Menempatkan droid (merah atau hijau) secara acak di peta
    def place_droid(self, color):
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if self.map_data[x][y] == 0:
                self.map_data[x][y] = color
                return (x, y)

    # Menggambar peta di kanvas, yang mewakili dinding dan jalur
    def draw_map(self):
        self.canvas.delete("map")
        for x in range(COLS):
            for y in range(ROWS):
                if self.map_data[x][y] == 1:
                    self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                                 (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                                 fill=WALL_COLOR, tags="map")
                else:
                    self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                                 (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                                 fill=PATH_COLOR, tags="map")

    # Menggambar droid merah dan hijau di atas kanvas
    def draw_droids(self):
        self.canvas.delete("droids")
        self.canvas.create_oval(self.red_droid[0] * CELL_SIZE, self.red_droid[1] * CELL_SIZE,
                                (self.red_droid[0] + 1) * CELL_SIZE, (self.red_droid[1] + 1) * CELL_SIZE,
                                fill=RED_COLOR, tags="droids")

        self.canvas.create_oval(self.green_droid[0] * CELL_SIZE, self.green_droid[1] * CELL_SIZE,
                                (self.green_droid[0] + 1) * CELL_SIZE, (self.green_droid[1] + 1) * CELL_SIZE,
                                fill=GREEN_COLOR, tags="droids")

    # Untuk memindahkan droid merah. Metode ini menggunakan algoritma A* 
    def move_red_droid(self):
        # Temukan jalur terpendek dari droid merah ke droid hijau
        path = self.find_shortest_path(self.red_droid, self.green_droid)
        if path:
            self.red_droid = path[1]

    # Untuk memindahkan droid hijau. Metode ini menggunakan algoritma A* 
    def move_green_droid(self):
        # Temukan jalur yang menjauhi droid merah
        path = self.find_path_away(self.green_droid, self.red_droid)
        if path:
            self.green_droid = path[1]

    def find_shortest_path(self, start, target):
        # Temukan jalur terpendek dari posisi awal ke posisi target menggunakan algoritma A*
        queue = [(0, start, [])] # Antrian prioritas untuk menyimpan posisi saat ini, biaya, dan jalur yang diikuti
        heapq.heapify(queue)  # Mengubah antrian menjadi antrian prioritas
        visited = set() # Set untuk melacak posisi yang sudah dikunjungi


        while queue:
            cost, current, path = heapq.heappop(queue)  # Ambil posisi dengan biaya terkecil dari antrian
            visited.add(current)  # Tandai posisi saat ini sebagai sudah dikunjungi

            if current == target:
                return path # Jalur terpendek ditemukan, kembalikan jalur

            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]  # Tetangga yang mungkin

            for neighbor in neighbors:
                if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and neighbor not in visited and \
                        self.map_data[neighbor[0]][neighbor[1]] != 1:
                    
                    # Periksa apakah tetangga berada dalam batas peta, belum dikunjungi, dan bukan dinding
                    new_cost = cost + 1 # Biaya baru untuk mencapai tetangga ini
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))  # Tambahkan tetangga ke antrian dengan biaya baru
                    visited.add(neighbor) # Tandai tetangga sebagai sudah dikunjungi

        return []

    def find_path_away(self, start, target):
    # Temukan jalur yang menjauhi posisi target
        queue = [(0, start, [])]  # Antrian prioritas untuk menyimpan posisi saat ini, biaya, dan jalur yang diikuti
        heapq.heapify(queue)  # Mengubah antrian menjadi antrian prioritas
        visited = set()  # Set untuk melacak posisi yang sudah dikunjungi

        while queue:
            cost, current, path = heapq.heappop(queue)  # Ambil posisi dengan biaya terkecil dari antrian
            visited.add(current)  # Tandai posisi saat ini sebagai sudah dikunjungi

            if current == target:
                return path  # Jalur ditemukan, kembalikan jalur

            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                        (current[0], current[1] - 1), (current[0], current[1] + 1)]  # Tetangga yang mungkin

            for neighbor in neighbors:
                if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and neighbor not in visited and \
                        self.map_data[neighbor[0]][neighbor[1]] != 1:
                    # Periksa apakah tetangga berada dalam batas peta, belum dikunjungi, dan bukan dinding
                    new_cost = cost + 1  # Biaya baru untuk mencapai tetangga ini
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))  # Tambahkan tetangga ke antrian dengan biaya baru
                    visited.add(neighbor)  # Tandai tetangga sebagai sudah dikunjungi

        return []  # Jika tidak ada jalur yang ditemukan, kembalikan jalur kosong

    def check_game_over(self):
        # Periksa apakah droid merah dan hijau berada di posisi yang sama
        return self.red_droid == self.green_droid

    def show_game_over(self):
        # Tampilkan teks "GAME OVER" di kanvas
        self.canvas.create_text(COLS * CELL_SIZE / 2, ROWS * CELL_SIZE / 2,
                                text="GAME OVER", fill="red", font=("Arial", 24), tags="gameover")

    def create_buttons(self):
        # Buat tombol untuk mengontrol game
        start_button = tk.Button(self.root, text="Mulai", command=self.start_game)
        start_button.pack(side=tk.LEFT)

        pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        pause_button.pack(side=tk.LEFT)

        random_map_button = tk.Button(self.root, text="Acak Peta", command=self.randomize_map)
        random_map_button.pack(side=tk.LEFT)

        random_droids_button = tk.Button(self.root, text="Acak Droid", command=self.randomize_droids)
        random_droids_button.pack(side=tk.LEFT)

    def start_game(self):
        # Mulai permainan dengan menyetel bendera paused ke False
        self.paused = False

    #  Untuk mengubah status jeda permainan
    def toggle_pause(self):
        # Alihkan bendera paused antara True dan False
        self.paused = not self.paused

        if not self.paused:
            self.clear_game_over()

    def randomize_map(self):
        # Acak ulang peta dengan memanggil metode generate_map
        self.map_data = self.generate_map()
        self.clear_game_over()

    def randomize_droids(self):
        # Acak ulang posisi droid merah dan hijau
        self.red_droid = self.place_droid(RED_COLOR)
        self.green_droid = self.place_droid(GREEN_COLOR)
        self.clear_game_over()
    
    def clear_game_over(self):
        # Hapus teks "GAME OVER" dari kanvas
        self.canvas.delete("gameover")

# Menjalankan permainan. 
if __name__ == "__main__":
    game = Game()