import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---- CONFIG ----
INPUT_CSV = "Faostat_cocoa.csv.csv"
OUTPUT_PDF = "cocoa_comparison.pdf"

# ---- HELPERS ----
def find_col(df_cols, keywords):
    for col in df_cols:
        for key in keywords:
            if key in col.lower():
                return col
    return None

def load_and_prepare(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    col_country = "Area"
    col_year = "Year"

    # filter indicators separately
    area_df = df[(df["Element"] == "Area harvested") & (df["Unit"] == "ha")][[col_country, col_year, "Value"]].rename(columns={"Value": "area_harvested"})
    yield_df = df[(df["Element"] == "Yield") & (df["Unit"] == "hg/ha")][[col_country, col_year, "Value"]].rename(columns={"Value": "yield"})
    prod_df = df[(df["Element"] == "Production") & (df["Unit"] == "tonnes")][[col_country, col_year, "Value"]].rename(columns={"Value": "production"})

    # merge them into one tidy table
    df = area_df.merge(yield_df, on=[col_country, col_year], how="outer")
    df = df.merge(prod_df, on=[col_country, col_year], how="outer")

    # rename cols
    df = df.rename(columns={col_country: "country", col_year: "year"})

    # make sure year and numbers are numeric
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    for col in ["area_harvested", "yield", "production"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # compute yield if missing
    if "yield" not in df.columns or df["yield"].isna().all():
        if "production" in df.columns and "area_harvested" in df.columns:
            df["yield"] = df["production"] / df["area_harvested"]

    return df.dropna(subset=["year"])
    rename_map = {}
    if col_country: rename_map[col_country] = "country"
    if col_year: rename_map[col_year] = "year"
    if col_area: rename_map[col_area] = "area_harvested"
    if col_yield: rename_map[col_yield] = "yield"
    if col_prod: rename_map[col_prod] = "production"
    df = df.rename(columns=rename_map)

    for col in ["year", "area_harvested", "yield", "production"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # compute yield if missing
    if "yield" not in df.columns or df["yield"].isna().all():
        if "production" in df.columns and "area_harvested" in df.columns:
            df["yield"] = df["production"] / df["area_harvested"]

    return df.dropna(subset=["year"])

def get_country_table(df, variants):
   mask = df["country"].astype(str).str.lower().apply(lambda x: any(v.lower() in x for v in variants))
   table = df[mask].copy().sort_values("year")
   cols_to_keep = [col for col in ["year", "area_harvested", "yield", "production"] if col in table.columns]
   table = table[cols_to_keep]
   table.reset_index(inplace=True, drop=True)
   return table
# ---- PLOTTING ----
def plot_yield(table, country, color, fname):
    plt.figure(figsize=(8,5))
    plt.scatter(table["year"], table["yield"], color=color, label="Yield")
    plt.title(f"{country} — Cocoa Yield by Year")
    plt.xlabel("Year")
    plt.ylabel("Yield (t/ha)")
    plt.grid(True, linestyle=":", linewidth=0.6)
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    print("Saved:", fname)

def plot_area(table, country, color, fname):
    plt.figure(figsize=(8,5))
    plt.bar(table["year"].astype(int).astype(str), table["area_harvested"], color=color)
    plt.title(f"{country} — Area Harvested by Year")
    plt.xlabel("Year")
    plt.ylabel("Area Harvested (ha)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    print("Saved:", fname)

def plot_combined(ghana, ivory):
    fig, axes = plt.subplots(2,2, figsize=(14,10))

    # Ghana yield (scatter)
    axes[0,0].scatter(ghana["year"], ghana["yield"], color="tab:green")
    axes[0,0].set_title("Ghana — Yield by Year")
    axes[0,0].set_xlabel("Year")
    axes[0,0].set_ylabel("Yield (t/ha)")
    axes[0,0].grid(True, linestyle=":", linewidth=0.6)

    # Ivory Coast yield (scatter)
    axes[0,1].scatter(ivory["year"], ivory["yield"], color="tab:blue")
    axes[0,1].set_title("Côte d'Ivoire — Yield by Year")
    axes[0,1].set_xlabel("Year")
    axes[0,1].set_ylabel("Yield (t/ha)")
    axes[0,1].grid(True, linestyle=":", linewidth=0.6)

    # Ghana area (bar)
    axes[1,0].bar(ghana["year"].astype(int).astype(str), ghana["area_harvested"], color="tab:green")
    axes[1,0].set_title("Ghana — Area Harvested by Year")
    axes[1,0].set_xlabel("Year")
    axes[1,0].set_ylabel("Area (ha)")
    axes[1,0].tick_params(axis="x", rotation=45)

    # Ivory Coast area (bar)
    axes[1,1].bar(ivory["year"].astype(int).astype(str), ivory["area_harvested"], color="tab:blue")
    axes[1,1].set_title("Côte d'Ivoire — Area Harvested by Year")
    axes[1,1].set_xlabel("Year")
    axes[1,1].set_ylabel("Area (ha)")
    axes[1,1].tick_params(axis="x", rotation=45)

    fig.suptitle("Cocoa Production in Ghana and Côte d'Ivoire", fontsize=18)
    plt.tight_layout(rect=[0,0.03,1,0.95])
    fig.savefig(OUTPUT_PDF)
    plt.close()
    print("Saved combined PDF:", OUTPUT_PDF)

# ---- MAIN ----
def main():
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: '{INPUT_CSV}' not found.")
        return

    df = load_and_prepare(INPUT_CSV)
    ghana = get_country_table(df, ["Ghana"])
    ivory = get_country_table(df, ["Côte d'Ivoire", "Cote d'Ivoire", "Ivory Coast"])

    ghana.to_csv("ghana_table.csv", index=False)
    ivory.to_csv("Ivory coast_table.csv", index=False)
    print("Tables saved: ghana_table.csv, Ivory coast_table.csv")

    # individual plots
    plot_yield(ghana, "Ghana", "tab:green", "ghana_yield.png")
    plot_area(ghana, "Ghana", "tab:green", "ghana_area.png")
    plot_yield(ivory, "Côte d'Ivoire", "tab:blue", "ivory_yield.png")
    plot_area(ivory, "Côte d'Ivoire", "tab:blue", "ivory_area.png")

    # combined plot
    plot_combined(ghana, ivory)

if __name__ == "__main__":
    main()