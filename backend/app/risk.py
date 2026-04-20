def compute_scene_score(exposure_years, hours_per_day, enclosed, base_weight):
    # normalize: years 0-40, hours 0-24
    y = min(max(exposure_years, 0), 40) / 40.0
    h = min(max(hours_per_day, 0), 24) / 24.0
    e = 1.0 if enclosed else 0.6
    score = (0.5 * y + 0.45 * h) * e * base_weight * 100
    return max(0.0, min(score, 100.0))

def compute_overall_score(data):
    # weights by scene
    base_weights = {"family": 1.0, "work": 0.85, "social": 0.7}
    # family: raw inputs
    fam = compute_scene_score(data.exposure_years, data.hours_per_day if data.main_environment=="family" else data.hours_per_day*0.7, data.environment_enclosed, base_weights["family"])
    work = compute_scene_score(data.exposure_years*0.9, data.hours_per_day*0.5, data.environment_enclosed, base_weights["work"])
    social = compute_scene_score(data.exposure_years*0.6, data.hours_per_day*0.6, data.environment_enclosed, base_weights["social"])
    overall = fam * 0.5 + work * 0.3 + social * 0.2
    level = "低" if overall < 35 else ("中" if overall < 65 else "高")
    return {
        "overall_score": round(overall, 1),
        "overall_level": level,
        "scene_scores": {"family": round(fam,1), "work": round(work,1), "social": round(social,1)}
    }
