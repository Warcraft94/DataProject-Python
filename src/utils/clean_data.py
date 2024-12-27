import geojson, geopandas, pandas
import os


def clean_energy_data():

    source_name = "countries.geojson"
    target_name = "cleaned_countries.geojson"

    base_dir = os.path.dirname(__file__)

    print(base_dir)

    source_path = os.path.join(base_dir, "..", "..", "data", "raw", source_name)
    target_path = os.path.join(base_dir, "..", "..", "data", "cleaned", target_name)
    

    # Lecture du fichier global
    countries = geopandas.read_file(source_path)
    
    mappingNameCountries = {
        "United States of America" : "United States",
        "Republic of Congo" : "Congo-Brazzaville",
        "Democratic Republic of the Congo" : "Congo-Kinshasa",
        "United Republic of Tanzania" : "Tanzania",
        "Myanmar" : "Burma", #(Burma = Birmanie)
        "Republic of Serbia" : "Former Serbia and Montenegro"
    }


    l = []
    # Sélection des données d'Ile de France
    for country in countries["ADMIN"]:
        if country != "World":
            
            
            # Add it to the list
            countrySelected = countries[countries["ADMIN"].str.startswith(country)]
            
            # Remplacer les noms de pays si nécessaire en utilisant le dictionnaire
            if countrySelected["ADMIN"].iloc[0] in mappingNameCountries:
                countrySelected["ADMIN"] = countrySelected["ADMIN"].replace(
                    mappingNameCountries
                )

            l.append(countrySelected)
    
    
    # Construction de la GeoDataFrame correspondante
    c = pandas.concat(l)
    
    # Ecriture dans un fichier
    with open(target_path, "w") as f:
        geojson.dump(c, f)

