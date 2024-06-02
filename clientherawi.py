import socket
import sys

# Fungsi untuk melakukan koneksi ke server dan mengambil data
def client(server, port_number, file_path):
    # Membuat objek socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Menghubungkan ke server
        client_socket.connect((server, int(port_number)))
        
        # Membuat permintaan HTTP GET
        request_line = f"GET {file_path} HTTP/1.1\r\n"
        headers = f"Host: {server}\r\nConnection: close\r\n\r\n"
        request = request_line + headers
        
        # Mengirim permintaan ke server
        client_socket.sendall(request.encode())
        
        # Menerima respons dari server
        response = b""
        while True:
            received_data = client_socket.recv(1024)
            if not received_data:
                break
            response += received_data
    
    finally:
        # Menutup socket
        client_socket.close()
    
    # Menampilkan respons
    print(response.decode())

if __name__ == "__main__":
    # Memeriksa apakah jumlah argumen baris perintah sesuai
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_address> <port_number> <file_path>")
        sys.exit(1)
    
    # Mengambil argumen dari baris perintah
    server_address = sys.argv[1]
    port_number = sys.argv[2]
    file_path = sys.argv[3]

    # Memanggil fungsi client dengan argumen yang sesuai
    client(server_address, port_number, file_path)
