def calculate_aspect(width: int, height: int) -> str:
    def gcd(a, b):
        """En büyük ortak böleni bulan fonksiyon"""
        return a if b == 0 else gcd(b, a % b)

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return f"{x}:{y}"
