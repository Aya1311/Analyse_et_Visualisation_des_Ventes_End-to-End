import csv
import random
import datetime
from faker import Faker

# Utiliser Faker pour générer certains champs aléatoires (noms, sociétés, emails, etc.)
fake = Faker('fr_FR')

# ========================================================
# Pour respecter la cohérence "Pays -> Villes",
# nous utilisons un dictionnaire statique :
# country_cities_map : { country_key: [liste_de_villes_cohérentes] }
# ========================================================
country_cities_map = {
    33: ["Paris", "Lyon", "Marseille", "Bordeaux", "Toulouse"],
    49: ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
    44: ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    39: ["Rome", "Milan", "Naples", "Turin", "Palermo"],
    34: ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    1: ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    55: ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
    81: ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo"],
    86: ["Shanghai", "Beijing", "Shenzhen", "Guangzhou", "Chengdu"],
    91: ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai"]
}


# -------------------------------------------------
# 1. Dimension DATE : dim_date.csv
#    PK = date_key (format AAAAMMJJ)
# -------------------------------------------------

def generate_dim_date(start_date, end_date, output_file='dim_date.csv'):
    """
    Génère un fichier CSV dim_date.csv avec :
      - PK: date_key = AAAAMMJJ
      - Autres colonnes : day, month, year, etc.
    """
    current_date = start_date
    rows = []

    while current_date <= end_date:
        date_key = int(current_date.strftime('%Y%m%d'))  # AAAAMMJJ => PK
        date_full = current_date.strftime('%Y-%m-%d')
        day = current_date.day
        month = current_date.month
        month_name = current_date.strftime('%B')  # Nom du mois
        quarter = (month - 1) // 3 + 1
        year = current_date.year
        day_of_week = current_date.isoweekday()  # 1 = Lundi, ... 7 = Dimanche
        week_of_year = int(current_date.strftime('%W'))  # 00..53
        day_name = current_date.strftime('%A')  # Nom du jour (Lundi, Mardi, etc.)

        rows.append([
            date_key,
            date_full,
            day,
            month,
            month_name,
            quarter,
            year,
            day_of_week,
            week_of_year,
            day_name
        ])

        current_date += datetime.timedelta(days=1)

    # Écriture du CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            'date_key', 'date_full', 'day', 'month', 'month_name',
            'quarter', 'year', 'day_of_week', 'week_of_year', 'day_name'
        ])
        writer.writerows(rows)

    print(f"[OK] dim_date.csv généré avec {len(rows)} lignes.")


# -------------------------------------------------
# 2. Dimension PAYS : dim_countries.csv
#    PK = country_key
# -------------------------------------------------

def generate_dim_countries(output_file='dim_countries.csv'):
    """
    Génère un fichier CSV dim_countries.csv avec la liste fixe de pays.
    PK = country_key.
    Retourne un dict {country_key: (ckey, cname, region, currency_code, language)}
    pour usage ultérieur.
    """
    countries_data = [
        (33, "France", "Europe", "EUR", "Français"),
        (49, "Allemagne", "Europe", "EUR", "Allemand"),
        (44, "Royaume-Uni", "Europe", "GBP", "Anglais"),
        (39, "Italie", "Europe", "EUR", "Italien"),
        (34, "Espagne", "Europe", "EUR", "Espagnol"),
        (1, "États-Unis", "Amérique", "USD", "Anglais"),
        (55, "Brésil", "Amérique", "BRL", "Portugais"),
        (81, "Japon", "Asie", "JPY", "Japonais"),
        (86, "Chine", "Asie", "CNY", "Chinois"),
        (91, "Inde", "Asie", "INR", "Hindi/Anglais")
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['country_key', 'country_name', 'region', 'currency_code', 'language'])

        for c in countries_data:
            writer.writerow(c)

    print(f"[OK] dim_countries.csv généré avec {len(countries_data)} lignes.")

    # On renvoie un dictionnaire pour usage ultérieur
    return {c[0]: c for c in countries_data}


# -------------------------------------------------
# 3. Dimension PRODUITS : dim_products.csv
#    PK = product_key
# -------------------------------------------------

