"""
Build the static supplementary website from Plots Final/ (copies figures into a clean
folder structure and writes index.html). Run:  python build_site.py
"""
import html, os, shutil

SRC = "/home/ratul/ratul/FCN3/Plots Final"
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "figures")

MODELS = [("FourCastNet3", "FourCastNet 3", "ensemble, 50 members"),
          ("Aurora", "Aurora 1.5", "ensemble, 50 members"),
          ("ECMWF_ENS", "ECMWF ENS", "operational ensemble, 50 members"),
          ("PanguWeather", "Pangu-Weather", "single forecast"),
          ("FengWu", "FengWu", "single forecast"),
          ("ECMWF_ENS_control", "ECMWF ENS control", "single forecast")]

PER_MODEL = {
 "01_position_error_mean.png": ("Mean track position error", "Mean great-circle distance between forecast and reference position against forecast lead time since genesis, one curve per genesis lead; shading is the 95% storm-bootstrap interval."),
 "02_position_error_mean_bars.png": ("Position error by day", "Mean track position error at whole days after genesis, by genesis lead, with 95% storm-bootstrap intervals."),
 "03_spread_skill.png": ("Spread and skill", "RMS spread of the members about the ensemble mean, RMSE of the ensemble mean, and their ratio (spread–skill ratio)."),
 "04_detection.png": ("Detection", "Detection rate against forecast lead time since genesis, the outcome of each storm–lead case, and (ensembles) the share of cases with at least k associated members."),
 "05_bias_envelope_24h.png": ("Displacement envelope, 24 h genesis lead", "Per-storm 5–95% envelope of the members' zonal and meridional displacement from the reference; blue where the envelope contains the reference."),
 "05_bias_envelope_48h.png": ("Displacement envelope, 48 h genesis lead", "As above, for forecasts started 48 h before genesis."),
 "05_bias_envelope_72h.png": ("Displacement envelope, 72 h genesis lead", "As above, for forecasts started 72 h before genesis."),
 "05_bias_envelope_120h.png": ("Displacement envelope, 120 h genesis lead", "As above, for forecasts started 120 h before genesis."),
 "06_ate_cte.png": ("Along- and cross-track error", "Mean along-track error (positive ahead) and cross-track error (positive right of track) against forecast lead time since genesis."),
 "07_fair_brier.png": ("Fair Brier score", "Fair and raw Brier score of the 1° LPS-presence event and the size of the finite-ensemble correction."),
 "08_hit_rate.png": ("Hit rate", "Share of members (or of cases, for a single forecast) within 120, 250 and 500 km of the reference position."),
}
COMP = {
 "C01_position_error_mean.png": ("Track position error – common sample", "All six systems on identical storm-times (the common sample), one panel per genesis lead; the row beneath gives the number of storm-times behind each point."),
 "C01b_position_error_mean_all.png": ("Track position error – each system's own sample", "As C01, but every system on every storm-time it found."),
 "C03_spread_skill_ratio.png": ("Spread–skill ratio", "The three ensembles on their common sample; one is calibrated, below one under-dispersive, above one over-dispersive."),
 "C04_detection_rate.png": ("Detection rate", "Mean share of nominal members holding the storm at every time the reference storm exists, one panel per genesis lead."),
 "C04b_detection_outcome.png": ("Case outcome", "Share of storm–lead cases associated, with tracks but none associated, and with no track at all."),
 "C05_ate_cte.png": ("Along- and cross-track error", "Mean along-track (top) and cross-track (bottom) error of the six systems on the common sample."),
 "C06_signed_displacement.png": ("Zonal and meridional displacement", "Mean eastward (top) and northward (bottom) displacement of the forecast position on the common sample."),
 "C07_fair_brier.png": ("Fair Brier score", "Fair Brier score of the 1° LPS-presence event for the three ensembles on their common sample."),
 "C08_hit_rate.png": ("Hit rate", "Hit rate within 120, 250 and 500 km for the six systems, each on its own sample."),
 "C09_summary.png": ("Summary by day", "Mean track position error and detection rate at whole days after genesis, by genesis lead."),
 "C10_genesis_box.png": ("Genesis", "Share of forecasts producing the storm, genesis timing error and genesis location error against genesis lead, as box plots."),
 "C12_class_position_error.png": ("Lows versus depressions – position error", "Mean track position error for monsoon lows and depressions, common sample within each class, pooled over genesis leads."),
 "C12_class_detection.png": ("Lows versus depressions – detection", "Detection rate for monsoon lows and depressions, pooled over genesis leads."),
 "S1_member_threshold_sensitivity.png": ("Sensitivity: member threshold", "How the ensemble-mean statistics change with the minimum share of members required to form a mean."),
 "S2_hit_radius_sensitivity.png": ("Sensitivity: hit radius", "Hit rate as a continuous function of the radius."),
 "S3_ssr_robustness.png": ("Robustness of the spread–skill ratio", "Spread–skill ratio by genesis lead with storm-bootstrap intervals, and its dependence on bin size."),
 "S4_sample_attrition.png": ("Sample size", "Reference storms still alive and storm-times with a forecast position, by genesis lead; the dotted line is the plotting floor."),
}
CASE = [(L, f"case_2024_V014_{L}h_{k}.png", k) for L in (24, 48, 72, 120) for k in ("ensembles", "deterministic")]
VS = [("V_FourCastNet_3_vs_ECMWF_ENS.png", "FourCastNet 3 vs ECMWF ENS"),
      ("V_Aurora_1.5_vs_ECMWF_ENS.png", "Aurora 1.5 vs ECMWF ENS"),
      ("V_Pangu-Weather_vs_ECMWF_ENS_control.png", "Pangu-Weather vs ECMWF ENS control"),
      ("V_FengWu_vs_ECMWF_ENS_control.png", "FengWu vs ECMWF ENS control")]
