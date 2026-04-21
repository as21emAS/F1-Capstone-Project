import psycopg2
conn = psycopg2.connect(
    "postgresql://racetrack_om7m_user:nmW9ojY9q2qHT51Hnxnoup3Whm7wEzQy@dpg-d7jebfq8qa3s73aht7jg-a.virginia-postgres.render.com/racetrack_om7m",
    sslmode="require"
)
cur = conn.cursor()
cur.execute("ALTER TABLE race_results ADD CONSTRAINT uq_race_result UNIQUE (race_id, driver_id);")
conn.commit()
print("done")
conn.close()