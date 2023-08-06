import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.text as mtext
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3
from py4pm.dateutilities import add_season


DB_AEROSOLS = "/home/webersa/Documents/BdD/bdd_aerosols/aerosols.db"

MAPPER_METALS_NAME_TO_SYMBOLE = {
        'Actinium': 'Ac', 'Aluminium': 'Al', 'Americium': 'Am', 'Antimony': 'Sb', 'Argon': 'Ar', 'Arsenic': 'As', 'Astatine': 'At', 'Barium': 'Ba', 'Berkelium': 'Bk', 'Beryllium': 'Be', 'Bismuth': 'Bi', 'Bohrium': 'Bh', 'Boron': 'B', 'Bromine': 'Br', 'Cadmium': 'Cd', 'Calcium': 'Ca', 'Californium': 'Cf', 'Carbon': 'C', 'Cerium': 'Ce', 'Cesium': 'Cs', 'Chlorine': 'Cl', 'Chromium': 'Cr', 'Cobalt': 'Co', 'Copper': 'Cu', 'Curium': 'Cm', 'Dubnium': 'Db', 'Dysprosium': 'Dy', 'Einsteinium': 'Es', 'Erbium': 'Er', 'Europium': 'Eu', 'Fermium': 'Fm', 'Fluorine': 'F', 'Francium': 'Fr', 'Gadolinium': 'Gd', 'Gallium': 'Ga', 'Germanium': 'Ge', 'Gold': 'Au', 'Hafnium': 'Hf', 'Hassium': 'Hs', 'Helium': 'He', 'Holmium': 'Ho', 'Hydrogen': 'H', 'Indium': 'In', 'Iodine': 'I', 'Iridium': 'Ir', 'Iron': 'Fe', 'Krypton': 'Kr', 'Lanthanum': 'La', 'Lawrencium': 'Lr', 'Lead': 'Pb', 'Lithium': 'Li', 'Lutetium': 'Lu', 'Magnesium': 'Mg', 'Manganese': 'Mn', 'Meitnerium': 'Mt', 'Mendelevium': 'Md', 'Mercury': 'Hg', 'Molybdenum': 'Mo', 'Neodymium': 'Nd', 'Neon': 'Ne', 'Neptunium': 'Np', 'Nickel': 'Ni', 'Niobium': 'Nb', 'Nitrogen': 'N', 'Nobelium': 'No', 'Osmium': 'Os', 'Oxygen': 'O', 'Palladium': 'Pd', 'Phosphorus': 'P', 'Platinum': 'Pt', 'Plutonium': 'Pu', 'Polonium': 'Po', 'Potassium': 'K', 'Praseodymium': 'Pr', 'Promethium': 'Pm', 'Protactinium': 'Pa', 'Radium': 'Ra', 'Radon': 'Rn', 'Rhenium': 'Re', 'Rhodium': 'Rh', 'Rubidium': 'Rb', 'Ruthenium': 'Ru', 'Rutherfordium': 'Rf', 'Samarium': 'Sm', 'Scandium': 'Sc', 'Seaborgium': 'Sg', 'Selenium': 'Se', 'Silicon': 'Si', 'Silver': 'Ag', 'Sodium': 'Na', 'Strontium': 'Sr', 'Sulfur': 'S', 'Tantalum': 'Ta', 'Technetium': 'Tc', 'Tellurium': 'Te', 'Terbium': 'Tb', 'Thallium': 'Tl', 'Thorium': 'Th', 'Thulium': 'Tm', 'Tin': 'Sn', 'Titanium': 'Ti', 'Tungsten': 'W', 'Ununbium': 'Uub', 'Ununnilium': 'Uun', 'Unununium': 'Uuu', 'Uranium': 'U', 'Vanadium': 'V', 'Xenon': 'Xe', 'Ytterbium': 'Yb', 'Yttrium': 'Y', 'Zinc': 'Zn', 'Zirconium': 'Zr'
        }

class LegendTitle(object):
    def __init__(self, text_props=None):
        self.text_props = text_props or {}
        super(LegendTitle, self).__init__()

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        title = mtext.Text(x0, y0, orig_handle, **self.text_props)
        handlebox.add_artist(title)
        return title

