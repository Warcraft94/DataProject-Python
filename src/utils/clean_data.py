import geojson, geopandas, pandas
import os


def clean_geojson():

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
    
    for country in countries["ADMIN"]:
        if country != "World":
            
            countrySelected = countries[countries["ADMIN"].str.startswith(country)]
            
            if countrySelected["ADMIN"].iloc[0] in mappingNameCountries:
                countrySelected["ADMIN"] = countrySelected["ADMIN"].replace(
                    mappingNameCountries
                )

            l.append(countrySelected)

    c = pandas.concat(l)
    
    # Ecriture dans un fichier
    with open(target_path, "w") as f:
        geojson.dump(c, f)

