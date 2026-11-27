import os
env = os.getenv("APP_ENV", "dev")
print(f"=== Mini-Quiz Docker (Mode : {env}) ===")
rep = input("Quelle commande liste les conteneurs actifs ? ")
print("Bonne réponse !" if rep.strip() == "docker ps" else "Faux (attendu : docker ps)")
