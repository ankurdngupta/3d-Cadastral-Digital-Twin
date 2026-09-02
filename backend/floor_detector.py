"""
AI Floor Detection Module
=========================
Detects distinct floors from raw LiDAR / Drone Z-coordinate height point clouds
using height clustering and gap analysis.
"""


def detect_floors(z_values, gap_threshold: float = 0.7):
    """
    Groups Z-elevation points into discrete floor levels by identifying inter-floor structural gaps.
    """
    if not z_values:
        return []

    sorted_z = sorted(z_values)
    clusters = [[sorted_z[0]]]

    for z in sorted_z[1:]:
        if z - clusters[-1][-1] > gap_threshold:
            clusters.append([z])  # gap exceeds threshold, initiate next floor cluster
        else:
            clusters[-1].append(z)

    detected = []
    for cluster in clusters:
        detected.append({
            "z_min": round(min(cluster), 2),
            "z_max": round(max(cluster), 2),
            "point_count": len(cluster)
        })

    return detected