def generate_dim_products(n_products=50, output_file='dim_products.csv'):
    """
    Génère n_products produits.
    PK = product_key.
    Retourne un dict {product_key: {...}}.
    """
    possible_categories = [
        ("Électronique", ["Smartphones", "Laptops", "TV", "Casques audio"]),
        ("Alimentaire", ["Snacks", "Boissons", "Produits frais"]),
        ("Vêtements", ["Homme", "Femme", "Enfant"]),
        ("Cosmétiques", ["Soins visage", "Maquillage", "Parfums"]),
        ("Maison", ["Décoration", "Meubles", "Electroménager"])
    ]

    products = []
    for product_key in range(1, n_products + 1):
        cat_tuple = random.choice(possible_categories)
        product_category = cat_tuple[0]
        product_subcategory = random.choice(cat_tuple[1])

        product_name = fake.word().capitalize() + " " + product_subcategory

        cost_price = round(random.uniform(5.0, 300.0), 2)

        products.append([
            product_key,
            product_name,
            product_category,
            product_subcategory,
            cost_price
        ])

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['product_key', 'product_name', 'product_category',
                         'product_subcategory', 'cost_price'])
        writer.writerows(products)

    print(f"[OK] dim_products.csv généré avec {len(products)} produits.")

    # Retour en dict
    product_dict = {}
    for p in products:
        product_dict[p[0]] = {
            'name': p[1],
            'category': p[2],
            'subcategory': p[3],
            'cost_price': p[4]
        }
    return product_dict


# -------------------------------------------------
# 4. Dimension CLIENTS : dim_customers.csv
#    PK = customer_key
# -------------------------------------------------

def pick_csp_by_age(age):
    """
    Retourne une CSP probable en fonction de l'âge (simplifié).
    """
    if age < 20:
        return "Étudiant"
    elif age < 30:
        return random.choice(["Employé", "Technicien", "Commerçant"])
    elif age < 50:
        return random.choice(["Cadre", "Profession libérale", "Entrepreneur"])
    else:
        return random.choice(["Retraité", "Cadre Supérieur", "Indépendant"])


def generate_dim_customers(n_customers=1000,
                           country_dict=None,
                           date_keys=None,
                           output_file='dim_customers.csv'):
    """
    Génère n_customers clients.
    PK = customer_key.
    - city choisie en fonction du pays (country_key).
    - created_date_key = FK vers la dimension DATE.
    - country_key = FK vers la dimension PAYS.
    """
    if not country_dict:
        raise ValueError("country_dict est requis pour lier les clients à un pays.")
    if not date_keys:
        raise ValueError("date_keys est requis pour la colonne created_date_key.")

    rows = []
    for customer_key in range(1, n_customers + 1):
        # 20% B2B, 80% B2C
        is_company = (random.random() < 0.2)
        if is_company:
            customer_name = fake.company()
            customer_type = "B2B"
        else:
            customer_name = fake.name()
            customer_type = "B2C"

        gender = random.choice(["M", "F"])
        age = random.randint(18, 70)
        csp = pick_csp_by_age(age)

        # Sélection d'un pays
        selected_country_key = random.choice(list(country_dict.keys()))

        # Sélection d'une ville en cohérence avec le pays
        if selected_country_key in country_cities_map:
            city = random.choice(country_cities_map[selected_country_key])
        else:
            # fallback (pas censé arriver ici, car on a mappé tous nos pays)
            city = fake.city()

        phone = fake.phone_number()
        email = fake.email()

        # Date de création du compte
        created_date_key = random.choice(date_keys)

        rows.append([
            customer_key,
            customer_name,
            customer_type,
            gender,
            age,
            csp,
            city,
            selected_country_key,  # FK vers dim_countries
            phone,
            email,
            created_date_key  # FK vers dim_date
        ])

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            'customer_key', 'customer_name', 'customer_type', 'gender', 'age',
            'csp', 'city', 'country_key', 'phone', 'email', 'created_date_key'
        ])
        writer.writerows(rows)

    print(f"[OK] dim_customers.csv généré avec {len(rows)} clients.")

    # On retourne un dict pour usage ultérieur (fact_sales)
    customer_dict = {}
    for r in rows:
        customer_dict[r[0]] = {
            'name': r[1],
            'type': r[2],
            'gender': r[3],
            'age': r[4],
            'csp': r[5],
            'city': r[6],
            'country_key': r[7],
            'phone': r[8],
            'email': r[9],
            'created_date_key': r[10]
        }
    return customer_dict


