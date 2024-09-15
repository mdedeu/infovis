import chess.pgn
import csv
from datetime import datetime, timedelta
import re

# Configura tu nombre de usuario
username = 'marcosdedeu'

# Abre el archivo PGN
pgn_file = 'tus_partidas.pgn'  # Reemplaza con la ruta a tu archivo PGN
pgn = open(pgn_file, encoding='utf-8')

# Prepara el archivo CSV
with open('datos_ajedrez.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = [
        'NumeroPartida', 'Fecha', 'Hora', 'Color', 'Oponente', 'Resultado',
        'ECO', 'Apertura', 'Victoria', 'TiempoEntreMovimientos', 'Movimientos'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    numero_partida = 0

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break  # No hay más partidas
        numero_partida += 1

        # Extrae los encabezados de la partida
        headers = game.headers
        fecha = headers.get('UTCDate', '')
        hora = headers.get('UTCTime', '')
        white_player = headers.get('White', '')
        black_player = headers.get('Black', '')
        resultado = headers.get('Result', '')
        eco = headers.get('ECO', '')
        apertura = headers.get('Opening', '')

        # Determina el color y el oponente
        if white_player == username:
            color = 'Blancas'
            oponente = black_player
        elif black_player == username:
            color = 'Negras'
            oponente = white_player
        else:
            continue  # Ignora partidas donde no jugaste

        # Determina si fue victoria (1), derrota (0) o tablas (0.5)
        if (resultado == '1-0' and color == 'Blancas') or (resultado == '0-1' and color == 'Negras'):
            victoria = 1
        elif resultado == '1/2-1/2':
            victoria = 0.5
        else:
            victoria = 0

        # Calcula el tiempo entre movimientos
        tiempos_movimientos = []
        nodo = game
        tiempos_reloj = []
        regex_tiempo = re.compile(r'\[%clk ([0-9:]+)\]')

        while nodo.variations:
            siguiente_nodo = nodo.variation(0)
            comentario = nodo.comment
            match = regex_tiempo.search(comentario)
            if match:
                tiempo_str = match.group(1)
                partes = tiempo_str.split(':')
                if len(partes) == 3:
                    horas, minutos, segundos = map(float, partes)
                else:
                    horas = 0
                    minutos, segundos = map(float, partes)
                tiempo_total = timedelta(hours=horas, minutes=minutos, seconds=segundos).total_seconds()
                tiempos_reloj.append(tiempo_total)
            nodo = siguiente_nodo

        # Calcula la diferencia de tiempo entre movimientos
        for i in range(1, len(tiempos_reloj)):
            tiempo_entre_movimientos = tiempos_reloj[i - 1] - tiempos_reloj[i]
            tiempos_movimientos.append(tiempo_entre_movimientos)

        # Promedio del tiempo entre movimientos
        if tiempos_movimientos:
            promedio_tiempo = sum(tiempos_movimientos) / len(tiempos_movimientos)
        else:
            promedio_tiempo = None

        # Escribe los datos en el CSV
        writer.writerow({
            'NumeroPartida': numero_partida,
            'Fecha': fecha,
            'Hora': hora,
            'Color': color,
            'Oponente': oponente,
            'Resultado': resultado,
            'ECO': eco,
            'Apertura': apertura,
            'Victoria': victoria,
            'TiempoEntreMovimientos': promedio_tiempo,
            'Movimientos': len(tiempos_movimientos) + 1
        })

print('El archivo CSV ha sido generado exitosamente.')