def get_all_species_pretty_index():
    carboneous = ["OC", "OC*", "EC"]
    ions = ["Cl-", "NO3-", "SO42-", "Na+", "NH4+", "K+", "Mg2+", "Ca2+"]
    organics = [
        "MSA",
        "Arabitol", "Sorbitol", "Mannitol", "Levoglucosan", "Mannosan",
        "Polyols",
        "Galactosan", "Glucose", "Cellulose", "Oxalate", 
        
        "Maleic", "Succinic", "Citraconic", "Glutaric", "Oxoheptanedioic",
        "MethylSuccinic", "Adipic", "Methylglutaric", "3-MBTCA", "Phtalic",
        "Pinic", "Suberic", "Azelaic", "Sebacic",

        "PAH_Sum", "Alkanes_Sum", "MethPAH_Sum", "PAHs_Sum", "Hopane_Sum",
        "Methoxyphenol_Sum", "MNC_Sum", "MC_Sum",
        "BNT(2,1)", "BNT(1,2)", "BNT(2,3)", "DNT(2,1)", "BPT(2,1)",
        "Vanilline", "Acetovanillone", "Guaiacylacetone", "Coniferylaldehyde",
        "Vanillic", "Hamovanillic", "Syringol", "4-methylsyringol",
        "4-propenylsyringol", "Acetosyringone", "Syringyl_acetone",
        "Sinapyl_aldehyde", "Syringic_acid", "Cholesterol",
        "Phe", "Ace", "For", "An", "Fla", "Pyr", "Tri", "Ret", "BaA", "Chr", "BeP", "BbF", "BkF",
        "BaP", "BghiP", "DBahA", "IP", "Cor",

        "Nb_VL",
    ]
    organics += ["C{}".format(i) for i in range(11,41)]
    organics += ["HP{c}".format(c=str(i)) for i in range(1,11)]
    organics += ["Alkanes_WAX", "Alkanes_noWAX"]

    metals = [
        "Al", "As", "Ba", "Ca", "Cd", "Ce", "Co", "Cr", "Cs", "Cu", "Fe", "K",
        "La", "Li", "Mg", "Mn", "Mo", "Na", "Ni", "Pb", "Pd", "Pt", "Rb", "Sb",
        "Sc", "Se", "Sn", "Sr", "Ti", "Tl", "V", "Zn", "Zr"
    ]

    keep_col = ["Date", "PM10", "PM10 corrigées", "PM2.5 corrigées",
                "PM10recons", "PMrecons"] + carboneous + ions + organics + metals
    return keep_col

def replace_QL(dftmp, species=None, conn=None):
    """Replace the -1 and -2 in the dataframe by the appropriate DL and QL
    values

    The change are done inplace.

    :dftmp: pandas DataFrame
    """
    stations = dftmp.station.unique()

    if species is None:
        species = dftmp.columns

    if conn is None:
        conn = sqlite3.connect("/home/webersa/Documents/BdD/BdD_PM/aerosols.db")
    
    sqlquery = """
        SELECT {sp} FROM QL 
        WHERE station IN ("{stations}")
        AND "sample ID" LIKE "%QL%";
        """.format(
            sp='", "'.join(species),
            stations='", "'.join(stations)
        )
    print(sqlquery)
    QLtmp = pd.read_sql(sqlquery, con=conn)
    print(QLtmp)
    conn.close()
    QLtmp = QLtmp.apply(pd.to_numeric, errors='ignore').dropna(how="all", axis=1)
    for station in stations:
        QLtmpmean = QLtmp[QLtmp.station==station].mean()
        to_replace = {
            c: {-2: QLtmpmean[c]/2, -1: QLtmpmean[c]/2} for c in QLtmpmean.index
        }
        for c in dftmp.columns:
            if c not in species: continue
            if (c in to_replace.keys()) and (pd.notna(to_replace[c][-1])):
                idx = dftmp.station == station
                dftmp.loc[idx, c] = dftmp.loc[idx, c].clip_lower(to_replace[c][-1])

def get_sourceColor(source=None):
    """Return the hexadecimal color of the source(s) 

    If no option, then return the whole dictionary
    
    Optional Parameters
    ===================

    source : str
        The name of the source
    """
    color = {
        "Traffic": "#000000",
        "Traffic 1": "#000000",
        "Traffic 2": "#102262",
        "Road traffic": "#000000",
        "Primary traffic": "#000000",
        "Traffic_ind": "#000000",
        "Traffic_exhaust": "#000000",
        "Traffic_dir": "#444444",
        "Traffic_non-exhaust": "#444444",
        "Resuspended_dust": "#444444",
        "Oil/Vehicular": "#000000",
        "Road traffic/oil combustion": "#000000",
        "Biomass_burning": "#92d050",
        "Biomass burning": "#92d050",
        "Biomass_burning1": "#92d050",
        "Biomass_burning2": "#92d050",
        "Sulfate-rich": "#ff2a2a",
        "Sulfate_rich": "#ff2a2a",
        "Sulfate rich": "#ff2a2a",
        "Nitrate-rich": "#217ecb", # "#ff7f2a",
        "Nitrate_rich": "#217ecb", # "#ff7f2a",
        "Nitrate rich": "#217ecb", # "#ff7f2a",
        "Secondary_inorganics": "#0000cc",
        "MSA_rich": "#ff7f2a", # 8c564b",
        "MSA-rich": "#ff7f2a", # 8c564b",
        "Secondary_oxidation": "#ff87dc",
        "Secondary_biogenic_oxidation": "#ff87dc",
        "Secondary oxidation": "#ff87dc",
        "Secondary biogenic oxidation": "#ff87dc",
        "Marine SOA": "#ff7f2a", # 8c564b",
        "Biogenic SOA": "#8c564b",
        "Anthropogenic SOA": "#8c564b",
        "Marine/HFO": "#a37f15", #8c564b",
        "Aged seasalt/HFO": "#8c564b",
        "Marine_biogenic": "#fc564b",
        "HFO": "#70564b",
        "HFO (stainless)": "#70564b",
        "Oil": "#70564b",
        "Vanadium rich": "#70564b",
        "Cadmium rich": "#70564b",
        "Marine": "#33b0f6",
        "Marin": "#33b0f6",
        "Salt": "#00b0f0",
        "Seasalt": "#00b0f0",
        "Sea-road salt": "#209ecc",
        "Sea/road salt": "#209ecc",
        "Fresh seasalt": "#00b0f0",
        "Aged_salt": "#97bdff", #00b0f0",
        "Aged seasalt": "#97bdff", #00b0f0",
        "Aged sea salt": "#97bdff", #00b0f0",
        "Fungal spores": "#ffc000",
        "Primary_biogenic": "#ffc000",
        "Primary biogenic": "#ffc000",
        "Biogenique": "#ffc000",
        "Biogenic": "#ffc000",
        "Dust": "#dac6a2",
        "Mineral dust": "#dac6a2",
        "Crustal_dust": "#dac6a2",
        "Industrial": "#7030a0",
        "Industries": "#7030a0",
        "Indus/veh": "#5c304b",
        "Industry/traffic": "#5c304b", #7030a0",
        "Arcellor": "#7030a0",
        "Siderurgie": "#7030a0",
        "Plant debris": "#2aff80",
        "Plant_debris": "#2aff80",
        "Débris végétaux": "#2aff80",
        "Choride": "#80e5ff",
        "PM other": "#cccccc",
        "Traffic/dust (Mix)": "#333333",
        "SOA/sulfate (Mix)": "#6c362b",
        "Sulfate rich/HFO": "#8c56b4",
        "nan": "#ffffff",
        "Undetermined": "#666"
    }
    color = pd.DataFrame(index=["color"], data=color)
    if source:
        if source not in color.keys():
            print("WARNING: no {} found in colors".format(source))
            return "#666666"
        return color.loc["color", source]
    else:
        return color