# -------------------------------------------------
# 5. Table de Faits : fact_sales.csv
#    PK (technique) = sale_id
#    FKs = date_key, product_key, customer_key, country_key
# -------------------------------------------------

def generate_fact_sales(n_sales=10000,
                        date_keys=None,
                        products=None,
                        customers=None,
                        countries=None,
                        output_file='fact_sales.csv'):
    """
    Génère n_sales transactions (table de faits).
    - sale_id = PK
    - FKs :
        date_key -> dim_date
        product_key -> dim_products
        customer_key -> dim_customers
        country_key -> dim_countries
    """
    if not date_keys or not products or not customers or not countries:
        raise ValueError("date_keys, products, customers et countries sont requis.")

    rows = []
    sale_id_counter = 1

    for _ in range(n_sales):
        sale_id = sale_id_counter
        sale_id_counter += 1

        # Choix d'un client (FK vers dim_customers)
        customer_key = random.choice(list(customers.keys()))
        customer_info = customers[customer_key]

        # On récupère le country_key depuis le client pour rester cohérent
        country_key = customer_info['country_key']
        country_info = countries[country_key]  # (ckey, cname, region, currency_code, language)

        # Choix d'un produit (FK vers dim_products)
        product_key = random.choice(list(products.keys()))
        product_info = products[product_key]

        # Choix d'une date de vente (FK vers dim_date)
        date_key = random.choice(date_keys)

        # Quantité vendue
        quantity = random.randint(1, 20)

        # Calcul du prix unitaire : entre cost_price et 2 * cost_price
        cost_price = product_info['cost_price']
        unit_price = round(random.uniform(cost_price, cost_price * 2.0), 2)

        # Devise = currency_code liée au pays du client
        currency = country_info[3]  # index 3 = currency_code

        rows.append([
            sale_id,
            date_key,
            product_key,
            customer_key,
            country_key,
            quantity,
            unit_price,
            currency
        ])

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            'sale_id',
            'date_key',
            'product_key',
            'customer_key',
            'country_key',
            'quantity',
            'unit_price',
            'currency'
        ])
        writer.writerows(rows)

    print(f"[OK] fact_sales.csv généré avec {len(rows)} lignes.")


# -------------------------------------------------
# MAIN : exécution de la génération
# -------------------------------------------------

if __name__ == "__main__":
    # 1) Générer la dimension DATE (PK = date_key)
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    generate_dim_date(start_date, end_date, output_file='dim_date.csv')

    # Charger la liste des date_keys pour s'en servir comme FK
    date_keys = []
    with open('dim_date.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            date_keys.append(int(row['date_key']))

    # 2) Générer la dimension PAYS (PK = country_key)
    countries_dict = generate_dim_countries(output_file='dim_countries.csv')
    # Ex : countries_dict[33] = (33, "France", "Europe", "EUR", "Français")

    # 3) Générer la dimension PRODUITS (PK = product_key)
    products_dict = generate_dim_products(n_products=50, output_file='dim_products.csv')
    # Ex : products_dict[1] = { 'name': ..., 'cost_price': ... }

    # 4) Générer la dimension CLIENTS (PK = customer_key)
    #    -> On a besoin de date_keys (FK: created_date_key) et countries_dict (FK: country_key)
    customers_dict = generate_dim_customers(
        n_customers=1000,
        country_dict=countries_dict,
        date_keys=date_keys,
        output_file='dim_customers.csv'
    )
    # Ex : customers_dict[1] = { 'name': ..., 'country_key': ..., 'created_date_key': ... }

    # 5) Générer la table de Faits (PK = sale_id)
    #    -> FKs : date_key, product_key, customer_key, country_key
    generate_fact_sales(
        n_sales=10000,
        date_keys=date_keys,
        products=products_dict,
        customers=customers_dict,
        countries=countries_dict,
        output_file='fact_sales.csv'
    )

    print("\nGénération terminée !")
