import chess.pgn
import csv
from datetime import datetime, timedelta
import re

username = 'marcosdedeu'

pgn_file = '/Users/marcosdedeu/Downloads/chess.pgn'
pgn = open(pgn_file, encoding='utf-8')

with open('datos_ajedrez.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = [
        'NumeroPartida', 'Fecha', 'Hora', 'Color', 'Oponente', 'Resultado',
        'ECO', 'Apertura', 'Victoria', 'TuELO', 'ELOOponente',
        'TiempoEntreMovimientos', 'Movimientos'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    numero_partida = 0

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        numero_partida += 1

        headers = game.headers
        fecha_str = headers.get('UTCDate', '')
        hora_str = headers.get('UTCTime', '')
        white_player = headers.get('White', '')
        black_player = headers.get('Black', '')
        resultado = headers.get('Result', '')
        eco = headers.get('ECO', '')
        apertura = headers.get('Opening', '')
        white_elo = headers.get('WhiteElo', '')
        black_elo = headers.get('BlackElo', '')

        # Parsear la fecha
        if fecha_str and fecha_str != '????.??.??':
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y.%m.%d').date()
                fecha_formateada = fecha_obj.strftime('%Y-%m-%d')
            except ValueError:
                fecha_formateada = ''
        else:
            fecha_formateada = ''

        # Parsear la hora (opcional)
        if hora_str and hora_str != '??:??:??':
            try:
                hora_obj = datetime.strptime(hora_str, '%H:%M:%S').time()
                hora_formateada = hora_obj.strftime('%H:%M:%S')
            except ValueError:
                hora_formateada = ''
        else:
            hora_formateada = ''

        # Determinar el color y el oponente
        if white_player == username:
            color = 'Blancas'
            oponente = black_player
            tu_elo = white_elo
            elo_oponente = black_elo
        elif black_player == username:
            color = 'Negras'
            oponente = white_player
            tu_elo = black_elo
            elo_oponente = white_elo
        else:
            continue  # Ignora partidas donde no jugaste

        if (resultado == '1-0' and color == 'Blancas') or (resultado == '0-1' and color == 'Negras'):
            victoria = 1
        elif resultado == '1/2-1/2':
            victoria = 0.5
        else:
            victoria = 0

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

        for i in range(1, len(tiempos_reloj)):
            tiempo_entre_movimientos = tiempos_reloj[i - 1] - tiempos_reloj[i]
            tiempos_movimientos.append(tiempo_entre_movimientos)

        if tiempos_movimientos:
            promedio_tiempo = sum(tiempos_movimientos) / len(tiempos_movimientos)
        else:
            promedio_tiempo = None

        writer.writerow({
            'NumeroPartida': numero_partida,
            'Fecha': fecha_formateada,
            'Hora': hora_formateada,
            'Color': color,
            'Oponente': oponente,
            'ECO': eco,
            'Apertura': apertura,
            'Victoria': victoria,
            'TuELO': tu_elo,
            'ELOOponente': elo_oponente,
            'TiempoEntreMovimientos': promedio_tiempo,
            'Movimientos': len(tiempos_movimientos) + 1
        })

print('El archivo CSV ha sido generado exitosamente con la fecha en formato adecuado.')