VSDESC = "Pooled over genesis leads, on the storm-times at which both systems hold a position: position error, detection rate, hit rate within 120 km, along- and cross-track error, and for ensembles the spread–skill ratio and fair Brier score."

if os.path.isdir(FIG):
    shutil.rmtree(FIG)
sections = []          # (id, title, intro, [(relpath, title, caption)])

def cp(src_rel, dst_rel):
    s, d = os.path.join(SRC, src_rel), os.path.join(FIG, dst_rel)
    if not os.path.exists(s):
        return None
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    return "figures/" + dst_rel

items = []
for f, (t, c) in COMP.items():
    p = cp(f"comparison/{f}", f"comparison/all-storms/{f}")
    if p: items.append((p, t, c))
sections.append(("comparison", "Comparison of the six systems – all 133 storms", "Every system against every other on the same storms. Forecast lead time is measured in hours since the genesis of the reference storm; one panel per genesis lead (how early the forecast was started).", items))
for cls, name in (("lows", "monsoon lows (77 storms)"), ("depressions", "monsoon depressions (56 storms)")):
    items = []
    for f, (t, c) in COMP.items():
        if f.startswith(("C12", "S1", "S2", "S3")):
            continue
        p = cp(f"comparison/{cls}/{f}", f"comparison/{cls}/{f}")
        if p: items.append((p, t, c))
    sections.append((f"comparison-{cls}", f"Comparison of the six systems – {name}", f"The comparison figures repeated for the {name} only, with the class taken from the Vishnu-algorithm label of each reference storm.", items))
items = []
for f, t in VS:
    p = cp(f"vs_ens/{f}", f"ai-vs-ecmwf/all-storms/{f}")
    if p: items.append((p, t, VSDESC))
for cls in ("lows", "depressions"):
    for f, t in VS:
        p = cp(f"vs_ens/{cls}/{f}", f"ai-vs-ecmwf/{cls}/{f}")
        if p: items.append((p, f"{t} – {cls}", VSDESC))
sections.append(("ai-vs-ecmwf", "Each AI weather model against its ECMWF counterpart", "FourCastNet 3 and Aurora 1.5 are compared with the 50-member ECMWF ensemble; Pangu-Weather and FengWu, which are deterministic, with the ECMWF ENS control.", items))
for slug, name, kind in MODELS:
    items = []
    for f, (t, c) in PER_MODEL.items():
        p = cp(f"per_model/{slug}/{f}", f"per-model/{slug}/{f}")
        if p: items.append((p, t, c))
    sections.append((f"model-{slug}", f"{name} ({kind})", f"Every statistic for {name} on its own sample, one curve per genesis lead.", items))