def get_sourcesCategories(profiles):
    """Get the sources category according to the sources name.

    Ex. Aged sea salt → Aged_sea_salt

    :profiles: list
    :returns: list

    """
    possible_sources = {
        "Vehicular": "Traffic",
        "VEH": "Traffic",
        "VEH ind": "Traffic_ind",
        "Traffic_exhaust": "Traffic_exhaust",
        "Traffic_non-exhaust": "Traffic_non-exhaust",
        "VEH dir": "Traffic_dir",
        "Oil/Vehicular": "Traffic",
        "Oil": "Oil",
        "Vanadium rich": "Vanadium rich",
        "Road traffic/oil combustion": "Traffic",
        "Traffic": "Road traffic",
        "Traffic 1": "Traffic 1",
        "Traffic 2": "Traffic 2",
        "Primary traffic": "Road traffic",
        "Road traffic": "Road traffic",
        "Road trafic": "Road traffic",
        "Road traffic/dust": "Traffic/dust (Mix)",
        "Bio. burning": "Biomass_burning",
        "Bio burning": "Biomass_burning",
        "Comb fossile/biomasse": "Biomass_burning",
        "BB": "Biomass_burning",
        "Biomass_burning": "Biomass_burning",
        "Biomass Burning": "Biomass_burning",
        "Biomass burning": "Biomass_burning",
        "BB1": "Biomass_burning1",
        "BB2": "Biomass_burning2",
        "Sulfate-rich": "Sulfate_rich",
        "Sulphate-rich": "Sulfate_rich",
        "Nitrate-rich": "Nitrate_rich",
        "Sulfate rich": "Sulfate_rich",
        "Sulfate_rich": "Sulfate_rich",
        "Nitrate rich": "Nitrate_rich",
        "Nitrate_rich": "Nitrate_rich",
        "Secondary inorganics": "Secondary_inorganics",
        "Secondaire": "MSA_rich",
        "Secondary bio": "MSA_rich",
        "Secondary biogenic": "MSA_rich",
        "Secondary organic": "MSA_rich",
        "Secondary oxidation": "Secondary_oxidation",
        "Secondary biogenic oxidation": "Secondary_biogenic_oxidation",
        "Secondaire organique": "MSA_rich",
        # "Marine SOA": "Marine SOA",
        "Marine SOA": "MSA_rich",
        "MSA_rich": "MSA_rich",
        "MSA-rich": "MSA-rich",
        "MSA rich": "MSA_rich",
        "Secondary biogenic/sulfate": "SOA/sulfate (Mix)",
        "Marine SOA/SO4": "SOA/sulfate (Mix)",
        "Marine/HFO": "Marine/HFO",
        "Marine biogenic/HFO": "Marine/HFO",
        "Secondary biogenic/HFO": "Marine/HFO",
        "Marine bio/HFO": "Marine/HFO",
        "Marin bio/HFO": "Marine/HFO",
        "Sulfate rich/HFO": "Marine/HFO",
        "Marine secondary": "MSA_rich",
        "Marin secondaire": "MSA_rich",
        "HFO": "HFO",
        "HFO (stainless)": "HFO",
        "Marin": "MSA_rich",
        "Sea/road salt": "Sea-road salt",
        "Sea-road salt": "Sea-road salt",
        "sea-road salt": "Sea-road salt",
        "Road salt": "Salt",
        "Sea salt": "Salt",
        "Seasalt": "Salt",
        "Salt": "Salt",
        "Fresh seasalt": "Salt",
        "Sels de mer": "Salt",
        "Aged_salt": "Aged_salt",
        "Aged sea salt": "Aged_salt",
        "Aged seasalt": "Aged_salt",
        "Aged seasalt": "Aged_salt",
        "Aged salt": "Aged_salt",
        "Primary_biogenic": "Primary_biogenic",
        "Primary bio": "Primary_biogenic",
        "Primary biogenic": "Primary_biogenic",
        "Biogénique primaire": "Primary_biogenic",
        "Biogenique": "Primary_biogenic",
        "Biogenic": "Primary_biogenic",
        "Mineral dust": "Dust",
        "Mineral dust ": "Dust",
        "Resuspended_dust": "Resuspended_dust",
        "Resuspended dust": "Resuspended_dust",
        "Dust": "Dust",
        "Crustal dust": "Dust",
        "Dust (mineral)": "Dust",
        "Dust/biogénique marin": "Dust",
        "AOS/dust": "Dust",
        "Industrial": "Industrial",
        "Industry": "Industrial",
        "Industrie": "Industrial",
        "Industries": "Industrial",
        "Industry/vehicular": "Industry/traffic",
        "Industry/traffic": "Industry/traffic",
        "Industries/trafic": "Industry/traffic",
        "Cadmium rich": "Cadmium rich",
        "Fioul lourd": "HFO",
        "Arcellor": "Industrial",
        "Siderurgie": "Industrial",
        "Débris végétaux": "Plant_debris",
        "Chlorure": "Chloride",
        "PM other": "Other",
        "Undetermined": "Undertermined"
        }
    s = [possible_sources[k] for k in profiles]
    return s

