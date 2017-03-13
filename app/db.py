from datetime import timedelta


def get_start_date(conn, symbol):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(date) FROM ohlcv WHERE symbol = %s", (symbol,))
        start_date, = cursor.fetchone() # returns none if there are no records

        if start_date:
            start_date += timedelta(days=1)
    finally:
    	cursor.close()
    
    return start_date


def save_stock_data(data, conn, symbol):
    cursor = conn.cursor()
    for record in data.itertuples():
            cursor.execute(
                "INSERT INTO ohlcv (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (symbol, record[0], record[1], record[2], record[3], record[4], record[5]),
            )
    conn.commit()
    cursor.close()