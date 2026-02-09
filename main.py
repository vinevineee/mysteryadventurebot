import random
import sys
import time


def slow(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


class Game:
    def __init__(self):
        self.health = 100
        self.sanity = 100
        self.inventory = []
        self.quests = {
            'temukan_relik': False,
            'bebaskan_arwah': False,
            'kabur': False
        }
        self.location = 'gerbang'

    def status(self):
        print(f"Kesehatan: {self.health} | Kewarasan: {self.sanity} | Lokasi: {self.location}")

    def change_sanity(self, amount):
        self.sanity = max(0, min(100, self.sanity + amount))

    def change_health(self, amount):
        self.health = max(0, min(100, self.health + amount))

    def random_scare(self):
        if random.random() < 0.35:
            msg = random.choice([
                "Anda mendengar suara bisikan dari dinding.",
                "Bayangan melintas di sudut mata Anda.",
                "Pintu di lantai atas menutup dengan semudah tarikan napas." 
            ])
            slow(msg)
            self.change_sanity(-random.randint(3, 12))

    def check_game_over(self):
        if self.health <= 0:
            slow('\nKamu tidak bisa melanjutkan. Kematian menyambutmu...')
            return True
        if self.sanity <= 0:
            slow('\nKewarasanmu hilang. Rumah ini memelukimu selamanya...')
            return True
        return False

    def show_quests(self):
        print('\nQuest:')
        for k, v in self.quests.items():
            status = 'Selesai' if v else 'Belum'
            desc = {
                'temukan_relik': 'Temukan relik peninggalan (keris tua) di rumah',
                'bebaskan_arwah': 'Bebaskan arwah yang terperangkap',
                'kabur': 'Keluar dari rumah dengan selamat'
            }[k]
            print(f"- {desc}: {status}")

    def play(self):
        slow("The Mystery Adventure Bot - Rumah Hantu Yogyakarta\n", 0.02)
        slow("Kamu adalah penjelajah urban yang penasaran. Malam ini, kabar beredar tentang rumah terbengkalai di pinggiran Yogyakarta yang dihuni oleh sesuatu yang tak biasa.")
        slow("Tugasmu: selesaikan quest, jangan kehilangan kewarasan, dan cari jalan keluar. \n")

        while True:
            if self.check_game_over():
                slow('\n-- GAME OVER --')
                break

            self.status()
            self.show_quests()
            self.describe_location()

            choice = input('\nApa yang ingin kamu lakukan? (explore/move/inventory/quests/quit) > ').strip().lower()
            if choice == 'quit':
                slow('Kamu memilih mundur dari petualangan ini...')
                break
            elif choice == 'inventory':
                print('Inventory:', self.inventory if self.inventory else 'Kosong')
            elif choice == 'quests':
                self.show_quests()
            elif choice == 'explore':
                self.explore()
            elif choice == 'move':
                self.move()
            else:
                slow('Perintah tidak dikenali.')

            if all(self.quests.values()):
                slow('\nKau telah menyelesaikan semua quest. Waktunya mengunci cerita dan pergi...')
                break

        slow('\nTerima kasih sudah bermain. Berani kembali?')

    def describe_location(self):
        desc = {
            'gerbang': 'Gerbang rumah tua yang besi-berkarat, diselimuti ilalang.',
            'halaman': 'Halaman penuh rumput kering dan patung yang retak.',
            'teras': 'Teras berdebu, langkahmu berderak di papan kayu usang.',
            'ruang_tamu': 'Ruang tamu dengan perabot ditutupi kain putih. Ada aroma apek.',
            'loteng': 'Loteng gelap, kotak-kotak lapuk berbaris. Angin menghembus tak wajar.',
            'ruang_bawah': 'Ruang bawah tanah lembab; ada bekas ritual di lantai.',
            'taman': 'Taman kecil di belakang, ada sumur tua yang tersembunyi.'
        }
        slow('\n' + desc.get(self.location, 'Sebuah tempat yang tak dikenal.'))

    def explore(self):
        slow('\nKamu mulai menjelajahi...')
        self.random_scare()

        # Events based on location
        if self.location == 'gerbang':
            slow('Di sela pagar, kamu menemukan sebuah amplop usang.')
            if 'amplop_usang' not in self.inventory:
                self.inventory.append('amplop_usang')
            slow('Isi amplop: sebuah peta kecil dengan tanda di dalam rumah.')
        elif self.location == 'halaman':
            slow('Di halaman, patung retak nampak seperti mata mengikutimu.')
            if 'peta_relik' not in self.inventory and random.random() < 0.5:
                slow('Kamu menemukan potongan kain berwarna merah—mungkin petunjuk.')
                self.inventory.append('potongan_kain_merah')
        elif self.location == 'teras':
            slow('Di bawah karpet ada bekas tapak kecil dan goresan pada lantai.')
            if 'kunci_kecil' not in self.inventory:
                slow('Kamu menemukan sebuah kunci kecil.')
                self.inventory.append('kunci_kecil')
        elif self.location == 'ruang_tamu':
            slow('Di ruang tamu, kamu melihat lembaran buku harian yang lapuk.')
            if 'buku_harian' not in self.inventory:
                slow('Kamu membaca cuplikan: "Ada yang terjebak di bawah..."')
                self.inventory.append('buku_harian')
            # chance to find relic
            if not self.quests['temukan_relik'] and 'keris' not in self.inventory and random.random() < 0.4:
                slow('Di balik sofa, kamu menemukan sebuah keris kecil—relik kuno.')
                self.inventory.append('keris')
                self.quests['temukan_relik'] = True
        elif self.location == 'loteng':
            slow('Loteng berisi peti dan boneka tua.')
            if 'boneka' not in self.inventory and random.random() < 0.3:
                slow('Boneka itu bergerak sendirinya sesaat—kamu menjerit dan menjatuhkannya.')
                self.inventory.append('boneka')
                self.change_sanity(-8)
        elif self.location == 'ruang_bawah':
            slow('Ruang bawah tanah dipenuhi lingkaran dan simbol aneh.')
            if 'keris' in self.inventory and not self.quests['bebaskan_arwah']:
                slow('Dengan keris, kamu melakukan ritual sederhana dan mendengar suara lega. Arwah terbebaskan.')
                self.quests['bebaskan_arwah'] = True
                self.change_sanity(+15)
            else:
                slow('Suasananya menekan; kamu hampir kehilangan kesadaranku.')
                self.change_sanity(-15)
        elif self.location == 'taman':
            slow('Di dekat sumur, ada batu nisan kecil dan coretan aneh.')
            if 'kunci_kecil' in self.inventory and not self.quests['kabur']:
                slow('Kunci cocok untuk pintu gerbang tersembunyi. Kamu membuka jalan keluar.')
                self.quests['kabur'] = True
        else:
            slow('Tidak ada yang istimewa.')

    def move(self):
        options = {
            'gerbang': ['halaman'],
            'halaman': ['gerbang', 'teras'],
            'teras': ['halaman', 'ruang_tamu'],
            'ruang_tamu': ['teras', 'loteng', 'ruang_bawah', 'taman'],
            'loteng': ['ruang_tamu'],
            'ruang_bawah': ['ruang_tamu'],
            'taman': ['ruang_tamu']
        }
        print('\nTempat yang dapat dituju:')
        for i, loc in enumerate(options.get(self.location, []), 1):
            print(f"{i}. {loc}")
        choice = input('Pilih nomor tujuan atau ketik batal: ').strip()
        if choice.isdigit():
            idx = int(choice) - 1
            dests = options.get(self.location, [])
            if 0 <= idx < len(dests):
                self.location = dests[idx]
                slow(f'Kamu berjalan ke {self.location}...')
                if random.random() < 0.25:
                    self.encounter()
            else:
                slow('Pilihan tidak valid.')
        else:
            slow('Berhenti berpindah.')

    def encounter(self):
        slow('\nSesuatu muncul...')
        event = random.choice(['bayangan', 'suara', 'jeritan'])
        if event == 'bayangan':
            slow('Bayangan menempel di punggungmu dan merenggut sedikit kekuatan.')
            self.change_health(-random.randint(5, 15))
            self.change_sanity(-random.randint(5, 12))
        elif event == 'suara':
            slow('Bisikan mengatakan: "Tinggalkan..." dan suaranya menusuk telingamu.')
            self.change_sanity(-random.randint(8, 18))
        else:
            slow('Jeritan membuatmu goyah; kamu hampir kehilangan kendali.')
            self.change_health(-random.randint(3, 10))
            self.change_sanity(-random.randint(3, 10))


def main():
    random.seed()
    game = Game()
    game.play()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nPermainan dihentikan. Sampai jumpa.')