def get_site_typology():
    import collections
    
    site_typologie = collections.OrderedDict()
    site_typologie["Urban"] = ["Talence", "Lyon", "Poitiers", "Nice", "MRS-5av",
                               "PdB", "Aix-en-provence", "Nogent", "Poitiers",
                               "Lens-2011-2012", "Lens-2013-2014", "Lens", "Rouen"]
    site_typologie["Valley"] = ["Chamonix", "Passy", "Marnaz", "GRE-cb", "VIF",
                                "GRE-fr", "Passy_decombio"]
    site_typologie["Traffic"] = ["Roubaix", "STG-cle"]
    site_typologie["Rural"] = ["Revin", "Peyrusse", "ANDRA-PM10", "ANDRA-PM2.5"]

    site_typologie_SOURCES = collections.OrderedDict()
    site_typologie_SOURCES["Urban"] = [
        "LEN", "LY", "MRS", "NGT", "NIC", "POI", "PdB", "PROV", "TAL", "ROU"
    ]
    site_typologie_SOURCES["Valley"] = ["CHAM", "GRE"]
    site_typologie_SOURCES["Traffic"] = ["RBX", "STRAS"]
    site_typologie_SOURCES["Rural"] = ["REV"]

    for typo in site_typologie.keys():
        site_typologie[typo] += site_typologie_SOURCES[typo]

    return site_typologie

def get_OC_from_OC_star_and_organic(df):
    """
    Re-compute OC taking into account the organic species

    OC = OC* + sum(eqC_sp)
    """
    OC = df.loc['OC*'].copy()
    equivC = {
        'Oxalate': 0.27,
        'Arabitol': 0.40,
        'Mannitol': 0.40,
        'Sorbitol': 0.40,
        'Polyols': 0.40,
        'Levoglucosan': 0.44,
        'Mannosan': 0.44,
        'Galactosan': 0.44,
        'MSA': 0.12,
        'Glucose': 0.44,
        'Cellulose': 0.44,
        'Maleic': 0.41,
        'Succinic': 0.41,
        'Citraconic': 0.46,
        'Glutaric': 0.45,
        'Oxoheptanedioic': 0.48,
        'MethylSuccinic': 0.53,
        'Adipic': 0.49,
        'Methylglutaric': 0.49,
        '3-MBTCA': 0.47,
        'Phtalic': 0.58,
        'Pinic': 0.58,
        'Suberic': 0.55,
        'Azelaic': 0.57,
        'Sebacic': 0.59,
    }
    for sp in equivC.keys():
        if sp in df.index:
            OC += df.loc[sp] * equivC[sp]
    return OC