items = []
for L, f, k in CASE:
    p = cp(f"comparison/case_study/{f}", f"case-study-2024/{f}")
    label = "FourCastNet 3, Aurora 1.5 and ECMWF ENS" if k == "ensembles" else "Pangu-Weather, FengWu and the ECMWF ENS control"
    if p: items.append((p, f"{L} h genesis lead – {label}", "Forecast tracks of the August–September 2024 Bay of Bengal depression over the ERA5 fields used by the tracker (850 hPa streamfunction, mean sea-level pressure, 850 hPa relative humidity, 10 m wind) at the time of peak pressure drop; black is the ERA5 reference track."))
sections.append(("case-study", "Case study: the August–September 2024 depression", "The depression that formed over the Bay of Bengal at the end of August 2024 and was followed by severe flooding in Andhra Pradesh and Telangana, shown for every genesis lead.", items))
items = []
p = cp("comparison/schematics/ate_cte_schematic.png", "schematics/ate_cte_schematic.png")
if p: items.append((p, "Along- and cross-track error", "How the displacement of a forecast position is split into its components along and across the direction of motion of the reference storm."))
sections.append(("schematics", "Schematics", "Illustrations of the verification method.", items))

E = html.escape
nav = "\n".join(f'<a href="#{sid}">{E(t)}</a>' for sid, t, _, it in sections if it)
body = []
for sid, title, intro, its in sections:
    if not its:
        continue
    cards = "\n".join(
        f'''<figure class="card"><a href="{p}" class="zoom" data-title="{E(t)}"><img loading="lazy" src="{p}" alt="{E(t)}"></a>
<figcaption><strong>{E(t)}</strong><span>{E(c)}</span><a class="file" href="{p}" download>{E(p.split("/")[-1])}</a></figcaption></figure>''' for p, t, c in its)
    body.append(f'<section id="{sid}"><h2>{E(title)}</h2><p class="intro">{E(intro)}</p><div class="grid">{cards}</div></section>')
n = sum(len(i) for *_, i in sections)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LPS Thesis Supplement</title>
<meta name="description" content="Supplementary figures for the thesis on forecasting monsoon low-pressure systems over the Indian subcontinent with AI weather models.">
<link rel="stylesheet" href="assets/style.css"></head>
<body>
<header class="top"><div class="wrap">
<h1>Supplementary material</h1>
<p class="sub">Forecasting Monsoon Low-Pressure Systems over the Indian Subcontinent with AI Weather Models: A Track-Based Verification against the ECMWF Ensemble</p>
<p class="meta">Ratul Tarafder · BS-MS thesis, Indian Institute of Science Education and Research Pune, 2026 · {n} figures</p>
</div></header>
<div class="wrap layout">
<nav class="side"><p class="navh">Contents</p>{nav}</nav>
<main>
<section id="about"><h2>About these figures</h2>
<p class="intro">Four AI weather models (FourCastNet 3, Aurora 1.5, Pangu-Weather, FengWu) are verified against the ECMWF ensemble (ENS) and its control on 133 monsoon low-pressure systems of 2018–2025. Reference tracks are found in ERA5 with the algorithm of Vishnu et al. (2020), and the same tracker is applied to every forecast. Each forecast was started 24, 48, 72 or 120 h before the genesis of the reference storm (the genesis lead). Shaded bands and error bars are 95% intervals from 1000 bootstrap replicates that resample whole storms. Click any figure to enlarge it; every file can be downloaded. The folder structure of this site mirrors the sections below.</p></section>
{''.join(body)}
<footer><p>Figures generated by the analysis code of the thesis. © 2026 Ratul Tarafder.</p></footer>
</main></div>
<div id="lb" class="lb" hidden><button class="close" aria-label="Close">×</button><img alt=""><p></p></div>
<script>
const lb=document.getElementById('lb'),li=lb.querySelector('img'),lp=lb.querySelector('p');
document.querySelectorAll('a.zoom').forEach(a=>a.addEventListener('click',e=>{{e.preventDefault();li.src=a.href;lp.textContent=a.dataset.title;lb.hidden=false;}}));
lb.addEventListener('click',e=>{{if(e.target!==li)lb.hidden=true;}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true;}});
</script>
</body></html>"""
open(os.path.join(OUT, "index.html"), "w").write(page)
print(n, "figures")
