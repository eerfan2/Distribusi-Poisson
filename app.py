from flask import Flask, request, render_template
import math

app = Flask(__name__)

# Fungsi untuk menghitung distribusi Poisson
def poisson_distribution(l, k):
    try:
        return (l**k * math.exp(-l)) / math.factorial(k)
    except OverflowError:
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            # Ambil input dari form
            lambda_total = float(request.form['lambda_total'])
            k_total = int(request.form['k_total'])
            
            # Validasi input
            if lambda_total < 0 or k_total < 0:
                error = "Nilai λ_total dan K_total harus lebih besar atau sama dengan nol."
                return render_template('index.html', error=error)

            # Rasio kendaraan
            motor_ratio = 0.7
            mobil_ratio = 0.3

            # Hitung rata-rata kendaraan motor dan mobil
            lambda_motor = round(lambda_total * motor_ratio, 2)
            lambda_mobil = round(lambda_total * mobil_ratio, 2)

            # Hitung jumlah kendaraan motor dan mobil berdasarkan rasio
            k_motor = round(k_total * motor_ratio)
            k_mobil = round(k_total * mobil_ratio)

            # Hitung distribusi Poisson untuk motor dan mobil
            result_motor = round(poisson_distribution(lambda_motor, k_motor), 1)
            result_mobil = round(poisson_distribution(lambda_mobil, k_mobil), 1)

            # Hitung peluang jembatan sepi
            result_sepi_motor = round(poisson_distribution(lambda_motor, 0), 1)
            result_sepi_mobil = round(poisson_distribution(lambda_mobil, 0), 1)

            # Hitung peluang gabungan motor dan mobil
            result_bersama = round(result_motor * result_mobil, 1)

            # Hitung peluang jumlah motor lebih banyak daripada mobil
            result_motor_banyak = result_motor > result_mobil

            # Hitung peluang jumlah motor dan mobil mencapai nilai tertentu
            result_skor_tertentu = round(result_motor * result_mobil, 1)

            return render_template('index.html', 
                                   lambda_total=lambda_total, 
                                   k_total=k_total, 
                                   lambda_motor=lambda_motor, 
                                   lambda_mobil=lambda_mobil, 
                                   k_motor=k_motor, 
                                   k_mobil=k_mobil, 
                                   result_motor=result_motor, 
                                   result_mobil=result_mobil,
                                   result_sepi_motor=result_sepi_motor, 
                                   result_sepi_mobil=result_sepi_mobil, 
                                   result_bersama=result_bersama,
                                   result_motor_banyak=result_motor_banyak, 
                                   result_skor_tertentu=result_skor_tertentu)
        except ValueError:
            error = "Input tidak valid. Harap masukkan angka yang sesuai."
    return render_template('index.html', error=error, result_motor=None, result_mobil=None)

if __name__ == '__main__':
    app.run(debug=True)