def get_sample_where(sites=None, date_min=None, date_max=None, species=None,
                     min_sample=None, particle_size=None, exclude_sites=None, con=None):
    """Get dataframe that meet conditions

    :sites: TODO
    :date_min: TODO
    :date_max: TODO
    :min_sample: int, minimum samples size
    :particle_size:
    :con: sqlite3 connection
    :returns: TODO

    """
    df = pd.read_sql("SELECT * FROM values_all;", con=con)

    df["Date"] = pd.to_datetime(df["Date"])
    if date_min:
        df = df.loc[date_min < df["Date"]]
    if date_max:
        df = df.loc[df["Date"] < date_max]
    if species:
        df = df.loc[df[species].notnull().all(axis=1)]

    if particle_size == "show":
        df["Station"] = df["Station"]+"—"+df["Particle_size"]
    elif particle_size in ["PM10", "PM2.5", "PM1"]:
        df = df.loc[df["Particle_size"] == particle_size]
    
    if exclude_sites:
        df = df.loc[~df["Station"].isin(exclude_sites)]

    if min_sample:
        keep_stations = df.groupby("Station").size()
        keep_stations = list(keep_stations.loc[keep_stations > min_sample].index)
        df = df.loc[df["Station"].isin(keep_stations)]
    return df

def compute_PMreconstructed(df, takeOnlyPM10=True):
    """
    Add a column `PM10recons`: the mass of the PM10 according to the chemistry

    Returns
    -------
    PMrecons: pd.DataFrame
    """

    if takeOnlyPM10 and ("PM10" not in df.index.get_level_values("Particle_size").unique()):
        print(
            "WARNING: no 'PM10' in 'Particle size'. Cannot reconstruct the PM "
            "mass."
        )
        return

    # The reconstruction method hold only for PM10.
    if takeOnlyPM10:
        idx = df.index.get_level_values("Particle_size") == "PM10"
        dftmp = df.loc[idx].copy()
    else:
        dftmp = df.copy()

    if "Date" not in df.index.names:
        dftmp.set_index(["Date"], inplace=True)

    num = dftmp._get_numeric_data()
    num[num < 0] = 0
    dftmp.dropna(axis=1, how="all", inplace=True)
    cols = dftmp.columns

    PMrecons = pd.DataFrame(index=dftmp.index, columns=[])

    required_cols = ["Na+", "Ca2+", "OC", "EC", "NH4+", "NO3-", "SO42-"]
    for c in required_cols:
        if c not in cols:
            print("WARNING: PM reconstrution fail, missing {c}".format(c=c))
            return
    nancol = pd.isna(df[required_cols]).any(axis=1)

    if "NO3-" in cols:
        PMrecons["NO3-"] = dftmp["NO3-"]/1000
    if "NH4+" in cols:
        PMrecons["NH4+"] = dftmp["NH4+"]/1000
    if "EC" in cols:
        PMrecons["EC"] = dftmp["EC"]
    if "OC" in cols:
        PMrecons["OM"] = 1.75*dftmp["OC"]
    if "SO42-" in cols:
        ssSO4 = 0.252 * dftmp["Na+"]
        nssSO4 = dftmp["SO42-"] - ssSO4
        PMrecons["nss-SO42-"] = nssSO4/1000

    # seasalt
    if "Cl-" in cols:
        seasalt = dftmp["Cl-"] + 1.47*dftmp["Na+"]
    else:
        seasalt = 2.252 * dftmp["Na+"]
    PMrecons["seasalt"] = seasalt/1000

    # ==== dust ===============================================================
    # Putaud : Putaud et al (2003a)
    #    dust = 4.6 * nssCa
    #         = 4.6 * (Ca2+ - Na+/26)
    # Malm : Malm et al (1993)
    #    dust = 0.16 * (1.90*Al + 2.15*Si + 1.41*Ca + 1.09*Fe + 1.67*Ti)
    # Querol/Perez : Querol et al (2000) & Pérez et al (2008)
    #    dust = Al2O3 + CO3 + SiO2
    #         = 1.89*Al + 1.5*Ca + 3*(1.89*Al)
    maskPutaud = pd.Series(index=dftmp.index, data=[True]*len(dftmp))
    maskMalm = pd.Series(index=dftmp.index, data=[True]*len(dftmp))
    maskQuerolPerez = pd.Series(index=dftmp.index, data=[True]*len(dftmp))
    dust = pd.DataFrame(
        columns=['dust'], data=np.nan, index=dftmp.index
    )

    # (Putaud et al., 2003a)
    maskPutaud = dftmp["Ca2+"].notnull() & dftmp["Na+"].notnull()
    nssCa = dftmp["Ca2+"] - dftmp["Na+"]/26
    dusttmp = 4.6 * nssCa
    dust.loc[maskPutaud, "dust"] = dusttmp[maskPutaud]
    # (Malm et al., 1993)
    if all([i in cols for i in ["Al", "Si", "Ca", "Fe", "Ti"]]):
        for c in ["Al", "Si", "Ca", "Fe", "Ti"]:
            maskMalm = maskMalm & dftmp[c].notnull()
        dusttmp = 0.16 * (1.90*dftmp["Al"] + 2.15*dftmp["Si"] + 1.41*dftmp["Ca"]
                          + 1.09*dftmp["Fe"] + 1.67*dftmp["Ti"])
        dust.loc[maskMalm, "dust"] = dusttmp[maskMalm]
    else:
        maskMalm = ~maskMalm
    # (Querol et al., 2000; Pérez et al., 2008)
    querolperez_metals = ["Al", "Ca", "Fe", "K", "Mg", "Mn", "Ti", "P"]
    if all([i in cols for i in querolperez_metals]):
        maskQuerolPerez = maskQuerolPerez & dftmp[querolperez_metals].notnull().all(axis=1)
        Al2O3 = 1.89 * dftmp["Al"]
        CO3 = 1.5 * dftmp["Ca"]
        SiO2 = 3 * Al2O3
        dusttmp = Al2O3 + CO3 + SiO2
        for c in ["Ca", "Fe", "K", "Mg", "Mn", "Ti", "P"]:
            dusttmp += dftmp[c]
        dust.loc[maskQuerolPerez, "dust"] = dusttmp[maskQuerolPerez]
    else:
        maskQuerolPerez = ~maskQuerolPerez

    PMrecons["dust"] = dust["dust"]

    PMreconsType = pd.DataFrame(index=PMrecons.index,
                                columns=["dust_recons_type"], data="None")
    PMreconsType.where(~maskPutaud, other="Putaud et al. 2003a", inplace=True)
    PMreconsType.where(~maskMalm, other="Malm et al, 1993", inplace=True)
    PMreconsType.where(~maskQuerolPerez, other="Querol et al., 2000 ; Pérez et al., 2008", inplace=True)
    PMrecons["dust"] /= 1000

    # ==== non dust (Salameh et al. 2014)
    nondust_metals = ["Cu", "Ni", "Pb", "V", "Zn"]
    if all([i in cols for i in nondust_metals]):
        nondust = dftmp[nondust_metals].sum(axis=1)
        PMrecons["nondust"] = nondust/1000

    # ==== PM recons ==========================================================
    # print(PMrecons.sum(axis=1))
    # print(df)
    # df["PM10recons"] = PMrecons.sum(axis=1).replace({0: np.nan})
    # df["PM10reconsDustType"] = PMreconsType
    # print(df["PM10recons"])
    # df.loc[nancol, "PM10recons"] = np.nan

    return PMrecons

