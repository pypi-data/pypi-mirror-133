import requests
from bs4 import BeautifulSoup

"""
Method = fungsi
Field/Attribute = variabel
"""

class Bencana:

    def __init__(self, url, description):
        self.description= description
        self.result = None
        self.url = url

    def tampilkan_Keterangan(self):
        print(self.description)
 
    def ekstraksi_data(self):
        print('ekstraksi_data not implemented')

    def tampilkan_data(self):
        print('tampilkan_data not implemented')

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


class BanjirTerkini(Bencana):

    def __init__(self, url):
        super(BanjirTerkini, self).__init__(url, 'NOT YET IMPLEMENTED, but it should return last flood in Indonesia')

    def tampilkan_Keterangan(self):
        print('UNDER CONSTRUCTION',(self.description))

class GempaTerkini(Bencana):
   
    def __init__(self, url):
        super(GempaTerkini, self).__init__(url, 'To get the latest earthquake in Indonesia from BMKG.go.id')

    def ekstraksi_data(self):
        """
        Tanggal: 26 Desember 2021 
        Waktu : 09:22:53 WIB
        Magnitudo: 5.2
        Kedalaman: 10 km
        Lokasi: 2.21 LU - 126.79 BT
        Pusat gempa: 130 km BaratLaut HALMAHERABARAT-MALUT
        Potensi: tidak berpotensi TSUNAMI
        """

        try:
            content = requests.get(self.url)
        except Exception:
            return None
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')
            title = soup.find('title')
            print(title.string)

            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            waktu = result[1]
            tanggal = result[0]

            result = soup.find(
                'div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')
            i = 0
            magnitudo = None
            ls = None
            bt = None
            pusat = None
            kedalaman = None
            potensi = None
            dirasakan = None
            tsunami = None
            for res in result:
            
                if i == 1:
                    magnitudo = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    tsunami = res.text
                # elif i == 5:
                #     dirasakan = res.text

                # print(i, res)

                i = i+1

            hasil = dict()
            hasil['tanggal'] = tanggal  # '26 Desember 2021'
            hasil['waktu'] = waktu  # '09:22:53 WIB'
            hasil['magnitudo'] = magnitudo  # 5.2
            hasil['kedalaman'] = kedalaman  # '10 km'
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            # '130 km BaratLaut HALMAHERABARAT-MALUT'
            # hasil['dirasakan'] = dirasakan
            # hasil['pusat'] = '130 km BaratLaut HALMAHERABARAT-MALUT'
            hasil['tsunami'] = tsunami  # 'Tidak berpotensi TSUNAMI'
            self.result = hasil
        else:
            return None


    def tampilkan_data(self):
        if self.result is None:
            print('Tidak bisa menemukan data gempa bumi terkini')
            return

        print('\nGempa Terakhir berdasarkan BMKG')
        print('Tanggal :', self.result['tanggal'])
        print('Waktu :', self.result['waktu'])
        print('Magnitudo :', self.result['magnitudo'])
        print('Kedalaman :', self.result['kedalaman'])
        print('Koordinat : LS=', (self.result['koordinat']
            ['ls']), 'BT=', (self.result['koordinat']['bt']))
        print('Lokasi :', self.result['lokasi'])
        # print('Dirasakan :', self.result['dirasakan'])
        # print('Pusat :',self.result['pusat'])
        print('Potensi :', self.result['tsunami'])
    
    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


if __name__ == '__main__' :
    gempa_di_indonesia = GempaTerkini('https://bmkg.go.id')
    gempa_di_indonesia.tampilkan_Keterangan()
    gempa_di_indonesia.run()
   

    banjir_di_indonesia = BanjirTerkini ('NOT YET')
    banjir_di_indonesia.tampilkan_Keterangan()
    banjir_di_indonesia.run()

    daftar_bencana = [gempa_di_indonesia, banjir_di_indonesia]
    print('\nSemua Bencana Yang Ada')
    for bencana in daftar_bencana:
        bencana.tampilkan_Keterangan()
   
    # gempa_di_dunia = GempaTerkini('https://bmkg.go.id')
    # print('Deskripsi class GempaTerkini', gempa_di_dunia.description)
    # gempa_di_dunia.run()


    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()