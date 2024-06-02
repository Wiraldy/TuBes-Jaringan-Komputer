import socket  # Mengimpor modul socket untuk komunikasi jaringan
import threading  # Mengimpor modul threading untuk menangani beberapa koneksi klien secara bersamaan
import os  # Mengimpor modul os untuk operasi sistem seperti mendapatkan path direktori saat ini

def handle_request(request):
    """
    Fungsi untuk menangani permintaan dari klien dan mengembalikan respons yang sesuai.
    """
    headers = request.split('\n')  # Memisahkan header dari permintaan HTTP berdasarkan baris baru
    requested_file = headers[0].split()[1]  # Mendapatkan path file yang diminta dari header pertama
    filepath = os.getcwd() + requested_file  # Menggabungkan path direktori saat ini dengan file yang diminta

    try:
        with open(filepath, 'rb') as file:  # Membuka file yang diminta dalam mode read binary
            response_content = file.read()  # Membaca konten file
            response_headers = 'HTTP/1.1 200 OK\n'  # Menyiapkan header respons HTTP untuk status 200 OK
            response_headers += 'Content-Type: text/html\n'  # Menambahkan header Content-Type
            response_headers += 'Content-Length: ' + str(len(response_content)) + '\n'  # Menambahkan header Content-Length
            response_headers += 'Connection: close\n\n'  # Menambahkan header Connection: close
        response = response_headers.encode() + response_content  # Menggabungkan header dan konten respons
    except FileNotFoundError:
        response_headers = 'HTTP/1.1 404 Not Found\n'  # Menyiapkan header respons HTTP untuk status 404 Not Found
        response_headers += 'Content-Type: text/html\n'  # Menambahkan header Content-Type
        response_headers += 'Connection: close\n\n'  # Menambahkan header Connection: close
        response_content = b'<html><body><h1>404 Not Found</h1></body></html>'  # Konten HTML sederhana untuk 404
        response = response_headers.encode() + response_content  # Menggabungkan header dan konten respons

    return response  # Mengembalikan respons ke klien

def handle_client(client_socket):
    """
    Fungsi untuk menangani koneksi dari klien.
    """
    with client_socket:  # Menggunakan with untuk memastikan socket ditutup setelah selesai
        request = client_socket.recv(1024).decode()  # Menerima data dari klien dengan ukuran buffer 1024 byte dan mendekodenya
        print(f"Received request: {request}")  # Mencetak permintaan yang diterima
        response = handle_request(request)  # Menangani permintaan dan mendapatkan respons
        client_socket.sendall(response)  # Mengirim respons ke klien
        print(f"Response sent to {client_socket.getpeername()}")  # Mencetak alamat klien yang menerima respons

def main():
    server_ip = '192.168.1.2'  # IP server yang akan digunakan, 0.0.0.0 berarti mendengarkan di semua antarmuka jaringan
    server_port = 6969  # Port server yang akan digunakan
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat socket dengan keluarga alamat IPv4 dan tipe TCP
    server.bind((server_ip, server_port))  # Mengikat socket ke IP dan port yang ditentukan
    server.listen(5)  # Menetapkan socket untuk mendengarkan koneksi masuk, dengan maksimal 5 antrian
    print(f"Mendengarkan pada {server_ip}:{server_port}")  # Mencetak bahwa server sedang mendengarkan pada IP dan port tertentu

    while True:
        client_socket, addr = server.accept()  # Menerima koneksi masuk dan mengembalikan socket klien dan alamatnya
        print(f"Koneksi diterima dari {addr}")  # Mencetak alamat klien yang terhubung
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))  # Membuat thread baru untuk menangani klien
        client_handler.start()  # Memulai thread baru

if __name__ == "__main__":
    main()  # Menjalankan fungsi main jika skrip dieksekusi langsung