def _pretty_specie(text):
    map_species = {
        "Cl-": "Cl$^-$",
        "Na+": "Na$^+$",
        "K+": "K$^+$",
        "NO3-": "NO$_3^-$",
        "NH4+": "NH$_4^+$",
        "SO42-": "SO$_4^{2-}$",
        "Mg2+": "Mg$^{2+}$",
        "Ca2+": "Ca$^{2+}$",
        "nss-SO42-": "nss-SO$_4^{2-}$",
        "OP_DTT_m3": "OP$^{DTT}_v$",
        "OP_AA_m3": "OP$^{AA}_v$",
        "OP_DTT_µg": "OP$^{DTT}_m$",
        "OP_AA_µg": "OP$^{AA}_m$",
        "PM_µg/m3": "PM mass",
        "PM10": "PM$_{10}$",
        "PM2.5": "PM$_{2.5}$"
    }
    if text in map_species.keys():
        return map_species[text]
    else:
        return text

def pretty_specie(text):
    if isinstance(text, list):
        mapped = [_pretty_specie(x) for x in text]
    elif isinstance(text, str):
        mapped = _pretty_specie(text)
    else:
        raise KeyError(
            "`text` must be a {x,y}ticklabels, a list of string or string"
        )
    return mapped

def format_ions(text):
    print("WARNING: format_ions is deprecated, use pretty_specie instead")
    return pretty_specie(text)

def _specie_unit(text):
    """Return the unit of a given species.

    Default unit is supposed to bo ng m⁻³
    """
    map_species = {
        "OP_DTT_m3": "nmol min⁻¹ m⁻³",
        "OP_AA_m3": "nmol min⁻¹ m⁻³",
        "OP_DTT_µg": "nmol min⁻¹ µg⁻¹",
        "OP_AA_µg": "nmol min⁻¹ µg⁻¹",
        "PM_µg/m3": "µg m⁻³",
        "OC": "µg m⁻³",
        "EC": "µg m⁻³",
        "PM10": "µg m⁻³",
        "PM2.5": "µg m⁻³",
        "PM10recons": "µg m⁻³",
    }
    if text in map_species.keys():
        return map_species[text]
    else:
        return "ng m⁻³"

def specie_unit(text):
    if isinstance(text, list):
        mapped = [_specie_unit(x) for x in text]
    elif isinstance(text, str):
        mapped = _specie_unit(text)
    else:
        raise KeyError(
            "`text` must be a {x,y}ticklabels, a list of string or string"
        )
    return mapped


class plot():
    
    def _mainComponentOfPM(dff, station):
        COLORS = {
            "OM": "#008000",
            "EC": "#000000",
            "Cl-": "#59B2B2",
            "NO3-": "#0000FF",
            "SO42-": "#FF0000",
            "NH4+": "#FF8000",
            "Ca2+": "#CED770",
            "Other ions": "#710077",
            "Metals": "#804000",
            "Anhydrous monosaccharides": "#004000",
            "Organic acids": "#CE9E8E",
            "Polyols": "#A0A015",
            "Oxalate": "#7D0000",
            "MSA": "#2D00BB",
            "Glucose": "#4B8A08",
            "Cellulose": "#0B3B0B",
            "HULIS": "#58ACFA"
        }
        TEXTCOLORS = {
            "OM": "#000000",
            "EC": "#FFFFFF",
            "Cl-": "#000000",
            "NO3-": "#FFFFFF",
            "SO42-": "#000000",
            "NH4+": "#000000",
            "Ca2+": "#000000",
            "Other ions": "#FFFFFF",
            "Metals": "#FFFFFF",
            "Anhydrous monosaccharides": "#FFFFFF",
            "Organic acids": "#000000",
            "Polyols": "#000000",
            "Oxalate": "#FFFFFF",
            "MSA": "#FFFFFF",
            "Glucose": "#FFFFFF",
            "Cellulose": "#FFFFFF",
            "HULIS": "#000000"
        }

        ORGANICS = ["HULIS", "Anhydrous monosaccharides", "Polyols", "Organic acids", "Oxalate",
                    "MSA", "Glucose", "Cellulose"]

        # 2 dataframes: one for the 'main' components, one for the organics
        df_proportion_perday = pd.DataFrame()
        nonorganics = list(set(dff.columns)-set(ORGANICS))
        for c in nonorganics:
            df_proportion_perday[c] = dff[c]/dff[nonorganics].sum(axis=1)

        df_proportion_OM_perday = pd.DataFrame()
        for c in dff.columns:
            if c in ORGANICS:
                df_proportion_OM_perday[c] = dff[c]/dff["OM"]

        d = pd.DataFrame(index=list(df_proportion_OM_perday.columns) +
                         list(df_proportion_perday.columns))

        d["other"] = df_proportion_perday.mean()
        d["organics"] = df_proportion_OM_perday.mean()
        d.loc[ORGANICS, "other"] = pd.np.nan
        df_mg_per_gOM = df_proportion_OM_perday.mean() * 1000

        # Plot part
        order1 = ["OM", "EC", "Cl-", "NO3-", "SO42-", "NH4+", "Ca2+", "Other ions",
                  "Metals"]
        order2 = ORGANICS.copy()

        d = d.reindex(order1+order2)
        d.dropna(axis=0, how="all", inplace=True)

        OMidentified = df_proportion_OM_perday.median().sum() * 100
        dnormalize = d/d.sum() * 100

        # d1 = d["other"].reindex(order1, axis=0)
        # d2 = d["organics"].reindex(order2, axis=0)
        # d1 = d1/d1.sum()
        # d2 = d2/d2.sum()


        f, ax = plt.subplots(figsize=(9.5,7.5))
        dnormalize.T.plot.bar(
            stacked=True,
            color=dnormalize.index.map(COLORS).dropna(),
            rot=0,
            ax=ax,
        )

        xpos = {"other": 0, "organics": 1}
        texts = {"other": [], "organics": []}
        for xvar in ["other", "organics"]:
            val = dnormalize[xvar].reset_index().melt(id_vars=["index"])
            cumsum = 0
            for i, v in zip(val["index"], val["value"]):
                if pd.np.isnan(v):
                    continue
                cumsum += v
                if xvar == "other":
                    annot = ax.annotate("{}".format(pretty_specie(i)), 
                                       (xpos[xvar]-0.28, (cumsum -v/2) ),
                                       ha="right",
                                       va="center"
                                      )
                else:
                    text = "{}\n({:.2f} mg.g$_{{OM}}^{{-1}}$)".format(i, df_mg_per_gOM.loc[i])
                    if len(text)<40:
                        text = text.replace("\n", " ")

                    annot = ax.annotate(text, 
                                        (xpos[xvar]+0.28, (cumsum -v/2) ),
                                        ha="left",
                                        va="center"
                                       )
                texts[xvar].append(annot)

                
                ax.annotate("{:.0f}%".format(v),
                            (xpos[xvar], (cumsum - v/2) ),
                            ha="center",
                            va="center",
                            color=TEXTCOLORS[i],
                            fontweight="bold"
                           )
        # texts = pd.Series(plt.gcf().get_children()[1].get_children())
        # idx = [type(t)==matplotlib.text.Annotation for t in texts]
        # texts = texts[idx].tolist()

        # adjust_text(
        #     texts["organics"],
        #     # arrowprops=dict(arrowstyle="->", color='r', lw=0.5),
        #     autoalign='', only_move={'points': 'y', 'text': 'y'}
        # )

        yOMidentified = OMidentified * dnormalize.loc["OM", "other"]/100
        ax.annotate("{:.0f}% identified".format(OMidentified),
                    (xpos["other"], yOMidentified/2),
                    ha="center",
                    va="center",
                    color="#FFFFFF",
                    fontweight="bold"
                   )
        ax.plot([0.25, 0.75], [yOMidentified, 100], "-k")
        ax.plot([-0.25, 0.25], [yOMidentified, yOMidentified], '-w')

        ax.set_title(station, fontsize=16)
        ax.set_xticklabels([])
        f.subplots_adjust(top=0.88,
                         bottom=0.11,
                         left=0.125,
                         right=0.85,
                         hspace=0.2,
                         wspace=0.2)
        ax.legend('', frameon=False)
        ax.yaxis.set_major_formatter(FuncFormatter('{0:.0f}%'.format))
        sns.despine()


    def mainCompentOfPM(station, dateStart, dateEnd, seasonal=False,
                        savefig=False, savedir=None, con=None):
        """
        Plot a stacked bar plot of the different constitutant of the PM

        Parameters
        ----------

        station : str
            name of the station
        dateStart, dateEnd : str
            starting and ending date
        seasonal : boolean, default False
            Either to make separate graph per season
        savefig : boolean, default False
            Save the fig in png and pdf
        savedir : str path, default None
            Where to save the figures
        con : sql connection, default None
            sql connection to the database
        """
        TO_GROUP = {
            "Metals": [
                "Al", "As", "Cd", "Cr", "Cu", "Fe", "Mn", "Mo", "Ni", "Pb", "Rb", "Sb",
                "Se", "Sn", "Ti", "V", "Zn"
            ],
            "Anhydrous monosaccharides":  ["Levoglucosan", "Mannosan", "Galactosan"],
            "Polyols":  ["Arabitol", "Sorbitol", "Mannitol"],
            "Organic acids": [
                "Maleic_acid", "Succinic_acid", "Citraconic_acid", "Glutaric_acid", "Oxoheptanedioic",
                "MethylSuccinic_acid", "Adipic_acid", "MethylGlutaric", "3-MBTCA", "Phthalic_acid",
                "Pinic_acid", "Suberic_acid", "Azelaic_acid", "Sebacic_acid"
            ],
            "Other ions": [
                "Na+", "K+", "Mg2+",
            ]
        }

        TO_MICROGRAMME = ["OM", "EC", "HULIS"]

        if con is None:
            con = sqlite3.connect("/home/webersa/Documents/BdD/bdd_aerosols/aerosols.db")

        df = pd.read_sql(
            "SELECT * FROM values_all WHERE Station IN ('{}');".format(station),
            con=con
        )

        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True, drop=True)

        df = df[(dateStart < df.index) & (df.index < dateEnd)]

        if seasonal:
            df = add_season(df)

        # Metals = [
        #     "Al", "As", "Ba", "Cd", "Co", "Cr", "Cs", "Cu", "Fe", "La", "Mn",
        #     "Mo", "Ni", "Pb", "Rb", "Sb", "Se", "Sn", "Sr", "Ti", "V", "Zn"
        # ]


        dff = pd.DataFrame()
        for k in TO_GROUP.keys():
            df[k] = df[TO_GROUP[k]].astype(float).clip(0).sum(axis=1, min_count=1)
        
        # Get only the columns we have
        dff = df[TO_GROUP.keys()]
        dff["OM"] = df["OC"]*1.8
        to_keep = ["EC", "NO3-", "NH4+", "Cl-", "SO42-", "Ca2+", "Oxalate", "MSA",
                   "Glucose", "Cellulose", "HULIS"]
        for k in to_keep:
            if k in df.columns:
                dff[k] = df[k]
        dff.apply(pd.to_numeric)

        if seasonal:
            dff["season"] = df["season"]
        
        # Convert ng to µg
        for i in TO_MICROGRAMME:
            dff[i] *= 1000
        
        DF = []
        seasonName = []
        if seasonal:
            for season in df["season"].unique():
                DF.append(dff[dff["season"] == season].drop("season", axis=1))
                seasonName.append(season)
        else:
            DF = [dff]
            seasonName = ["annual"]

        for dfff, season in zip(DF, seasonName):
            plot._mainComponentOfPM(dfff, station)
            ax = plt.gca()
            if season:
                title = ax.get_title()
                plt.title(title+" "+season)
            if savefig:
                plt.savefig(
                    "{BDIR}/{station}_{temp}.png".format(
                        BDIR=savedir, station=station, temp=season
                    )
                )
                plt.savefig(
                    "{BDIR}/{station}_{temp}.pdf".format(
                        BDIR=savedir, station=station, temp=season
                    )
                )


    def what_do_we_have(sites=None, date_min=None, date_max=None, species=None,
                        min_sample=None, particle_size=None, exclude_sites=None, con=None):
        """TODO: Docstring for what_do_we_have.

        :sites: TODO
        :date_min: TODO
        :date_max: TODO
        :species: TODO
        :min_sample: TODO
        :con: TODO
        :returns: TODO

        """
        if con is None:
            con = sqlite3.connect(DB_AEROSOLS)

        df = get_sample_where(
            sites=sites,
            date_min=date_min,
            date_max=date_max,
            species=species,
            min_sample=min_sample,
            particle_size=particle_size,
            exclude_sites=exclude_sites,
            con=con
        )

        df.set_index(["Station", "Date"], inplace=True)
        stations = df.index.get_level_values("Station").unique()

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
        for i, station in enumerate(stations):
            date = df.loc[station].index
            ax.plot(date, [i]*len(date), "-o", label=station)

        ax.set_yticks(range(len(stations)))
        ax.set_ylim(-0.5, len(stations)-0.5)
        ax.set_yticklabels(stations)

